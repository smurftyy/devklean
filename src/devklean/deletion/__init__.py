from __future__ import annotations

from importlib import import_module

__all__ = [
    "IntegrityReport",
    "MetadataManager",
    "SafetyValidator",
    "SafetyViolation",
    "check_integrity",
    "delete_items",
    "get_deletion_metadata_dir",
]


def __getattr__(name: str):
    if name == "IntegrityReport":
        return import_module("devklean.deletion.integrity").IntegrityReport
    if name == "check_integrity":
        return import_module("devklean.deletion.integrity").check_integrity
    if name == "MetadataManager":
        return import_module("devklean.deletion.metadata").MetadataManager
    if name == "get_deletion_metadata_dir":
        return import_module("devklean.deletion.paths").get_deletion_metadata_dir
    if name == "SafetyValidator":
        return import_module("devklean.deletion.safety").SafetyValidator
    if name == "SafetyViolation":
        return import_module("devklean.deletion.safety").SafetyViolation
    if name == "delete_items":
        return import_module("devklean.deletion.trash").delete_items
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
