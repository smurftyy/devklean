from __future__ import annotations

import os
import sys
from typing import TextIO

import click

from devklean.output.theme import Palette, get_theme

# Semantic symbols — fixed across every command and renderer.
SYM_SUCCESS = "✓"
SYM_ERROR = "✗"
SYM_WARNING = "⚠"
SYM_INFO = "•"

_ROLE_TO_CODE = {
    "success": "green",
    "error": "red",
    "warning": "yellow",
    "info": "cyan",
    "detail": "dim",
    "bold": "bold",
}


def should_use_color(stream: TextIO, theme_name: str) -> bool:
    """Color is on only when NO_COLOR is unset, stream is a tty, theme != mono."""
    if os.environ.get("NO_COLOR") is not None:
        return False
    if theme_name == "mono":
        return False
    isatty = getattr(stream, "isatty", None)
    return bool(isatty and isatty())


class Console:
    """Centralized, color-gated terminal output with a fixed symbol scheme."""

    def __init__(
        self,
        stream: TextIO | None = None,
        theme: str = "default",
        color: bool | None = None,
    ) -> None:
        self._stream = stream if stream is not None else sys.stdout
        self._theme = get_theme(theme)
        self._use_color = color if color is not None else should_use_color(self._stream, theme)

    @property
    def palette(self) -> Palette:
        return self._theme.palette

    @property
    def use_color(self) -> bool:
        return self._use_color

    def code(self, role: str) -> str:
        """Return the ANSI code for a semantic role, or '' when color is off."""
        if not self._use_color:
            return ""
        attr = _ROLE_TO_CODE.get(role)
        return getattr(self.palette, attr) if attr else ""

    @property
    def reset(self) -> str:
        return self.palette.reset if self._use_color else ""

    def paint(self, text: str, role: str) -> str:
        """Wrap text in the role's color, or return it unchanged when color is off."""
        code = self.code(role)
        if not code:
            return text
        return f"{code}{text}{self.reset}"

    def _line(self, symbol: str, role: str, message: str) -> None:
        prefix = self.paint(symbol, role)
        click.echo(f"{prefix} {message}", file=self._stream)

    def success(self, message: str) -> None:
        self._line(SYM_SUCCESS, "success", message)

    def error(self, message: str) -> None:
        self._line(SYM_ERROR, "error", message)

    def warning(self, message: str) -> None:
        self._line(SYM_WARNING, "warning", message)

    def info(self, message: str) -> None:
        self._line(SYM_INFO, "info", message)

    def detail(self, message: str) -> None:
        click.echo(self.paint(message, "detail"), file=self._stream)

    def plain(self, message: str = "") -> None:
        click.echo(message, file=self._stream)
