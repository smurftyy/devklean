"""Tests for the large-deletion typed-confirmation gate."""

from __future__ import annotations

import io

from devklean.cli.confirmation import (
    DEFAULT_LARGE_THRESHOLD,
    confirm_large_deletion,
    exceeds_threshold,
)


def test_default_threshold_is_one_gibibyte() -> None:
    assert DEFAULT_LARGE_THRESHOLD == 1024**3


def test_exceeds_threshold_true_at_or_above() -> None:
    assert exceeds_threshold(1024**3, 1024**3) is True
    assert exceeds_threshold(2 * 1024**3, 1024**3) is True


def test_exceeds_threshold_false_below() -> None:
    assert exceeds_threshold(500, 1024**3) is False


def test_exceeds_threshold_zero_disables_gate() -> None:
    assert exceeds_threshold(10**12, 0) is False


def test_confirm_large_deletion_accepts_exact_word() -> None:
    assert (
        confirm_large_deletion(
            count=7,
            total_size=3 * 1024**3,
            threshold=1024**3,
            input_fn=lambda prompt: "DELETE",
            stream=io.StringIO(),
        )
        is True
    )


def test_confirm_large_deletion_is_case_sensitive() -> None:
    assert (
        confirm_large_deletion(
            count=7,
            total_size=3 * 1024**3,
            threshold=1024**3,
            input_fn=lambda prompt: "delete",
            stream=io.StringIO(),
        )
        is False
    )


def test_confirm_large_deletion_rejects_plain_yes() -> None:
    assert (
        confirm_large_deletion(
            count=7,
            total_size=3 * 1024**3,
            threshold=1024**3,
            input_fn=lambda prompt: "y",
            stream=io.StringIO(),
        )
        is False
    )


def test_confirm_large_deletion_prompt_shows_count_and_size() -> None:
    seen = {}

    def capture(prompt: str) -> str:
        seen["prompt"] = prompt
        return "DELETE"

    stream = io.StringIO()
    confirm_large_deletion(
        count=7,
        total_size=3 * 1024**3,
        threshold=1024**3,
        input_fn=capture,
        stream=stream,
    )
    shown = seen["prompt"] + stream.getvalue()
    assert "7" in shown
    assert "3.0 GB" in shown
    assert "DELETE" in shown
