from __future__ import annotations

from importlib import import_module

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


def __getattr__(name: str):
    if name == "ArtifactSignature":
        return import_module("devklean.signatures.registry").ArtifactSignature
    if name == "RiskLevel":
        return import_module("devklean.signatures.registry").RiskLevel
    if name == "SIGNATURE_REGISTRY":
        return import_module("devklean.signatures.registry").SIGNATURE_REGISTRY
    if name == "lookup":
        return import_module("devklean.signatures.registry").lookup
    if name == "match_signature":
        return import_module("devklean.signatures.registry").match_signature
    if name == "AnalysisReport":
        return import_module("devklean.signatures.analysis").AnalysisReport
    if name == "RecognizedCandidate":
        return import_module("devklean.signatures.analysis").RecognizedCandidate
    if name == "analyze_candidates":
        return import_module("devklean.signatures.analysis").analyze_candidates
    if name == "StalenessResult":
        return import_module("devklean.signatures.staleness").StalenessResult
    if name == "estimate_staleness":
        return import_module("devklean.signatures.staleness").estimate_staleness
    if name == "LockfileConflict":
        return import_module("devklean.signatures.structural").LockfileConflict
    if name == "detect_lockfile_conflicts":
        return import_module("devklean.signatures.structural").detect_lockfile_conflicts
    if name == "HealthInputs":
        return import_module("devklean.signatures.health").HealthInputs
    if name == "HealthScore":
        return import_module("devklean.signatures.health").HealthScore
    if name == "compute_health_score":
        return import_module("devklean.signatures.health").compute_health_score
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
