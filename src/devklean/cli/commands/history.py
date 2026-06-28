from __future__ import annotations

from devklean.config.models import AppConfig
from devklean.deletion.history import build_history
from devklean.deletion.metadata import MetadataManager
from devklean.output.base import Renderer


def run_history(args, renderer: Renderer, config: AppConfig) -> int:
    """Display previous cleanup operations from the metadata store."""
    snapshot = MetadataManager().load_records()
    operations = build_history(snapshot.records)
    renderer.history(operations, snapshot.invalid_count)
    return 0
