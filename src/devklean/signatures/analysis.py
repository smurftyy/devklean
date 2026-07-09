"""Bucket already-discovered candidates via the signature registry and score them.

This module never walks the filesystem to find candidates — it only accepts
the ``CleanableItem`` list ``scan_tree`` already produced (the same discovery
``clean``/``scan`` use) and layers registry lookups, staleness estimates, and
structural checks on top of it.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from devklean.models import CleanableItem
from devklean.signatures.health import HealthInputs, HealthScore, compute_health_score
from devklean.signatures.registry import ArtifactSignature, lookup
from devklean.signatures.staleness import StalenessResult, estimate_staleness
from devklean.signatures.structural import LockfileConflict, detect_lockfile_conflicts


@dataclass(frozen=True)
class RecognizedCandidate:
    """A scanned candidate with a matched signature and staleness estimate."""

    item: CleanableItem
    signature: ArtifactSignature
    staleness: StalenessResult


@dataclass(frozen=True)
class AnalysisReport:
    root: str
    recognized: tuple[RecognizedCandidate, ...]
    unrecognized: tuple[CleanableItem, ...]
    lockfile_conflicts: tuple[LockfileConflict, ...]
    health: HealthScore


def analyze_candidates(root: str, items: list[CleanableItem]) -> AnalysisReport:
    """Bucket ``items`` into recognized/unrecognized and attach analysis.

    "Recognized" means the candidate's directory name has a
    ``SIGNATURE_REGISTRY`` entry; everything else — e.g. a custom target
    added via config with no registry entry — is "unrecognized" and gets no
    risk/confidence/staleness verdict, per the same no-guessing rule
    ``explain`` follows.
    """
    abs_root = os.path.abspath(root)
    recognized: list[RecognizedCandidate] = []
    unrecognized: list[CleanableItem] = []
    staleness_cache: dict[str, StalenessResult] = {}
    project_roots: set[str] = {abs_root}

    for item in items:
        project_roots.add(os.path.dirname(item.path))

        signature = lookup(item.name)
        if signature is None:
            unrecognized.append(item)
            continue

        project_root = os.path.dirname(item.path)
        if project_root not in staleness_cache:
            staleness_cache[project_root] = estimate_staleness(project_root)

        recognized.append(
            RecognizedCandidate(
                item=item,
                signature=signature,
                staleness=staleness_cache[project_root],
            )
        )

    conflicts = tuple(
        conflict
        for conflict in (detect_lockfile_conflicts(p) for p in sorted(project_roots))
        if conflict is not None
    )

    recognized_total = sum(c.item.size for c in recognized)
    unrecognized_total = sum(i.size for i in unrecognized)
    weighted = sum(c.item.size * c.signature.risk.weight for c in recognized)

    health = compute_health_score(
        HealthInputs(
            recognized_weighted_size=weighted,
            recognized_total_size=recognized_total,
            unrecognized_total_size=unrecognized_total,
            lockfile_conflicts=len(conflicts),
        )
    )

    return AnalysisReport(
        root=abs_root,
        recognized=tuple(recognized),
        unrecognized=tuple(unrecognized),
        lockfile_conflicts=conflicts,
        health=health,
    )
