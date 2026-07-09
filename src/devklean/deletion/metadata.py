from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping, Sequence
from uuid import uuid4

from devklean.deletion.paths import get_deletion_metadata_dir
from devklean.models import CleanableItem, DeleteResult

# The only recognized strategy value. Shared with trash.py's STRATEGY_NAME so
# the write side and this validation can't drift; a record with any other value
# was written by a removed backend and is treated as corrupt.
TRASH_STRATEGY = "trash"
# Bumped for the archive dict gaining compressed/original_size/compressed_size;
# the new fields are optional on read so schema_version <= 4 records still parse.
SCHEMA_VERSION = 5


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
class DeletionArchive:
    path: str
    format: str
    # True whenever this record was produced by the compress-before-trash path
    # (the only path that creates DeletionArchive today). Kept as an explicit
    # field rather than inferred from archive-presence so future callers can
    # record an archive without implying it was compressed.
    compressed: bool = True
    original_size: int | None = None
    compressed_size: int | None = None

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "path": self.path,
            "format": self.format,
            "compressed": self.compressed,
        }
        if self.original_size is not None:
            payload["original_size"] = self.original_size
        if self.compressed_size is not None:
            payload["compressed_size"] = self.compressed_size
        return payload


@dataclass(frozen=True)
class DeletionMetadataRecord:
    schema_version: int
    deletion_id: str
    run_id: str | None
    timestamp: str
    strategy: str
    item: DeletionMetadataItem
    archive: DeletionArchive | None = None

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
        if self.archive is not None:
            payload["archive"] = self.archive.to_dict()
        return payload


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


def _parse_record(data: dict[str, object]) -> DeletionMetadataRecord:
    deletion = data.get("deletion")
    item = data.get("item")
    if not isinstance(deletion, dict) or not isinstance(item, dict):
        raise ValueError("missing or invalid 'deletion'/'item' section")

    deletion_id = deletion.get("id")
    run_id = deletion.get("run_id")
    timestamp = deletion.get("timestamp")
    strategy = deletion.get("strategy")
    original_path = item.get("original_path")
    display_name = item.get("display_name")
    size = item.get("size")
    archive_data = data.get("archive")

    # Records predating the schema_version field are treated as v1. Any integer
    # version is accepted as-is; there are no migrations yet.
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

    archive: DeletionArchive | None = None
    if archive_data is not None:
        if not isinstance(archive_data, dict):
            raise ValueError("missing or invalid 'archive' section")
        archive_path = archive_data.get("path")
        archive_format = archive_data.get("format")
        if not isinstance(archive_path, str) or not isinstance(archive_format, str):
            raise ValueError("missing or wrong-typed archive fields")

        # compressed/original_size/compressed_size postdate schema_version 4;
        # older records simply lack them, so absence is not an error.
        compressed = archive_data.get("compressed", True)
        original_size = archive_data.get("original_size")
        compressed_size = archive_data.get("compressed_size")
        if not isinstance(compressed, bool):
            raise ValueError("archive 'compressed' field must be a boolean")
        if original_size is not None and not isinstance(original_size, int):
            raise ValueError("archive 'original_size' field must be an integer")
        if compressed_size is not None and not isinstance(compressed_size, int):
            raise ValueError("archive 'compressed_size' field must be an integer")

        archive = DeletionArchive(
            path=archive_path,
            format=archive_format,
            compressed=compressed,
            original_size=original_size,
            compressed_size=compressed_size,
        )

    if strategy != TRASH_STRATEGY:
        raise ValueError(f"unrecognized strategy {strategy!r}")

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
        archive=archive,
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
                record = _parse_record(data)
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

    def remove_record(self, entry: StoredDeletionMetadata | CorruptMetadata) -> None:
        """Delete a single metadata file from the store (valid or corrupt)."""
        entry.path.unlink(missing_ok=True)

    def record_successes(
        self,
        items: Sequence[CleanableItem],
        result: DeleteResult,
        strategy: str,
        archives: Mapping[str, DeletionArchive] | None = None,
    ) -> None:
        deleted_paths = set(result.deleted)
        if not deleted_paths:
            return

        self._storage_dir.mkdir(parents=True, exist_ok=True)

        run_id = uuid4().hex
        timestamp = datetime.now(timezone.utc).isoformat()
        archives = archives or {}

        for item in items:
            if item.path not in deleted_paths:
                continue

            archive = archives.get(item.path)

            record = DeletionMetadataRecord(
                schema_version=SCHEMA_VERSION,
                deletion_id=uuid4().hex,
                run_id=run_id,
                timestamp=timestamp,
                strategy=strategy,
                item=DeletionMetadataItem(
                    original_path=item.path,
                    display_name=item.display_label,
                    size=item.size,
                ),
                archive=archive,
            )
            stamp = record.timestamp.replace(":", "").replace("+00:00", "Z")
            filename = f"{stamp}_{record.deletion_id}.json"
            path = self._storage_dir / filename
            path.write_text(json.dumps(record.to_dict(), indent=2) + "\n", encoding="utf-8")
