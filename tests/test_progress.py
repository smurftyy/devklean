"""Tests for the stdlib progress/spinner widgets (stderr, tty-gated)."""

from __future__ import annotations

import io

from devklean.output.progress import ProgressBar, Spinner, progress_enabled


class _FakeTTY(io.StringIO):
    def isatty(self) -> bool:
        return True


def test_progress_disabled_when_not_a_tty() -> None:
    assert progress_enabled(io.StringIO()) is False


def test_progress_enabled_on_tty(monkeypatch) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)
    assert progress_enabled(_FakeTTY()) is True


def test_progress_disabled_with_no_color(monkeypatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    assert progress_enabled(_FakeTTY()) is False


def test_spinner_writes_nothing_when_disabled() -> None:
    stream = io.StringIO()
    spinner = Spinner(stream=stream, label="scanning", enabled=False)
    spinner.start()
    spinner.update("scanning 5 dirs")
    spinner.stop()
    assert stream.getvalue() == ""


def test_spinner_context_manager_disabled_is_silent() -> None:
    stream = io.StringIO()
    with Spinner(stream=stream, label="x", enabled=False):
        pass
    assert stream.getvalue() == ""


def test_spinner_emits_label_when_enabled() -> None:
    stream = io.StringIO()
    spinner = Spinner(stream=stream, label="scanning", enabled=True)
    spinner.start()
    spinner.stop()
    assert "scanning" in stream.getvalue()


def test_progress_bar_disabled_writes_nothing() -> None:
    stream = io.StringIO()
    bar = ProgressBar(total=4, stream=stream, label="deleting", enabled=False)
    bar.advance()
    bar.close()
    assert stream.getvalue() == ""


def test_progress_bar_renders_counts_when_enabled() -> None:
    bar = ProgressBar(total=4, stream=io.StringIO(), label="deleting", enabled=True)
    assert bar.render(2) == "deleting [####----] 2/4" or "2/4" in bar.render(2)


def test_progress_bar_advance_writes_progress() -> None:
    stream = io.StringIO()
    bar = ProgressBar(total=2, stream=stream, label="deleting", enabled=True)
    bar.advance()
    bar.advance()
    bar.close()
    out = stream.getvalue()
    assert "2/2" in out


def test_progress_bar_zero_total_does_not_crash() -> None:
    stream = io.StringIO()
    bar = ProgressBar(total=0, stream=stream, label="x", enabled=True)
    bar.close()  # no advances; must not divide by zero
