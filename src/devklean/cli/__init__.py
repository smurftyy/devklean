from __future__ import annotations

from importlib import import_module

__all__ = ["main"]


def __getattr__(name: str):
    if name == "main":
        return import_module("devklean.cli.main").main
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
