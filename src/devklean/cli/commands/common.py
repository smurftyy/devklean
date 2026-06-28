from __future__ import annotations

import os

from devklean.config.models import AppConfig
from devklean.logging_setup import get_logger
from devklean.models import CleanableItem
from devklean.output.base import Renderer
from devklean.scanner.scanner import scan_tree


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
    report = scan_tree(root, settings=config.scan_settings)
    get_logger().info(
        "scan root=%s found=%d permission_errors=%d",
        root,
        len(report.items),
        len(report.permission_errors),
    )
    if report.permission_errors:
        renderer.permission_warnings(report.permission_errors)

    if not report.items:
        renderer.nothing_to_clean()
        return 0, None

    return 0, report.items
