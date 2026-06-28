from __future__ import annotations

from devklean.deletion.interfaces import DeletionStrategy
from devklean.deletion.metadata import MetadataManager
from devklean.deletion.paths import get_deletion_metadata_dir
from devklean.deletion.service import default_deletion_strategy, delete_items
from devklean.deletion.trash import TrashStrategy

__all__ = [
    "DeletionStrategy",
    "MetadataManager",
    "TrashStrategy",
    "default_deletion_strategy",
    "get_deletion_metadata_dir",
    "delete_items",
]
