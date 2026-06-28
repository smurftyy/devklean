from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional

from devclean.config.defaults import DEFAULT_TARGETS
from devclean.config.models import AppConfig, DefaultsConfig
from devclean.config.paths import get_config_path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    import tomli as tomllib


class ConfigManager:
    """Load and merge user configuration with built-in defaults."""

    def __init__(self, config_path: Optional[Path] = None) -> None:
        self._config_path = config_path if config_path is not None else get_config_path()

    @property
    def config_path(self) -> Path:
        return self._config_path

    def load(self) -> AppConfig:
        if not self._config_path.is_file():
            return self._default_config()

        data = tomllib.loads(self._config_path.read_text(encoding="utf-8"))
        return self._merge_config(data)

    def apply_defaults(self, args, raw_argv: list[str]) -> None:
        """Apply configured defaults when the CLI did not override them."""
        config = getattr(args, "_config", None)
        if config is None:
            return

        if getattr(args, "command", None) == "clean":
            if "--dry-run" not in raw_argv:
                args.dry_run = config.defaults.dry_run
            if "-i" not in raw_argv and "--interactive" not in raw_argv:
                args.interactive = config.defaults.interactive

        if not _explicit_path_provided(raw_argv) and args.path == ".":
            args.path = os.path.expanduser(config.defaults.path)

    def _default_config(self) -> AppConfig:
        return AppConfig(
            targets=dict(DEFAULT_TARGETS),
            ignored_paths=(),
            defaults=DefaultsConfig(),
        )

    def _merge_config(self, data: dict[str, Any]) -> AppConfig:
        defaults_section = data.get("defaults", {})
        targets_section = data.get("targets", {})
        ignore_section = data.get("ignore", {})

        merged_targets = dict(DEFAULT_TARGETS)

        for name in _as_str_list(targets_section.get("exclude", [])):
            merged_targets.pop(name, None)

        custom_targets = targets_section.get("custom", {})
        if isinstance(custom_targets, dict):
            for name, label in custom_targets.items():
                merged_targets[str(name)] = str(label)

        ignored_paths = tuple(
            _normalize_path(path)
            for path in _as_str_list(ignore_section.get("paths", []))
        )

        defaults = DefaultsConfig(
            dry_run=bool(defaults_section.get("dry_run", False)),
            interactive=bool(defaults_section.get("interactive", False)),
            path=str(defaults_section.get("path", ".")),
        )

        return AppConfig(
            targets=merged_targets,
            ignored_paths=ignored_paths,
            defaults=defaults,
        )


def _as_str_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _normalize_path(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))


def _explicit_path_provided(argv: list[str]) -> bool:
    """Return True when a positional path appears on the command line."""
    command_names = {
        "scan", "clean", "stats", "restore", "config", "plugins",
    }
    index = 1
    if index < len(argv) and argv[index] in command_names:
        index += 1

    while index < len(argv):
        if argv[index].startswith("-"):
            index += 1
            continue
        return True
    return False
