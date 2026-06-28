from __future__ import annotations

from typing import Protocol

from devklean.models import CleanableItem, DeleteResult


class Renderer(Protocol):
    """Output abstraction for presenting devklean results to the user."""

    def scan_start(self, root: str) -> None:
        ...

    def scan_summary(self, items: list[CleanableItem]) -> int:
        ...

    def nothing_to_clean(self) -> None:
        ...

    def dry_run_nothing_deleted(self) -> None:
        ...

    def dry_run_selected(self, count: int) -> None:
        ...

    def aborted(self) -> None:
        ...

    def no_items_selected(self) -> None:
        ...

    def invalid_directory(self, path: str) -> None:
        ...

    def confirm_prompt(self, count: int) -> str:
        ...

    def deletion_result(self, result: DeleteResult) -> None:
        ...
