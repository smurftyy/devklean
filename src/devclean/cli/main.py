from __future__ import annotations

import sys

from devclean.cli.dispatcher import dispatch
from devclean.cli.parser import build_parser, preprocess_argv
from devclean.config import ConfigManager
from devclean.output import TextRenderer


def main() -> None:
    raw_argv = list(sys.argv)
    argv = preprocess_argv(raw_argv)

    config_manager = ConfigManager()
    config = config_manager.load()

    parser = build_parser()
    args = parser.parse_args(argv[1:])
    args._config = config
    config_manager.apply_defaults(args, raw_argv)

    renderer = TextRenderer()
    exit_code = dispatch(args, renderer, config)

    if exit_code != 0:
        sys.exit(exit_code)
