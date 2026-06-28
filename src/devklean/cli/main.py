from __future__ import annotations

import sys

from devklean.cli.dispatcher import dispatch
from devklean.cli.parser import build_parser, preprocess_argv
from devklean.config import ConfigManager
from devklean.output import JsonRenderer, TextRenderer


def select_renderer(args):
    if getattr(args, "command", None) == "scan" and getattr(args, "json", False):
        return JsonRenderer()
    return TextRenderer()


def main() -> None:
    raw_argv = list(sys.argv)
    argv = preprocess_argv(raw_argv)

    config_manager = ConfigManager()
    config = config_manager.load()

    parser = build_parser()
    args = parser.parse_args(argv[1:])
    args._config = config
    config_manager.apply_defaults(args, raw_argv)

    renderer = select_renderer(args)
    exit_code = dispatch(args, renderer, config)

    if exit_code != 0:
        sys.exit(exit_code)
