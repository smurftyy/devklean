from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DefaultsConfig:
    dry_run: bool = False
    interactive: bool = False
    path: str = "."


@dataclass(frozen=True)
class AppConfig:
    targets: dict[str, str]
    ignored_paths: tuple[str, ...] = ()
    defaults: DefaultsConfig = field(default_factory=DefaultsConfig)
