from __future__ import annotations

from importlib import import_module

__all__ = ["JsonRenderer", "Renderer", "TextRenderer"]


def __getattr__(name: str):
    if name == "Renderer":
        return import_module("devklean.output.base").Renderer
    if name == "JsonRenderer":
        return import_module("devklean.output.json").JsonRenderer
    if name == "TextRenderer":
        return import_module("devklean.output.text").TextRenderer
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
