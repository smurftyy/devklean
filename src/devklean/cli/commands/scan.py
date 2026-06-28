from __future__ import annotations

from devklean.cli.commands.common import scan_directory
from devklean.config.models import AppConfig
from devklean.output.base import Renderer


def run_scan(args, renderer: Renderer, config: AppConfig) -> int:
    """Scan for cleanable directories and display results without deleting."""
    exit_code, found = scan_directory(args, renderer, config)
    if exit_code != 0 or found is None:
        return exit_code

    renderer.scan_summary(found)
    renderer.dry_run_nothing_deleted()
    return 0
