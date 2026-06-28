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
class DeletionMetadataTrash:
    path: str

    def to_dict(self) -> dict[str, object]:
        return {"path": self.path}


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
    run_id: str | None
    timestamp: str
    strategy: str
    item: DeletionMetadataItem
    trash: DeletionMetadataTrash | None = None

    def to_dict(self) -> dict[str, object]:
        payload = {
            "schema_version": self.schema_version,
            "deletion": {
                "id": self.deletion_id,
                "run_id": self.run_id,
                "timestamp": self.timestamp,
                "strategy": self.strategy,
            },
            "item": self.item.to_dict(),
        }
        if self.trash is not None:
            payload["trash"] = self.trash.to_dict()
        return payload

    @property
    def trash_path(self) -> str | None:
        if self.trash is None:
            return None
        return self.trash.path


@dataclass(frozen=True)
class StoredDeletionMetadata:
    path: Path
    record: DeletionMetadataRecord


@dataclass(frozen=True)
class CorruptMetadata:
    """A metadata file that could not be parsed, with the reason why."""

    path: Path
    reason: str


@dataclass(frozen=True)
class MetadataLoadResult:
    records: tuple[StoredDeletionMetadata, ...]
    corrupt: tuple[CorruptMetadata, ...]

    @property
    def invalid_count(self) -> int:
        return len(self.corrupt)


def _parse_record_path(path: Path, data: dict[str, object]) -> DeletionMetadataRecord:
    deletion = data.get("deletion")
    item = data.get("item")
    if not isinstance(deletion, dict) or not isinstance(item, dict):
        raise ValueError("missing or invalid 'deletion'/'item' section")

    trash_data = data.get("trash")
    trash = None
    if isinstance(trash_data, dict):
        trash_path = trash_data.get("path")
        if isinstance(trash_path, str) and trash_path:
            trash = DeletionMetadataTrash(path=trash_path)

    deletion_id = deletion.get("id")
    run_id = deletion.get("run_id")
    timestamp = deletion.get("timestamp")
    strategy = deletion.get("strategy")
    original_path = item.get("original_path")
    display_name = item.get("display_name")
    size = item.get("size")

    schema_version = data.get("schema_version", 1)

    if not (
        isinstance(deletion_id, str)
        and (run_id is None or isinstance(run_id, str))
        and isinstance(timestamp, str)
        and isinstance(strategy, str)
        and isinstance(original_path, str)
        and isinstance(display_name, str)
        and isinstance(size, int)
        and isinstance(schema_version, int)
    ):
        raise ValueError("missing or wrong-typed metadata fields")

    return DeletionMetadataRecord(
        schema_version=schema_version,
        deletion_id=deletion_id,
        run_id=run_id,
        timestamp=timestamp,
        strategy=strategy,
        item=DeletionMetadataItem(
            original_path=original_path,
            display_name=display_name,
            size=size,
        ),
        trash=trash,
    )


def _metadata_sort_key(entry: StoredDeletionMetadata) -> str:
    return entry.record.timestamp


class MetadataManager:
    """Persist deletion metadata in the app data directory."""

    def __init__(self, storage_dir: Path | None = None) -> None:
        self._storage_dir = storage_dir if storage_dir is not None else get_deletion_metadata_dir()

    @property
    def storage_dir(self) -> Path:
        return self._storage_dir

    def load_records(self) -> MetadataLoadResult:
        if not self._storage_dir.exists():
            return MetadataLoadResult(records=(), corrupt=())

        records: list[StoredDeletionMetadata] = []
        corrupt: list[CorruptMetadata] = []

        for path in sorted(self._storage_dir.glob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                if not isinstance(data, dict):
                    raise ValueError("metadata file is not a JSON object")
                record = _parse_record_path(path, data)
            except json.JSONDecodeError:
                corrupt.append(CorruptMetadata(path=path, reason="malformed JSON"))
                continue
            except OSError as exc:
                corrupt.append(CorruptMetadata(path=path, reason=f"unreadable file: {exc}"))
                continue
            except (ValueError, TypeError) as exc:
                corrupt.append(CorruptMetadata(path=path, reason=str(exc)))
                continue

            records.append(StoredDeletionMetadata(path=path, record=record))

        records.sort(key=_metadata_sort_key, reverse=True)
        return MetadataLoadResult(records=tuple(records), corrupt=tuple(corrupt))

    def remove_record(self, stored: StoredDeletionMetadata) -> None:
        stored.path.unlink(missing_ok=True)

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

        trashed_paths = iter(result.trashed)
        run_id = uuid4().hex
        timestamp = datetime.now(timezone.utc).isoformat()

        for item in items:
            if item.path not in deleted_paths:
                continue

            trashed_path = next(trashed_paths, None)
            record = DeletionMetadataRecord(
                schema_version=3,
                deletion_id=uuid4().hex,
                run_id=run_id,
                timestamp=timestamp,
                strategy=strategy,
                item=DeletionMetadataItem(
                    original_path=item.path,
                    display_name=item.display_label,
                    size=item.size,
                ),
                trash=DeletionMetadataTrash(path=trashed_path) if trashed_path else None,
            )
            stamp = record.timestamp.replace(":", "").replace("+00:00", "Z")
            filename = f"{stamp}_{record.deletion_id}.json"
            path = self._storage_dir / filename
            path.write_text(json.dumps(record.to_dict(), indent=2) + "\n", encoding="utf-8")
