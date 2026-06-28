"""File-based structured logging, kept entirely separate from terminal output.

The renderers own everything the user sees on stdout/stderr. This logger writes
detail to a rotating file and never attaches a console handler, so the two
concerns cannot interfere.
"""

from __future__ import annotations

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

_LOGGER_NAME = "devklean"
_MAX_BYTES = 1_000_000
_BACKUP_COUNT = 5


def get_log_path() -> Path:
    """Return the rotating log file path (XDG cache / Windows LOCALAPPDATA aware)."""
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA")
        root = Path(base) if base else Path.home() / "AppData" / "Local"
        return root / "devklean" / "logs" / "latest.log"

    cache = os.environ.get("XDG_CACHE_HOME")
    root = Path(cache) if cache else Path.home() / ".cache"
    return root / "devklean" / "logs" / "latest.log"


def get_logger() -> logging.Logger:
    return logging.getLogger(_LOGGER_NAME)


def configure_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure the devklean file logger. Idempotent and re-pointable."""
    logger = get_logger()
    logger.setLevel(level)
    logger.propagate = False

    # Reset handlers so repeated calls (and tests pointing elsewhere) re-target.
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()

    try:
        log_path = get_log_path()
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handler = RotatingFileHandler(
            log_path, maxBytes=_MAX_BYTES, backupCount=_BACKUP_COUNT, encoding="utf-8"
        )
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s %(levelname)s %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S%z",
            )
        )
        logger.addHandler(handler)
    except OSError:
        # Logging must never break the CLI; degrade to no file logging.
        logger.addHandler(logging.NullHandler())
    return logger


def log_invocation(argv: list[str], command: str | None) -> None:
    get_logger().info("invoke command=%s argv=%s", command, " ".join(argv))
