from __future__ import annotations

import shutil
from collections.abc import Sequence
from pathlib import Path

from send2trash import send2trash

from devklean.config.models import DEFAULT_COMPRESS_FORMAT, DEFAULT_COMPRESS_MIN_SIZE
from devklean.deletion.compression import (
    CompressionVerificationError,
    compress_path,
    verify_archive,
)
from devklean.deletion.metadata import TRASH_STRATEGY, DeletionArchive, MetadataManager
from devklean.deletion.safety import SafetyValidator
from devklean.logging_setup import get_logger
from devklean.models import CleanableItem, DeleteFailure, DeleteResult

# The single deletion backend is the native OS trash (Recycle Bin on Windows,
# ~/.Trash on macOS, the freedesktop trash on Linux) via send2trash. The name
# recorded in metadata/history is the shared constant defined in metadata.py.
STRATEGY_NAME = TRASH_STRATEGY


def delete_items(
    items: Sequence[CleanableItem],
    total_size: int,
    *,
    validator: SafetyValidator | None = None,
    metadata_manager: MetadataManager | None = None,
    dry_run: bool = False,
    compress: bool = False,
    compress_min_size: int = DEFAULT_COMPRESS_MIN_SIZE,
    compress_format: str = DEFAULT_COMPRESS_FORMAT,
) -> DeleteResult:
    """Validate, then move safe items to the native OS trash via ``send2trash``.

    Safety validation runs first; only validated ("safe") items are ever passed
    to ``send2trash``. Under ``dry_run`` the function returns the planned result
    *before any ``send2trash`` call is reachable* — the structural guarantee
    that a dry run performs no filesystem operations. Successful deletions are
    recorded in the metadata store (used by ``history`` and ``doctor``).

    When ``compress`` is set, eligible items go through ``_send_to_trash``'s
    compress -> verify -> trash -> remove-original ordering (see its
    docstring); a failure at any step before the original is removed leaves
    it completely untouched and is reported as a per-item failure, the same
    as any other ``send2trash`` error.
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
    archives: dict[str, DeletionArchive] = {}
    for item in safe:
        try:
            archive = _send_to_trash(
                item,
                compress=compress,
                compress_min_size=compress_min_size,
                compress_format=compress_format,
            )
            if archive is not None:
                archives[item.path] = archive
            deleted.append(item.path)
        except (OSError, CompressionVerificationError) as exc:
            # TrashPermissionError subclasses OSError; ENOENT/EACCES and
            # platform-specific failures surface here too, alongside
            # CompressionVerificationError from a failed compress/verify.
            # Report the path and keep going so one bad item never aborts
            # the batch.
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
        "deletion summary strategy=%s deleted=%d failed=%d size=%d compressed=%d",
        STRATEGY_NAME,
        result.deleted_count,
        result.failed_count,
        result.total_size,
        len(archives),
    )

    manager = metadata_manager or MetadataManager()
    manager.record_successes(items, result, STRATEGY_NAME, archives=archives)
    return result


def _send_to_trash(
    item: CleanableItem,
    *,
    compress: bool,
    compress_min_size: int,
    compress_format: str,
) -> DeletionArchive | None:
    """Send one item to the native OS trash, compressing first when eligible.

    The ordering here is the entire compress-before-trash safety contract:

    1. Compress the source to a temp archive. The source is never touched.
    2. Verify the archive (test-extract + count/size cross-check). The
       source is still untouched; a failure here removes only the temp
       archive and raises — nothing has happened to the source.
    3. ``send2trash`` the *archive*. Only once this call returns successfully
       has anything been "deleted" from the user's perspective.
    4. Only now, with a verified copy already confirmed in the trash, remove
       the original directory directly. This does not also go through
       ``send2trash`` — the archive already serves as the recoverable copy,
       so trashing the original too would duplicate space there and defeat
       the point of compressing first.

    A failure at step 4 (the original can't be removed after all) is
    reported distinctly from a failure at steps 1-3: the archive is already
    safe in the trash, so no data has been lost, but the original directory
    is still on disk and the caller must be told that plainly.
    """
    if not (compress and _should_compress(item, compress_min_size)):
        send2trash(item.path)
        return None

    source = Path(item.path)
    result = compress_path(source, compress_format=compress_format)
    try:
        verify_archive(result)
    except CompressionVerificationError:
        result.archive_path.unlink(missing_ok=True)
        raise

    compressed_size = result.compressed_size  # read now: the file moves to trash next
    try:
        send2trash(str(result.archive_path))
    except OSError:
        result.archive_path.unlink(missing_ok=True)
        raise

    try:
        shutil.rmtree(source)
    except OSError as exc:
        raise OSError(
            f"compressed archive was trashed, but the original directory {source} "
            f"could not be removed ({exc}); remove it manually to reclaim the disk space"
        ) from exc

    return DeletionArchive(
        path=str(result.archive_path),
        format=result.format,
        compressed=True,
        original_size=result.original_size,
        compressed_size=compressed_size,
    )


def _should_compress(item: CleanableItem, compress_min_size: int) -> bool:
    source = Path(item.path)
    if not source.is_dir() or source.is_symlink():
        return False
    return item.size >= compress_min_size
