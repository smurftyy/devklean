from __future__ import annotations

import shutil
from pathlib import Path

from devklean.deletion.metadata import MetadataManager, StoredDeletionMetadata


def restore_metadata_entry(
    manager: MetadataManager,
    entry: StoredDeletionMetadata,
) -> tuple[bool, str]:
    record = entry.record
    trash_path = record.trash_path
    if not trash_path:
        return False, "metadata entry is missing trash location"

    source = Path(trash_path)
    if not source.exists():
        return False, f"missing trash item: {source}"

    destination = Path(record.item.original_path)
    if destination.exists():
        return False, f"destination already exists: {destination}"

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(destination))
    manager.remove_record(entry)
    return True, str(destination)
