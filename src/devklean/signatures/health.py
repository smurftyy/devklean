"""Workspace-health scoring: one documented formula, fixed inputs.

The score is a static function of counted bytes and structural-conflict
counts — never a model, never a hidden heuristic. ``HealthScore.formula`` and
``HealthScore.inputs`` are always populated (not just under a debug flag) so
the number is inspectable on demand, e.g. via ``devklean analyze --verbose``.
"""

from __future__ import annotations

from dataclasses import dataclass

# Flat penalty subtracted per detected lockfile conflict (see
# devklean.signatures.structural). A fixed constant, not a computed weight.
LOCKFILE_CONFLICT_PENALTY = 10

_FORMULA = (
    "score = round(100 * (sum(recognized_size_i * risk_weight_i) / total_size)) "
    f"- {LOCKFILE_CONFLICT_PENALTY} * lockfile_conflicts, clamped to [0, 100]. "
    "risk_weight: low=1.0, medium=0.6, high=0.2 (devklean.signatures.registry.RiskLevel.weight). "
    "unrecognized_total_size counts toward total_size but contributes 0 to the "
    "weighted sum, since devklean has no risk data for it. "
    "total_size = recognized_total_size + unrecognized_total_size; "
    "an empty scan (total_size == 0) scores 100."
)


@dataclass(frozen=True)
class HealthInputs:
    """Every value the formula reads — nothing else feeds the score."""

    recognized_weighted_size: float
    recognized_total_size: int
    unrecognized_total_size: int
    lockfile_conflicts: int

    @property
    def total_size(self) -> int:
        return self.recognized_total_size + self.unrecognized_total_size


@dataclass(frozen=True)
class HealthScore:
    score: int
    inputs: HealthInputs
    formula: str = _FORMULA


def compute_health_score(inputs: HealthInputs) -> HealthScore:
    if inputs.total_size == 0:
        return HealthScore(score=100, inputs=inputs)

    weighted_share = inputs.recognized_weighted_size / inputs.total_size
    raw = round(100 * weighted_share) - LOCKFILE_CONFLICT_PENALTY * inputs.lockfile_conflicts
    score = max(0, min(100, raw))
    return HealthScore(score=score, inputs=inputs)
