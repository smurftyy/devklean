from __future__ import annotations

from collections.abc import Sequence

from devklean.deletion.interfaces import DeletionStrategy
from devklean.deletion.metadata import MetadataManager
from devklean.deletion.safety import SafetyValidator
from devklean.deletion.trash import TrashStrategy
from devklean.models import CleanableItem, DeleteResult


def default_deletion_strategy(allow_symlinks: bool = False) -> DeletionStrategy:
    return TrashStrategy(validator=SafetyValidator(allow_symlinks=allow_symlinks))


def default_metadata_manager() -> MetadataManager:
    return MetadataManager()


def delete_items(
    items: Sequence[CleanableItem],
    total_size: int,
    strategy: DeletionStrategy | None = None,
    metadata_manager: MetadataManager | None = None,
) -> DeleteResult:
    backend = strategy or default_deletion_strategy()
    result = backend.delete(items, total_size)

    manager = metadata_manager or default_metadata_manager()
    manager.record_successes(items, result, _strategy_name(backend))
    return result


def _strategy_name(strategy: DeletionStrategy) -> str:
    name = getattr(strategy, "name", "")
    if isinstance(name, str) and name:
        return name

    class_name = strategy.__class__.__name__
    if class_name.endswith("Strategy"):
        class_name = class_name[: -len("Strategy")]
    return class_name.lower() or strategy.__class__.__name__.lower()
