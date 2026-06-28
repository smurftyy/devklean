from __future__ import annotations

import argparse
import os
import sys

from devclean.deleter import delete_items
from devclean.models import CleanableItem
from devclean.output import Renderer, TextRenderer
from devclean.scanner import scan
from devclean.tui import run_interactive


def run_standard(renderer: Renderer, found: list[CleanableItem], dry_run: bool) -> None:
    total_size = renderer.scan_summary(found)

    if dry_run:
        renderer.dry_run_nothing_deleted()
        return

    confirm = input(renderer.confirm_prompt(len(found))).strip().lower()
    if confirm != "y":
        renderer.aborted()
        return

    result = delete_items(found, total_size)
    renderer.deletion_result(result)


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

    renderer: Renderer = TextRenderer()

    root = os.path.abspath(args.path)
    if not os.path.isdir(root):
        renderer.invalid_directory(root)
        sys.exit(1)

    renderer.scan_start(root)
    found = scan(root)
    if not found:
        renderer.nothing_to_clean()
        return

    if args.interactive:
        run_interactive(renderer, found, args.dry_run)
    else:
        run_standard(renderer, found, args.dry_run)
