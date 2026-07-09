"""Compress-before-trash: build and verify an archive without ever touching
the source directory.

This module only does two things — ``compress_path`` and ``verify_archive`` —
and neither one deletes or modifies the source. Ordering the source's removal
around a *verified* archive is the caller's job (``devklean.deletion.trash``);
keeping that decision out of this module is what makes the ordering testable
on its own.

Default format is gzip via the stdlib ``tarfile`` ('w:gz') — no new hard
dependency. zstd is opt-in via the ``devklean[zstd]`` extra (the
``zstandard`` package); stdlib ``tarfile`` only gained native zstd support in
Python 3.14, so this is manual streaming through ``zstandard`` for older
versions. If zstd is requested but the extra isn't installed, this silently
(but loggedly) falls back to gzip rather than crashing.
"""

from __future__ import annotations

import os
import tarfile
from contextlib import ExitStack, contextmanager
from dataclasses import dataclass
from pathlib import Path
from tempfile import mkstemp
from typing import Iterator

from devklean.logging_setup import get_logger
from devklean.scanner import get_dir_size

GZIP_FORMAT = "gzip"
ZSTD_FORMAT = "zstd"
SUPPORTED_FORMATS = (GZIP_FORMAT, ZSTD_FORMAT)

_ARCHIVE_SUFFIX = {
    GZIP_FORMAT: ".tar.gz",
    ZSTD_FORMAT: ".tar.zst",
}

# Read/write back through the decompressor in chunks during verification,
# rather than materializing whole files in memory.
_VERIFY_CHUNK_SIZE = 1024 * 1024


class CompressionVerificationError(Exception):
    """A freshly built archive failed verification.

    Callers must treat this the same as a compression failure: the source
    directory has not been touched and must stay exactly as it was.
    """


@dataclass(frozen=True)
class CompressionResult:
    """Everything the trash pipeline needs to verify and then record an archive."""

    archive_path: Path
    format: str
    original_size: int
    file_count: int

    @property
    def compressed_size(self) -> int:
        return self.archive_path.stat().st_size


def compress_path(source: Path, *, compress_format: str = GZIP_FORMAT) -> CompressionResult:
    """Archive ``source`` into a new temp file. Never reads-then-deletes;
    ``source`` is left completely untouched, success or failure.

    The archive is written next to ``source`` (same filesystem as the
    original, so a later move never has to cross devices) with a name that
    cannot collide with a real scan target. On any failure while writing,
    the partial temp file is removed and the exception propagates. An
    ``OSError`` propagates as-is; anything else (``tarfile.TarError``,
    a zstd encoder error, ...) is normalized to
    ``CompressionVerificationError`` so callers only ever have to handle
    those two exception types to treat this "maybe partially done" case
    the same as any other compression failure.
    """
    resolved_format = _resolve_format(compress_format)
    archive_path = _new_temp_archive_path(source, resolved_format)

    try:
        with _open_archive_for_write(archive_path, resolved_format) as tar:
            file_count = _add_tree(tar, source)
    except Exception as exc:
        archive_path.unlink(missing_ok=True)
        if isinstance(exc, OSError):
            raise
        raise CompressionVerificationError(f"failed to build archive for {source}: {exc}") from exc

    original_size = get_dir_size(str(source))
    return CompressionResult(
        archive_path=archive_path,
        format=resolved_format,
        original_size=original_size,
        file_count=file_count,
    )


