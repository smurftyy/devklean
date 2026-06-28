"""Tests for the informational `restore` command.

Since items are sent to the native OS trash (which devklean does not own or
track), `restore` no longer moves files back — it explains how to recover them
through the OS trash UI.
"""

from __future__ import annotations

from argparse import Namespace
from io import StringIO

from devklean.cli.commands.restore import run_restore
from devklean.output.console import Console
from devklean.output.text import TextRenderer


def test_restore_explains_native_trash_recovery(capsys) -> None:
    code = run_restore(Namespace(), TextRenderer(), None)

    out = capsys.readouterr().out.lower()
    assert code == 0
    assert "trash" in out
    # points the user at the per-platform recovery path and at history
    assert "recycle bin" in out
    assert "history" in out


def test_restore_uses_injected_renderer() -> None:
    # C3 regression: restore must write through the injected renderer's stream,
    # not construct its own Console pointed at sys.stdout.
    stream = StringIO()
    renderer = TextRenderer(console=Console(stream=stream))

    code = run_restore(Namespace(), renderer, None)

    assert code == 0
    assert "trash" in stream.getvalue().lower()


def test_restore_does_not_touch_the_filesystem(tmp_path, monkeypatch) -> None:
    # It must not call into send2trash or the metadata store at all.
    def _boom(*args, **kwargs):
        raise AssertionError("restore must not invoke send2trash")

    monkeypatch.setattr("devklean.deletion.trash.send2trash", _boom)

    assert run_restore(Namespace(), TextRenderer(), None) == 0
