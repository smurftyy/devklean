from __future__ import annotations

from pathlib import Path

from devklean.deletion.metadata import MetadataManager, StoredDeletionMetadata
from devklean.deletion.restore import restore_metadata_entry
from devklean.formatting import format_size


def _selection_prompt(count: int) -> str:
    return (
        f"Restore which items? "
        f"{count} available. "
        f"Enter comma-separated numbers, 'a' for all, or ENTER to cancel: "
    )


def _confirm_prompt(count: int) -> str:
    return f"Restore {count} item{'s' if count != 1 else ''}? (y/N) "


def _format_status(entry: StoredDeletionMetadata) -> str:
    record = entry.record
    if not record.trash_path:
        return "invalid metadata"
    if not Path(record.trash_path).exists():
        return "missing trash item"
    return "available"


def _print_listing(entries: list[StoredDeletionMetadata]) -> None:
    print("\nAvailable deleted items:\n")
    for index, entry in enumerate(entries, start=1):
        record = entry.record
        status = _format_status(entry)
        print(
            f"{index:>2}. {record.item.display_name:<18} "
            f"{format_size(record.item.size):>8}  "
            f"{record.item.original_path}  "
            f"[{status}]"
        )
    print()


def _parse_selection(selection: str, count: int) -> list[int]:
    selection = selection.strip().lower()
    if not selection:
        return []
    if selection in {"a", "all"}:
        return list(range(count))

    indices: list[int] = []
    seen: set[int] = set()
    for token in selection.split(","):
        token = token.strip()
        if not token:
            continue
        if not token.isdigit():
            continue
        value = int(token)
        if value < 1 or value > count:
            continue
        index = value - 1
        if index in seen:
            continue
        seen.add(index)
        indices.append(index)
    return indices


def run_restore(args, renderer, config) -> int:
    """List deleted items from metadata and restore selected entries."""
    manager = MetadataManager()
    snapshot = manager.load_records()
    entries = list(snapshot.records)

    if not entries:
        print("No deleted items available to restore.")
        return 0

    _print_listing(entries)

    if snapshot.invalid_count:
        print(f"Skipped {snapshot.invalid_count} invalid metadata file"
              f"{'s' if snapshot.invalid_count != 1 else ''}.")

    selection = input(_selection_prompt(len(entries)))
    selected_indices = _parse_selection(selection, len(entries))
    if not selected_indices:
        print("No items selected. Nothing restored.")
        return 0

    confirm = input(_confirm_prompt(len(selected_indices))).strip().lower()
    if confirm != "y":
        print("Aborted. Nothing restored.")
        return 0

    restored: list[str] = []
    skipped: list[str] = []
    failed: list[str] = []

    for index in selected_indices:
        entry = entries[index]
        ok, message = restore_metadata_entry(manager, entry)
        if ok:
            restored.append(message)
            print(f"  ✓ {message}")
        else:
            skipped.append(entry.record.item.original_path)
            print(f"  - {entry.record.item.original_path}: {message}")

    print(
        f"\nRestored {len(restored)} item"
        f"{'s' if len(restored) != 1 else ''}. "
        f"Skipped {len(skipped)}."
    )
    return 0
