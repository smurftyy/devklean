from __future__ import annotations

import argparse

from devklean._version import __version__

COMMAND_NAMES = frozenset(
    {"scan", "clean", "history", "doctor", "stats", "restore", "config", "plugins"}
)
IMPLEMENTED_COMMANDS = frozenset({"scan", "clean", "history", "doctor", "restore"})
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
        "--compress",
        action="store_true",
        help="Compress eligible directories into zip archives before trashing them",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Interactively select items to delete (Linux/macOS only)",
    )
    parser.add_argument(
        "--allow-symlinks",
        action="store_true",
        help="Permit deletion of symbolic links (blocked by default)",
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Skip the confirmation prompt (large deletions still require typing DELETE)",
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

    subparsers.add_parser(
        "restore", help="Show how to recover deleted items from your system trash"
    )

    history_parser = subparsers.add_parser(
        "history",
        help="Show previous cleanup operations",
    )
    history_parser.add_argument(
        "--json",
        action="store_true",
        help="Output history as JSON",
    )

    doctor_parser = subparsers.add_parser(
        "doctor",
        help="Inspect and repair the deletion metadata store",
    )
    doctor_parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Remove corrupt records without confirmation",
    )

    subparsers.add_parser("stats", help="Show cleanup statistics (not yet implemented)")
    subparsers.add_parser("config", help="Manage configuration (not yet implemented)")
    subparsers.add_parser("plugins", help="Manage plugins (not yet implemented)")


def default_command_for_flags(args: list[str]) -> str:
    """Pick the default subcommand for a bare top-level invocation.

    With no explicit command, a bare ``--dry-run`` (without ``-i``) is a preview,
    so it maps to ``scan``; everything else defaults to ``clean``.
    """
    dry_run = "--dry-run" in args
    interactive = "-i" in args or "--interactive" in args
    if dry_run and not interactive:
        return "scan"
    return "clean"


def strip_flags(argv: list[str], flags: set[str]) -> list[str]:
    """Remove specific flags from an argument vector."""
    return [arg for arg in argv if arg not in flags]


def resolve_bare_invocation(argv: list[str]) -> list[str]:
    """Resolve a bare invocation (no explicit subcommand) to one.

    devklean accepts a default-command shorthand: ``devklean`` alone, or with a
    path/flags but no command word, runs ``clean`` (e.g. ``devklean ~/code`` ==
    ``devklean clean ~/code``); a bare ``--dry-run`` is treated as ``scan``.
    Explicit subcommands and global options (``--help``/``--version``) pass
    through unchanged.
    """
    if len(argv) <= 1:
        return [argv[0], "clean"]

    if argv[1] in GLOBAL_OPTIONS:
        return argv

    if argv[1] in COMMAND_NAMES:
        return argv

    if not argv[1].startswith("-"):
        command = default_command_for_flags(argv[2:])
        rewritten = [argv[0], command, argv[1], *argv[2:]]
        if command == "scan":
            return strip_flags(rewritten, {"--dry-run", "--allow-symlinks"})
        return rewritten

    command = default_command_for_flags(argv[1:])
    rewritten = [argv[0], command, *argv[1:]]
    if command == "scan":
        return strip_flags(rewritten, {"--dry-run", "--allow-symlinks"})
    return rewritten


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scan and remove node_modules/venvs to reclaim disk space.",
    )
    _add_global_arguments(parser)
    _add_subparsers(parser)
    return parser
