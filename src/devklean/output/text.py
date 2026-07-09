from __future__ import annotations

from typing import Sequence

from devklean.deletion.history import HistoryOperation
from devklean.deletion.integrity import IntegrityReport
from devklean.formatting import format_size, format_timestamp, truncate
from devklean.models import CleanableItem, DeleteResult
from devklean.output.console import SYM_ERROR, SYM_SUCCESS, Console
from devklean.output.sorting import items_by_size_desc
from devklean.signatures import ArtifactSignature
from devklean.signatures.analysis import AnalysisReport


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

    # --- explain ---

    def explain_match(self, path: str, signature: ArtifactSignature) -> None:
        c = self._console
        self._println()
        c.success(path)
        self._println(f"  {c.paint('ecosystem:', 'detail')}    {signature.ecosystem}")
        self._println(f"  {c.paint('generated by:', 'detail')} {signature.generated_by}")
        self._println(f"  {c.paint('regenerate:', 'detail')}   {signature.regenerate_command}")
        self._println(f"  {c.paint('risk:', 'detail')}         {signature.risk.value}")
        self._println(f"  {c.paint('confidence:', 'detail')}   {signature.confidence:.2f}")
        self._println(f"  {c.paint('why:', 'detail')}          {signature.rationale}")
        self._println()

    def explain_no_match(self, path: str) -> None:
        c = self._console
        self._println()
        c.warning(path)
        c.detail("  not recognized — no signature in the registry for this directory name.")
        c.detail("  no risk or confidence verdict is given for unrecognized paths.")
        self._println()

    # --- analyze ---

    def analysis_report(self, report: AnalysisReport, *, verbose: bool = False) -> None:
        c = self._console
        self._println()
        self._println(f"{c.paint('devklean analyze', 'bold')} {c.paint(report.root, 'detail')}")
        self._println()

        self._println(c.paint("RECOGNIZED — safe to remove (per signature registry)", "bold"))
        if not report.recognized:
            c.detail("  none")
        else:
            self._println(f"  {'TYPE':<18} {'SIZE':>10}  {'RISK':<8} {'ECOSYSTEM':<28} STALENESS")
            self._println(c.paint("  " + "─" * 100, "detail"))
            ordered = sorted(report.recognized, key=lambda rc: rc.item.size, reverse=True)
            for rc in ordered:
                self._println(
                    f"  {c.paint(f'{rc.item.display_label:<18}', 'detail')} "
                    f"{format_size(rc.item.size):>10}  "
                    f"{rc.signature.risk.value:<8} "
                    f"{truncate(rc.signature.ecosystem, 28):<28} "
                    f"{rc.staleness.detail}"
                )
        self._println()

        self._println(c.paint("NOT RECOGNIZED — skipped (no signature registry entry)", "bold"))
        if not report.unrecognized:
            c.detail("  none")
        else:
            for item in report.unrecognized:
                c.detail(f"  {item.display_label:<18} {item.path}")
        self._println()

        self._println(c.paint("STRUCTURAL", "bold"))
        if not report.lockfile_conflicts:
            c.detail("  no structural issues found")
        else:
            for conflict in report.lockfile_conflicts:
                c.warning(
                    f"  conflicting lockfiles in {conflict.project_root}: "
                    f"{', '.join(conflict.lockfiles)}"
                )
        self._println()

        score = report.health.score
        role = "success" if score >= 70 else "warning" if score >= 40 else "error"
        self._println(c.paint("WORKSPACE HEALTH: ", "bold") + c.paint(f"{score}/100", role))
        if verbose:
            inputs = report.health.inputs
            c.detail(f"  formula: {report.health.formula}")
            c.detail(
                "  inputs: "
                f"recognized_weighted_size={inputs.recognized_weighted_size:.0f} "
                f"recognized_total_size={inputs.recognized_total_size} "
                f"unrecognized_total_size={inputs.unrecognized_total_size} "
                f"lockfile_conflicts={inputs.lockfile_conflicts}"
            )
        self._println()

    # --- restore ---

    def restore_help(self) -> None:
        c = self._console
        c.info("devklean moves deleted items to your system trash, not to a devklean-owned store.")
        self._println()
        c.detail("To recover something you deleted:")
        c.detail("  • Windows — open the Recycle Bin and restore the item.")
        c.detail("  • macOS   — open Trash in Finder and 'Put Back'.")
        c.detail("  • Linux   — open Trash in your file manager and restore.")
        self._println()
        c.detail(
            "If it was deleted with --compress, what's sitting in the trash is a "
            "compressed archive (.tar.gz, or .tar.zst if zstd was used) — not the "
            "original directory."
        )
        c.detail(
            "After restoring the archive from trash, extract it yourself to get the "
            "files back, e.g. `tar -xf <name>.tar.gz` (or `tar --zstd -xf <name>.tar.zst`)."
        )
        self._println()
        c.detail(
            "Run `devklean history` to see what was removed, when, and whether it was "
            "compressed."
        )
