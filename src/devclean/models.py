from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CleanableItem:
    """A discovered directory that devclean can remove."""

    path: str
    name: str
    size: int
    display_label: str
