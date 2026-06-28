from __future__ import annotations

from typing import Callable

from devclean.cli.commands.clean import run_clean
from devclean.output.base import Renderer

CommandHandler = Callable[..., int]

DEFAULT_COMMAND = "clean"

_COMMANDS: dict[str, CommandHandler] = {
    "clean": run_clean,
    # Future: "scan": run_scan,
    # Future: "stats": run_stats,
    # Future: "restore": run_restore,
    # Future: "config": run_config,
}


def dispatch(args, renderer: Renderer) -> int:
    """Route parsed arguments to the appropriate command handler."""
    command = getattr(args, "command", None) or DEFAULT_COMMAND
    handler = _COMMANDS[command]
    return handler(args, renderer)
