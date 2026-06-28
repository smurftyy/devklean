from __future__ import annotations

import sys
from typing import Callable

from devklean.cli.commands.clean import run_clean
from devklean.cli.commands.doctor import run_doctor
from devklean.cli.commands.history import run_history
from devklean.cli.commands.restore import run_restore
from devklean.cli.commands.scan import run_scan
from devklean.cli.parser import IMPLEMENTED_COMMANDS, RESERVED_COMMANDS
from devklean.config.models import AppConfig
from devklean.deletion import SafetyValidator
from devklean.output.base import Renderer

CommandHandler = Callable[..., int]

DEFAULT_COMMAND = "clean"

_COMMANDS: dict[str, CommandHandler] = {
    "scan": run_scan,
    "clean": run_clean,
    "history": run_history,
    "doctor": run_doctor,
    "restore": run_restore,
}


def dispatch(args, renderer: Renderer, config: AppConfig) -> int:
    """Route parsed arguments to the appropriate command handler."""
    command = getattr(args, "command", None) or DEFAULT_COMMAND

    if command in RESERVED_COMMANDS:
        print(f"devklean {command}: not yet implemented", file=sys.stderr)
        return 2

    if command not in IMPLEMENTED_COMMANDS:
        print(f"devklean: unknown command {command!r}", file=sys.stderr)
        return 2

    handler = _COMMANDS[command]
    if command == "clean":
        allow_symlinks = getattr(args, "allow_symlinks", False)
        return handler(args, renderer, config, SafetyValidator(allow_symlinks=allow_symlinks))
    return handler(args, renderer, config)
