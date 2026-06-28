"""Shared pytest fixtures for devclean tests."""

from __future__ import annotations

from pathlib import Path

import pytest


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
