"""Integration tests for `devclean scan --json`."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_scan_json_cli(sample_tree: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "devclean", "scan", "--json", str(sample_tree)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["version"] == "1.0"
    assert payload["root"] == str(sample_tree.resolve())
    assert payload["summary"]["count"] >= 1
    assert "display_name" in payload["items"][0]
    assert "formatted_size" in payload["items"][0]


def test_scan_json_empty_tree(empty_tree: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "devclean", "scan", "--json", str(empty_tree)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["items"] == []
    assert payload["summary"]["count"] == 0
