from __future__ import annotations

from dataclasses import dataclass

from devklean.deletion.metadata import (
    CorruptMetadata,
    MetadataManager,
    StoredDeletionMetadata,
)


@dataclass(frozen=True)
class IntegrityReport:
    """The outcome of inspecting the metadata store."""

    valid: tuple[StoredDeletionMetadata, ...]
    corrupt: tuple[CorruptMetadata, ...]

    @property
    def has_issues(self) -> bool:
        return bool(self.corrupt)

    @property
    def healthy(self) -> bool:
        return not self.has_issues


def check_integrity(manager: MetadataManager) -> IntegrityReport:
    """Inspect the metadata store for corruption.

    Detects malformed JSON, missing fields, and type mismatches on load.

    Orphan detection (records whose trashed item was later emptied from the
    trash) is no longer possible: items go to the native OS trash via
    ``send2trash``, which devklean neither owns nor tracks, so there is no trash
    path to check for existence.
    """
    snapshot = manager.load_records()
    return IntegrityReport(valid=snapshot.records, corrupt=snapshot.corrupt)
