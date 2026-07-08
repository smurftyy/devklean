"""Tests for devklean.signatures.structural (plain file-existence checks)."""

from __future__ import annotations

from pathlib import Path

from devklean.signatures.structural import detect_lockfile_conflicts


def test_no_conflict_with_a_single_lockfile(tmp_path: Path) -> None:
    (tmp_path / "package-lock.json").write_text("{}")

    assert detect_lockfile_conflicts(str(tmp_path)) is None


def test_no_conflict_with_no_lockfiles(tmp_path: Path) -> None:
    assert detect_lockfile_conflicts(str(tmp_path)) is None


def test_flags_npm_and_pnpm_lockfile_conflict(tmp_path: Path) -> None:
    (tmp_path / "package-lock.json").write_text("{}")
    (tmp_path / "pnpm-lock.yaml").write_text("lockfileVersion: 6")

    conflict = detect_lockfile_conflicts(str(tmp_path))

    assert conflict is not None
    assert conflict.project_root == str(tmp_path)
    assert set(conflict.lockfiles) == {"package-lock.json", "pnpm-lock.yaml"}


def test_flags_three_way_lockfile_conflict(tmp_path: Path) -> None:
    (tmp_path / "package-lock.json").write_text("{}")
    (tmp_path / "yarn.lock").write_text("")
    (tmp_path / "pnpm-lock.yaml").write_text("")

    conflict = detect_lockfile_conflicts(str(tmp_path))

    assert conflict is not None
    assert len(conflict.lockfiles) == 3
