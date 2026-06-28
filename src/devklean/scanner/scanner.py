"""Scanner performance notes.

Before (per directory visited during ``os.walk``):
- Rebuilt ``dirnames`` via list comprehension (new list allocation).
- Copied ``dirnames`` with ``list()`` for safe removal during iteration.
- Called ``dirnames.remove`` multiple times (O(n) each).
- Called ``os.path.abspath`` on every ``dirpath`` and matched path.
- Ran ignore-path checks even when the ignore list was empty.

After:
- Single-pass ``dirnames`` filtering via slice assignment (one list built per node).
- ``root`` normalized once so walk paths stay absolute; filters skip ``abspath``.
- Ignore-path checks gated on ``has_ignored_paths`` (empty config = no work).
- Directory-name ignore checks gated on ``has_ignored_directories``.
- ``active_targets[dirname]`` used directly after membership test (no redundant ``.get``).

Complexity (unchanged asymptotics, improved constants):
- Walk: still O(N) over filesystem nodes under ``root``.
- Per node: O(d) directory entries; target/ignore lookups O(1) average.
- Size calculation: O(M) per matched target (unchanged; inherent second walk).
- Found-path pruning: O(1) per child via ``found_paths`` set (unchanged).

All optimizations preserve behavior: same targets matched, same paths ignored,
same sizes reported, same traversal boundaries (no recursion into matched targets).
"""

from __future__ import annotations

import os

from devklean.config.defaults import DEFAULT_TARGETS
from devklean.config.models import ScanSettings
from devklean.models import CleanableItem
from devklean.scanner.filters import (
    dir_is_under_ignored_path,
    normalize_paths,
    path_is_excluded,
)


def get_dir_size(path: str) -> int:
    """Return the combined byte size of all files under ``path``.

    Safe: uses ``followlinks=False`` (default) so symlinks are not traversed,
    matching the previous ``os.walk`` behaviour.
    """
    total = 0
    try:
        for dirpath, _, filenames in os.walk(path, followlinks=False):
            for filename in filenames:
                try:
                    total += os.path.getsize(os.path.join(dirpath, filename))
                except (OSError, FileNotFoundError):
                    pass
    except PermissionError:
        pass
    return total


def scan(root: str, settings: ScanSettings | None = None) -> list[CleanableItem]:
    """Discover cleanable directories under root using scan settings."""
    active = settings or ScanSettings.defaults()

    # Safe: absolute root => os.walk yields absolute dirpaths; ignored paths
    # are normalized the same way in ConfigManager / normalize_paths.
    root = os.path.abspath(root)
    ignored_paths = normalize_paths(active.ignored_paths)
    has_ignored_paths = bool(ignored_paths)
    ignored_directories = active.ignored_directories
    has_ignored_directories = bool(ignored_directories)
    active_targets = active.targets

    found: list[CleanableItem] = []
    found_paths: set[str] = set()

    for dirpath, dirnames, _ in os.walk(root, topdown=True, followlinks=False):
        if has_ignored_paths and dir_is_under_ignored_path(dirpath, ignored_paths):
            dirnames.clear()
            continue

        # Single-pass filter: avoid list(dirnames) copy, comprehension allocation,
        # and repeated O(n) dirnames.remove calls.
        kept_dirnames: list[str] = []
        for dirname in dirnames:
            if has_ignored_directories and dirname in ignored_directories:
                continue

            child_path = os.path.join(dirpath, dirname)

            if child_path in found_paths:
                continue

            if dirname in active_targets:
                if has_ignored_paths and path_is_excluded(child_path, ignored_paths):
                    continue
                size = get_dir_size(child_path)
                found.append(CleanableItem(
                    path=child_path,
                    name=dirname,
                    size=size,
                    display_label=active_targets[dirname],
                ))
                found_paths.add(child_path)
                continue

            kept_dirnames.append(dirname)

        dirnames[:] = kept_dirnames

    return found


# Backward-compatible alias.
TARGETS = DEFAULT_TARGETS
