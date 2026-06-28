from __future__ import annotations

import sys

from devclean.cli.dispatcher import dispatch
from devclean.cli.parser import build_parser, preprocess_argv
from devclean.output import TextRenderer


def main() -> None:
    argv = preprocess_argv(sys.argv)
    parser = build_parser()
    args = parser.parse_args(argv[1:])

    renderer = TextRenderer()
    exit_code = dispatch(args, renderer)

    if exit_code != 0:
        sys.exit(exit_code)
