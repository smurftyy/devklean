from __future__ import annotations

from devklean.formatting import format_size
from devklean.models import CleanableItem
from devklean.output.sorting import items_by_size_desc

SCAN_OUTPUT_VERSION = "1.0"


def build_scan_payload(root: str, items: list[CleanableItem]) -> dict:
    """Build the canonical scan result structure for renderers and tooling."""
    sorted_items = items_by_size_desc(items)
    total_size = sum(item.size for item in items)

    return {
        "version": SCAN_OUTPUT_VERSION,
        "root": root,
        "items": [serialize_cleanable_item(item) for item in sorted_items],
        "summary": {
            "count": len(sorted_items),
            "total_size": total_size,
            "formatted_total_size": format_size(total_size),
        },
    }


def serialize_cleanable_item(item: CleanableItem) -> dict:
    return {
        "path": item.path,
        "display_name": item.display_label,
        "size": item.size,
        "formatted_size": format_size(item.size),
        "type": item.name,
    }


def build_error_payload(code: str, message: str) -> dict:
    return {
        "version": SCAN_OUTPUT_VERSION,
        "error": {
            "code": code,
            "message": message,
        },
    }
