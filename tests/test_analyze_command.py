"""Tests for `devklean analyze`."""

from __future__ import annotations

import subprocess
import sys
from argparse import Namespace
from io import StringIO
from pathlib import Path

from devklean.cli.commands.analyze import run_analyze
from devklean.config.defaults import DEFAULT_TARGETS
from devklean.config.models import AppConfig
from devklean.output.console import Console
from devklean.output.text import TextRenderer


def _config() -> AppConfig:
    return AppConfig(targets=dict(DEFAULT_TARGETS))


def _renderer() -> tuple[TextRenderer, StringIO]:
    stream = StringIO()
    return TextRenderer(console=Console(stream=stream)), stream


def _args(path: str, *, verbose: bool = False) -> Namespace:
    return Namespace(path=path, verbose=verbose)


def test_analyze_buckets_recognized_and_unrecognized(tmp_path: Path) -> None:
    project = tmp_path / "project"
    node_modules = project / "node_modules"
    node_modules.mkdir(parents=True)
    (node_modules / "pkg.json").write_text("{}")

    # A custom target with no signature-registry entry: recognized by
    # scan_tree (it's a configured target) but must land in "unrecognized"
    # here, since devklean.signatures has no data for it.
    config = AppConfig(targets={**DEFAULT_TARGETS, "turbo-cache": "Turborepo cache"})
    custom = project / "turbo-cache"
    custom.mkdir()
    (custom / "x").write_text("x")

    renderer, stream = _renderer()

    code = run_analyze(_args(str(project)), renderer, config)

    out = stream.getvalue()
    assert code == 0
    assert "RECOGNIZED" in out
    assert "Node.js" in out
    assert "NOT RECOGNIZED" in out
    assert str(custom) in out


def test_analyze_reports_no_candidates_cleanly(tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    renderer, stream = _renderer()

    code = run_analyze(_args(str(empty)), renderer, _config())

    out = stream.getvalue()
    assert code == 0
    assert "none" in out
    assert "WORKSPACE HEALTH: 100/100" in out


def test_analyze_invalid_directory_returns_error(tmp_path: Path) -> None:
    renderer, stream = _renderer()

    code = run_analyze(_args(str(tmp_path / "does-not-exist")), renderer, _config())

    assert code == 1
    assert "not a directory" in stream.getvalue()


def test_analyze_flags_lockfile_conflict(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    (project / "package-lock.json").write_text("{}")
    (project / "pnpm-lock.yaml").write_text("")
    node_modules = project / "node_modules"
    node_modules.mkdir()
    (node_modules / "pkg.json").write_text("{}")

    renderer, stream = _renderer()

    code = run_analyze(_args(str(project)), renderer, _config())

    out = stream.getvalue()
    assert code == 0
    assert "conflicting lockfiles" in out
    assert "package-lock.json" in out and "pnpm-lock.yaml" in out


def test_analyze_verbose_shows_formula_and_inputs(tmp_path: Path) -> None:
    project = tmp_path / "project"
    node_modules = project / "node_modules"
    node_modules.mkdir(parents=True)
    (node_modules / "pkg.json").write_text("{}")

    renderer, stream = _renderer()

    code = run_analyze(_args(str(project), verbose=True), renderer, _config())

    out = stream.getvalue()
    assert code == 0
    assert "formula:" in out
    assert "inputs:" in out
    assert "recognized_weighted_size=" in out


def test_analyze_reports_unknown_staleness_when_no_signal(tmp_path: Path) -> None:
    """Integration check for the staleness fallback: no git repo, and the
    only file present lives inside the artifact directory itself."""
    project = tmp_path / "project"
    node_modules = project / "node_modules"
    node_modules.mkdir(parents=True)
    (node_modules / "pkg.json").write_text("{}")

    renderer, stream = _renderer()

    code = run_analyze(_args(str(project)), renderer, _config())

    out = stream.getvalue()
    assert code == 0
    assert "no reliable signal" in out


def test_analyze_command_end_to_end(tmp_path: Path) -> None:
    project = tmp_path / "project"
    node_modules = project / "node_modules"
    node_modules.mkdir(parents=True)
    (node_modules / "pkg.json").write_text("{}")

    result = subprocess.run(
        [sys.executable, "-m", "devklean", "analyze", str(project)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "WORKSPACE HEALTH" in result.stdout
