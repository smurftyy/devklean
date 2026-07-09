"""Tests for Phase 4 config: new keys, project precedence, validation."""

from __future__ import annotations

from pathlib import Path

from devklean.config.manager import ConfigManager


def _global(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "global.toml"
    path.write_text(body.strip(), encoding="utf-8")
    return path


# --- new defaults keys ---


def test_new_default_keys_parsed(tmp_path: Path) -> None:
    cfg_path = _global(
        tmp_path,
        """
[defaults]
default_yes = true
compress = true
theme = "mono"
confirm_threshold = 5368709120
""",
    )
    config = ConfigManager(config_path=cfg_path, project_dir=tmp_path).load()
    assert config.defaults.default_yes is True
    assert config.defaults.compress is True
    assert config.defaults.theme == "mono"
    assert config.defaults.confirm_threshold == 5368709120


def test_default_keys_have_sane_defaults(tmp_path: Path) -> None:
    config = ConfigManager(config_path=tmp_path / "missing.toml", project_dir=tmp_path).load()
    assert config.defaults.default_yes is False
    assert config.defaults.compress is False
    assert config.defaults.theme == "default"
    assert config.defaults.confirm_threshold == 1024**3


def test_top_level_exclude_merges_into_ignored_directories(tmp_path: Path) -> None:
    cfg_path = _global(tmp_path, 'exclude = ["node_modules", ".venv"]')
    config = ConfigManager(config_path=cfg_path, project_dir=tmp_path).load()
    assert "node_modules" in config.ignored_directories
    assert ".venv" in config.ignored_directories


# --- project precedence ---


def test_project_config_overrides_global_scalar(tmp_path: Path) -> None:
    global_path = _global(tmp_path, '[defaults]\ndefault_yes = false\ntheme = "default"')
    project_dir = tmp_path / "proj" / "sub"
    project_dir.mkdir(parents=True)
    (tmp_path / "proj" / ".devklean.toml").write_text(
        '[defaults]\ndefault_yes = true\ntheme = "mono"', encoding="utf-8"
    )

    config = ConfigManager(config_path=global_path, project_dir=project_dir).load()

    assert config.defaults.default_yes is True  # project wins
    assert config.defaults.theme == "mono"


def test_project_and_global_list_keys_union(tmp_path: Path) -> None:
    global_path = _global(tmp_path, 'exclude = ["global_dir"]')
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    (project_dir / ".devklean.toml").write_text('exclude = ["project_dir"]', encoding="utf-8")

    config = ConfigManager(config_path=global_path, project_dir=project_dir).load()

    assert "global_dir" in config.ignored_directories
    assert "project_dir" in config.ignored_directories


def test_no_project_file_uses_global_only(tmp_path: Path) -> None:
    global_path = _global(tmp_path, "[defaults]\ndefault_yes = true")
    empty = tmp_path / "empty"
    empty.mkdir()
    config = ConfigManager(config_path=global_path, project_dir=empty).load()
    assert config.defaults.default_yes is True


# --- validation ---


def test_unknown_top_level_key_warns(tmp_path: Path) -> None:
    cfg_path = _global(tmp_path, 'bogus_key = 1\n[defaults]\ntheme = "default"')
    result = ConfigManager(config_path=cfg_path, project_dir=tmp_path).load_full()
    assert any("bogus_key" in w for w in result.warnings)


def test_unknown_defaults_key_warns(tmp_path: Path) -> None:
    cfg_path = _global(tmp_path, "[defaults]\nnot_a_real_option = true")
    result = ConfigManager(config_path=cfg_path, project_dir=tmp_path).load_full()
    assert any("not_a_real_option" in w for w in result.warnings)


def test_malformed_toml_warns_and_does_not_crash(tmp_path: Path) -> None:
    cfg_path = _global(tmp_path, "this is = = not valid toml [[[")
    result = ConfigManager(config_path=cfg_path, project_dir=tmp_path).load_full()
    assert result.warnings  # at least one warning
    # falls back to defaults rather than crashing
    assert result.config.defaults.theme == "default"


def test_load_still_returns_app_config(tmp_path: Path) -> None:
    config = ConfigManager(config_path=tmp_path / "x.toml", project_dir=tmp_path).load()
    assert hasattr(config, "targets")
