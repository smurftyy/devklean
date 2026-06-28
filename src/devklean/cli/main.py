from __future__ import annotations

import sys

from devklean.cli.dispatcher import dispatch
from devklean.cli.parser import build_parser, resolve_bare_invocation
from devklean.config import ConfigManager
from devklean.logging_setup import configure_logging, log_invocation
from devklean.output import JsonRenderer, TextRenderer
from devklean.output.console import Console


def select_renderer(args, config=None):
    theme = "default"
    if config is not None:
        theme = getattr(config.defaults, "theme", "default")
    if getattr(args, "command", None) in {"scan", "history"} and getattr(args, "json", False):
        return JsonRenderer()
    return TextRenderer(console=Console(stream=sys.stdout, theme=theme))


def main() -> None:
    # Force UTF-8 on the console before anything writes output. Windows' default
    # console codepage can't encode the Unicode symbols (⚠/✓/✗) the renderers
    # emit, so a stock cmd.exe/PowerShell session would crash with
    # UnicodeEncodeError. errors="replace" degrades any future unencodable
    # character to a placeholder rather than crashing.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    raw_argv = list(sys.argv)
    argv = resolve_bare_invocation(raw_argv)

    configure_logging()

    config_manager = ConfigManager()
    result = config_manager.load_full()
    config = result.config

    parser = build_parser()
    args = parser.parse_args(argv[1:])
    args._config = config
    config_manager.apply_defaults(args, raw_argv)

    log_invocation(raw_argv, getattr(args, "command", None))

    # Surface config warnings on stderr so stdout/JSON stay clean.
    if result.warnings:
        warn_console = Console(
            stream=sys.stderr, theme=getattr(config.defaults, "theme", "default")
        )
        for warning in result.warnings:
            warn_console.warning(warning)

    renderer = select_renderer(args, config)
    exit_code = dispatch(args, renderer, config)

    if exit_code != 0:
        sys.exit(exit_code)
