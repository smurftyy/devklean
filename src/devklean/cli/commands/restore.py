from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devklean.output.text import TextRenderer


def run_restore(args, renderer: TextRenderer, config) -> int:
    """Explain how to recover deleted items from the native OS trash.

    devklean moves items to the operating system's own trash rather than
    deleting them, and the OS owns that trash — devklean cannot move items back
    programmatically. Recovery is done through the file manager's trash UI.

    Text-only by design (human guidance), so it is always given a
    ``TextRenderer`` and never runs in JSON mode.
    """
    renderer.restore_help()
    return 0
