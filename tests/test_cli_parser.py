"""Tests for bare-invocation CLI argument resolution (default-command shorthand)."""

from __future__ import annotations

from devklean.cli.parser import default_command_for_flags, resolve_bare_invocation


def test_bare_invocation_defaults_to_clean() -> None:
    assert resolve_bare_invocation(["devklean"]) == ["devklean", "clean"]


def test_bare_dry_run_maps_to_scan() -> None:
    assert resolve_bare_invocation(["devklean", "--dry-run"]) == ["devklean", "scan"]
    assert resolve_bare_invocation(["devklean", "--dry-run", "."]) == ["devklean", "scan", "."]


def test_bare_path_then_dry_run_maps_to_scan() -> None:
    assert resolve_bare_invocation(["devklean", "/tmp/code", "--dry-run"]) == [
        "devklean",
        "scan",
        "/tmp/code",
    ]


def test_bare_path_or_interactive_defaults_to_clean() -> None:
    assert resolve_bare_invocation(["devklean", "."]) == ["devklean", "clean", "."]
    assert resolve_bare_invocation(["devklean", "-i"]) == ["devklean", "clean", "-i"]


def test_bare_dry_run_with_interactive_stays_clean() -> None:
    assert resolve_bare_invocation(["devklean", "--dry-run", "-i"]) == [
        "devklean",
        "clean",
        "--dry-run",
        "-i",
    ]


def test_explicit_subcommand_unchanged() -> None:
    assert resolve_bare_invocation(["devklean", "scan", "."]) == ["devklean", "scan", "."]
    assert resolve_bare_invocation(["devklean", "clean", "--dry-run"]) == [
        "devklean",
        "clean",
        "--dry-run",
    ]


def test_global_options_unchanged() -> None:
    assert resolve_bare_invocation(["devklean", "--help"]) == ["devklean", "--help"]
    assert resolve_bare_invocation(["devklean", "--version"]) == ["devklean", "--version"]


def test_default_command_for_flags() -> None:
    assert default_command_for_flags(["--dry-run"]) == "scan"
    assert default_command_for_flags(["--dry-run", "."]) == "scan"
    assert default_command_for_flags(["--dry-run", "-i"]) == "clean"
    assert default_command_for_flags(["-i"]) == "clean"
