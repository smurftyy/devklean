"""Tests for color-gating and standardized formatting in TextRenderer."""

from __future__ import annotations

import io

from devklean.models import CleanableItem, DeleteFailure, DeleteResult
from devklean.output.console import Console
from devklean.output.text import TextRenderer


def _piped_renderer() -> tuple[TextRenderer, io.StringIO]:
    stream = io.StringIO()
    return TextRenderer(console=Console(stream=stream, theme="default")), stream


def test_scan_summary_has_no_ansi_when_piped() -> None:
    renderer, stream = _piped_renderer()
    renderer.scan_summary([CleanableItem("/p/nm", "node_modules", 1024, "Node.js")])
    assert "\x1b[" not in stream.getvalue()


def test_deletion_result_has_no_ansi_when_piped_and_uses_symbols() -> None:
    renderer, stream = _piped_renderer()
    result = DeleteResult(deleted=("/p/nm",), failed=(), total_size=1024)
    renderer.deletion_result(result)
    out = stream.getvalue()
    assert "\x1b[" not in out
    assert "✓" in out


def test_deletion_result_failure_uses_cross_symbol() -> None:
    renderer, stream = _piped_renderer()
    result = DeleteResult(
        deleted=(),
        failed=(DeleteFailure(path="/p/x", error="permission denied"),),
        total_size=0,
    )
    renderer.deletion_result(result)
    out = stream.getvalue()
    assert "✗" in out
    assert "permission denied" in out


def test_confirm_prompt_includes_count_and_size() -> None:
    renderer, _ = _piped_renderer()
    prompt = renderer.confirm_prompt(7, 880 * 1024 * 1024)
    assert "7" in prompt
    assert "880" in prompt  # formatted size shown


def test_no_color_env_disables_ansi_on_tty(monkeypatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")

    class _TTY(io.StringIO):
        def isatty(self) -> bool:
            return True

    stream = _TTY()
    renderer = TextRenderer(console=Console(stream=stream, theme="default"))
    renderer.scan_summary([CleanableItem("/p/nm", "node_modules", 1024, "Node.js")])
    assert "\x1b[" not in stream.getvalue()
