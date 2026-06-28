"""Tests for legacy CLI argument preprocessing."""

from __future__ import annotations

from devklean.cli.parser import legacy_command_for_flags, preprocess_argv


def test_preprocess_bare_invocation() -> None:
    assert preprocess_argv(["devklean"]) == ["devklean", "clean"]


def test_preprocess_legacy_dry_run() -> None:
    assert preprocess_argv(["devklean", "--dry-run"]) == ["devklean", "scan"]
    assert preprocess_argv(["devklean", "--dry-run", "."]) == ["devklean", "scan", "."]


def test_preprocess_legacy_path_first_dry_run() -> None:
    assert preprocess_argv(["devklean", "/tmp/code", "--dry-run"]) == [
        "devklean",
        "scan",
        "/tmp/code",
    ]


def test_preprocess_legacy_clean_default() -> None:
    assert preprocess_argv(["devklean", "."]) == ["devklean", "clean", "."]
    assert preprocess_argv(["devklean", "-i"]) == ["devklean", "clean", "-i"]


def test_preprocess_legacy_interactive_dry_run_stays_clean() -> None:
    assert preprocess_argv(["devklean", "--dry-run", "-i"]) == [
        "devklean",
        "clean",
        "--dry-run",
        "-i",
    ]


def test_preprocess_explicit_subcommand_unchanged() -> None:
    assert preprocess_argv(["devklean", "scan", "."]) == ["devklean", "scan", "."]
    assert preprocess_argv(["devklean", "clean", "--dry-run"]) == [
        "devklean",
        "clean",
        "--dry-run",
    ]


def test_preprocess_global_options_unchanged() -> None:
    assert preprocess_argv(["devklean", "--help"]) == ["devklean", "--help"]
    assert preprocess_argv(["devklean", "--version"]) == ["devklean", "--version"]


def test_legacy_command_for_flags() -> None:
    assert legacy_command_for_flags(["--dry-run"]) == "scan"
    assert legacy_command_for_flags(["--dry-run", "."]) == "scan"
    assert legacy_command_for_flags(["--dry-run", "-i"]) == "clean"
    assert legacy_command_for_flags(["-i"]) == "clean"
