from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence
from uuid import uuid4

from devklean.deletion.paths import get_deletion_metadata_dir
from devklean.models import CleanableItem, DeleteResult


@dataclass(frozen=True)
class DeletionMetadataItem:
    original_path: str
    display_name: str
    size: int

    def to_dict(self) -> dict[str, object]:
        return {
            "original_path": self.original_path,
            "display_name": self.display_name,
            "size": self.size,
        }


@dataclass(frozen=True)
class DeletionMetadataRecord:
    schema_version: int
    deletion_id: str
    timestamp: str
    strategy: str
    item: DeletionMetadataItem

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "deletion": {
                "id": self.deletion_id,
                "timestamp": self.timestamp,
                "strategy": self.strategy,
            },
            "item": self.item.to_dict(),
        }


class MetadataManager:
    """Persist deletion metadata in the app data directory."""

    def __init__(self, storage_dir: Path | None = None) -> None:
        self._storage_dir = storage_dir if storage_dir is not None else get_deletion_metadata_dir()

    @property
    def storage_dir(self) -> Path:
        return self._storage_dir

    def record_successes(
        self,
        items: Sequence[CleanableItem],
        result: DeleteResult,
        strategy: str,
    ) -> None:
        deleted_paths = set(result.deleted)
        if not deleted_paths:
            return

        self._storage_dir.mkdir(parents=True, exist_ok=True)

        for item in items:
            if item.path not in deleted_paths:
                continue

            record = DeletionMetadataRecord(
                schema_version=1,
                deletion_id=uuid4().hex,
                timestamp=datetime.now(timezone.utc).isoformat(),
                strategy=strategy,
                item=DeletionMetadataItem(
                    original_path=item.path,
                    display_name=item.display_label,
                    size=item.size,
                ),
            )
            filename = f"{record.timestamp.replace(':', '').replace('+00:00', 'Z')}_{record.deletion_id}.json"
            path = self._storage_dir / filename
            path.write_text(json.dumps(record.to_dict(), indent=2) + "\n", encoding="utf-8")
