from __future__ import annotations

from typing import TYPE_CHECKING

from devklean.deletion.integrity import check_integrity
from devklean.deletion.metadata import MetadataManager

if TYPE_CHECKING:
    from devklean.output.text import TextRenderer


def run_doctor(args, renderer: TextRenderer, config) -> int:
    """Inspect the metadata store and remove confirmed-corrupt records.

    Text-only by design: the command is interactive (it prompts before
    deleting), so it is always given a ``TextRenderer`` and never runs in JSON
    mode.
    """
    manager = MetadataManager()
    report = check_integrity(manager)

    if report.healthy:
        renderer.doctor_healthy()
        return 0

    renderer.doctor_corruption_report(report)

    if not getattr(args, "yes", False):
        confirm = input(renderer.doctor_confirm_prompt(len(report.corrupt))).strip().lower()
        if confirm != "y":
            renderer.doctor_kept()
            return 0

    removed = 0
    for entry in report.corrupt:
        try:
            manager.remove_record(entry)
            removed += 1
        except OSError as exc:
            renderer.doctor_remove_error(entry.path.name, str(exc))

    renderer.doctor_removed(removed)
    return 0
