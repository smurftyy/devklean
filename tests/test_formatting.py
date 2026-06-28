"""Tests for devklean.formatting utilities."""

from __future__ import annotations

import pytest

from devklean.formatting import format_size, format_timestamp, truncate


def test_format_timestamp_converts_utc_iso_to_local_minute(utc_timezone) -> None:
    assert format_timestamp("2026-06-28T14:02:11+00:00") == "2026-06-28 14:02"


def test_format_timestamp_falls_back_to_raw_value_when_unparseable() -> None:
    assert format_timestamp("not-a-timestamp") == "not-a-timestamp"


@pytest.mark.parametrize(
    ("size_bytes", "expected"),
    [
        (0, "0.0 B"),
        (512, "512.0 B"),
        (1023, "1023.0 B"),
        (1024, "1.0 KB"),
        (1536, "1.5 KB"),
        (1024 * 1024, "1.0 MB"),
        (50 * 1024 * 1024, "50.0 MB"),
        (1024 * 1024 * 1024, "1.0 GB"),
        (1024 * 1024 * 1024 * 1024, "1.0 TB"),
        (5 * 1024**4, "5.0 TB"),
        (1024**5, "1024.0 TB"),
    ],
)
def test_format_size(size_bytes: int, expected: str) -> None:
    assert format_size(size_bytes) == expected


@pytest.mark.parametrize(
    ("text", "max_len", "expected"),
    [
        ("hello", 10, "hello"),
        ("hello", 5, "hello"),
        ("hello world", 8, "hello..."),
        ("hello", 3, "hel"),
        ("hello", 0, ""),
        ("hello", -1, ""),
    ],
)
def test_truncate(text: str, max_len: int, expected: str) -> None:
    assert truncate(text, max_len) == expected
