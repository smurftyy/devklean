from __future__ import annotations

import os

from devclean.config.models import AppConfig
from devclean.models import CleanableItem
from devclean.output.base import Renderer
from devclean.scanner import scan


def scan_directory(
    args,
    renderer: Renderer,
    config: AppConfig,
) -> tuple[int, list[CleanableItem] | None]:
    """Validate the root path, scan, and report when nothing is found."""
    root = os.path.abspath(args.path)
    if not os.path.isdir(root):
        renderer.invalid_directory(root)
        return 1, None

    renderer.scan_start(root)
    found = scan(
        root,
        targets=config.targets,
        ignored_paths=config.ignored_paths,
    )
    if not found:
        renderer.nothing_to_clean()
        return 0, None

    return 0, found
