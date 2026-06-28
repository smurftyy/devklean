"""Tests for scandir-based sizing and parallel scan correctness."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from devklean.config.models import ScanSettings
from devklean.scanner.scanner import get_dir_size, scan_tree


def test_get_dir_size_sums_file_sizes(tmp_path: Path) -> None:
    root = tmp_path / "d"
    (root / "sub").mkdir(parents=True)
    (root / "a.bin").write_bytes(b"\x00" * 100)
    (root / "sub" / "b.bin").write_bytes(b"\x00" * 250)

    assert get_dir_size(str(root)) == 350


def test_get_dir_size_empty_directory_is_zero(tmp_path: Path) -> None:
    (tmp_path / "empty").mkdir()
    assert get_dir_size(str(tmp_path / "empty")) == 0


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX symlinks")
def test_get_dir_size_does_not_double_count_symlinked_dir(tmp_path: Path) -> None:
    target = tmp_path / "t"
    real = target / "real"
    real.mkdir(parents=True)
    (real / "f.bin").write_bytes(b"\x00" * 500)
    (target / "link").symlink_to(real)  # symlinked dir must not be re-counted

    assert get_dir_size(str(target)) == 500


def test_parallel_scan_computes_correct_sizes(tmp_path: Path) -> None:
    root = tmp_path / "proj"
    for i, size in enumerate([100, 200, 300]):
        nm = root / f"app{i}" / "node_modules"
        nm.mkdir(parents=True)
        (nm / "pkg.bin").write_bytes(b"\x00" * size)

    result = scan_tree(str(root))
    sizes = sorted(item.size for item in result.items)

    assert sizes == [100, 200, 300]


def test_parallel_scan_matches_target_names(tmp_path: Path) -> None:
    root = tmp_path / "proj"
    (root / "a" / "node_modules").mkdir(parents=True)
    (root / "b" / ".venv").mkdir(parents=True)
    (root / "b" / ".venv" / "pyvenv.cfg").write_text("x")

    result = scan_tree(str(root))
    names = {item.name for item in result.items}

    assert "node_modules" in names
    assert ".venv" in names


def test_many_targets_all_discovered(tmp_path: Path) -> None:
    root = tmp_path / "proj"
    for i in range(25):
        (root / f"p{i}" / "node_modules").mkdir(parents=True)

    result = scan_tree(str(root), ScanSettings.defaults())
    assert len(result.items) == 25
