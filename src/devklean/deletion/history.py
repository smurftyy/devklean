from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from devklean.deletion.metadata import StoredDeletionMetadata


@dataclass(frozen=True)
class HistoryOperation:
    """A single cleanup operation aggregated from per-item metadata records."""

    run_id: str | None
    timestamp: str
    strategy: str
    item_count: int
    reclaimed_size: int


def build_history(
    records: Sequence[StoredDeletionMetadata],
) -> tuple[HistoryOperation, ...]:
    """Aggregate per-item deletion records into cleanup operations.

    Records sharing a ``run_id`` are grouped into one operation. Legacy
    records without a ``run_id`` each become their own single-item operation.
    Operations are returned newest-first by timestamp.
    """
    grouped: dict[str, list[StoredDeletionMetadata]] = {}
    ungrouped: list[StoredDeletionMetadata] = []

    for stored in records:
        run_id = stored.record.run_id
        if run_id is None:
            ungrouped.append(stored)
        else:
            grouped.setdefault(run_id, []).append(stored)

    operations: list[HistoryOperation] = []

    for run_id, group in grouped.items():
        first = group[0].record
        operations.append(
            HistoryOperation(
                run_id=run_id,
                timestamp=first.timestamp,
                strategy=first.strategy,
                item_count=len(group),
                reclaimed_size=sum(entry.record.item.size for entry in group),
            )
        )

    for stored in ungrouped:
        record = stored.record
        operations.append(
            HistoryOperation(
                run_id=None,
                timestamp=record.timestamp,
                strategy=record.strategy,
                item_count=1,
                reclaimed_size=record.item.size,
            )
        )

    operations.sort(key=lambda op: op.timestamp, reverse=True)
    return tuple(operations)
