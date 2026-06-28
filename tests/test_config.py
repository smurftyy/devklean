"""Tests for devklean configuration loading."""

from __future__ import annotations

from pathlib import Path

from devklean.config import DEFAULT_TARGETS, ConfigManager, ScanSettings, merge_targets
from devklean.scanner import scan


def test_config_manager_uses_defaults_when_missing(tmp_path: Path) -> None:
    config_path = tmp_path / "config.toml"
    manager = ConfigManager(config_path=config_path)

    config = manager.load()

    assert config.targets == DEFAULT_TARGETS
    assert config.ignored_paths == ()
    assert config.ignored_directories == ()
    assert config.defaults.dry_run is False
    assert config.defaults.interactive is False


def test_config_manager_merges_user_settings(tmp_path: Path) -> None:
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        """
[defaults]
dry_run = true
interactive = true
path = "~/projects"

[targets]
exclude = ["env", "dist"]

[targets.custom]
".turbo" = "Turborepo cache"

[ignore]
paths = ["/tmp/keep/node_modules"]
directories = [".git"]
""".strip(),
        encoding="utf-8",
    )
    manager = ConfigManager(config_path=config_path)

    config = manager.load()

    assert "env" not in config.targets
    assert "dist" not in config.targets
    assert "node_modules" in config.targets
    assert config.targets[".turbo"] == "Turborepo cache"
    assert config.ignored_paths == (str(Path("/tmp/keep/node_modules")),)
    assert config.ignored_directories == (".git",)
    assert config.defaults.dry_run is True
    assert config.defaults.interactive is True
    assert config.defaults.path == "~/projects"


def test_merge_targets() -> None:
    merged = merge_targets(
        exclude=["env"],
        custom={".turbo": "Turborepo cache"},
    )

    assert "env" not in merged
    assert merged[".turbo"] == "Turborepo cache"
    assert "node_modules" in merged


def test_scan_settings_from_app_config(tmp_path: Path) -> None:
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        """
[targets]
exclude = ["dist"]

[ignore]
paths = ["/tmp/keep"]
directories = ["vendor"]
""".strip(),
        encoding="utf-8",
    )
    config = ConfigManager(config_path=config_path).load()
    settings = config.scan_settings

    assert "dist" not in settings.targets
    assert "/tmp/keep" in settings.ignored_paths or str(Path("/tmp/keep")) in {
        str(Path(p)) for p in settings.ignored_paths
    }
    assert "vendor" in settings.ignored_directories


def test_apply_defaults_respects_explicit_cli_flags(tmp_path: Path) -> None:
    config_path = tmp_path / "config.toml"
    config_path.write_text("[defaults]\ndry_run = true\ninteractive = true\n", encoding="utf-8")
    manager = ConfigManager(config_path=config_path)
    config = manager.load()

    class Args:
        command = "clean"
        path = "."
        dry_run = True
        interactive = False
        _config = config

    args = Args()
    manager.apply_defaults(args, ["devklean", "clean", "--dry-run"])

    assert args.dry_run is True
    assert args.interactive is True


def test_scan_honors_excluded_and_custom_targets(tmp_path: Path) -> None:
    root = tmp_path / "project"
    root.mkdir()
    (root / "env").mkdir()
    (root / ".turbo").mkdir()
    (root / "node_modules").mkdir()

    settings = ScanSettings(
        targets=merge_targets(exclude=["env"], custom={".turbo": "Turborepo cache"}),
    )
    found = scan(str(root), settings=settings)
    names = {item.name for item in found}

    assert "env" not in names
    assert ".turbo" in names
    assert "node_modules" in names


def test_scan_honors_excluded_paths(tmp_path: Path) -> None:
    root = tmp_path / "project"
    root.mkdir()
    preserved = root / "node_modules"
    preserved.mkdir()
    (preserved / "package.json").write_text("{}")

    other = root / "apps" / "web" / "node_modules"
    other.mkdir(parents=True)
    (other / "package.json").write_text("{}")

    settings = ScanSettings(
        targets=dict(DEFAULT_TARGETS),
        ignored_paths=frozenset([str(preserved)]),
    )
    found = scan(str(root), settings=settings)
    paths = {item.path for item in found}

    assert str(preserved) not in paths
    assert str(other) in paths


def test_scan_honors_ignored_directories(tmp_path: Path) -> None:
    root = tmp_path / "project"
    root.mkdir()
    (root / "node_modules").mkdir()
    vendor = root / "vendor"
    vendor.mkdir()
    (vendor / "package").mkdir()

    settings = ScanSettings(
        targets={**DEFAULT_TARGETS, "vendor": "Vendor directory"},
        ignored_directories=frozenset(["vendor"]),
    )
    found = scan(str(root), settings=settings)
    names = {item.name for item in found}

    assert "vendor" not in names
    assert "node_modules" in names


def test_scan_end_to_end_with_config_file(tmp_path: Path) -> None:
    root = tmp_path / "project"
    root.mkdir()
    (root / "node_modules").mkdir()
    (root / "env").mkdir()
    (root / ".turbo").mkdir()

    config_path = tmp_path / "config.toml"
    config_path.write_text(
        """
[targets]
exclude = ["env"]

[targets.custom]
".turbo" = "Turborepo cache"
""".strip(),
        encoding="utf-8",
    )

    config = ConfigManager(config_path=config_path).load()
    found = scan(str(root), settings=config.scan_settings)
    names = {item.name for item in found}

    assert "env" not in names
    assert ".turbo" in names
    assert "node_modules" in names
