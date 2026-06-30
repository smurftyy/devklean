"""Tests for top-level signal handling in the CLI entry point."""

from __future__ import annotations

import sys

import pytest

import devklean.cli.main  # noqa: F401  (ensure the submodule is imported)

# devklean.cli.__init__ rebinds the name "main" to the function, shadowing the
# submodule attribute, so reach the module object through sys.modules.
main_module = sys.modules["devklean.cli.main"]


def test_main_handles_keyboard_interrupt_cleanly(tmp_path, monkeypatch, capsys) -> None:
    # Ctrl+C at a confirmation prompt raises KeyboardInterrupt from deep in the
    # call stack. main() must turn that into a clean exit (code 130, the Unix
    # SIGINT convention) with an "Aborted." notice rather than a traceback.
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    monkeypatch.setattr("sys.argv", ["devklean", "scan", str(tmp_path)])

    def _raise(*args, **kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(main_module, "dispatch", _raise)

    with pytest.raises(SystemExit) as excinfo:
        main_module.main()

    assert excinfo.value.code == 130
    assert "Aborted." in capsys.readouterr().err
