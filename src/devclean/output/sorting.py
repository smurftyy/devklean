from __future__ import annotations

from devclean.models import CleanableItem


def items_by_size_desc(items: list[CleanableItem]) -> list[CleanableItem]:
    """Return items sorted largest-first by size.

    Safe: sort is stable; equal sizes retain relative order. Used by all
    output paths so sort logic lives in one place without affecting scan order.
    """
    return sorted(items, key=lambda item: item.size, reverse=True)
