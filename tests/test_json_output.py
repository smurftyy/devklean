"""Tests for JSON scan output."""

from __future__ import annotations

import json
from io import StringIO
from pathlib import Path

from devclean.models import CleanableItem
from devclean.output.json import JsonRenderer
from devclean.output.scan_payload import build_scan_payload, serialize_cleanable_item


def test_serialize_cleanable_item() -> None:
    item = CleanableItem(
        path="/tmp/project/node_modules",
        name="node_modules",
        size=1536,
        display_label="Node.js",
    )

    data = serialize_cleanable_item(item)

    assert data == {
        "path": "/tmp/project/node_modules",
        "display_name": "Node.js",
        "size": 1536,
        "formatted_size": "1.5 KB",
        "type": "node_modules",
    }


def test_build_scan_payload_sorts_by_size() -> None:
    items = [
        CleanableItem("/tmp/small", "dist", 100, "Build output"),
        CleanableItem("/tmp/large", "node_modules", 5000, "Node.js"),
    ]

    payload = build_scan_payload("/tmp", items)

    assert payload["version"] == "1.0"
    assert payload["root"] == "/tmp"
    assert payload["items"][0]["type"] == "node_modules"
    assert payload["summary"]["count"] == 2
    assert payload["summary"]["total_size"] == 5100


def test_json_renderer_emits_scan_results(sample_tree: Path) -> None:
    stream = StringIO()
    renderer = JsonRenderer(stream=stream)
    items = [
        CleanableItem(
            path=str(sample_tree / "node_modules"),
            name="node_modules",
            size=1024,
            display_label="Node.js",
        )
    ]

    renderer.scan_start(str(sample_tree))
    renderer.scan_summary(items)

    payload = json.loads(stream.getvalue())
    assert payload["root"] == str(sample_tree)
    assert len(payload["items"]) == 1
    assert payload["items"][0]["display_name"] == "Node.js"


def test_json_renderer_emits_empty_scan() -> None:
    stream = StringIO()
    renderer = JsonRenderer(stream=stream)

    renderer.scan_start("/tmp/empty")
    renderer.nothing_to_clean()

    payload = json.loads(stream.getvalue())
    assert payload["items"] == []
    assert payload["summary"]["count"] == 0


def test_json_renderer_emits_invalid_directory_error() -> None:
    stream = StringIO()
    renderer = JsonRenderer(stream=stream)

    renderer.invalid_directory("/not-a-dir")

    payload = json.loads(stream.getvalue())
    assert payload["error"]["code"] == "invalid_directory"
