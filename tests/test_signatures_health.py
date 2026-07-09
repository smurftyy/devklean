"""Tests for the documented workspace-health formula (devklean.signatures.health)."""

from __future__ import annotations

from devklean.signatures.health import HealthInputs, compute_health_score


def test_empty_scan_scores_100() -> None:
    inputs = HealthInputs(
        recognized_weighted_size=0,
        recognized_total_size=0,
        unrecognized_total_size=0,
        lockfile_conflicts=0,
    )

    result = compute_health_score(inputs)

    assert result.score == 100
    assert result.formula


def test_all_low_risk_recognized_bytes_scores_100() -> None:
    inputs = HealthInputs(
        recognized_weighted_size=1000 * 1.0,
        recognized_total_size=1000,
        unrecognized_total_size=0,
        lockfile_conflicts=0,
    )

    assert compute_health_score(inputs).score == 100


def test_all_high_risk_recognized_bytes_scores_low() -> None:
    inputs = HealthInputs(
        recognized_weighted_size=1000 * 0.2,
        recognized_total_size=1000,
        unrecognized_total_size=0,
        lockfile_conflicts=0,
    )

    assert compute_health_score(inputs).score == 20


def test_unrecognized_bytes_drag_the_score_down() -> None:
    # 500 low-risk recognized bytes, 500 unrecognized (zero-weight) bytes.
    inputs = HealthInputs(
        recognized_weighted_size=500 * 1.0,
        recognized_total_size=500,
        unrecognized_total_size=500,
        lockfile_conflicts=0,
    )

    assert compute_health_score(inputs).score == 50


def test_lockfile_conflict_applies_flat_penalty() -> None:
    inputs = HealthInputs(
        recognized_weighted_size=1000 * 1.0,
        recognized_total_size=1000,
        unrecognized_total_size=0,
        lockfile_conflicts=1,
    )

    assert compute_health_score(inputs).score == 90


def test_score_is_clamped_to_zero() -> None:
    inputs = HealthInputs(
        recognized_weighted_size=0,
        recognized_total_size=100,
        unrecognized_total_size=0,
        lockfile_conflicts=5,  # 5 * 10 = 50 points, more than the 0 base score
    )

    assert compute_health_score(inputs).score == 0


def test_inputs_are_exposed_on_the_result() -> None:
    inputs = HealthInputs(
        recognized_weighted_size=10,
        recognized_total_size=20,
        unrecognized_total_size=5,
        lockfile_conflicts=2,
    )

    result = compute_health_score(inputs)

    assert result.inputs is inputs
    assert result.inputs.total_size == 25
