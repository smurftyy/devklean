from __future__ import annotations

from devklean.signatures.analysis import AnalysisReport, RecognizedCandidate, analyze_candidates
from devklean.signatures.health import HealthInputs, HealthScore, compute_health_score
from devklean.signatures.registry import (
    SIGNATURE_REGISTRY,
    ArtifactSignature,
    RiskLevel,
    lookup,
    match_signature,
)
from devklean.signatures.staleness import StalenessResult, estimate_staleness
from devklean.signatures.structural import LockfileConflict, detect_lockfile_conflicts

__all__ = [
    "ArtifactSignature",
    "RiskLevel",
    "SIGNATURE_REGISTRY",
    "lookup",
    "match_signature",
    "AnalysisReport",
    "RecognizedCandidate",
    "analyze_candidates",
    "StalenessResult",
    "estimate_staleness",
    "LockfileConflict",
    "detect_lockfile_conflicts",
    "HealthInputs",
    "HealthScore",
    "compute_health_score",
]
