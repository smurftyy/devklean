from __future__ import annotations

import argparse


def _add_global_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--version",
        action="version",
        version="devclean v1.1.0",
    )


def _add_clean_arguments(parser: argparse.ArgumentParser) -> None:
    """Arguments for the clean command (currently attached to the root parser)."""
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Root directory to scan (default: current directory)",
    )
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


def _add_subparsers(_parser: argparse.ArgumentParser) -> None:
    """Register subcommand parsers when commands are introduced.

    Future commands (scan, clean, stats, restore, config) will register here.
    Clean arguments currently live on the root parser; they will move to a
    ``clean`` subparser when subcommands are exposed.
    """
    # Not yet active — adding subparsers now would change --help and break
    # existing invocations like ``devclean [path] [--dry-run]``.
    pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scan and remove node_modules/venvs to reclaim disk space.",
    )
    _add_global_arguments(parser)

    # Until subcommands are exposed, attach clean arguments to the root parser
    # so existing invocations (devclean [path] [--dry-run] [-i]) keep working.
    _add_clean_arguments(parser)

    _add_subparsers(parser)

    return parser
