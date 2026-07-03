from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

ARCHIVE_FORMAT = "zip"


@dataclass(frozen=True)
class CompressionArchive:
    path: str
    format: str


def compress_directory(source: Path) -> CompressionArchive:
    """Archive a directory into a sibling zip file and remove the source tree."""
    archive_path = Path(
        shutil.make_archive(
            str(source),
            ARCHIVE_FORMAT,
            root_dir=source.parent,
            base_dir=source.name,
        )
    )
    shutil.rmtree(source)
    return CompressionArchive(path=str(archive_path), format=ARCHIVE_FORMAT)
