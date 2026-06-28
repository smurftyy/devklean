from __future__ import annotations

import os

from devclean.deleter import delete_items
from devclean.models import CleanableItem
from devclean.output.base import Renderer
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


def run_clean(args, renderer: Renderer) -> int:
    """Scan and optionally delete cleanable directories (current default behaviour)."""
    root = os.path.abspath(args.path)
    if not os.path.isdir(root):
        renderer.invalid_directory(root)
        return 1

    renderer.scan_start(root)
    found = scan(root)
    if not found:
        renderer.nothing_to_clean()
        return 0

    if args.interactive:
        run_interactive(renderer, found, args.dry_run)
    else:
        run_standard(renderer, found, args.dry_run)

    return 0
