from __future__ import annotations

import os


def normalize_paths(paths: frozenset[str] | set[str] | list[str] | tuple[str, ...]) -> set[str]:
    if not paths:
        return set()
    return {os.path.abspath(os.path.expanduser(path)) for path in paths}


def dir_is_under_ignored_path(dirpath: str, ignored_paths: set[str]) -> bool:
    normalized = os.path.abspath(dirpath)
    for ignored_path in ignored_paths:
        if normalized == ignored_path or normalized.startswith(ignored_path + os.sep):
            return True
    return False


def path_is_excluded(full_path: str, ignored_paths: set[str]) -> bool:
    normalized = os.path.abspath(full_path)
    for ignored_path in ignored_paths:
        if normalized == ignored_path or normalized.startswith(ignored_path + os.sep):
            return True
    return False
