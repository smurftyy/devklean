"""Tests for shared output sorting."""

from __future__ import annotations

from devklean.models import CleanableItem
from devklean.output.sorting import items_by_size_desc


def test_items_by_size_desc() -> None:
    items = [
        CleanableItem("/a", "dist", 100, "Build output"),
        CleanableItem("/b", "node_modules", 500, "Node.js"),
        CleanableItem("/c", "venv", 500, "Python venv"),
    ]

    sorted_items = items_by_size_desc(items)

    assert [item.path for item in sorted_items] == ["/b", "/c", "/a"]
    assert sorted_items[0].size == 500
