"""Tests for metadata corruption diagnostics and integrity checking."""

from __future__ import annotations

import json
from pathlib import Path

from devklean.deletion.integrity import (
    IntegrityReport,
    OrphanedRecord,
    check_integrity,
)
from devklean.deletion.metadata import CorruptMetadata, MetadataManager


def _valid_payload(*, deletion_id: str, trash_path: str | None, size: int = 100) -> dict:
    payload = {
        "schema_version": 3,
        "deletion": {
            "id": deletion_id,
            "run_id": "run1",
            "timestamp": "2026-06-28T14:00:00+00:00",
            "strategy": "trash",
        },
        "item": {
            "original_path": f"/tmp/{deletion_id}",
            "display_name": deletion_id,
            "size": size,
        },
    }
    if trash_path is not None:
        payload["trash"] = {"path": trash_path}
    return payload


def _write(directory: Path, name: str, payload) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / name
    if isinstance(payload, str):
        path.write_text(payload, encoding="utf-8")
    else:
        path.write_text(json.dumps(payload), encoding="utf-8")
    return path


# --- metadata corruption diagnostics ---


def test_load_records_reports_malformed_json_with_reason(tmp_path: Path) -> None:
    _write(tmp_path, "bad.json", "{ not valid json")

    result = MetadataManager(storage_dir=tmp_path).load_records()

    assert result.records == ()
    assert len(result.corrupt) == 1
    corrupt = result.corrupt[0]
    assert isinstance(corrupt, CorruptMetadata)
    assert corrupt.path.name == "bad.json"
    assert "json" in corrupt.reason.lower()
    assert result.invalid_count == 1


def test_load_records_reports_missing_fields(tmp_path: Path) -> None:
    _write(tmp_path, "incomplete.json", {"schema_version": 3, "deletion": {}})

    result = MetadataManager(storage_dir=tmp_path).load_records()

    assert result.records == ()
    assert len(result.corrupt) == 1
    assert result.corrupt[0].path.name == "incomplete.json"


def test_load_records_keeps_valid_and_isolates_corrupt(tmp_path: Path) -> None:
    _write(tmp_path, "good.json", _valid_payload(deletion_id="a", trash_path=None))
    _write(tmp_path, "bad.json", "{garbage")

    result = MetadataManager(storage_dir=tmp_path).load_records()

    assert len(result.records) == 1
    assert len(result.corrupt) == 1


# --- integrity checking ---


def test_check_integrity_healthy_store(tmp_path: Path) -> None:
    trash = tmp_path / "trash" / "node_modules"
    trash.mkdir(parents=True)
    _write(
        tmp_path / "meta",
        "a.json",
        _valid_payload(deletion_id="a", trash_path=str(trash)),
    )

    report = check_integrity(MetadataManager(storage_dir=tmp_path / "meta"))

    assert isinstance(report, IntegrityReport)
    assert report.healthy
    assert len(report.valid) == 1
    assert report.corrupt == ()
    assert report.orphaned == ()


def test_check_integrity_detects_orphaned_record(tmp_path: Path) -> None:
    _write(
        tmp_path / "meta",
        "gone.json",
        _valid_payload(deletion_id="g", trash_path=str(tmp_path / "trash" / "missing")),
    )

    report = check_integrity(MetadataManager(storage_dir=tmp_path / "meta"))

    assert not report.healthy
    assert len(report.orphaned) == 1
    orphan = report.orphaned[0]
    assert isinstance(orphan, OrphanedRecord)
    assert "missing" in orphan.reason


def test_check_integrity_separates_corrupt_and_orphaned(tmp_path: Path) -> None:
    meta = tmp_path / "meta"
    _write(meta, "bad.json", "{nope")
    _write(
        meta,
        "gone.json",
        _valid_payload(deletion_id="g", trash_path=str(tmp_path / "trash" / "missing")),
    )

    report = check_integrity(MetadataManager(storage_dir=meta))

    assert len(report.corrupt) == 1
    assert len(report.orphaned) == 1
    assert report.valid == ()


def test_check_integrity_record_without_trash_is_valid_not_orphaned(tmp_path: Path) -> None:
    _write(tmp_path / "meta", "a.json", _valid_payload(deletion_id="a", trash_path=None))

    report = check_integrity(MetadataManager(storage_dir=tmp_path / "meta"))

    assert report.healthy
    assert len(report.valid) == 1
    assert report.orphaned == ()
