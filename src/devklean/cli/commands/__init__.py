from __future__ import annotations

from importlib import import_module

__all__ = ["run_clean", "run_scan"]


def __getattr__(name: str):
    if name == "run_clean":
        return import_module("devklean.cli.commands.clean").run_clean
    if name == "run_scan":
        return import_module("devklean.cli.commands.scan").run_scan
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
