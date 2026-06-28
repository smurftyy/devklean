from __future__ import annotations

from dataclasses import dataclass, field

from devclean.config.defaults import DEFAULT_TARGETS


@dataclass(frozen=True)
class DefaultsConfig:
    dry_run: bool = False
    interactive: bool = False
    path: str = "."


@dataclass(frozen=True)
class AppConfig:
    targets: dict[str, str]
    ignored_paths: tuple[str, ...] = ()
    ignored_directories: tuple[str, ...] = ()
    defaults: DefaultsConfig = field(default_factory=DefaultsConfig)

    @property
    def scan_settings(self) -> ScanSettings:
        return ScanSettings(
            targets=dict(self.targets),
            ignored_paths=frozenset(self.ignored_paths),
            ignored_directories=frozenset(self.ignored_directories),
        )


@dataclass(frozen=True)
class ScanSettings:
    """Scan-specific settings derived from application configuration."""

    targets: dict[str, str]
    ignored_paths: frozenset[str] = field(default_factory=frozenset)
    ignored_directories: frozenset[str] = field(default_factory=frozenset)

    @classmethod
    def defaults(cls) -> ScanSettings:
        return cls(targets=dict(DEFAULT_TARGETS))
