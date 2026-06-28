from __future__ import annotations

import argparse
import os
import sys

from devclean.deleter import delete_items
from devclean.formatting import BOLD, CYAN, DIM, GREEN, RED, RESET, YELLOW, format_size
from devclean.models import CleanableItem
from devclean.scanner import scan
from devclean.tui import run_interactive


def print_scan_start(root: str) -> None:
    print(f"\n{BOLD}{CYAN}devclean{RESET} {DIM}scanning {root}...{RESET}\n")


def print_summary(found: list[CleanableItem]) -> int:
    total_size = sum(item.size for item in found)

    print(f"{'TYPE':<18} {'SIZE':>8}  {'PATH'}")
    print(f"{DIM}{'─'*70}{RESET}")

    for item in sorted(found, key=lambda x: -x.size):
        color = RED if item.size > 50 * 1024 * 1024 else YELLOW
        print(f"{DIM}{item.display_label:<18}{RESET} {color}{format_size(item.size):>8}{RESET}  {DIM}{item.path}{RESET}")

    print(f"{DIM}{'─'*70}{RESET}")
    print(f"{'TOTAL':<18} {BOLD}{RED}{format_size(total_size):>8}{RESET}\n")

    return total_size


def run_standard(found: list[CleanableItem], dry_run: bool) -> None:
    total_size = print_summary(found)

    if dry_run:
        print(f"{YELLOW}[dry-run] nothing deleted.{RESET}\n")
        return

    confirm = input(f"{BOLD}Delete all {len(found)} director{'y' if len(found)==1 else 'ies'}? {DIM}(y/N){RESET} ").strip().lower()
    if confirm != "y":
        print(f"\n{DIM}Aborted. Nothing deleted.{RESET}\n")
        return

    delete_items(found, total_size)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scan and remove node_modules/venvs to reclaim disk space."
    )
    parser.add_argument(
        "--version",
        action="version",
        version="devclean v1.1.0"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Root directory to scan (default: current directory)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without deleting anything"
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Interactively select items to delete"
    )
    args = parser.parse_args()

    root = os.path.abspath(args.path)
    if not os.path.isdir(root):
        print(f"{RED}Error: '{root}' is not a directory.{RESET}")
        sys.exit(1)

    print_scan_start(root)
    found = scan(root)
    if not found:
        print(f"{GREEN}✓ Nothing to clean.{RESET}\n")
        return

    if args.interactive:
        run_interactive(found, args.dry_run)
    else:
        run_standard(found, args.dry_run)
