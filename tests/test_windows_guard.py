"""Windows platform-support guard for interactive mode.

Interactive mode depends on ``curses``, a Unix-only stdlib module. On Windows
devklean must (1) import cleanly for all non-interactive commands and (2) fail
with a friendly message — never a traceback — when ``-i`` is requested.

These are the Windows-relevant behaviors, so they run on every platform.
"""

from __future__ import annotations

import io
import os
import subprocess
import sys
from argparse import Namespace
from pathlib import Path

from devklean.cli.commands.clean import run_clean
from devklean.config.defaults import DEFAULT_TARGETS
from devklean.config.models import AppConfig, DefaultsConfig
from devklean.output.console import Console
from devklean.output.text import TextRenderer


def _config(**defaults) -> AppConfig:
    return AppConfig(targets=dict(DEFAULT_TARGETS), defaults=DefaultsConfig(**defaults))


def _renderer() -> TextRenderer:
    return TextRenderer(console=Console(stream=io.StringIO()))


def _tree(tmp_path: Path) -> Path:
    tree = tmp_path / "proj"
    nm = tree / "app" / "node_modules"
    nm.mkdir(parents=True)
    (nm / "pkg.json").write_text("{}")
    return tree


def _args(tree: Path, **over) -> Namespace:
    base = dict(path=str(tree), dry_run=False, interactive=False, yes=True, command="clean")
    base.update(over)
    return Namespace(**base)


def test_tui_module_imports_cold_without_curses() -> None:
    """A cold ``import devklean.tui`` must succeed on its own.

    Run in a fresh interpreter so nothing else has pre-loaded the package — this
    catches both a re-introduced module-level ``import curses`` (which would
    crash every command on Windows) and an import-order/circular-import
    regression that an in-process import would mask.
    """
    env = {**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src")}
    result = subprocess.run(
        [sys.executable, "-c", "import devklean.tui; print(devklean.tui.run_interactive.__name__)"],
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0, result.stderr
    assert "run_interactive" in result.stdout


def test_interactive_on_windows_shows_friendly_message_and_exits(
    tmp_path, monkeypatch, capsys
) -> None:
    monkeypatch.setattr("devklean.cli.commands.clean.sys.platform", "win32")
    tree = _tree(tmp_path)
    nm = tree / "app" / "node_modules"

    code = run_clean(_args(tree, interactive=True), _renderer(), _config(), None)

    assert code != 0
    err = capsys.readouterr().err.lower()
    assert "interactive" in err
    assert "windows" in err
    # The guard must short-circuit before touching the filesystem.
    assert nm.exists()
