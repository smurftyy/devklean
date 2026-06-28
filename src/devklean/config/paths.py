from __future__ import annotations

import os
import sys
from pathlib import Path


def get_config_path() -> Path:
    """Return the platform-appropriate config file path.

    An explicit ``XDG_CONFIG_HOME`` override is honored on every platform; the
    Windows-native ``APPDATA`` location is only the fallback when it is unset.
    """
    xdg_config = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config:
        return Path(xdg_config) / "devklean" / "config.toml"

    if sys.platform == "win32":
        base = os.environ.get("APPDATA")
        if base:
            return Path(base) / "devklean" / "config.toml"
        return Path.home() / "AppData" / "Roaming" / "devklean" / "config.toml"

    return Path.home() / ".config" / "devklean" / "config.toml"
