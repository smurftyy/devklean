# Backward-compatible alias used by tests and external imports.
from devklean.config.defaults import DEFAULT_TARGETS
from devklean.scanner.filters import (
    dir_is_under_ignored_path,
    normalize_paths,
    path_is_excluded,
)
from devklean.scanner.scanner import ScanResult, get_dir_size, scan, scan_tree

TARGETS = DEFAULT_TARGETS

__all__ = [
    "DEFAULT_TARGETS",
    "ScanResult",
    "TARGETS",
    "dir_is_under_ignored_path",
    "get_dir_size",
    "normalize_paths",
    "path_is_excluded",
    "scan",
    "scan_tree",
]
