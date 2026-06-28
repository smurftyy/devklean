"""Tests for the theme/color-gating console layer."""

from __future__ import annotations

import io

from devklean.output.console import Console, should_use_color
from devklean.output.theme import get_theme


class _FakeTTY(io.StringIO):
    def isatty(self) -> bool:  # noqa: D401
        return True


def _tty() -> _FakeTTY:
    return _FakeTTY()


# --- theme registry ---


def test_get_theme_default_has_color_codes() -> None:
    theme = get_theme("default")
    assert theme.palette.green != ""
    assert theme.palette.reset != ""


def test_get_theme_mono_has_empty_codes() -> None:
    theme = get_theme("mono")
    assert theme.palette.green == ""
    assert theme.palette.red == ""
    assert theme.palette.reset == ""


def test_get_theme_unknown_falls_back_to_default() -> None:
    assert get_theme("does-not-exist").name == "default"


# --- color gating ---


def test_color_disabled_when_not_a_tty() -> None:
    assert should_use_color(io.StringIO(), "default") is False


def test_color_enabled_on_tty_with_default_theme(monkeypatch) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)
    assert should_use_color(_tty(), "default") is True


def test_no_color_env_disables_color(monkeypatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    assert should_use_color(_tty(), "default") is False


def test_mono_theme_disables_color_even_on_tty(monkeypatch) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)
    assert should_use_color(_tty(), "mono") is False


# --- console output ---


def test_console_success_emits_check_symbol_without_color_when_piped() -> None:
    stream = io.StringIO()
    Console(stream=stream, theme="default").success("done")
    out = stream.getvalue()
    assert "✓" in out
    assert "done" in out
    assert "\x1b[" not in out  # piped => no ANSI


def test_console_error_emits_cross_symbol() -> None:
    stream = io.StringIO()
    Console(stream=stream, theme="default").error("boom")
    assert "✗" in stream.getvalue()


def test_console_warning_emits_warning_symbol() -> None:
    stream = io.StringIO()
    Console(stream=stream, theme="default").warning("careful")
    assert "⚠" in stream.getvalue()


def test_console_uses_ansi_on_tty(monkeypatch) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)
    stream = _tty()
    Console(stream=stream, theme="default").success("done")
    assert "\x1b[" in stream.getvalue()


def test_console_paint_is_noop_when_color_disabled() -> None:
    console = Console(stream=io.StringIO(), theme="default")
    assert console.paint("x", "success") == "x"


def test_console_force_color_overrides_tty_detection() -> None:
    stream = io.StringIO()
    console = Console(stream=stream, theme="default", color=True)
    assert console.paint("x", "error").startswith("\x1b[")
