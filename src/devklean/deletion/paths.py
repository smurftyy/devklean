from __future__ import annotations

import os
import sys
from pathlib import Path


def get_deletion_metadata_dir() -> Path:
    """Return the directory used to persist deletion metadata.

    An explicit ``XDG_DATA_HOME`` override is honored on every platform; the
    Windows-native ``APPDATA`` location is only the fallback when it is unset.
    """
    xdg_data = os.environ.get("XDG_DATA_HOME")
    if xdg_data:
        return Path(xdg_data) / "devklean" / "deletions"

    if sys.platform == "win32":
        base = os.environ.get("APPDATA")
        if base:
            return Path(base) / "devklean" / "deletions"
        return Path.home() / "AppData" / "Roaming" / "devklean" / "deletions"

    return Path.home() / ".local" / "share" / "devklean" / "deletions"
