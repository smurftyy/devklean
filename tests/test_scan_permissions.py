"""Tests for graceful permission-error handling during scanning."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

from devklean.scanner.scanner import ScanResult, scan_tree

_is_root = hasattr(os, "geteuid") and os.geteuid() == 0


def test_scan_tree_returns_scan_result(sample_tree: Path) -> None:
    report = scan_tree(str(sample_tree))
    assert isinstance(report, ScanResult)
    assert isinstance(report.items, list)
    assert report.permission_errors == []


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX permission model")
@pytest.mark.skipif(_is_root, reason="root bypasses filesystem permissions")
def test_scan_reports_permission_denied_directory(tmp_path: Path) -> None:
    root = tmp_path / "proj"
    locked = root / "locked"
    (locked / "node_modules").mkdir(parents=True)
    os.chmod(locked, 0o000)
    try:
        report = scan_tree(str(root))
    finally:
        os.chmod(locked, 0o755)  # restore so tmp cleanup works

    assert any("locked" in path for path in report.permission_errors)


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX permission model")
@pytest.mark.skipif(_is_root, reason="root bypasses filesystem permissions")
def test_scan_continues_past_permission_denied(tmp_path: Path) -> None:
    root = tmp_path / "proj"
    (root / "readable" / "node_modules").mkdir(parents=True)
    locked = root / "locked"
    locked.mkdir(parents=True)
    os.chmod(locked, 0o000)
    try:
        report = scan_tree(str(root))
    finally:
        os.chmod(locked, 0o755)

    # the readable target is still discovered despite the locked sibling
    assert any(item.name == "node_modules" for item in report.items)
