from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Palette:
    """ANSI codes for semantic roles. Empty strings mean 'no color'."""

    green: str
    red: str
    yellow: str
    cyan: str
    dim: str
    bold: str
    reset: str


_COLOR_PALETTE = Palette(
    green="\033[32m",
    red="\033[31m",
    yellow="\033[33m",
    cyan="\033[36m",
    dim="\033[2m",
    bold="\033[1m",
    reset="\033[0m",
)

_MONO_PALETTE = Palette(green="", red="", yellow="", cyan="", dim="", bold="", reset="")


@dataclass(frozen=True)
class Theme:
    name: str
    palette: Palette


_THEMES = {
    "default": Theme(name="default", palette=_COLOR_PALETTE),
    "mono": Theme(name="mono", palette=_MONO_PALETTE),
}


def theme_names() -> tuple[str, ...]:
    return tuple(_THEMES)


def get_theme(name: str) -> Theme:
    """Return the named theme, falling back to 'default' for unknown names."""
    return _THEMES.get(name, _THEMES["default"])
