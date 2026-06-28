from __future__ import annotations

from devklean.formatting import BOLD, CYAN, DIM, GREEN, RED, RESET, YELLOW, format_size
from devklean.models import CleanableItem, DeleteResult
from devklean.output.sorting import items_by_size_desc


class TextRenderer:
    """ANSI-colored terminal output matching the original CLI presentation."""

    def scan_start(self, root: str) -> None:
        print(f"\n{BOLD}{CYAN}devklean{RESET} {DIM}scanning {root}...{RESET}\n")

    def scan_summary(self, items: list[CleanableItem]) -> int:
        total_size = sum(item.size for item in items)

        print(f"{'TYPE':<18} {'SIZE':>8}  {'PATH'}")
        print(f"{DIM}{'─'*70}{RESET}")

        for item in items_by_size_desc(items):
            color = RED if item.size > 50 * 1024 * 1024 else YELLOW
            print(
                f"{DIM}{item.display_label:<18}{RESET} "
                f"{color}{format_size(item.size):>8}{RESET}  "
                f"{DIM}{item.path}{RESET}"
            )

        print(f"{DIM}{'─'*70}{RESET}")
        print(f"{'TOTAL':<18} {BOLD}{RED}{format_size(total_size):>8}{RESET}\n")

        return total_size

    def nothing_to_clean(self) -> None:
        print(f"{GREEN}✓ Nothing to clean.{RESET}\n")

    def dry_run_nothing_deleted(self) -> None:
        print(f"{YELLOW}[dry-run] nothing deleted.{RESET}\n")

    def dry_run_selected(self, count: int) -> None:
        print(
            f"{YELLOW}[dry-run] {count} director"
            f"{'y' if count == 1 else 'ies'} selected, nothing deleted.{RESET}\n"
        )

    def aborted(self) -> None:
        print(f"\n{DIM}Aborted. Nothing deleted.{RESET}\n")

    def no_items_selected(self) -> None:
        print(f"\n{DIM}No items selected. Nothing deleted.{RESET}\n")

    def invalid_directory(self, path: str) -> None:
        print(f"{RED}Error: '{path}' is not a directory.{RESET}")

    def confirm_prompt(self, count: int) -> str:
        return (
            f"{BOLD}Delete all {count} director"
            f"{'y' if count == 1 else 'ies'}? {DIM}(y/N){RESET} "
        )

    def deletion_result(self, result: DeleteResult) -> None:
        print()
        for path in result.deleted:
            print(f"  {GREEN}✓{RESET} {DIM}{path}{RESET}")
        for failure in result.failed:
            print(f"  {RED}✗{RESET} {failure.path} — {failure.error}")

        deleted = result.deleted_count
        print(
            f"\n{GREEN}{BOLD}Cleaned {deleted} director"
            f"{'y' if deleted == 1 else 'ies'}, "
            f"freed ~{format_size(result.total_size)}.{RESET}"
        )
        if result.failed_count:
            print(f"{RED}{result.failed_count} failed.{RESET}")
        print()
