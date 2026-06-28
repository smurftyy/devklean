from __future__ import annotations

import sys

from devclean.cli.dispatcher import dispatch
from devclean.cli.parser import build_parser
from devclean.output import TextRenderer


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    renderer = TextRenderer()
    exit_code = dispatch(args, renderer)

    if exit_code != 0:
        sys.exit(exit_code)
