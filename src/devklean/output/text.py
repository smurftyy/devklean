from __future__ import annotations

from typing import Sequence

from devklean.deletion.history import HistoryOperation
from devklean.deletion.integrity import IntegrityReport
from devklean.formatting import format_size, format_timestamp
from devklean.models import CleanableItem, DeleteResult
from devklean.output.console import SYM_ERROR, SYM_SUCCESS, Console
from devklean.output.sorting import items_by_size_desc


class TextRenderer:
    """Color-gated terminal output with a standardized symbol scheme."""

    def __init__(self, console: Console | None = None) -> None:
        self._console = console if console is not None else Console()

    def _println(self, text: str = "") -> None:
        self._console.plain(text)

    def scan_start(self, root: str) -> None:
        c = self._console
        banner = f"{c.paint('devklean', 'bold')} {c.paint(f'scanning {root}...', 'detail')}"
        self._println(f"\n{banner}\n")

    def scan_summary(self, items: list[CleanableItem]) -> int:
        c = self._console
        total_size = sum(item.size for item in items)

        self._println(f"{'TYPE':<18} {'SIZE':>8}  {'PATH'}")
        self._println(c.paint("─" * 70, "detail"))

        for item in items_by_size_desc(items):
            role = "error" if item.size > 50 * 1024 * 1024 else "warning"
            self._println(
                f"{c.paint(f'{item.display_label:<18}', 'detail')} "
                f"{c.paint(f'{format_size(item.size):>8}', role)}  "
                f"{c.paint(item.path, 'detail')}"
            )

        self._println(c.paint("─" * 70, "detail"))
        total = c.paint(c.paint(f"{format_size(total_size):>8}", "bold"), "error")
        self._println(f"{'TOTAL':<18} {total}\n")

        return total_size

    def nothing_to_clean(self) -> None:
        self._console.success("Nothing to clean.")
        self._println()

    def dry_run_nothing_deleted(self) -> None:
        self._console.warning("[dry-run] would delete nothing.")
        self._println()

    def dry_run_selected(self, count: int) -> None:
        word = "directory" if count == 1 else "directories"
        self._console.warning(f"[dry-run] would delete {count} {word}; nothing deleted.")
        self._println()

    def aborted(self) -> None:
        self._println()
        self._console.detail("Aborted. Nothing deleted.")
        self._println()

    def no_items_selected(self) -> None:
        self._println()
        self._console.detail("No items selected. Nothing deleted.")
        self._println()

    def invalid_directory(self, path: str) -> None:
        self._console.error(f"'{path}' is not a directory.")

    def confirm_prompt(self, count: int, total_size: int = 0) -> str:
        word = "directory" if count == 1 else "directories"
        return (
            f"{self._console.paint('Delete', 'bold')} {count} {word} "
            f"(~{format_size(total_size)})? "
            f"{self._console.paint('(y/N)', 'detail')} "
        )

    def deletion_result(self, result: DeleteResult) -> None:
        c = self._console
        self._println()
        for path in result.deleted:
            self._println(f"  {c.paint(SYM_SUCCESS, 'success')} {c.paint(path, 'detail')}")
        for failure in result.failed:
            self._println(f"  {c.paint(SYM_ERROR, 'error')} {failure.path} — {failure.error}")

        deleted = result.deleted_count
        word = "directory" if deleted == 1 else "directories"
        self._println()
        self._console.success(
            c.paint(f"Cleaned {deleted} {word}, freed ~{format_size(result.total_size)}.", "bold")
        )
        if result.failed_count:
            self._console.error(f"{result.failed_count} failed.")
        self._println()

    def permission_warnings(self, paths: Sequence[str]) -> None:
        if not paths:
            return
        count = len(paths)
        plural = "s" if count != 1 else ""
        self._console.warning(f"Skipped {count} path{plural} (permission denied):")
        for path in paths:
            self._console.detail(f"    {path}")

    def history(
        self,
        operations: Sequence[HistoryOperation],
        invalid_count: int,
    ) -> None:
        c = self._console
        if not operations:
            c.detail("No cleanup history.")
            self._print_invalid_note(invalid_count)
            return

        self._println(f"\n{c.paint('Cleanup history', 'bold')}\n")
        self._println(f"{'WHEN':<18} {'SIZE':>9}  {'STRATEGY':<10} {'ITEMS':>5}")
        self._println(c.paint("─" * 48, "detail"))

        for op in operations:
            self._println(
                f"{c.paint(f'{format_timestamp(op.timestamp):<18}', 'detail')} "
                f"{c.paint(f'{format_size(op.reclaimed_size):>9}', 'success')}  "
                f"{op.strategy:<10} "
                f"{op.item_count:>5}"
            )
        self._println()
        self._print_invalid_note(invalid_count)

    def _print_invalid_note(self, invalid_count: int) -> None:
        if invalid_count:
            plural = "s" if invalid_count != 1 else ""
            self._console.warning(
                f"Skipped {invalid_count} corrupt metadata record{plural} "
                f"— run `devklean doctor` to inspect."
            )

    # --- doctor ---

    def doctor_healthy(self) -> None:
        self._console.success("Metadata store is healthy.")

    def doctor_corruption_report(self, report: IntegrityReport) -> None:
        c = self._console
        self._println()
        c.warning(
            c.paint(f"CORRUPT ({len(report.corrupt)})", "error")
            + " — unparseable metadata, will be removed on confirmation"
        )
        for entry in report.corrupt:
            c.detail(f"  {SYM_ERROR} {entry.path.name}  — {entry.reason}")

    def doctor_confirm_prompt(self, count: int) -> str:
        plural = "s" if count != 1 else ""
        return f"\nRemove {count} corrupt metadata record{plural}? (y/N) "

    def doctor_kept(self) -> None:
        self._console.detail("Kept all records. Nothing removed.")

    def doctor_removed(self, removed: int) -> None:
        plural = "s" if removed != 1 else ""
        self._println()
        self._console.success(f"Removed {removed} corrupt metadata record{plural}.")

    def doctor_remove_error(self, name: str, error: str) -> None:
        self._console.error(f"could not remove {name}: {error}")

    # --- restore ---

    def restore_help(self) -> None:
        c = self._console
        c.info("devklean moves deleted items to your system trash, not to a devklean-owned store.")
        self._println()
        c.detail("To recover something you deleted:")
        c.detail("  • Windows — open the Recycle Bin and restore the item.")
        c.detail("  • macOS   — open Trash in Finder and 'Put Back'.")
        c.detail("  • Linux   — open Trash in your file manager and restore.")
        c.detail(
            "If compression was enabled, restore the archive from trash and unpack it "
            "to the original path."
        )
        self._println()
        c.detail("Run `devklean history` to see what was removed and when.")
