from __future__ import annotations

from devklean.deletion.interfaces import DeletionStrategy
from devklean.deletion.service import default_deletion_strategy, delete_items
from devklean.deletion.trash import TrashStrategy

__all__ = [
    "DeletionStrategy",
    "TrashStrategy",
    "default_deletion_strategy",
    "delete_items",
]
