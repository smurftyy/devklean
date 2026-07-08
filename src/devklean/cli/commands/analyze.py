from __future__ import annotations

import os
from typing import TYPE_CHECKING

from devklean.config.models import AppConfig
from devklean.scanner.scanner import scan_tree
from devklean.signatures.analysis import analyze_candidates

if TYPE_CHECKING:
    from devklean.output.text import TextRenderer


def run_analyze(args, renderer: TextRenderer, config: AppConfig) -> int:
    """Scan for cleanable directories and report a signature-backed analysis.

    Calls ``scan_tree`` directly — the exact discovery function ``clean``/
    ``scan`` use via ``scan_directory`` — rather than a second walker.
    ``scan_directory`` isn't reused as-is because its "nothing found" path
    renders clean/scan's own summary and stops; analyze always wants to
    render its own report (recognized/unrecognized buckets, structural
    checks, health score), even over an empty candidate list.
    """
    root = os.path.abspath(args.path)
    if not os.path.isdir(root):
        renderer.invalid_directory(root)
        return 1

    scan_report = scan_tree(root, settings=config.scan_settings)
    if scan_report.permission_errors:
        renderer.permission_warnings(scan_report.permission_errors)

    analysis = analyze_candidates(root, scan_report.items)
    renderer.analysis_report(analysis, verbose=getattr(args, "verbose", False))
    return 0
