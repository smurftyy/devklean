from __future__ import annotations

from typing import Sequence

from devklean.deletion.safety import SafetyValidator
from devklean.models import CleanableItem, DeleteFailure, DeleteResult


class BaseDeletionStrategy:
    """Template strategy that validates safety before delegating deletion.

    Concrete strategies implement :meth:`_delete_safe`. Safety validation
    happens here, in one place, so no strategy duplicates the checks and
    validation always runs before any item is removed.
    """

    name = ""

    def __init__(self, validator: SafetyValidator | None = None) -> None:
        self._validator = validator if validator is not None else SafetyValidator()

    def delete(
        self,
        items: Sequence[CleanableItem],
        total_size: int,
        dry_run: bool = False,
    ) -> DeleteResult:
        safe, blocked = self._validator.partition(items)

        blocked_failures = tuple(
            DeleteFailure(path=item.path, error=violation.message) for item, violation in blocked
        )

        safe_total = sum(item.size for item in safe)

        if dry_run:
            # Structural guard: under dry-run no strategy performs any I/O.
            return DeleteResult(
                deleted=tuple(item.path for item in safe),
                failed=blocked_failures,
                total_size=safe_total,
            )

        if not safe:
            return DeleteResult(deleted=(), failed=blocked_failures, total_size=0)

        result = self._delete_safe(safe, safe_total)

        return DeleteResult(
            deleted=result.deleted,
            failed=result.failed + blocked_failures,
            total_size=result.total_size,
        )

    def _delete_safe(
        self,
        items: Sequence[CleanableItem],
        total_size: int,
    ) -> DeleteResult:
        raise NotImplementedError
