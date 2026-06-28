"""Target merge logic for configuration."""

from __future__ import annotations

from devclean.config.defaults import DEFAULT_TARGETS


def merge_targets(
    *,
    exclude: list[str] | tuple[str, ...] = (),
    custom: dict[str, str] | None = None,
) -> dict[str, str]:
    """Merge built-in defaults with user exclusions and custom targets."""
    merged = dict(DEFAULT_TARGETS)

    for name in exclude:
        merged.pop(name, None)

    if custom:
        for name, label in custom.items():
            merged[str(name)] = str(label)

    return merged
