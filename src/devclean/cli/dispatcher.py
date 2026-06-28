from __future__ import annotations

import sys
from typing import Callable

from devclean.cli.commands.clean import run_clean
from devclean.cli.commands.scan import run_scan
from devclean.cli.parser import IMPLEMENTED_COMMANDS, RESERVED_COMMANDS
from devclean.config.models import AppConfig
from devclean.output.base import Renderer

CommandHandler = Callable[..., int]

DEFAULT_COMMAND = "clean"

_COMMANDS: dict[str, CommandHandler] = {
    "scan": run_scan,
    "clean": run_clean,
}


def dispatch(args, renderer: Renderer, config: AppConfig) -> int:
    """Route parsed arguments to the appropriate command handler."""
    command = getattr(args, "command", None) or DEFAULT_COMMAND

    if command in RESERVED_COMMANDS:
        print(f"devclean {command}: not yet implemented", file=sys.stderr)
        return 2

    if command not in IMPLEMENTED_COMMANDS:
        print(f"devclean: unknown command {command!r}", file=sys.stderr)
        return 2

    handler = _COMMANDS[command]
    return handler(args, renderer, config)
