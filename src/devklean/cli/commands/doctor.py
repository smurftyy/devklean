from __future__ import annotations

from devklean.deletion.integrity import IntegrityReport, check_integrity
from devklean.deletion.metadata import MetadataManager
from devklean.output.console import Console


def _print_report(console: Console, report: IntegrityReport) -> None:
    console.plain()
    console.warning(
        console.paint(f"CORRUPT ({len(report.corrupt)})", "error")
        + " — unparseable metadata, will be removed on confirmation"
    )
    for entry in report.corrupt:
        console.detail(f"  ✗ {entry.path.name}  — {entry.reason}")


def run_doctor(args, renderer, config) -> int:
    """Inspect the metadata store and remove confirmed-corrupt records."""
    console = Console()
    report = check_integrity(MetadataManager())

    if report.healthy:
        console.success("Metadata store is healthy.")
        return 0

    _print_report(console, report)

    if not getattr(args, "yes", False):
        count = len(report.corrupt)
        plural = "s" if count != 1 else ""
        confirm = input(f"\nRemove {count} corrupt metadata record{plural}? (y/N) ").strip().lower()
        if confirm != "y":
            console.detail("Kept all records. Nothing removed.")
            return 0

    removed = 0
    for entry in report.corrupt:
        try:
            entry.path.unlink()
            removed += 1
        except OSError as exc:
            console.error(f"could not remove {entry.path.name}: {exc}")

    plural = "s" if removed != 1 else ""
    console.plain()
    console.success(f"Removed {removed} corrupt metadata record{plural}.")
    return 0
