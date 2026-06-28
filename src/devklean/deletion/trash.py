from __future__ import annotations

from collections.abc import Sequence

from send2trash import send2trash

from devklean.deletion.metadata import MetadataManager
from devklean.deletion.safety import SafetyValidator
from devklean.logging_setup import get_logger
from devklean.models import CleanableItem, DeleteFailure, DeleteResult

# The single deletion backend is the native OS trash (Recycle Bin on Windows,
# ~/.Trash on macOS, the freedesktop trash on Linux) via send2trash. There is
# only one method, so the name recorded in metadata/history is a literal.
STRATEGY_NAME = "trash"


def delete_items(
    items: Sequence[CleanableItem],
    total_size: int,
    *,
    validator: SafetyValidator | None = None,
    metadata_manager: MetadataManager | None = None,
    dry_run: bool = False,
) -> DeleteResult:
    """Validate, then move safe items to the native OS trash via ``send2trash``.

    Safety validation runs first; only validated ("safe") items are ever passed
    to ``send2trash``. Under ``dry_run`` the function returns the planned result
    *before any ``send2trash`` call is reachable* — the structural guarantee
    that a dry run performs no filesystem operations. Successful deletions are
    recorded in the metadata store (used by ``history`` and ``doctor``).
    """
    validator = validator or SafetyValidator()
    safe, blocked = validator.partition(items)
    blocked_failures = tuple(
        DeleteFailure(path=item.path, error=violation.message) for item, violation in blocked
    )
    safe_total = sum(item.size for item in safe)
    logger = get_logger()

    if dry_run:
        # Structural dry-run guard: no send2trash call below is reachable.
        result = DeleteResult(
            deleted=tuple(item.path for item in safe),
            failed=blocked_failures,
            total_size=safe_total,
        )
        logger.info(
            "dry-run plan strategy=%s would_delete=%d size=%d",
            STRATEGY_NAME,
            result.deleted_count,
            result.total_size,
        )
        return result

    deleted: list[str] = []
    failures: list[DeleteFailure] = []
    for item in safe:
        try:
            send2trash(item.path)
            deleted.append(item.path)
        except OSError as exc:
            # TrashPermissionError subclasses OSError; ENOENT/EACCES and
            # platform-specific failures surface here too. Report the path and
            # keep going so one bad item never aborts the batch.
            failures.append(DeleteFailure(path=item.path, error=str(exc)))

    result = DeleteResult(
        deleted=tuple(deleted),
        failed=tuple(failures) + blocked_failures,
        total_size=safe_total,
    )

    for path in result.deleted:
        logger.info("deleted strategy=%s path=%s", STRATEGY_NAME, path)
    for failure in result.failed:
        logger.warning("delete failed path=%s error=%s", failure.path, failure.error)
    logger.info(
        "deletion summary strategy=%s deleted=%d failed=%d size=%d",
        STRATEGY_NAME,
        result.deleted_count,
        result.failed_count,
        result.total_size,
    )

    manager = metadata_manager or MetadataManager()
    manager.record_successes(items, result, STRATEGY_NAME)
    return result
