from __future__ import annotations

from typing import Sequence

from devklean.deletion.history import HistoryOperation
from devklean.formatting import format_size, format_timestamp
from devklean.models import CleanableItem, DeleteResult
from devklean.output.console import SYM_ERROR, SYM_SUCCESS, Console
from devklean.output.sorting import items_by_size_desc


class TextRenderer:
    """Color-gated terminal output with a standardized symbol scheme."""

    def __init__(self, console: Console | None = None) -> None:
        self._c = console if console is not None else Console()

    def _p(self, text: str = "") -> None:
        self._c.plain(text)

    def scan_start(self, root: str) -> None:
        c = self._c
        self._p(f"\n{c.paint('devklean', 'bold')} {c.paint(f'scanning {root}...', 'detail')}\n")

    def scan_summary(self, items: list[CleanableItem]) -> int:
        c = self._c
        total_size = sum(item.size for item in items)

        self._p(f"{'TYPE':<18} {'SIZE':>8}  {'PATH'}")
        self._p(c.paint("─" * 70, "detail"))

        for item in items_by_size_desc(items):
            role = "error" if item.size > 50 * 1024 * 1024 else "warning"
            self._p(
                f"{c.paint(f'{item.display_label:<18}', 'detail')} "
                f"{c.paint(f'{format_size(item.size):>8}', role)}  "
                f"{c.paint(item.path, 'detail')}"
            )

        self._p(c.paint("─" * 70, "detail"))
        total = c.paint(c.paint(f"{format_size(total_size):>8}", "bold"), "error")
        self._p(f"{'TOTAL':<18} {total}\n")

        return total_size

    def nothing_to_clean(self) -> None:
        self._c.success("Nothing to clean.")
        self._p()

    def dry_run_nothing_deleted(self) -> None:
        self._c.warning("[dry-run] would delete nothing.")
        self._p()

    def dry_run_selected(self, count: int) -> None:
        word = "directory" if count == 1 else "directories"
        self._c.warning(f"[dry-run] would delete {count} {word}; nothing deleted.")
        self._p()

    def aborted(self) -> None:
        self._p()
        self._c.detail("Aborted. Nothing deleted.")
        self._p()

    def no_items_selected(self) -> None:
        self._p()
        self._c.detail("No items selected. Nothing deleted.")
        self._p()

    def invalid_directory(self, path: str) -> None:
        self._c.error(f"'{path}' is not a directory.")

    def confirm_prompt(self, count: int, total_size: int = 0) -> str:
        word = "directory" if count == 1 else "directories"
        return (
            f"{self._c.paint('Delete', 'bold')} {count} {word} "
            f"(~{format_size(total_size)})? "
            f"{self._c.paint('(y/N)', 'detail')} "
        )

    def deletion_result(self, result: DeleteResult) -> None:
        c = self._c
        self._p()
        for path in result.deleted:
            self._p(f"  {c.paint(SYM_SUCCESS, 'success')} {c.paint(path, 'detail')}")
        for failure in result.failed:
            self._p(f"  {c.paint(SYM_ERROR, 'error')} {failure.path} — {failure.error}")

        deleted = result.deleted_count
        word = "directory" if deleted == 1 else "directories"
        self._p()
        self._c.success(
            c.paint(f"Cleaned {deleted} {word}, freed ~{format_size(result.total_size)}.", "bold")
        )
        if result.failed_count:
            self._c.error(f"{result.failed_count} failed.")
        self._p()

    def permission_warnings(self, paths: Sequence[str]) -> None:
        if not paths:
            return
        count = len(paths)
        plural = "s" if count != 1 else ""
        self._c.warning(f"Skipped {count} path{plural} (permission denied):")
        for path in paths:
            self._c.detail(f"    {path}")

    def history(
        self,
        operations: Sequence[HistoryOperation],
        invalid_count: int,
    ) -> None:
        c = self._c
        if not operations:
            c.detail("No cleanup history.")
            self._print_invalid_note(invalid_count)
            return

        self._p(f"\n{c.paint('Cleanup history', 'bold')}\n")
        self._p(f"{'WHEN':<18} {'SIZE':>9}  {'STRATEGY':<10} {'ITEMS':>5}")
        self._p(c.paint("─" * 48, "detail"))

        for op in operations:
            self._p(
                f"{c.paint(f'{format_timestamp(op.timestamp):<18}', 'detail')} "
                f"{c.paint(f'{format_size(op.reclaimed_size):>9}', 'success')}  "
                f"{op.strategy:<10} "
                f"{op.item_count:>5}"
            )
        self._p()
        self._print_invalid_note(invalid_count)

    def _print_invalid_note(self, invalid_count: int) -> None:
        if invalid_count:
            plural = "s" if invalid_count != 1 else ""
            self._c.warning(
                f"Skipped {invalid_count} corrupt metadata record{plural} "
                f"— run `devclean doctor` to inspect."
            )
