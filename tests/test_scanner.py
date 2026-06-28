"""Tests for devclean.scanner."""

from __future__ import annotations

from pathlib import Path

from devclean.models import CleanableItem
from devclean.scanner import TARGETS, get_dir_size, scan


def test_scan_empty_tree(empty_tree: Path) -> None:
    assert scan(str(empty_tree)) == []


def test_scan_finds_known_targets(sample_tree: Path) -> None:
    found = scan(str(sample_tree))

    names = {item.name for item in found}
    assert names == {"node_modules", ".venv", "__pycache__"}


def test_scan_item_fields(sample_tree: Path) -> None:
    found = scan(str(sample_tree))
    node_modules = next(item for item in found if item.name == "node_modules")

    assert isinstance(node_modules, CleanableItem)
    assert node_modules.path == str(sample_tree / "node_modules")
    assert node_modules.display_label == TARGETS["node_modules"]
    assert node_modules.size > 0


def test_scan_does_not_recurse_into_found_target(sample_tree: Path) -> None:
    """A node_modules inside another target should not be scanned separately."""
    nested_nm = sample_tree / "node_modules" / "nested" / "node_modules"
    nested_nm.mkdir(parents=True)
    (nested_nm / "dep.js").write_text("export {}")

    found = scan(str(sample_tree))
    node_modules_items = [item for item in found if item.name == "node_modules"]

    assert len(node_modules_items) == 1
    assert node_modules_items[0].path == str(sample_tree / "node_modules")


def test_get_dir_size_sums_files(tmp_path: Path) -> None:
    target = tmp_path / "dist"
    target.mkdir()
    (target / "a.bin").write_bytes(b"\x00" * 100)
    (target / "b.bin").write_bytes(b"\x00" * 250)

    assert get_dir_size(str(target)) == 350
