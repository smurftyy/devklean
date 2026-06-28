"""Packaging sanity checks: single-source version and a working entry point."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    import tomli as tomllib

ROOT = Path(__file__).resolve().parent.parent


def test_version_is_a_valid_string() -> None:
    from devklean._version import __version__

    assert re.fullmatch(r"\d+\.\d+\.\d+([.-].+)?", __version__), __version__


def test_version_is_dynamic_in_pyproject() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert "version" in data["project"]["dynamic"]
    assert data["tool"]["hatch"]["version"]["path"] == "src/devklean/_version.py"


def test_version_not_hardcoded_elsewhere() -> None:
    from devklean._version import __version__

    # The version literal must live only in _version.py (single source of truth).
    offenders = []
    for path in (ROOT / "src" / "devklean").rglob("*.py"):
        if path.name == "_version.py":
            continue
        if f'"{__version__}"' in path.read_text(encoding="utf-8"):
            offenders.append(str(path))
    assert offenders == [], f"version string duplicated in: {offenders}"


def test_console_script_entry_point_is_importable() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    target = data["project"]["scripts"]["devklean"]
    module_path, func_name = target.split(":")

    module = __import__(module_path, fromlist=[func_name])
    assert callable(getattr(module, func_name))


@pytest.mark.skipif(not (ROOT / "LICENSE").is_file(), reason="LICENSE not present")
def test_license_declared_and_present() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert data["project"]["license"] == "MIT"
    assert "MIT License" in (ROOT / "LICENSE").read_text(encoding="utf-8")
