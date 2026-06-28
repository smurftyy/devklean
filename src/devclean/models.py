from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CleanableItem:
    """A discovered directory that devclean can remove."""

    path: str
    name: str
    size: int
    display_label: str


@dataclass(frozen=True)
class DeleteFailure:
    path: str
    error: str


@dataclass(frozen=True)
class DeleteResult:
    deleted: tuple[str, ...]
    failed: tuple[DeleteFailure, ...]
    total_size: int

    @property
    def deleted_count(self) -> int:
        return len(self.deleted)

    @property
    def failed_count(self) -> int:
        return len(self.failed)
