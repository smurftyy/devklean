from __future__ import annotations

from importlib import import_module

__all__ = [
    "ArtifactSignature",
    "RiskLevel",
    "SIGNATURE_REGISTRY",
    "lookup",
    "match_signature",
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
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
