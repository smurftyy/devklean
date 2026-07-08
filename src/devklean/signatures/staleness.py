"""Staleness estimation for a candidate's parent project.

The artifact directory's own mtime/atime is never used as a signal: package
managers rewrite files inside it on every install, and atime is frequently
disabled at the mount level (``noatime``/``relatime``), so neither reflects
when the *project* was actually last worked on. Instead this derives
staleness from the parent project itself, in a fixed priority order:

1. The git repository's last commit date, if the project is inside one.
2. The newest mtime among the parent project's own files, excluding known
   artifact directories (so a fresh ``npm install`` doesn't look like recent
   activity).

If neither produces a usable timestamp, ``estimate_staleness`` returns a
result with ``known=False`` — callers must surface that explicitly rather
than print a number that looks confident but means nothing.
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone

from devklean.signatures.registry import SIGNATURE_REGISTRY

# Directory names never treated as "source" when computing the fallback
# mtime signal — the same set of artifact names the registry knows about,
# plus .git (its internal mtimes aren't project activity either).
_EXCLUDED_DIR_NAMES = frozenset(SIGNATURE_REGISTRY) | {".git"}


@dataclass(frozen=True)
class StalenessResult:
    """A staleness estimate for one project root.

    ``known=False`` means no reliable signal existed; ``detail`` always holds
    a human-readable explanation regardless of ``known``, so it's always safe
    to display.
    """

    known: bool
    source: str | None  # "git" | "source-mtime" | None
    last_activity: datetime | None
    days_since: int | None
    detail: str


def estimate_staleness(project_root: str) -> StalenessResult:
    """Resolve a staleness signal for ``project_root``, git first, then mtime."""
    return _from_git(project_root) or _from_source_mtime(project_root) or StalenessResult(
        known=False,
        source=None,
        last_activity=None,
        days_since=None,
        detail="no reliable signal (no git repository and no source files found)",
    )


def _days_since(moment: datetime) -> int:
    return (datetime.now(tz=timezone.utc) - moment).days


def _from_git(project_root: str) -> StalenessResult | None:
    try:
        proc = subprocess.run(
            ["git", "-C", project_root, "log", "-1", "--format=%ct"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None

    if proc.returncode != 0:
        return None

    output = proc.stdout.strip()
    if not output:
        return None

    try:
        epoch = int(output)
    except ValueError:
        return None

    last_activity = datetime.fromtimestamp(epoch, tz=timezone.utc)
    days = _days_since(last_activity)
    return StalenessResult(
        known=True,
        source="git",
        last_activity=last_activity,
        days_since=days,
        detail=f"{days} day{'s' if days != 1 else ''} since last git commit",
    )


def _from_source_mtime(project_root: str) -> StalenessResult | None:
    latest: float | None = None
    for dirpath, dirnames, filenames in os.walk(project_root):
        dirnames[:] = [d for d in dirnames if d not in _EXCLUDED_DIR_NAMES]
        for filename in filenames:
            try:
                mtime = os.stat(os.path.join(dirpath, filename)).st_mtime
            except OSError:
                continue
            if latest is None or mtime > latest:
                latest = mtime

    if latest is None:
        return None

    last_activity = datetime.fromtimestamp(latest, tz=timezone.utc)
    days = _days_since(last_activity)
    return StalenessResult(
        known=True,
        source="source-mtime",
        last_activity=last_activity,
        days_since=days,
        detail=f"{days} day{'s' if days != 1 else ''} since newest source-file change",
    )
