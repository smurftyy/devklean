from __future__ import annotations

import ctypes
import os
import shutil
import sys
from ctypes import byref, create_unicode_buffer, wintypes
from pathlib import Path
from typing import Sequence

from devklean.deletion.base import BaseDeletionStrategy
from devklean.deletion.safety import SafetyValidator
from devklean.models import CleanableItem, DeleteFailure, DeleteResult


class TrashStrategy(BaseDeletionStrategy):
    """Move deleted items to the operating system trash when possible."""

    name = "trash"

    def __init__(
        self,
        trash_root: Path | None = None,
        validator: SafetyValidator | None = None,
    ) -> None:
        super().__init__(validator)
        self._trash_root = trash_root

    def _delete_safe(
        self,
        items: Sequence[CleanableItem],
        total_size: int,
    ) -> DeleteResult:
        deleted: list[str] = []
        failed: list[DeleteFailure] = []
        trashed: list[str] = []

        for item in items:
            try:
                trashed_path = self._trash_path(Path(item.path))
                deleted.append(item.path)
                trashed.append(str(trashed_path))
            except Exception as exc:  # pragma: no cover - platform-specific failures
                failed.append(DeleteFailure(path=item.path, error=str(exc)))

        return DeleteResult(
            deleted=tuple(deleted),
            failed=tuple(failed),
            total_size=total_size,
            trashed=tuple(trashed),
        )

    def _trash_path(self, source: Path) -> Path:
        if os.name == "nt":
            return self._trash_windows(source)
        return self._trash_unix(source)

    def _trash_unix(self, source: Path) -> Path:
        trash_root = self._trash_root_for_unix()
        trash_files = trash_root / "files"
        trash_files.mkdir(parents=True, exist_ok=True)

        destination = self._unique_destination(trash_files, source.name)
        shutil.move(str(source), str(destination))
        return destination

    def _trash_windows(self, source: Path) -> Path:
        class SHFILEOPSTRUCTW(ctypes.Structure):
            _fields_ = [
                ("hwnd", wintypes.HWND),
                ("wFunc", wintypes.UINT),
                ("pFrom", wintypes.LPCWSTR),
                ("pTo", wintypes.LPCWSTR),
                ("fFlags", wintypes.USHORT),
                ("fAnyOperationsAborted", wintypes.BOOL),
                ("hNameMappings", ctypes.c_void_p),
                ("lpszProgressTitle", wintypes.LPCWSTR),
            ]

        fo_delete = 0x0003
        fof_allowundo = 0x0040
        fof_noconfirmation = 0x0010
        fof_silent = 0x0004

        source_buffer = create_unicode_buffer(str(source.resolve()) + "\0")
        operation = SHFILEOPSTRUCTW()
        operation.wFunc = fo_delete
        operation.pFrom = ctypes.cast(source_buffer, wintypes.LPCWSTR)
        operation.fFlags = fof_allowundo | fof_noconfirmation | fof_silent

        # windll exists only on Windows; this branch only runs there.
        result = ctypes.windll.shell32.SHFileOperationW(byref(operation))  # type: ignore[attr-defined]
        if result != 0:
            raise OSError(f"Windows trash operation failed with code {result}")
        if operation.fAnyOperationsAborted:
            raise OSError("Windows trash operation was aborted")
        return source

    def _trash_root_for_unix(self) -> Path:
        if self._trash_root is not None:
            return self._trash_root

        if sys_platform_is_macos():
            return Path.home() / ".Trash"

        data_home = os.environ.get("XDG_DATA_HOME")
        if data_home:
            return Path(data_home) / "Trash"

        return Path.home() / ".local" / "share" / "Trash"

    def _unique_destination(self, trash_dir: Path, name: str) -> Path:
        destination = trash_dir / name
        if not destination.exists():
            return destination

        suffix = 1
        while True:
            candidate = trash_dir / f"{name}.{suffix}"
            if not candidate.exists():
                return candidate
            suffix += 1


def sys_platform_is_macos() -> bool:
    return sys_platform() == "darwin"


def sys_platform() -> str:
    return sys.platform
