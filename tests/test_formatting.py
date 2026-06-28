"""Tests for devclean.formatting utilities."""

from __future__ import annotations

import pytest

from devclean.formatting import format_size, truncate


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
