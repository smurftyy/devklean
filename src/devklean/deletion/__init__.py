from __future__ import annotations

from devklean.deletion.integrity import IntegrityReport, check_integrity
from devklean.deletion.metadata import MetadataManager
from devklean.deletion.paths import get_deletion_metadata_dir
from devklean.deletion.safety import SafetyValidator, SafetyViolation
from devklean.deletion.trash import delete_items

__all__ = [
    "IntegrityReport",
    "MetadataManager",
    "SafetyValidator",
    "SafetyViolation",
    "check_integrity",
    "delete_items",
    "get_deletion_metadata_dir",
]
