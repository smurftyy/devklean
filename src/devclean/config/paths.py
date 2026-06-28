from __future__ import annotations

import os
import sys
from pathlib import Path


def get_config_path() -> Path:
    """Return the platform-appropriate config file path."""
    if sys.platform == "win32":
        base = os.environ.get("APPDATA")
        if base:
            return Path(base) / "devclean" / "config.toml"
        return Path.home() / "AppData" / "Roaming" / "devclean" / "config.toml"

    xdg_config = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config:
        return Path(xdg_config) / "devclean" / "config.toml"
    return Path.home() / ".config" / "devclean" / "config.toml"
