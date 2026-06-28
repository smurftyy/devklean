"""Large-deletion typed confirmation.

This is a *batch-magnitude* gate, deliberately separate from the per-path
``SafetyValidator``. The validator answers "is this path safe to delete?"; this
answers "is this batch large enough to demand an explicit, typed confirmation?".
The two concerns do not share logic.

The gate is NOT bypassed by ``default_yes``/``--yes`` — only dry-run skips it —
because allowing config to defeat the large-deletion guard would defeat its
purpose.
"""

from __future__ import annotations

import sys
from typing import Callable, TextIO

from devklean.config.models import DEFAULT_CONFIRM_THRESHOLD
from devklean.formatting import format_size
from devklean.output.console import Console

# Re-export the single source of truth (config.models) under the name the
# confirmation flow uses.
DEFAULT_LARGE_THRESHOLD = DEFAULT_CONFIRM_THRESHOLD

_CONFIRM_WORD = "DELETE"


def exceeds_threshold(total_size: int, threshold: int) -> bool:
    """True when a deletion is large enough to require typed confirmation."""
    return threshold > 0 and total_size >= threshold


def confirm_large_deletion(
    count: int,
    total_size: int,
    threshold: int,
    *,
    input_fn: Callable[[str], str] | None = None,
    stream: TextIO | None = None,
) -> bool:
    """Prompt for an explicit typed confirmation; return True only on 'DELETE'."""
    # Resolve at call time so a monkeypatched builtins.input is honored.
    ask = input_fn if input_fn is not None else input
    out = stream if stream is not None else sys.stderr
    console = Console(stream=out)
    word = "directory" if count == 1 else "directories"
    console.warning(f"About to delete {count} {word} (~{format_size(total_size)}).")
    console.detail(f"This exceeds the {format_size(threshold)} safety threshold.")
    answer = ask(f"Type {_CONFIRM_WORD} to confirm: ")
    return answer.strip() == _CONFIRM_WORD
