from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from devklean.deletion.metadata import (
    CorruptMetadata,
    MetadataManager,
    StoredDeletionMetadata,
)


@dataclass(frozen=True)
class OrphanedRecord:
    """A valid record whose trashed item no longer exists on disk."""

    stored: StoredDeletionMetadata
    reason: str


@dataclass(frozen=True)
class IntegrityReport:
    """The outcome of inspecting the metadata store."""

    valid: tuple[StoredDeletionMetadata, ...]
    corrupt: tuple[CorruptMetadata, ...]
    orphaned: tuple[OrphanedRecord, ...]

    @property
    def has_issues(self) -> bool:
        return bool(self.corrupt or self.orphaned)

    @property
    def healthy(self) -> bool:
        return not self.has_issues


def check_integrity(manager: MetadataManager) -> IntegrityReport:
    """Inspect the metadata store for corruption and orphaned trash.

    Corruption is detected on load (malformed JSON, missing fields, type
    mismatches). Orphan detection is one-directional: records whose referenced
    trash path no longer exists. The shared OS trash is never scanned for files
    that have no record, since those may belong to other applications.
    """
    snapshot = manager.load_records()

    valid: list[StoredDeletionMetadata] = []
    orphaned: list[OrphanedRecord] = []

    for stored in snapshot.records:
        trash_path = stored.record.trash_path
        if trash_path and not Path(trash_path).exists():
            orphaned.append(
                OrphanedRecord(
                    stored=stored,
                    reason=f"trash item no longer exists: {trash_path}",
                )
            )
        else:
            valid.append(stored)

    return IntegrityReport(
        valid=tuple(valid),
        corrupt=snapshot.corrupt,
        orphaned=tuple(orphaned),
    )
