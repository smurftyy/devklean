from __future__ import annotations

import json
import sys

from devklean.models import CleanableItem, DeleteResult
from devklean.output.scan_payload import (
    build_error_payload,
    build_scan_payload,
)


class JsonRenderer:
    """Machine-readable JSON output for tooling and automation."""

    def __init__(self, *, stream=None) -> None:
        self._stream = stream if stream is not None else sys.stdout
        self._root = ""

    def scan_start(self, root: str) -> None:
        self._root = root

    def scan_summary(self, items: list[CleanableItem]) -> int:
        payload = build_scan_payload(self._root, items)
        self._emit(payload)
        return payload["summary"]["total_size"]

    def nothing_to_clean(self) -> None:
        self._emit(build_scan_payload(self._root, []))

    def dry_run_nothing_deleted(self) -> None:
        pass

    def dry_run_selected(self, count: int) -> None:
        pass

    def aborted(self) -> None:
        pass

    def no_items_selected(self) -> None:
        pass

    def invalid_directory(self, path: str) -> None:
        self._emit(build_error_payload(
            "invalid_directory",
            f"'{path}' is not a directory.",
        ))

    def confirm_prompt(self, count: int) -> str:
        raise NotImplementedError("confirm_prompt is not supported in JSON mode")

    def deletion_result(self, result: DeleteResult) -> None:
        pass

    def _emit(self, payload: dict) -> None:
        json.dump(payload, self._stream, indent=2)
        self._stream.write("\n")
