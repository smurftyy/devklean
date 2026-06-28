"""End-to-end integration tests for full command flows."""

from __future__ import annotations

import io
from argparse import Namespace
from pathlib import Path

from devklean.cli.commands.clean import run_clean
from devklean.cli.commands.scan import run_scan
from devklean.config.defaults import DEFAULT_TARGETS
from devklean.config.models import AppConfig, DefaultsConfig
from devklean.deletion.metadata import MetadataManager
from devklean.deletion.trash import TrashStrategy
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


def test_clean_end_to_end_deletes(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data"))
    tree = _tree(tmp_path)
    nm = tree / "app" / "node_modules"

    code = run_clean(
        _args(tree),
        _renderer(),
        _config(default_yes=True),
        TrashStrategy(trash_root=tmp_path / "trash"),
    )

    assert code == 0
    assert not nm.exists()  # moved to trash
    # a metadata record was written
    records = MetadataManager(
        storage_dir=tmp_path / "data" / "devklean" / "deletions"
    ).load_records()
    assert len(records.records) == 1


def test_clean_dry_run_deletes_nothing(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data"))
    tree = _tree(tmp_path)
    nm = tree / "app" / "node_modules"

    code = run_clean(
        _args(tree, dry_run=True),
        _renderer(),
        _config(default_yes=True),
        TrashStrategy(trash_root=tmp_path / "trash"),
    )

    assert code == 0
    assert nm.exists()  # untouched
    meta = tmp_path / "data" / "devklean" / "deletions"
    assert not meta.exists() or list(meta.glob("*.json")) == []


def test_clean_zero_matches_reports_nothing_to_clean(tmp_path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    stream = io.StringIO()
    renderer = TextRenderer(console=Console(stream=stream))

    code = run_clean(_args(empty), renderer, _config(default_yes=True), None)

    assert code == 0
    assert "Nothing to clean" in stream.getvalue()


def test_scan_command_zero_matches(tmp_path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    stream = io.StringIO()
    renderer = TextRenderer(console=Console(stream=stream))
    args = Namespace(path=str(empty), command="scan", json=False)

    code = run_scan(args, renderer, _config())

    assert code == 0
    assert "Nothing to clean" in stream.getvalue()


def test_clean_invalid_directory_returns_error(tmp_path) -> None:
    stream = io.StringIO()
    renderer = TextRenderer(console=Console(stream=stream))
    args = _args(tmp_path / "does-not-exist")

    code = run_clean(args, renderer, _config(default_yes=True), None)

    assert code == 1
    assert "not a directory" in stream.getvalue()
