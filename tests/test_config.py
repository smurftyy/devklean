"""Tests for devclean configuration loading."""

from __future__ import annotations

from pathlib import Path

from devclean.config import ConfigManager, DEFAULT_TARGETS
from devclean.scanner import scan


def test_config_manager_uses_defaults_when_missing(tmp_path: Path) -> None:
    config_path = tmp_path / "config.toml"
    manager = ConfigManager(config_path=config_path)

    config = manager.load()

    assert config.targets == DEFAULT_TARGETS
    assert config.ignored_paths == ()
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
    assert config.defaults.dry_run is True
    assert config.defaults.interactive is True
    assert config.defaults.path == "~/projects"


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
    manager.apply_defaults(args, ["devclean", "clean", "--dry-run"])

    assert args.dry_run is True
    assert args.interactive is True


def test_scan_honors_excluded_and_custom_targets(tmp_path: Path) -> None:
    root = tmp_path / "project"
    root.mkdir()
    (root / "env").mkdir()
    (root / ".turbo").mkdir()
    (root / "node_modules").mkdir()

    targets = dict(DEFAULT_TARGETS)
    targets.pop("env", None)
    targets[".turbo"] = "Turborepo cache"

    found = scan(str(root), targets=targets)
    names = {item.name for item in found}

    assert "env" not in names
    assert ".turbo" in names
    assert "node_modules" in names


def test_scan_honors_ignored_paths(tmp_path: Path) -> None:
    root = tmp_path / "project"
    root.mkdir()
    preserved = root / "node_modules"
    preserved.mkdir()
    (preserved / "package.json").write_text("{}")

    other = root / "apps" / "web" / "node_modules"
    other.mkdir(parents=True)
    (other / "package.json").write_text("{}")

    found = scan(str(root), ignored_paths=[str(preserved)])
    paths = {item.path for item in found}

    assert str(preserved) not in paths
    assert str(other) in paths
