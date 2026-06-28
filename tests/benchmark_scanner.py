"""Scanner performance benchmark.

Run manually:

    python -m pytest tests/benchmark_scanner.py -s

Safe to run locally; not enforced in CI (timing varies by machine).
"""

from __future__ import annotations

import time
from pathlib import Path

from devclean.config import ScanSettings
from devclean.scanner import scan


def _build_large_tree(root: Path, *, projects: int = 5, targets_per_project: int = 4) -> None:
    for project_index in range(projects):
        project = root / f"project-{project_index}"
        project.mkdir()
        (project / "src").mkdir()
        (project / "src" / "main.py").write_text("print('ok')\n")

        for target_name in ("node_modules", ".venv", "__pycache__", "dist")[:targets_per_project]:
            target = project / target_name
            target.mkdir()
            for file_index in range(20):
                (target / f"file-{file_index}.bin").write_bytes(b"\x00" * 4096)


def test_benchmark_scan_large_tree(tmp_path: Path) -> None:
    tree = tmp_path / "workspace"
    tree.mkdir()
    _build_large_tree(tree, projects=8, targets_per_project=4)

    settings = ScanSettings.defaults()
    start = time.perf_counter()
    found = scan(str(tree), settings=settings)
    elapsed = time.perf_counter() - start

    assert len(found) == 32
    print(
        f"\n[benchmark] scan found {len(found)} targets in {elapsed:.3f}s "
        f"({elapsed / len(found):.3f}s per target)"
    )
