"""Tests for the deletion backend abstraction."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from devklean.cli.commands.clean import run_standard
from devklean.deletion.metadata import MetadataManager
from devklean.deletion.service import delete_items
from devklean.deletion.trash import TrashStrategy
from devklean.models import CleanableItem, DeleteFailure, DeleteResult


def test_trash_strategy_moves_directory_to_trash(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data-home"))

    source_root = tmp_path / "workspace"
    source = source_root / "node_modules"
    source.mkdir(parents=True)
    (source / "package.json").write_text("{}")

    item = CleanableItem(
        path=str(source),
        name="node_modules",
        size=1024,
        display_label="Node.js",
    )

    result = TrashStrategy().delete([item], total_size=1024)

    trash_target = tmp_path / "data-home" / "Trash" / "files" / "node_modules"
    assert not source.exists()
    assert trash_target.exists()
    assert result.deleted == (str(source),)
    assert result.failed == ()
    assert result.total_size == 1024


@dataclass
class _RecordingRenderer:
    summary_calls: int = 0
    prompt_count: int | None = None
    aborted_calls: int = 0
    dry_run_calls: int = 0
    result: DeleteResult | None = None

    def scan_start(self, root: str) -> None:
        raise AssertionError("scan_start should not be called")

    def scan_summary(self, items: list[CleanableItem]) -> int:
        self.summary_calls += 1
        return sum(item.size for item in items)

    def nothing_to_clean(self) -> None:
        raise AssertionError("nothing_to_clean should not be called")

    def dry_run_nothing_deleted(self) -> None:
        self.dry_run_calls += 1

    def dry_run_selected(self, count: int) -> None:
        raise AssertionError("dry_run_selected should not be called")

    def aborted(self) -> None:
        self.aborted_calls += 1

    def no_items_selected(self) -> None:
        raise AssertionError("no_items_selected should not be called")

    def invalid_directory(self, path: str) -> None:
        raise AssertionError("invalid_directory should not be called")

    def confirm_prompt(self, count: int) -> str:
        self.prompt_count = count
        return "delete?"

    def deletion_result(self, result: DeleteResult) -> None:
        self.result = result


class _RecordingStrategy:
    def __init__(self) -> None:
        self.called = False
        self.name = "recording"

    def delete(self, items, total_size: int) -> DeleteResult:
        self.called = True
        return DeleteResult(
            deleted=tuple(item.path for item in items),
            failed=(),
            total_size=total_size,
        )


def test_run_standard_honors_dry_run_and_skips_backend(monkeypatch) -> None:
    renderer = _RecordingRenderer()
    strategy = _RecordingStrategy()
    items = [CleanableItem("/tmp/node_modules", "node_modules", 100, "Node.js")]

    def fail_input(*args, **kwargs):
        raise AssertionError("input should not be called during dry-run")

    monkeypatch.setattr("builtins.input", fail_input)

    run_standard(renderer, items, True, strategy)

    assert renderer.summary_calls == 1
    assert renderer.dry_run_calls == 1
    assert strategy.called is False
    assert renderer.result is None
    assert renderer.prompt_count is None


def test_run_standard_uses_injected_backend(monkeypatch) -> None:
    renderer = _RecordingRenderer()
    strategy = _RecordingStrategy()
    items = [CleanableItem("/tmp/node_modules", "node_modules", 100, "Node.js")]

    monkeypatch.setattr("builtins.input", lambda prompt: "y")

    run_standard(renderer, items, False, strategy)

    assert renderer.summary_calls == 1
    assert renderer.prompt_count == 1
    assert strategy.called is True
    assert renderer.result is not None
    assert renderer.result.deleted == ("/tmp/node_modules",)


def test_delete_items_records_only_successes(tmp_path: Path) -> None:
    storage_dir = tmp_path / "metadata"
    manager = MetadataManager(storage_dir=storage_dir)
    items = [
        CleanableItem("/tmp/a", "a", 10, "A"),
        CleanableItem("/tmp/b", "b", 20, "B"),
    ]

    class _PartialStrategy:
        name = "trash"

        def delete(self, items, total_size: int) -> DeleteResult:
            return DeleteResult(
                deleted=("/tmp/a",),
                failed=(),
                total_size=total_size,
            )

    result = delete_items(items, 30, _PartialStrategy(), manager)

    records = sorted(storage_dir.glob("*.json"))
    assert len(records) == 1
    payload = json.loads(records[0].read_text(encoding="utf-8"))

    assert result.deleted == ("/tmp/a",)
    assert payload["schema_version"] == 1
    assert payload["deletion"]["strategy"] == "trash"
    assert payload["item"]["original_path"] == "/tmp/a"
    assert payload["item"]["display_name"] == "A"
    assert payload["item"]["size"] == 10


def test_metadata_manager_skips_failed_deletions(tmp_path: Path) -> None:
    storage_dir = tmp_path / "metadata"
    manager = MetadataManager(storage_dir=storage_dir)
    items = [
        CleanableItem("/tmp/a", "a", 10, "A"),
        CleanableItem("/tmp/b", "b", 20, "B"),
    ]
    result = DeleteResult(
        deleted=("/tmp/a",),
        failed=(DeleteFailure(path="/tmp/b", error="permission denied"),),
        total_size=30,
    )

    manager.record_successes(items, result, "trash")

    records = sorted(storage_dir.glob("*.json"))
    assert len(records) == 1
    assert json.loads(records[0].read_text(encoding="utf-8"))["item"]["original_path"] == "/tmp/a"
