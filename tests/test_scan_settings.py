"""Tests for scan settings and filters."""

from __future__ import annotations

from devklean.config import ScanSettings
from devklean.config.defaults import DEFAULT_TARGETS
from devklean.scanner.filters import dir_is_under_ignored_path, path_is_excluded


def test_scan_settings_defaults_match_builtin_targets() -> None:
    settings = ScanSettings.defaults()

    assert settings.targets == DEFAULT_TARGETS
    assert settings.ignored_paths == frozenset()
    assert settings.ignored_directories == frozenset()


def test_dir_is_under_ignored_path() -> None:
    ignored = {"/tmp/keep"}

    assert dir_is_under_ignored_path("/tmp/keep", ignored)
    assert dir_is_under_ignored_path("/tmp/keep/nested", ignored)
    assert not dir_is_under_ignored_path("/tmp/other", ignored)


def test_path_is_excluded() -> None:
    ignored = {"/tmp/keep/node_modules"}

    assert path_is_excluded("/tmp/keep/node_modules", ignored)
    assert not path_is_excluded("/tmp/other/node_modules", ignored)
