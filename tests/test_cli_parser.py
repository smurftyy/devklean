"""Tests for legacy CLI argument preprocessing."""

from __future__ import annotations

from devclean.cli.parser import legacy_command_for_flags, preprocess_argv


def test_preprocess_bare_invocation() -> None:
    assert preprocess_argv(["devclean"]) == ["devclean", "clean"]


def test_preprocess_legacy_dry_run() -> None:
    assert preprocess_argv(["devclean", "--dry-run"]) == ["devclean", "scan"]
    assert preprocess_argv(["devclean", "--dry-run", "."]) == ["devclean", "scan", "."]


def test_preprocess_legacy_path_first_dry_run() -> None:
    assert preprocess_argv(["devclean", "/tmp/code", "--dry-run"]) == [
        "devclean",
        "scan",
        "/tmp/code",
    ]


def test_preprocess_legacy_clean_default() -> None:
    assert preprocess_argv(["devclean", "."]) == ["devclean", "clean", "."]
    assert preprocess_argv(["devclean", "-i"]) == ["devclean", "clean", "-i"]


def test_preprocess_legacy_interactive_dry_run_stays_clean() -> None:
    assert preprocess_argv(["devclean", "--dry-run", "-i"]) == [
        "devclean",
        "clean",
        "--dry-run",
        "-i",
    ]


def test_preprocess_explicit_subcommand_unchanged() -> None:
    assert preprocess_argv(["devclean", "scan", "."]) == ["devclean", "scan", "."]
    assert preprocess_argv(["devclean", "clean", "--dry-run"]) == [
        "devclean",
        "clean",
        "--dry-run",
    ]


def test_preprocess_global_options_unchanged() -> None:
    assert preprocess_argv(["devclean", "--help"]) == ["devclean", "--help"]
    assert preprocess_argv(["devclean", "--version"]) == ["devclean", "--version"]


def test_legacy_command_for_flags() -> None:
    assert legacy_command_for_flags(["--dry-run"]) == "scan"
    assert legacy_command_for_flags(["--dry-run", "."]) == "scan"
    assert legacy_command_for_flags(["--dry-run", "-i"]) == "clean"
    assert legacy_command_for_flags(["-i"]) == "clean"
