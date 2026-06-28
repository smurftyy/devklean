from __future__ import annotations

import sys

from devklean.output.console import Console


def run_restore(args, renderer, config) -> int:
    """Explain how to recover deleted items from the native OS trash.

    devklean moves items to the operating system's own trash rather than
    deleting them, and the OS owns that trash — devklean cannot move items back
    programmatically. Recovery is done through the file manager's trash UI.
    """
    console = Console(stream=sys.stdout)
    console.info(
        "devklean moves deleted items to your system trash, not to a devklean-owned store."
    )
    console.plain()
    console.detail("To recover something you deleted:")
    console.detail("  • Windows — open the Recycle Bin and restore the item.")
    console.detail("  • macOS   — open Trash in Finder and 'Put Back'.")
    console.detail("  • Linux   — open Trash in your file manager and restore.")
    console.plain()
    console.detail("Run `devklean history` to see what was removed and when.")
    return 0
