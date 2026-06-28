"""Tests for devclean.models."""

from __future__ import annotations

import dataclasses

import pytest

from devclean.models import CleanableItem, DeleteFailure, DeleteResult


def test_cleanable_item_fields() -> None:
    item = CleanableItem(
        path="/tmp/node_modules",
        name="node_modules",
        size=1024,
        display_label="Node.js",
    )

    assert item.path == "/tmp/node_modules"
    assert item.name == "node_modules"
    assert item.size == 1024
    assert item.display_label == "Node.js"


def test_cleanable_item_is_frozen() -> None:
    item = CleanableItem(
        path="/tmp/venv",
        name="venv",
        size=0,
        display_label="Python venv",
    )

    with pytest.raises(dataclasses.FrozenInstanceError):
        item.size = 999  # type: ignore[misc]


def test_delete_result_counts() -> None:
    result = DeleteResult(
        deleted=("/tmp/a", "/tmp/b"),
        failed=(DeleteFailure(path="/tmp/c", error="permission denied"),),
        total_size=2048,
    )

    assert result.deleted_count == 2
    assert result.failed_count == 1
    assert result.total_size == 2048
