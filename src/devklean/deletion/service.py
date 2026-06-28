from __future__ import annotations

from collections.abc import Sequence

from devklean.deletion.interfaces import DeletionStrategy
from devklean.deletion.trash import TrashStrategy
from devklean.models import CleanableItem, DeleteResult


def default_deletion_strategy() -> DeletionStrategy:
    return TrashStrategy()


def delete_items(
    items: Sequence[CleanableItem],
    total_size: int,
    strategy: DeletionStrategy | None = None,
) -> DeleteResult:
    backend = strategy or default_deletion_strategy()
    return backend.delete(items, total_size)
