from __future__ import annotations

from devclean.cli.commands.common import scan_directory
from devclean.deleter import delete_items
from devclean.models import CleanableItem
from devclean.output.base import Renderer
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
    """Scan and optionally delete cleanable directories."""
    exit_code, found = scan_directory(args, renderer)
    if exit_code != 0 or found is None:
        return exit_code

    if args.interactive:
        run_interactive(renderer, found, args.dry_run)
    else:
        run_standard(renderer, found, args.dry_run)

    return 0
