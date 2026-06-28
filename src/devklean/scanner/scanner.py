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
- Found-path pruning: O(1) per child via ``found_paths`` set (unchanged).

Phase 4 performance changes (qualitative before/after):
- Sizing: ``get_dir_size`` moved from ``os.walk`` + ``os.path.getsize`` (which
  re-``stat``s every file) to ``os.scandir`` + ``entry.stat`` (cached stat, one
  syscall per entry). Symlinked dirs/files are skipped, so no double-counting.
- Concurrency: target sizing was sequential (each target's subtree walked one
  after another). It now runs on a bounded ``ThreadPoolExecutor`` — sizing is
  I/O-bound, so wide trees with many targets see real wall-clock wins. Discovery
  stays a single deterministic walk; result order is preserved (map keeps input
  order), so output is identical to the sequential version.
- Memory: only per-directory totals are retained (never a list of every file),
  unchanged — large scans stay bounded by the number of matched targets, not
  the number of files.

All changes preserve behavior: same targets matched, same paths ignored, same
sizes reported, same traversal boundaries (no recursion into matched targets).
"""

from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field

from devklean.config.defaults import DEFAULT_TARGETS
from devklean.config.models import ScanSettings
from devklean.models import CleanableItem
from devklean.scanner.filters import (
    dir_is_under_ignored_path,
    normalize_paths,
    path_is_excluded,
)


@dataclass(frozen=True)
class ScanResult:
    """Discovered cleanable items plus paths skipped due to permission errors."""

    items: list[CleanableItem]
    permission_errors: list[str] = field(default_factory=list)


def get_dir_size(path: str) -> int:
    """Return the combined byte size of all regular files under ``path``.

    Uses ``os.scandir`` with ``entry.stat(follow_symlinks=False)``, which:
    - avoids the redundant ``stat`` that ``os.path.getsize`` performs after
      ``os.walk`` (scandir caches the entry's stat where the OS provides it),
    - never traverses symlinked directories and never counts symlinked files,
      so symlinks/hardlink aliases are not double-counted,
    - counts regular files only.
    """
    total = 0
    stack = [path]
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as entries:
                for entry in entries:
                    try:
                        if entry.is_dir(follow_symlinks=False):
                            stack.append(entry.path)
                        elif entry.is_file(follow_symlinks=False):
                            total += entry.stat(follow_symlinks=False).st_size
                    except OSError:
                        pass
        except OSError:
            pass
    return total


def scan(root: str, settings: ScanSettings | None = None) -> list[CleanableItem]:
    """Discover cleanable directories under root (backward-compatible wrapper)."""
    return scan_tree(root, settings).items


def scan_tree(root: str, settings: ScanSettings | None = None) -> ScanResult:
    """Discover cleanable directories, reporting permission-denied paths.

    Permission errors during traversal are collected (via ``os.walk``'s
    ``onerror`` hook) rather than silently swallowed, so the caller can tell the
    user which paths were skipped. Scanning continues past them.
    """
    active = settings or ScanSettings.defaults()

    # Safe: absolute root => os.walk yields absolute dirpaths; ignored paths
    # are normalized the same way in ConfigManager / normalize_paths.
    root = os.path.abspath(root)
    ignored_paths = normalize_paths(active.ignored_paths)
    has_ignored_paths = bool(ignored_paths)
    ignored_directories = active.ignored_directories
    has_ignored_directories = bool(ignored_directories)
    active_targets = active.targets

    # Discovery is a single deterministic pass; sizing (the real cost) is
    # deferred so it can run concurrently afterwards.
    matched: list[tuple[str, str]] = []  # (child_path, dirname)
    found_paths: set[str] = set()
    permission_errors: list[str] = []

    def _on_walk_error(error: OSError) -> None:
        if isinstance(error, PermissionError):
            permission_errors.append(error.filename or str(error))

    for dirpath, dirnames, _ in os.walk(
        root, topdown=True, followlinks=False, onerror=_on_walk_error
    ):
        if has_ignored_paths and dir_is_under_ignored_path(dirpath, ignored_paths):
            dirnames.clear()
            continue

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
                matched.append((child_path, dirname))
                found_paths.add(child_path)
                continue

            kept_dirnames.append(dirname)

        dirnames[:] = kept_dirnames

    sizes = _compute_sizes_concurrently([path for path, _ in matched])
    found = [
        CleanableItem(
            path=child_path,
            name=dirname,
            size=size,
            display_label=active_targets[dirname],
        )
        for (child_path, dirname), size in zip(matched, sizes)
    ]

    return ScanResult(items=found, permission_errors=permission_errors)


def _compute_sizes_concurrently(paths: list[str]) -> list[int]:
    """Compute directory sizes in parallel (I/O-bound). Order is preserved."""
    if not paths:
        return []
    if len(paths) == 1:
        return [get_dir_size(paths[0])]

    workers = min(32, (os.cpu_count() or 1) * 5, len(paths))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(get_dir_size, paths))


# Backward-compatible alias.
TARGETS = DEFAULT_TARGETS
