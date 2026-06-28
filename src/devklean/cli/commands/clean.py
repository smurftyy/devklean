from __future__ import annotations

import sys

from devklean.cli.commands.common import scan_directory
from devklean.cli.confirmation import (
    DEFAULT_LARGE_THRESHOLD,
    confirm_large_deletion,
    exceeds_threshold,
)
from devklean.config.models import AppConfig
from devklean.deletion import SafetyValidator, delete_items
from devklean.models import CleanableItem
from devklean.output.base import Renderer


def _confirm_deletion(
    renderer: Renderer,
    count: int,
    total_size: int,
    default_yes: bool,
    confirm_threshold: int,
) -> bool:
    """Return True when the user has authorized the deletion.

    Large batches (>= threshold) always require a typed confirmation, even when
    ``default_yes`` is set — config must not be able to defeat that guard.
    """
    if exceeds_threshold(total_size, confirm_threshold):
        return confirm_large_deletion(count, total_size, confirm_threshold)
    if default_yes:
        return True
    return input(renderer.confirm_prompt(count, total_size)).strip().lower() == "y"


def run_standard(
    renderer: Renderer,
    found: list[CleanableItem],
    dry_run: bool,
    validator: SafetyValidator | None = None,
    *,
    default_yes: bool = False,
    confirm_threshold: int = DEFAULT_LARGE_THRESHOLD,
) -> None:
    total_size = renderer.scan_summary(found)

    if dry_run:
        renderer.dry_run_selected(len(found))
        return

    if not _confirm_deletion(renderer, len(found), total_size, default_yes, confirm_threshold):
        renderer.aborted()
        return

    result = delete_items(found, total_size, validator=validator)
    renderer.deletion_result(result)


def run_clean(
    args,
    renderer: Renderer,
    config: AppConfig,
    validator: SafetyValidator | None = None,
) -> int:
    """Scan and optionally delete cleanable directories."""
    exit_code, found = scan_directory(args, renderer, config)
    if exit_code != 0 or found is None:
        return exit_code

    defaults = config.defaults
    default_yes = getattr(args, "yes", False) or getattr(defaults, "default_yes", False)
    confirm_threshold = getattr(defaults, "confirm_threshold", DEFAULT_LARGE_THRESHOLD)

    if args.interactive:
        # Interactive mode relies on curses, which is unavailable on Windows.
        # Fail with a clear message rather than crashing on the curses import.
        if sys.platform == "win32":
            print(
                "devklean: interactive mode (-i/--interactive) isn't available on "
                "Windows yet. Run without -i, or see the 'Platform support' section "
                "of the README for details.",
                file=sys.stderr,
            )
            return 2
        # Imported lazily so non-interactive commands never load the TUI/curses
        # stack, and to avoid a circular import (tui -> cli -> clean -> tui).
        from devklean.tui import run_interactive

        run_interactive(
            renderer,
            found,
            args.dry_run,
            validator,
            confirm_threshold=confirm_threshold,
        )
    else:
        run_standard(
            renderer,
            found,
            args.dry_run,
            validator,
            default_yes=default_yes,
            confirm_threshold=confirm_threshold,
        )

    return 0
