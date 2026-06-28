from __future__ import annotations

from devclean.cli.commands.common import scan_directory
from devclean.config.models import AppConfig
from devclean.output.base import Renderer


def run_scan(args, renderer: Renderer, config: AppConfig) -> int:
    """Scan for cleanable directories and display results without deleting."""
    exit_code, found = scan_directory(args, renderer, config)
    if exit_code != 0 or found is None:
        return exit_code

    renderer.scan_summary(found)
    renderer.dry_run_nothing_deleted()
    return 0
