from __future__ import annotations

from devklean.deletion.integrity import IntegrityReport, check_integrity
from devklean.deletion.metadata import MetadataManager
from devklean.formatting import BOLD, DIM, GREEN, RED, RESET, YELLOW


def _print_report(report: IntegrityReport) -> None:
    if report.corrupt:
        print(f"\n{RED}{BOLD}CORRUPT ({len(report.corrupt)}){RESET} "
              f"{DIM}— unparseable, will be removed on confirmation{RESET}")
        for entry in report.corrupt:
            print(f"  {RED}✗{RESET} {entry.path.name}  {DIM}— {entry.reason}{RESET}")

    if report.orphaned:
        print(f"\n{YELLOW}{BOLD}ORPHANED ({len(report.orphaned)}){RESET} "
              f"{DIM}— trash gone, cannot restore (reported only, kept){RESET}")
        for orphan in report.orphaned:
            record = orphan.stored.record
            print(f"  {YELLOW}!{RESET} {record.item.display_name}  {DIM}— {orphan.reason}{RESET}")


def run_doctor(args, renderer, config) -> int:
    """Inspect the metadata store and repair confirmed-corrupt records."""
    manager = MetadataManager()
    report = check_integrity(manager)

    if report.healthy:
        print(f"{GREEN}✓ Metadata store is healthy.{RESET}")
        return 0

    _print_report(report)

    if not report.corrupt:
        # Only orphaned records — nothing doctor removes.
        print(f"\n{DIM}No corrupt records to remove. "
              f"Orphaned records are kept as history.{RESET}")
        return 0

    if not getattr(args, "yes", False):
        count = len(report.corrupt)
        plural = "s" if count != 1 else ""
        confirm = input(
            f"\nRemove {count} corrupt metadata record{plural}? (y/N) "
        ).strip().lower()
        if confirm != "y":
            print(f"{DIM}Kept all records. Nothing removed.{RESET}")
            return 0

    removed = 0
    for entry in report.corrupt:
        try:
            entry.path.unlink()
            removed += 1
        except OSError as exc:
            print(f"  {RED}✗{RESET} could not remove {entry.path.name}: {exc}")

    plural = "s" if removed != 1 else ""
    print(f"\n{GREEN}Removed {removed} corrupt metadata record{plural}.{RESET}")
    if report.orphaned:
        kept = len(report.orphaned)
        plural = "s" if kept != 1 else ""
        print(f"{DIM}Kept {kept} orphaned record{plural} (historical).{RESET}")
    return 0
