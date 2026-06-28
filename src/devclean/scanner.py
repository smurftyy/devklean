from __future__ import annotations

import os

from devclean.config.defaults import DEFAULT_TARGETS
from devclean.models import CleanableItem

# Backward-compatible alias used by tests and external imports.
TARGETS = DEFAULT_TARGETS


def get_dir_size(path: str) -> int:
    total = 0
    try:
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    total += os.path.getsize(fp)
                except (OSError, FileNotFoundError):
                    pass
    except PermissionError:
        pass
    return total


def _normalize_ignored_paths(ignored_paths: list[str] | tuple[str, ...] | None) -> set[str]:
    if not ignored_paths:
        return set()
    return {os.path.abspath(os.path.expanduser(path)) for path in ignored_paths}


def _dir_is_ignored(dirpath: str, ignored: set[str]) -> bool:
    normalized = os.path.abspath(dirpath)
    for ignored_path in ignored:
        if normalized == ignored_path or normalized.startswith(ignored_path + os.sep):
            return True
    return False


def _path_is_ignored(full_path: str, ignored: set[str]) -> bool:
    normalized = os.path.abspath(full_path)
    for ignored_path in ignored:
        if normalized == ignored_path or normalized.startswith(ignored_path + os.sep):
            return True
    return False


def scan(
    root: str,
    *,
    targets: dict[str, str] | None = None,
    ignored_paths: list[str] | tuple[str, ...] | None = None,
) -> list[CleanableItem]:
    active_targets = targets if targets is not None else DEFAULT_TARGETS
    ignored = _normalize_ignored_paths(ignored_paths)
    found: list[CleanableItem] = []

    for dirpath, dirnames, _ in os.walk(root, topdown=True):
        if _dir_is_ignored(dirpath, ignored):
            dirnames.clear()
            continue

        # Prune already-found targets from further traversal
        dirnames[:] = [
            d for d in dirnames
            if os.path.join(dirpath, d) not in {item.path for item in found}
        ]

        for dirname in list(dirnames):
            if dirname in active_targets:
                full_path = os.path.join(dirpath, dirname)
                if _path_is_ignored(full_path, ignored):
                    continue
                size = get_dir_size(full_path)
                found.append(CleanableItem(
                    path=full_path,
                    name=dirname,
                    size=size,
                    display_label=active_targets.get(dirname, dirname),
                ))
                dirnames.remove(dirname)  # don't recurse into it

    return found
