from __future__ import annotations

import shutil

from devklean.models import CleanableItem, DeleteFailure, DeleteResult


def delete_items(items: list[CleanableItem], total_size: int) -> DeleteResult:
    deleted: list[str] = []
    failed: list[DeleteFailure] = []

    for item in items:
        try:
            shutil.rmtree(item.path)
            deleted.append(item.path)
        except Exception as e:
            failed.append(DeleteFailure(path=item.path, error=str(e)))

    return DeleteResult(
        deleted=tuple(deleted),
        failed=tuple(failed),
        total_size=total_size,
    )
