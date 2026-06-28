from __future__ import annotations

from devklean.deletion.base import BaseDeletionStrategy
from devklean.deletion.integrity import IntegrityReport, check_integrity
from devklean.deletion.interfaces import DeletionStrategy
from devklean.deletion.metadata import MetadataManager
from devklean.deletion.paths import get_deletion_metadata_dir
from devklean.deletion.safety import SafetyValidator, SafetyViolation
from devklean.deletion.service import default_deletion_strategy, delete_items
from devklean.deletion.trash import TrashStrategy

__all__ = [
    "BaseDeletionStrategy",
    "DeletionStrategy",
    "IntegrityReport",
    "MetadataManager",
    "SafetyValidator",
    "SafetyViolation",
    "TrashStrategy",
    "check_integrity",
    "default_deletion_strategy",
    "get_deletion_metadata_dir",
    "delete_items",
]
