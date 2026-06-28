from __future__ import annotations

from typing import Sequence

from devklean.deletion.history import HistoryOperation
from devklean.formatting import format_size

HISTORY_OUTPUT_VERSION = "1.0"


def build_history_payload(operations: Sequence[HistoryOperation]) -> dict:
    """Build the canonical history result structure for renderers and tooling."""
    total_reclaimed_size = sum(op.reclaimed_size for op in operations)

    return {
        "version": HISTORY_OUTPUT_VERSION,
        "operations": [serialize_history_operation(op) for op in operations],
        "summary": {
            "count": len(operations),
            "total_reclaimed_size": total_reclaimed_size,
            "formatted_total_reclaimed_size": format_size(total_reclaimed_size),
        },
    }


def serialize_history_operation(operation: HistoryOperation) -> dict:
    return {
        "run_id": operation.run_id,
        "timestamp": operation.timestamp,
        "strategy": operation.strategy,
        "item_count": operation.item_count,
        "reclaimed_size": operation.reclaimed_size,
        "formatted_reclaimed_size": format_size(operation.reclaimed_size),
    }
