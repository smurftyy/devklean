"""Structural checks: deterministic file-existence checks, not judgment calls.

Each check here only asks "do these specific files exist in this directory?"
No sizes, no content inspection, no guessing about what a directory is for.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

# Groups of lockfiles that indicate two different, mutually exclusive package
# managers were both used against the same project root. Presence of 2+ names
# from the same group is flagged, regardless of which ones.
_CONFLICTING_LOCKFILE_GROUPS: tuple[tuple[str, ...], ...] = (
    ("package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb"),
)


@dataclass(frozen=True)
class LockfileConflict:
    """Two or more mutually exclusive lockfiles found in one project root."""

    project_root: str
    lockfiles: tuple[str, ...]


def detect_lockfile_conflicts(project_root: str) -> LockfileConflict | None:
    """Flag a project root that has 2+ lockfiles from the same conflict group.

    Plain ``os.path.isfile`` checks — no inference about which lockfile is
    "correct" or which package manager is actually in use.
    """
    for group in _CONFLICTING_LOCKFILE_GROUPS:
        present = tuple(
            name for name in group if os.path.isfile(os.path.join(project_root, name))
        )
        if len(present) >= 2:
            return LockfileConflict(project_root=project_root, lockfiles=present)
    return None
