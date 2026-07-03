from __future__ import annotations

from dataclasses import dataclass, field

from devklean.config.defaults import DEFAULT_TARGETS

# Single source of truth for the large-deletion confirmation threshold; the
# CLI/TUI confirmation flow re-exports this as DEFAULT_LARGE_THRESHOLD.
DEFAULT_CONFIRM_THRESHOLD = 1024**3  # 1 GiB


@dataclass(frozen=True)
class DefaultsConfig:
    dry_run: bool = False
    interactive: bool = False
    compress: bool = False
    path: str = "."
    default_yes: bool = False
    theme: str = "default"
    confirm_threshold: int = DEFAULT_CONFIRM_THRESHOLD


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
