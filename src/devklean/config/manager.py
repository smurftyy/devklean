from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from devklean.config.models import AppConfig, DefaultsConfig
from devklean.config.paths import get_config_path
from devklean.config.targets import merge_targets

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    import tomli as tomllib

PROJECT_CONFIG_NAME = ".devklean.toml"

_KNOWN_TOP_LEVEL = {"defaults", "targets", "ignore", "exclude"}
_KNOWN_DEFAULTS = {
    "dry_run",
    "interactive",
    "compress",
    "compress_min_size",
    "compress_format",
    "path",
    "default_yes",
    "theme",
    "confirm_threshold",
}


@dataclass(frozen=True)
class ConfigLoadResult:
    config: AppConfig
    warnings: list[str]


class ConfigManager:
    """Load and merge user configuration with built-in defaults.

    Precedence (lowest to highest): built-in defaults < global config file <
    project ``.devklean.toml`` discovered by walking up from the start dir.
    Scalar keys take the highest-precedence value; list keys are unioned.
    """

    def __init__(
        self,
        config_path: Path | None = None,
        project_dir: Path | None = None,
    ) -> None:
        self._config_path = config_path if config_path is not None else get_config_path()
        self._project_dir = project_dir if project_dir is not None else Path.cwd()

    @property
    def config_path(self) -> Path:
        return self._config_path

    def load(self) -> AppConfig:
        return self.load_full().config

    def load_full(self) -> ConfigLoadResult:
        warnings: list[str] = []

        global_raw = self._read_toml(self._config_path, warnings)
        _validate(global_raw, str(self._config_path), warnings)

        project_path = self._find_project_config()
        project_raw: dict[str, Any] = {}
        if project_path is not None:
            project_raw = self._read_toml(project_path, warnings)
            _validate(project_raw, str(project_path), warnings)

        # Layers in increasing precedence.
        config = self._build_config([global_raw, project_raw])
        return ConfigLoadResult(config=config, warnings=warnings)

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
            if "--compress" not in raw_argv:
                args.compress = config.defaults.compress

        if getattr(args, "path", None) == "." and not _explicit_path_provided(raw_argv):
            args.path = os.path.expanduser(config.defaults.path)

    # --- internals ---

    def _read_toml(self, path: Path, warnings: list[str]) -> dict[str, Any]:
        if not path.is_file():
            return {}
        try:
            return tomllib.loads(path.read_text(encoding="utf-8"))
        except (tomllib.TOMLDecodeError, OSError) as exc:
            warnings.append(f"Could not parse config '{path}': {exc}; ignoring it.")
            return {}

    def _find_project_config(self) -> Path | None:
        current = self._project_dir.resolve()
        for directory in (current, *current.parents):
            candidate = directory / PROJECT_CONFIG_NAME
            if candidate.is_file():
                return candidate
        return None

    def _build_config(self, layers: list[dict[str, Any]]) -> AppConfig:
        # Scalars: highest-precedence (last non-empty) layer wins.
        # Lists: unioned across layers preserving order.
        defaults = self._merge_defaults(layers)

        exclude_dirs = _union_lists(*[_as_str_list(layer.get("exclude", [])) for layer in layers])

        target_excludes = _union_lists(
            *[_as_str_list(layer.get("targets", {}).get("exclude", [])) for layer in layers]
        )
        custom_targets: dict[str, str] = {}
        for layer in layers:
            custom = layer.get("targets", {}).get("custom", {})
            if isinstance(custom, dict):
                custom_targets.update({str(k): str(v) for k, v in custom.items()})

        merged_targets = merge_targets(exclude=target_excludes, custom=custom_targets)

        ignored_paths = tuple(
            _normalize_path(path)
            for path in _union_lists(
                *[_as_str_list(layer.get("ignore", {}).get("paths", [])) for layer in layers]
            )
        )
        ignored_directories = tuple(
            _union_lists(
                exclude_dirs,
                *[_as_str_list(layer.get("ignore", {}).get("directories", [])) for layer in layers],
            )
        )

        return AppConfig(
            targets=merged_targets,
            ignored_paths=ignored_paths,
            ignored_directories=ignored_directories,
            defaults=defaults,
        )

    def _merge_defaults(self, layers: list[dict[str, Any]]) -> DefaultsConfig:
        base = DefaultsConfig()
        merged: dict[str, Any] = {
            "dry_run": base.dry_run,
            "interactive": base.interactive,
            "compress": base.compress,
            "compress_min_size": base.compress_min_size,
            "compress_format": base.compress_format,
            "path": base.path,
            "default_yes": base.default_yes,
            "theme": base.theme,
            "confirm_threshold": base.confirm_threshold,
        }
        for layer in layers:
            section = layer.get("defaults", {})
            if not isinstance(section, dict):
                continue
            for key in ("dry_run", "interactive", "default_yes"):
                if key in section:
                    merged[key] = bool(section[key])
            if "compress" in section:
                merged["compress"] = bool(section["compress"])
            if "compress_min_size" in section:
                try:
                    merged["compress_min_size"] = int(section["compress_min_size"])
                except (TypeError, ValueError):
                    pass
            if "compress_format" in section:
                merged["compress_format"] = str(section["compress_format"])
            if "path" in section:
                merged["path"] = str(section["path"])
            if "theme" in section:
                merged["theme"] = str(section["theme"])
            if "confirm_threshold" in section:
                try:
                    merged["confirm_threshold"] = int(section["confirm_threshold"])
                except (TypeError, ValueError):
                    pass
        return DefaultsConfig(**merged)


def _validate(data: dict[str, Any], source: str, warnings: list[str]) -> None:
    for key in data:
        if key not in _KNOWN_TOP_LEVEL:
            warnings.append(f"Unknown config key '{key}' in '{source}' (ignored).")
    defaults_section = data.get("defaults", {})
    if isinstance(defaults_section, dict):
        for key in defaults_section:
            if key not in _KNOWN_DEFAULTS:
                warnings.append(f"Unknown key 'defaults.{key}' in '{source}' (ignored).")


def _union_lists(*lists: list[str]) -> list[str]:
    seen: dict[str, None] = {}
    for items in lists:
        for item in items:
            seen.setdefault(item, None)
    return list(seen)


def _as_str_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _normalize_path(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))


def _explicit_path_provided(argv: list[str]) -> bool:
    """Return True when a positional path appears on the command line."""
    command_names = {
        "scan",
        "clean",
        "history",
        "doctor",
        "stats",
        "restore",
        "explain",
        "analyze",
        "config",
        "plugins",
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
