"""Minimal PEP 517/660 backend for devklean."""

from __future__ import annotations

import base64
import csv
import hashlib
import re
import shutil
import tarfile
import tempfile
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Iterable
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "src"
PACKAGE_DIR = SRC_DIR / "devklean"
DIST_NAME = "devklean"
SUMMARY = "Clean up common development artifacts to reclaim disk space"
REQUIRES_PYTHON = ">=3.8"
LICENSE = "Proprietary"
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: End Users/Desktop",
    "License :: Other/Proprietary License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: System :: Filesystems",
    "Topic :: Utilities",
]
KEYWORDS = ["cleanup", "cli", "disk-space", "development"]
DEPENDENCIES = ['tomli>=2.0.0; python_version < "3.11"']
ENTRY_POINTS = {"console_scripts": {"devklean": "devklean.cli.main:main"}}
PY_TAG = "py3"
ABI_TAG = "none"
PLATFORM_TAG = "any"


@dataclass(frozen=True)
class WheelFile:
    archive_name: str
    source_path: Path | None
    data: bytes | None = None


def _version() -> str:
    version_file = PACKAGE_DIR / "_version.py"
    match = re.search(r'__version__\s*=\s*"([^"]+)"', version_file.read_text(encoding="utf-8"))
    if not match:
        raise RuntimeError("Unable to determine package version")
    return match.group(1)


def _distribution_name() -> str:
    return DIST_NAME.replace("-", "_")


def _dist_info_dir() -> str:
    return f"{_distribution_name()}-{_version()}.dist-info"


def _wheel_name() -> str:
    return f"{DIST_NAME}-{_version()}-{PY_TAG}-{ABI_TAG}-{PLATFORM_TAG}.whl"


def _sdist_name() -> str:
    return f"{DIST_NAME}-{_version()}.tar.gz"


def _metadata_text() -> str:
    lines = [
        "Metadata-Version: 2.4",
        f"Name: {DIST_NAME}",
        f"Version: {_version()}",
        f"Summary: {SUMMARY}",
        f"License: {LICENSE}",
        f"Requires-Python: {REQUIRES_PYTHON}",
    ]
    lines.extend(f"Classifier: {classifier}" for classifier in CLASSIFIERS)
    lines.append(f"Keywords: {', '.join(KEYWORDS)}")
    lines.extend(f"Requires-Dist: {requirement}" for requirement in DEPENDENCIES)
    lines.append("")
    return "\n".join(lines)


def _wheel_text(editable: bool = False) -> str:
    generator = "build_backend (editable)" if editable else "build_backend"
    return "\n".join(
        [
            "Wheel-Version: 1.0",
            f"Generator: {generator}",
            "Root-Is-Purelib: true",
            f"Tag: {PY_TAG}-{ABI_TAG}-{PLATFORM_TAG}",
            "",
        ]
    )


def _entry_points_text() -> str:
    lines = ["[console_scripts]"]
    lines.extend(f"{name} = {target}" for name, target in ENTRY_POINTS["console_scripts"].items())
    lines.append("")
    return "\n".join(lines)


def _record_line(path: str, data: bytes) -> list[str]:
    digest = hashlib.sha256(data).digest()
    encoded = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return [path, f"sha256={encoded}", str(len(data))]


def _write_metadata(dist_info_dir: Path, editable: bool = False) -> None:
    dist_info_dir.mkdir(parents=True, exist_ok=True)
    (dist_info_dir / "METADATA").write_text(_metadata_text(), encoding="utf-8")
    (dist_info_dir / "WHEEL").write_text(_wheel_text(editable=editable), encoding="utf-8")
    (dist_info_dir / "entry_points.txt").write_text(_entry_points_text(), encoding="utf-8")
    (dist_info_dir / "top_level.txt").write_text("devklean\n", encoding="utf-8")


def _package_files() -> Iterable[Path]:
    for path in sorted(PACKAGE_DIR.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        yield path


def _wheel_files(editable: bool = False) -> list[WheelFile]:
    files: list[WheelFile] = []
    if editable:
        pth_data = f"{SRC_DIR}\n".encode("utf-8")
        files.append(WheelFile(f"{_distribution_name()}.pth", None, pth_data))
        return files

    for source_path in _package_files():
        archive_name = source_path.relative_to(SRC_DIR).as_posix()
        files.append(WheelFile(archive_name, source_path))
    return files


def _build_wheel_archive(wheel_directory: str, editable: bool = False) -> str:
    wheel_path = Path(wheel_directory) / _wheel_name()
    dist_info = _dist_info_dir()
    record_rows: list[list[str]] = []

    with ZipFile(wheel_path, "w", compression=ZIP_DEFLATED) as archive:
        for wheel_file in _wheel_files(editable=editable):
            if wheel_file.data is not None:
                data = wheel_file.data
            elif wheel_file.source_path is not None:
                data = wheel_file.source_path.read_bytes()
            else:
                data = b""
            archive.writestr(wheel_file.archive_name, data)
            record_rows.append(_record_line(wheel_file.archive_name, data))

        metadata_files = {
            f"{dist_info}/METADATA": _metadata_text().encode("utf-8"),
            f"{dist_info}/WHEEL": _wheel_text(editable=editable).encode("utf-8"),
            f"{dist_info}/entry_points.txt": _entry_points_text().encode("utf-8"),
            f"{dist_info}/top_level.txt": b"devklean\n",
        }
        for archive_name, data in metadata_files.items():
            archive.writestr(archive_name, data)
            record_rows.append(_record_line(archive_name, data))

        record_rows.append([f"{dist_info}/RECORD", "", ""])
        record_buffer = StringIO()
        writer = csv.writer(record_buffer, lineterminator="\n")
        writer.writerows(record_rows)
        record_data = record_buffer.getvalue().encode("utf-8")
        archive.writestr(f"{dist_info}/RECORD", record_data)

    return wheel_path.name


def get_requires_for_build_wheel(config_settings=None):  # noqa: D401
    return []


def get_requires_for_build_editable(config_settings=None):  # noqa: D401
    return []


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    dist_info_dir = Path(metadata_directory) / _dist_info_dir()
    _write_metadata(dist_info_dir)
    return dist_info_dir.name


def prepare_metadata_for_build_editable(metadata_directory, config_settings=None):
    dist_info_dir = Path(metadata_directory) / _dist_info_dir()
    _write_metadata(dist_info_dir, editable=True)
    return dist_info_dir.name


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    return _build_wheel_archive(wheel_directory, editable=False)


def build_editable(wheel_directory, config_settings=None, metadata_directory=None):
    return _build_wheel_archive(wheel_directory, editable=True)


def build_sdist(sdist_directory, config_settings=None):
    sdist_path = Path(sdist_directory) / _sdist_name()
    sdist_root = f"{DIST_NAME}-{_version()}"

    files = [
        Path("pyproject.toml"),
        Path("README.md"),
        Path("build_backend.py"),
    ]
    files.extend(path.relative_to(ROOT) for path in _package_files())

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir) / sdist_root
        temp_root.mkdir(parents=True, exist_ok=True)
        for relative_path in files:
            destination = temp_root / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative_path, destination)

        with tarfile.open(sdist_path, "w:gz") as archive:
            archive.add(temp_root, arcname=sdist_root)

    return sdist_path.name
