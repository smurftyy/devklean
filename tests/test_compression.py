"""Real-filesystem tests for compress_path/verify_archive.

Per the compress-before-trash safety contract, compress_path must never touch
the source directory, and verify_archive must reliably reject anything that
doesn't read back cleanly. These tests exercise real tar/gzip (and, when
available, real zstd) I/O rather than mocking the compression internals —
mocks alone can't catch a real corrupt-archive or real-filesystem-permission
failure mode.
"""

from __future__ import annotations

import logging
import os
from dataclasses import replace
from pathlib import Path
from tarfile import TarError

import pytest

from devklean.deletion.compression import (
    CompressionVerificationError,
    compress_path,
    verify_archive,
)


def _make_tree(root: Path) -> int:
    """Create a small real directory tree; returns its total byte size."""
    root.mkdir(parents=True)
    (root / "a.txt").write_text("hello" * 100, encoding="utf-8")
    nested = root / "nested"
    nested.mkdir()
    (nested / "b.bin").write_bytes(b"\x00" * 4096)
    return sum(f.stat().st_size for f in root.rglob("*") if f.is_file())


def test_compress_path_never_touches_the_source(tmp_path: Path) -> None:
    source = tmp_path / "node_modules"
    size = _make_tree(source)

    result = compress_path(source)

    assert source.exists()
    assert (source / "a.txt").exists()
    assert (source / "nested" / "b.bin").exists()
    assert result.archive_path.exists()
    assert result.archive_path.parent == source.parent
    assert result.format == "gzip"
    assert result.original_size == size
    assert result.file_count == 2
    assert result.compressed_size > 0

    result.archive_path.unlink()


def test_verify_archive_passes_for_a_valid_archive(tmp_path: Path) -> None:
    source = tmp_path / "node_modules"
    _make_tree(source)
    result = compress_path(source)

    verify_archive(result)  # must not raise

    result.archive_path.unlink()


def test_verify_archive_raises_on_truncated_archive(tmp_path: Path) -> None:
    source = tmp_path / "node_modules"
    _make_tree(source)
    result = compress_path(source)

    data = result.archive_path.read_bytes()
    result.archive_path.write_bytes(data[: len(data) // 2])

    with pytest.raises(CompressionVerificationError):
        verify_archive(result)

    assert source.exists()  # verification failure must never touch the source
    result.archive_path.unlink()


def test_verify_archive_raises_on_file_count_mismatch(tmp_path: Path) -> None:
    source = tmp_path / "node_modules"
    _make_tree(source)
    result = compress_path(source)
    tampered = replace(result, file_count=result.file_count + 1)

    with pytest.raises(CompressionVerificationError, match="files"):
        verify_archive(tampered)

    result.archive_path.unlink()


def test_verify_archive_raises_on_size_mismatch(tmp_path: Path) -> None:
    source = tmp_path / "node_modules"
    _make_tree(source)
    result = compress_path(source)
    tampered = replace(result, original_size=result.original_size + 1)

    with pytest.raises(CompressionVerificationError, match="bytes"):
        verify_archive(tampered)

    result.archive_path.unlink()


def test_compress_path_handles_hardlinked_files(tmp_path: Path) -> None:
    """A directory containing hardlinks (e.g. an npm/pnpm install cache) must
    still verify: tar collapses repeat hardlinks into zero-size reference
    members, so a naive size/count check that doesn't account for that would
    reject a perfectly valid archive."""
    source = tmp_path / "node_modules"
    source.mkdir()
    (source / "a.txt").write_text("hello" * 100, encoding="utf-8")
    try:
        os.link(source / "a.txt", source / "b.txt")
    except OSError:
        pytest.skip("filesystem does not support hardlinks")

    result = compress_path(source)

    assert result.file_count == 2
    assert result.original_size == 2 * (source / "a.txt").stat().st_size
    verify_archive(result)  # must not raise

    result.archive_path.unlink()


def test_compress_path_normalizes_non_os_errors(tmp_path: Path, monkeypatch) -> None:
    source = tmp_path / "node_modules"
    _make_tree(source)

    def _boom(*args, **kwargs):
        raise TarError("simulated tar corruption")

    monkeypatch.setattr("tarfile.TarFile.add", _boom)

    with pytest.raises(CompressionVerificationError):
        compress_path(source)

    assert source.exists()
    assert (source / "a.txt").exists()
    assert list(tmp_path.glob(".node_modules-*")) == []


def test_compress_path_cleans_up_temp_file_on_failure(tmp_path: Path, monkeypatch) -> None:
    source = tmp_path / "node_modules"
    _make_tree(source)

    def _boom(*args, **kwargs):
        raise OSError("simulated tar write failure")

    monkeypatch.setattr("tarfile.TarFile.add", _boom)

    with pytest.raises(OSError):
        compress_path(source)

    assert source.exists()
    assert (source / "a.txt").exists()
    assert list(tmp_path.glob(".node_modules-*")) == []


def test_zstd_format_round_trips_with_real_zstandard(tmp_path: Path) -> None:
    pytest.importorskip("zstandard")
    source = tmp_path / "dist"
    _make_tree(source)

    result = compress_path(source, compress_format="zstd")

    assert result.format == "zstd"
    verify_archive(result)
    assert source.exists()
    result.archive_path.unlink()


def test_zstd_falls_back_to_gzip_when_package_missing(
    tmp_path: Path, monkeypatch, caplog: pytest.LogCaptureFixture
) -> None:
    source = tmp_path / "dist"
    _make_tree(source)
    monkeypatch.setattr("devklean.deletion.compression._zstd_available", lambda: False)

    with caplog.at_level(logging.WARNING, logger="devklean"):
        result = compress_path(source, compress_format="zstd")

    assert result.format == "gzip"
    assert any("falling back to gzip" in record.message for record in caplog.records)
    verify_archive(result)
    result.archive_path.unlink()
