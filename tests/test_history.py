"""Tests for deletion history aggregation and rendering."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from io import StringIO
from pathlib import Path

import pytest

from devklean.deletion.history import HistoryOperation, build_history
from devklean.output.json import JsonRenderer
from devklean.output.text import TextRenderer
from devklean.deletion.metadata import (
    DeletionMetadataItem,
    DeletionMetadataRecord,
    StoredDeletionMetadata,
)
from devklean.output.history_payload import build_history_payload


def _stored(
    *,
    run_id: str | None,
    timestamp: str,
    strategy: str = "trash",
    original_path: str = "/tmp/x",
    display_name: str = "X",
    size: int = 100,
    deletion_id: str = "d0",
) -> StoredDeletionMetadata:
    record = DeletionMetadataRecord(
        schema_version=3,
        deletion_id=deletion_id,
        run_id=run_id,
        timestamp=timestamp,
        strategy=strategy,
        item=DeletionMetadataItem(
            original_path=original_path,
            display_name=display_name,
            size=size,
        ),
    )
    return StoredDeletionMetadata(path=Path(f"/meta/{deletion_id}.json"), record=record)


def test_build_history_groups_records_sharing_a_run_id() -> None:
    records = [
        _stored(run_id="run1", timestamp="2026-06-28T14:00:00+00:00", size=100, deletion_id="a"),
        _stored(run_id="run1", timestamp="2026-06-28T14:00:00+00:00", size=250, deletion_id="b"),
        _stored(run_id="run1", timestamp="2026-06-28T14:00:00+00:00", size=50, deletion_id="c"),
    ]

    operations = build_history(records)

    assert operations == (
        HistoryOperation(
            run_id="run1",
            timestamp="2026-06-28T14:00:00+00:00",
            strategy="trash",
            item_count=3,
            reclaimed_size=400,
        ),
    )


def test_build_history_legacy_records_without_run_id_become_individual_rows() -> None:
    records = [
        _stored(run_id=None, timestamp="2026-06-28T10:00:00+00:00", size=10, deletion_id="a"),
        _stored(run_id=None, timestamp="2026-06-28T11:00:00+00:00", size=20, deletion_id="b"),
    ]

    operations = build_history(records)

    assert len(operations) == 2
    assert all(op.item_count == 1 for op in operations)
    assert {op.reclaimed_size for op in operations} == {10, 20}
    assert all(op.run_id is None for op in operations)


def test_build_history_sorts_newest_first() -> None:
    records = [
        _stored(run_id="old", timestamp="2026-06-28T08:00:00+00:00", deletion_id="a"),
        _stored(run_id="new", timestamp="2026-06-28T20:00:00+00:00", deletion_id="b"),
    ]

    operations = build_history(records)

    assert [op.run_id for op in operations] == ["new", "old"]


def test_build_history_empty_input_returns_empty() -> None:
    assert build_history([]) == ()


def test_build_history_payload_shape() -> None:
    operations = (
        HistoryOperation(
            run_id="run1",
            timestamp="2026-06-28T14:00:00+00:00",
            strategy="trash",
            item_count=3,
            reclaimed_size=400,
        ),
        HistoryOperation(
            run_id=None,
            timestamp="2026-06-01T09:00:00+00:00",
            strategy="trash",
            item_count=1,
            reclaimed_size=42,
        ),
    )

    payload = build_history_payload(operations)

    assert payload["version"] == "1.0"
    assert payload["summary"] == {
        "count": 2,
        "total_reclaimed_size": 442,
        "formatted_total_reclaimed_size": "442.0 B",
    }
    assert payload["operations"][0] == {
        "run_id": "run1",
        "timestamp": "2026-06-28T14:00:00+00:00",
        "strategy": "trash",
        "item_count": 3,
        "reclaimed_size": 400,
        "formatted_reclaimed_size": "400.0 B",
    }
    assert payload["operations"][1]["run_id"] is None


def test_build_history_payload_empty() -> None:
    payload = build_history_payload(())

    assert payload["operations"] == []
    assert payload["summary"]["count"] == 0
    assert payload["summary"]["total_reclaimed_size"] == 0


@pytest.fixture
def utc_timezone(monkeypatch):
    monkeypatch.setenv("TZ", "UTC")
    time.tzset()
    yield
    monkeypatch.undo()
    time.tzset()


def test_json_renderer_emits_history() -> None:
    stream = StringIO()
    renderer = JsonRenderer(stream=stream)
    operations = (
        HistoryOperation("run1", "2026-06-28T14:00:00+00:00", "trash", 3, 400),
    )

    renderer.history(operations, invalid_count=0)

    payload = json.loads(stream.getvalue())
    assert payload["summary"]["count"] == 1
    assert payload["operations"][0]["item_count"] == 3


def test_text_renderer_history_lists_operations(capsys, utc_timezone) -> None:
    operations = (
        HistoryOperation("run1", "2026-06-28T14:02:00+00:00", "trash", 3, 400),
    )

    TextRenderer().history(operations, invalid_count=0)

    out = capsys.readouterr().out
    assert "2026-06-28 14:02" in out
    assert "trash" in out
    assert "3" in out


def test_text_renderer_history_empty_state(capsys) -> None:
    TextRenderer().history((), invalid_count=0)

    assert "No cleanup history" in capsys.readouterr().out


def _write_metadata(directory: Path, *, deletion_id: str, run_id, size: int) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 3,
        "deletion": {
            "id": deletion_id,
            "run_id": run_id,
            "timestamp": "2026-06-28T14:00:00+00:00",
            "strategy": "trash",
        },
        "item": {
            "original_path": f"/tmp/{deletion_id}",
            "display_name": deletion_id,
            "size": size,
        },
    }
    (directory / f"{deletion_id}.json").write_text(json.dumps(payload), encoding="utf-8")


def test_history_command_text_output(tmp_path: Path) -> None:
    deletions = tmp_path / "data" / "devklean" / "deletions"
    _write_metadata(deletions, deletion_id="a", run_id="run1", size=100)
    _write_metadata(deletions, deletion_id="b", run_id="run1", size=300)

    env = {"XDG_DATA_HOME": str(tmp_path / "data"), "PATH": "/usr/bin:/bin"}
    result = subprocess.run(
        [sys.executable, "-m", "devklean", "history"],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )

    assert result.returncode == 0
    assert "STRATEGY" in result.stdout
    assert "trash" in result.stdout
    assert "2" in result.stdout  # two items in the single operation


def test_history_command_json_output(tmp_path: Path) -> None:
    deletions = tmp_path / "data" / "devklean" / "deletions"
    _write_metadata(deletions, deletion_id="a", run_id="run1", size=100)
    _write_metadata(deletions, deletion_id="b", run_id="run1", size=300)

    env = {"XDG_DATA_HOME": str(tmp_path / "data"), "PATH": "/usr/bin:/bin"}
    result = subprocess.run(
        [sys.executable, "-m", "devklean", "history", "--json"],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["summary"]["count"] == 1
    assert payload["operations"][0]["item_count"] == 2
    assert payload["operations"][0]["reclaimed_size"] == 400


def test_history_command_empty_store(tmp_path: Path) -> None:
    env = {"XDG_DATA_HOME": str(tmp_path / "data"), "PATH": "/usr/bin:/bin"}
    result = subprocess.run(
        [sys.executable, "-m", "devklean", "history"],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )

    assert result.returncode == 0
    assert "No cleanup history" in result.stdout
