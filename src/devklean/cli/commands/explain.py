from __future__ import annotations

import os
from typing import TYPE_CHECKING

from devklean.signatures import match_signature

if TYPE_CHECKING:
    from devklean.output.text import TextRenderer


def run_explain(args, renderer: TextRenderer, config) -> int:
    """Resolve a path against the artifact-signature registry and explain it.

    Every field printed on a match comes straight from the matched
    ``ArtifactSignature`` — nothing here is generated freeform. On no match,
    no risk/confidence verdict is given at all; guessing about an unrecognized
    path is a hard constraint, not a style choice.

    Text-only by design, like ``doctor``/``restore``: this is a direct lookup
    report, not a scannable result set, so it never needs the JSON scan/history
    payload shape.
    """
    path = os.path.abspath(args.path)
    signature = match_signature(path)

    if signature is None:
        renderer.explain_no_match(path)
        return 0

    renderer.explain_match(path, signature)
    return 0
