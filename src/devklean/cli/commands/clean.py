from __future__ import annotations

from devklean.cli.commands.common import scan_directory
from devklean.deletion import DeletionStrategy, delete_items
from devklean.config.models import AppConfig
from devklean.models import CleanableItem
from devklean.output.base import Renderer
from devklean.tui import run_interactive


def run_standard(
    renderer: Renderer,
    found: list[CleanableItem],
    dry_run: bool,
    deletion_strategy: DeletionStrategy | None = None,
) -> None:
    total_size = renderer.scan_summary(found)

    if dry_run:
        renderer.dry_run_nothing_deleted()
        return

    confirm = input(renderer.confirm_prompt(len(found))).strip().lower()
    if confirm != "y":
        renderer.aborted()
        return

    result = delete_items(found, total_size, deletion_strategy)
    renderer.deletion_result(result)


def run_clean(
    args,
    renderer: Renderer,
    config: AppConfig,
    deletion_strategy: DeletionStrategy | None = None,
) -> int:
    """Scan and optionally delete cleanable directories."""
    exit_code, found = scan_directory(args, renderer, config)
    if exit_code != 0 or found is None:
        return exit_code

    if args.interactive:
        run_interactive(renderer, found, args.dry_run, deletion_strategy)
    else:
        run_standard(renderer, found, args.dry_run, deletion_strategy)

    return 0
