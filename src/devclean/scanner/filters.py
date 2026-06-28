from __future__ import annotations

import os


def normalize_paths(paths: frozenset[str] | set[str] | list[str] | tuple[str, ...]) -> set[str]:
    if not paths:
        return set()
    return {os.path.abspath(os.path.expanduser(path)) for path in paths}


def dir_is_under_ignored_path(dirpath: str, ignored_paths: set[str]) -> bool:
    """Return True when ``dirpath`` is inside an ignored path.

    Safe: callers pass absolute ``dirpath`` values from ``os.walk(abspath(root))``
    and absolute entries in ``ignored_paths`` from ``normalize_paths``.
    """
    for ignored_path in ignored_paths:
        if dirpath == ignored_path or dirpath.startswith(ignored_path + os.sep):
            return True
    return False


def path_is_excluded(full_path: str, ignored_paths: set[str]) -> bool:
    """Return True when ``full_path`` should be excluded from scan results.

    Safe: same absolute-path precondition as ``dir_is_under_ignored_path``.
    """
    for ignored_path in ignored_paths:
        if full_path == ignored_path or full_path.startswith(ignored_path + os.sep):
            return True
    return False
