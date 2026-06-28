"""Shared pytest fixtures for devklean tests."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest


@pytest.fixture
def fake_trash(monkeypatch):
    """Replace ``send2trash`` with a deterministic, OS-independent fake.

    Unit tests must not depend on the real native trash (that platform
    dependence is exactly what broke CI on macOS/Windows). This records each
    trashed path and removes it from disk, so ``send2trash``-was-called and
    "the original no longer exists" assertions both hold on every platform.
    Returns the list of paths the strategy asked to trash.
    """
    trashed: list[str] = []

    def _fake_send2trash(path) -> None:
        target = Path(os.fspath(path))
        trashed.append(str(target))
        if not target.exists():
            raise OSError(f"File not found: {target}")
        if target.is_dir() and not target.is_symlink():
            shutil.rmtree(target)
        else:
            target.unlink()

    monkeypatch.setattr("devklean.deletion.trash.send2trash", _fake_send2trash)
    return trashed


@pytest.fixture
def sample_tree(tmp_path: Path) -> Path:
    """A temporary project tree with common cleanable directories."""
    root = tmp_path / "project"
    root.mkdir()

    # Top-level targets
    node_modules = root / "node_modules"
    node_modules.mkdir()
    (node_modules / "package.json").write_text("{}")

    venv = root / ".venv"
    venv.mkdir()
    (venv / "pyvenv.cfg").write_text("home = /usr/bin/python3")

    # Nested target (should be discovered independently)
    nested = root / "apps" / "web"
    nested.mkdir(parents=True)
    nested_cache = nested / "__pycache__"
    nested_cache.mkdir()
    (nested_cache / "module.cpython-312.pyc").write_bytes(b"\x00" * 512)

    # Non-target directory (should be ignored)
    src = root / "src"
    src.mkdir()
    (src / "main.py").write_text("print('hello')")

    return root


@pytest.fixture
def empty_tree(tmp_path: Path) -> Path:
    """An empty temporary directory with no cleanable targets."""
    root = tmp_path / "empty"
    root.mkdir()
    return root
