from __future__ import annotations

import os

from devclean.config.defaults import DEFAULT_TARGETS
from devclean.config.models import ScanSettings
from devclean.models import CleanableItem
from devclean.scanner.filters import (
    dir_is_under_ignored_path,
    normalize_paths,
    path_is_excluded,
)


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


def scan(root: str, settings: ScanSettings | None = None) -> list[CleanableItem]:
    """Discover cleanable directories under root using scan settings."""
    active = settings or ScanSettings.defaults()
    ignored_paths = normalize_paths(active.ignored_paths)
    ignored_directories = active.ignored_directories
    active_targets = active.targets

    found: list[CleanableItem] = []
    found_paths = set()

    for dirpath, dirnames, _ in os.walk(root, topdown=True):
        if dir_is_under_ignored_path(dirpath, ignored_paths):
            dirnames.clear()
            continue

        dirnames[:] = [
            d for d in dirnames
            if os.path.join(dirpath, d) not in found_paths
        ]

        for dirname in list(dirnames):
            if dirname in ignored_directories:
                dirnames.remove(dirname)
                continue

            if dirname not in active_targets:
                continue

            full_path = os.path.join(dirpath, dirname)
            if path_is_excluded(full_path, ignored_paths):
                continue

            size = get_dir_size(full_path)
            found.append(CleanableItem(
                path=full_path,
                name=dirname,
                size=size,
                display_label=active_targets.get(dirname, dirname),
            ))
            found_paths.add(full_path)
            dirnames.remove(dirname)

    return found


# Backward-compatible alias.
TARGETS = DEFAULT_TARGETS
