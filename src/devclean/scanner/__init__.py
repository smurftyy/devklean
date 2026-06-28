from devclean.scanner.filters import (
    dir_is_under_ignored_path,
    normalize_paths,
    path_is_excluded,
)
from devclean.scanner.scanner import get_dir_size, scan

# Backward-compatible alias used by tests and external imports.
from devclean.config.defaults import DEFAULT_TARGETS

TARGETS = DEFAULT_TARGETS

__all__ = [
    "DEFAULT_TARGETS",
    "TARGETS",
    "dir_is_under_ignored_path",
    "get_dir_size",
    "normalize_paths",
    "path_is_excluded",
    "scan",
]
