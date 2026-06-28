from __future__ import annotations

import argparse

from devklean._version import __version__

COMMAND_NAMES = frozenset({"scan", "clean", "stats", "restore", "config", "plugins"})
IMPLEMENTED_COMMANDS = frozenset({"scan", "clean", "restore"})
RESERVED_COMMANDS = frozenset({"stats", "config", "plugins"})
GLOBAL_OPTIONS = frozenset({"-h", "--help", "--version"})


def _add_global_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--version",
        action="version",
        version=f"devklean v{__version__}",
    )


def _add_path_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Root directory to scan (default: current directory)",
    )


def _add_clean_arguments(parser: argparse.ArgumentParser) -> None:
    _add_path_argument(parser)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without deleting anything",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Interactively select items to delete",
    )


def _add_subparsers(parser: argparse.ArgumentParser) -> None:
    subparsers = parser.add_subparsers(dest="command")

    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan for cleanable directories without deleting",
    )
    _add_path_argument(scan_parser)
    scan_parser.add_argument(
        "--json",
        action="store_true",
        help="Output scan results as JSON",
    )

    clean_parser = subparsers.add_parser(
        "clean",
        help="Scan and remove cleanable directories",
    )
    _add_clean_arguments(clean_parser)

    subparsers.add_parser("restore", help="List and restore deleted items")
    subparsers.add_parser("stats", help="Show cleanup statistics (not yet implemented)")
    subparsers.add_parser("config", help="Manage configuration (not yet implemented)")
    subparsers.add_parser("plugins", help="Manage plugins (not yet implemented)")


def legacy_command_for_flags(args: list[str]) -> str:
    """Map legacy root-level flags to the equivalent subcommand."""
    dry_run = "--dry-run" in args
    interactive = "-i" in args or "--interactive" in args
    if dry_run and not interactive:
        return "scan"
    return "clean"


def strip_flags(argv: list[str], flags: set[str]) -> list[str]:
    """Remove specific flags from an argument vector."""
    return [arg for arg in argv if arg not in flags]


def preprocess_argv(argv: list[str]) -> list[str]:
    """Rewrite legacy invocations to explicit subcommands."""
    if len(argv) <= 1:
        return [argv[0], "clean"]

    if argv[1] in GLOBAL_OPTIONS:
        return argv

    if argv[1] in COMMAND_NAMES:
        return argv

    if not argv[1].startswith("-"):
        command = legacy_command_for_flags(argv[2:])
        rewritten = [argv[0], command, argv[1], *argv[2:]]
        if command == "scan":
            return strip_flags(rewritten, {"--dry-run"})
        return rewritten

    command = legacy_command_for_flags(argv[1:])
    rewritten = [argv[0], command, *argv[1:]]
    if command == "scan":
        return strip_flags(rewritten, {"--dry-run"})
    return rewritten


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scan and remove node_modules/venvs to reclaim disk space.",
    )
    _add_global_arguments(parser)
    _add_subparsers(parser)
    return parser
