from __future__ import annotations

from typing import Protocol, Sequence

from devklean.models import CleanableItem, DeleteResult


class DeletionStrategy(Protocol):
    """Contract for backends that remove cleanable items."""

    name: str

    def delete(
        self,
        items: Sequence[CleanableItem],
        total_size: int,
        dry_run: bool = False,
    ) -> DeleteResult: ...
