"""Tests for metadata corruption diagnostics and integrity checking."""

from __future__ import annotations

import json
from pathlib import Path

from devklean.deletion.integrity import IntegrityReport, check_integrity
from devklean.deletion.metadata import CorruptMetadata, MetadataManager


def _valid_payload(
    *,
    deletion_id: str,
    trash_path: str | None,
    size: int = 100,
    archive_path: str | None = None,
    compression_format: str | None = None,
) -> dict:
    payload = {
        "schema_version": 4,
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
    if archive_path is not None:
        payload["archive"] = {"path": archive_path, "format": compression_format or "zip"}
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
    _write(tmp_path / "meta", "a.json", _valid_payload(deletion_id="a", trash_path=None))

    report = check_integrity(MetadataManager(storage_dir=tmp_path / "meta"))

    assert isinstance(report, IntegrityReport)
    assert report.healthy
    assert len(report.valid) == 1
    assert report.corrupt == ()


def test_check_integrity_reports_corrupt(tmp_path: Path) -> None:
    meta = tmp_path / "meta"
    _write(meta, "good.json", _valid_payload(deletion_id="a", trash_path=None))
    _write(meta, "bad.json", "{nope")

    report = check_integrity(MetadataManager(storage_dir=meta))

    assert not report.healthy
    assert len(report.corrupt) == 1
    assert len(report.valid) == 1


def test_load_records_flags_unrecognized_strategy_as_corrupt(tmp_path: Path) -> None:
    # Records written by older builds carried strategy values ("recording",
    # "rec") that no longer name a real deletion backend. The only valid
    # strategy is "trash"; anything else is semantically corrupt.
    payload = _valid_payload(deletion_id="a", trash_path=None)
    payload["deletion"]["strategy"] = "recording"
    _write(tmp_path, "stale.json", payload)

    result = MetadataManager(storage_dir=tmp_path).load_records()

    assert result.records == ()
    assert len(result.corrupt) == 1
    assert "strategy" in result.corrupt[0].reason.lower()


def test_check_integrity_flags_unrecognized_strategy(tmp_path: Path) -> None:
    meta = tmp_path / "meta"
    _write(meta, "good.json", _valid_payload(deletion_id="a", trash_path=None))
    stale = _valid_payload(deletion_id="b", trash_path=None)
    stale["deletion"]["strategy"] = "rec"
    _write(meta, "stale.json", stale)

    report = check_integrity(MetadataManager(storage_dir=meta))

    assert not report.healthy
    assert len(report.valid) == 1
    assert len(report.corrupt) == 1


def test_check_integrity_does_not_treat_missing_trash_as_a_problem(tmp_path: Path) -> None:
    # Items now go to the native OS trash, which devklean does not track. A
    # record that references a no-longer-present path is still a valid record;
    # orphan detection has been removed with the move to send2trash.
    _write(
        tmp_path / "meta",
        "gone.json",
        _valid_payload(deletion_id="g", trash_path=str(tmp_path / "trash" / "missing")),
    )

    report = check_integrity(MetadataManager(storage_dir=tmp_path / "meta"))

    assert report.healthy
    assert len(report.valid) == 1


def test_check_integrity_accepts_compressed_metadata(tmp_path: Path) -> None:
    meta = tmp_path / "meta"
    _write(
        meta,
        "compressed.json",
        _valid_payload(
            deletion_id="c",
            trash_path=None,
            archive_path="/tmp/c.zip",
            compression_format="zip",
        ),
    )

    report = check_integrity(MetadataManager(storage_dir=meta))

    assert report.healthy
    assert len(report.valid) == 1
