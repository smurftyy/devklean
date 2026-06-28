from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from devklean.models import CleanableItem


@dataclass(frozen=True)
class SafetyViolation:
    """A single safety rule that a path violated."""

    rule: str
    path: str
    message: str


def _posix_protected_paths() -> set[str]:
    paths = {
        "/",
        "/bin",
        "/sbin",
        "/boot",
        "/dev",
        "/etc",
        "/lib",
        "/lib32",
        "/lib64",
        "/proc",
        "/sys",
        "/usr",
        "/var",
        "/opt",
        "/root",
        "/run",
        "/srv",
    }
    if sys.platform == "darwin":
        paths |= {
            "/System",
            "/Library",
            "/Applications",
            "/private",
            "/cores",
            "/Volumes",
        }
    return paths


def _windows_protected_paths() -> set[str]:
    paths: set[str] = set()
    system_root = os.environ.get("SystemRoot")
    if system_root:
        paths.add(system_root)
    system_drive = os.environ.get("SystemDrive", "C:")
    paths.add(system_drive + "\\")
    paths.add(system_drive + "\\Program Files")
    paths.add(system_drive + "\\Program Files (x86)")
    return paths


def protected_system_paths() -> frozenset[str]:
    """Return the platform-aware set of protected system directories.

    Paths are normalized (and lower-cased on Windows) for exact-match
    comparison against a resolved real path.
    """
    raw = _windows_protected_paths() if os.name == "nt" else _posix_protected_paths()
    return frozenset(_normalize(path) for path in raw)


def _normalize(path: str) -> str:
    normalized = os.path.normpath(path)
    if os.name == "nt":
        return normalized.lower()
    return normalized


class SafetyValidator:
    """The single place safety checks live for all deletion strategies.

    Every rule is checked here so strategies never duplicate validation.
    """

    def __init__(
        self,
        allow_symlinks: bool = False,
        protected_paths: frozenset[str] | None = None,
    ) -> None:
        self._allow_symlinks = allow_symlinks
        self._protected = (
            protected_paths if protected_paths is not None else protected_system_paths()
        )

    def validate(self, path: str) -> SafetyViolation | None:
        """Return the first violated rule for ``path``, or None if safe.

        Structural location rules (root, home, mount, protected) are checked
        before the symlink rule, and against both the literal and the resolved
        path. This matters on macOS, where ``/etc``, ``/var``, and ``/tmp`` are
        themselves symlinks into ``/private``: such a path must be reported as a
        protected system directory — and must not be bypassable with
        ``--allow-symlinks`` — rather than as a plain symbolic link.
        """
        real = os.path.realpath(path)

        if real == os.path.abspath(os.sep) or self._normalized(real) == os.sep:
            return SafetyViolation(
                rule="filesystem_root",
                path=path,
                message=f"Refusing to delete '{path}': it is the filesystem root.",
            )

        home = self._home_dir()
        if home is not None and self._normalized(real) == home:
            return SafetyViolation(
                rule="home_directory",
                path=path,
                message=f"Refusing to delete '{path}': it is your home directory.",
            )

        if os.path.ismount(real):
            return SafetyViolation(
                rule="mount_point",
                path=path,
                message=f"Refusing to delete '{path}': it is a mounted drive root.",
            )

        if self._normalized(path) in self._protected or self._normalized(real) in self._protected:
            return SafetyViolation(
                rule="protected_system_directory",
                path=path,
                message=f"Refusing to delete '{path}': protected system directory.",
            )

        if not self._allow_symlinks and os.path.islink(path):
            return SafetyViolation(
                rule="symlink",
                path=path,
                message=(
                    f"Refusing to delete '{path}': it is a symbolic link "
                    f"(use --allow-symlinks to override)."
                ),
            )

        return None

    def partition(
        self,
        items: Sequence[CleanableItem],
    ) -> tuple[list[CleanableItem], list[tuple[CleanableItem, SafetyViolation]]]:
        """Split items into (safe, blocked) where blocked carries the violation."""
        safe: list[CleanableItem] = []
        blocked: list[tuple[CleanableItem, SafetyViolation]] = []
        for item in items:
            violation = self.validate(item.path)
            if violation is None:
                safe.append(item)
            else:
                blocked.append((item, violation))
        return safe, blocked

    def _normalized(self, real: str) -> str:
        return _normalize(real)

    def _home_dir(self) -> str | None:
        try:
            return _normalize(os.path.realpath(Path.home()))
        except (RuntimeError, OSError):
            return None
