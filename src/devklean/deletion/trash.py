from __future__ import annotations

from typing import Sequence

from send2trash import send2trash

from devklean.deletion.base import BaseDeletionStrategy
from devklean.models import CleanableItem, DeleteFailure, DeleteResult


class TrashStrategy(BaseDeletionStrategy):
    """Move deleted items to the native operating-system trash.

    Delegates to ``send2trash``, which uses the real per-platform trash: the
    Recycle Bin on Windows, ``~/.Trash`` on macOS, and the freedesktop trash on
    Linux. The OS owns the trash, so devklean does not track where an item
    landed (``send2trash`` does not expose the destination) and cannot move
    items back — recover them through your file manager's trash instead.

    Safety validation and the dry-run guard live in
    :class:`~devklean.deletion.base.BaseDeletionStrategy`; this class only
    performs the actual trashing of already-validated items.
    """

    name = "trash"

    def _delete_safe(
        self,
        items: Sequence[CleanableItem],
        total_size: int,
    ) -> DeleteResult:
        deleted: list[str] = []
        failed: list[DeleteFailure] = []

        for item in items:
            try:
                send2trash(item.path)
                deleted.append(item.path)
            except OSError as exc:
                # TrashPermissionError subclasses OSError; ENOENT/EACCES and
                # platform-specific failures surface here too. Report the path
                # and keep going so one bad item never aborts the batch.
                failed.append(DeleteFailure(path=item.path, error=str(exc)))

        return DeleteResult(
            deleted=tuple(deleted),
            failed=tuple(failed),
            total_size=total_size,
        )
