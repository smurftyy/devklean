"""Tests for the structural dry-run guard inside delete_items."""

from __future__ import annotations

from pathlib import Path

from devklean.deletion import delete_items
from devklean.deletion.metadata import MetadataManager
from devklean.models import CleanableItem


def _item(path: str, size: int = 100) -> CleanableItem:
    return CleanableItem(path=path, name="node_modules", size=size, display_label="Node.js")


def test_dry_run_performs_no_filesystem_ops(tmp_path: Path, fake_trash) -> None:
    target = tmp_path / "proj" / "node_modules"
    target.mkdir(parents=True)
    (target / "package.json").write_text("{}")

    result = delete_items([_item(str(target))], 100, dry_run=True)

    # planned result, but nothing actually moved
    assert result.deleted == (str(target),)
    assert result.total_size == 100
    assert target.exists()  # not removed
    assert fake_trash == []  # send2trash never invoked


def test_dry_run_still_reports_blocked_paths(tmp_path: Path, fake_trash) -> None:
    safe = tmp_path / "proj" / "node_modules"
    safe.mkdir(parents=True)

    result = delete_items([_item("/"), _item(str(safe))], 200, dry_run=True)

    assert result.deleted == (str(safe),)
    assert len(result.failed) == 1
    assert result.failed[0].path == "/"


def test_delete_items_dry_run_writes_no_metadata(tmp_path: Path, fake_trash) -> None:
    storage = tmp_path / "meta"
    manager = MetadataManager(storage_dir=storage)
    target = tmp_path / "proj" / "node_modules"
    target.mkdir(parents=True)

    delete_items(
        [_item(str(target))],
        100,
        metadata_manager=manager,
        dry_run=True,
    )

    assert target.exists()
    assert fake_trash == []
    assert list(storage.glob("*.json")) == [] if storage.exists() else True