def verify_archive(result: CompressionResult) -> None:
    """Test-extract every regular-file entry and cross-check count/size.

    Entries are streamed and discarded (never written to disk), so this costs
    time but no extra disk space. Raises ``CompressionVerificationError`` on
    any mismatch, corruption, or unreadable entry — never returns a partial
    or best-effort "probably fine" result.
    """
    file_count = 0
    total_size = 0
    sizes_by_name: dict[str, int] = {}

    try:
        with _open_archive_for_read(result.archive_path, result.format) as tar:
            for member in tar:
                if member.isreg():
                    extracted = tar.extractfile(member)
                    if extracted is None:
                        raise CompressionVerificationError(
                            f"archive entry {member.name!r} in {result.archive_path} "
                            "could not be read back"
                        )
                    while extracted.read(_VERIFY_CHUNK_SIZE):
                        pass
                    file_count += 1
                    total_size += member.size
                    sizes_by_name[member.name] = member.size
                elif member.islnk():
                    # A hardlink to an earlier regular member: tar stores it
                    # as a zero-size reference rather than duplicating the
                    # data, but it represents a distinct source file with
                    # identical content, so it must still count as one file
                    # of the linked-to size — the same way get_dir_size
                    # counts each hardlinked directory entry independently.
                    linked_size = sizes_by_name.get(member.linkname, 0)
                    file_count += 1
                    total_size += linked_size
                else:
                    continue
    except CompressionVerificationError:
        raise
    except Exception as exc:
        # Corruption can surface as tarfile.TarError, OSError, EOFError
        # (truncated gzip stream), zlib/zstd decode errors, and more,
        # depending on exactly where the archive was damaged. Every one of
        # them means the same thing here: the archive does not read back
        # cleanly, so it must not be trusted as a stand-in for the source.
        raise CompressionVerificationError(
            f"archive {result.archive_path} failed verification: {exc}"
        ) from exc

    if file_count != result.file_count:
        raise CompressionVerificationError(
            f"archive {result.archive_path} contains {file_count} files, "
            f"expected {result.file_count}"
        )
    if total_size != result.original_size:
        raise CompressionVerificationError(
            f"archive {result.archive_path} contains {total_size} uncompressed bytes, "
            f"expected {result.original_size}"
        )


# --- internals ---


def _resolve_format(compress_format: str) -> str:
    if compress_format == ZSTD_FORMAT and not _zstd_available():
        get_logger().warning(
            "zstd compression requested but the 'zstandard' package is not installed "
            "(pip install 'devklean[zstd]'); falling back to gzip"
        )
        return GZIP_FORMAT
    if compress_format not in SUPPORTED_FORMATS:
        get_logger().warning("unknown compression format %r; falling back to gzip", compress_format)
        return GZIP_FORMAT
    return compress_format


def _zstd_available() -> bool:
    try:
        import zstandard  # noqa: F401
    except ImportError:
        return False
    return True


def _new_temp_archive_path(source: Path, resolved_format: str) -> Path:
    fd, name = mkstemp(
        prefix=f".{source.name}-",
        suffix=_ARCHIVE_SUFFIX[resolved_format],
        dir=source.parent,
    )
    os.close(fd)
    return Path(name)


def _add_tree(tar: tarfile.TarFile, source: Path) -> int:
    """Add ``source`` (recursively) to ``tar``. Returns the file count
    (regular files plus hardlinks to an already-added file)."""
    count = 0

    def _count_filter(tarinfo: tarfile.TarInfo) -> tarfile.TarInfo:
        nonlocal count
        # A hardlink to an already-added file becomes an LNKTYPE member (tar
        # stores it as a zero-size reference, not duplicate data) but is
        # still a distinct source file — see the matching count in
        # verify_archive.
        if tarinfo.isreg() or tarinfo.islnk():
            count += 1
        return tarinfo

    tar.add(str(source), arcname=source.name, recursive=True, filter=_count_filter)
    return count


@contextmanager
def _open_archive_for_write(archive_path: Path, resolved_format: str) -> Iterator[tarfile.TarFile]:
    with ExitStack() as stack:
        if resolved_format == ZSTD_FORMAT:
            # _resolve_format only returns ZSTD_FORMAT when the import already
            # succeeded, so this is guaranteed to be available here.
            import zstandard

            raw = stack.enter_context(archive_path.open("wb"))
            writer = stack.enter_context(zstandard.ZstdCompressor().stream_writer(raw))
            tar = stack.enter_context(tarfile.open(fileobj=writer, mode="w|"))
        else:
            tar = stack.enter_context(tarfile.open(archive_path, mode="w:gz"))
        yield tar


@contextmanager
def _open_archive_for_read(archive_path: Path, resolved_format: str) -> Iterator[tarfile.TarFile]:
    with ExitStack() as stack:
        if resolved_format == ZSTD_FORMAT:
            # The archive was written with this same format, so if it got
            # this far the import already succeeded once (see
            # _open_archive_for_write).
            import zstandard

            raw = stack.enter_context(archive_path.open("rb"))
            reader = stack.enter_context(zstandard.ZstdDecompressor().stream_reader(raw))
            tar = stack.enter_context(tarfile.open(fileobj=reader, mode="r|"))
        else:
            tar = stack.enter_context(tarfile.open(archive_path, mode="r:gz"))
        yield tar
