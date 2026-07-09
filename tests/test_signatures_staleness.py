"""Tests for devklean.signatures.staleness.

Staleness must never come from the artifact directory's own mtime/atime — it
is always derived from the parent project (git last-commit date, or the
newest mtime among the project's own non-artifact files), and must say so
explicitly when neither signal is available.
"""

from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path

from devklean.signatures.staleness import estimate_staleness


def _git(*args: str, cwd: Path) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


def test_staleness_uses_git_last_commit_when_available(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    _git("init", "-q", cwd=project)
    _git("config", "user.email", "a@example.com", cwd=project)
    _git("config", "user.name", "a", cwd=project)
    (project / "main.py").write_text("print('hi')")
    _git("add", "-A", cwd=project)
    _git("commit", "-q", "-m", "init", cwd=project)

    result = estimate_staleness(str(project))

    assert result.known is True
    assert result.source == "git"
    assert result.days_since is not None
    assert result.days_since >= 0
    assert "git commit" in result.detail


def test_staleness_falls_back_to_source_mtime_without_git(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    (project / "main.py").write_text("print('hi')")
    node_modules = project / "node_modules"
    node_modules.mkdir()
    # Touch the artifact dir's own file *after* the source file, to prove the
    # signal comes from source files, not the artifact directory.
    time.sleep(0.01)
    (node_modules / "pkg.json").write_text("{}")

    result = estimate_staleness(str(project))

    assert result.known is True
    assert result.source == "source-mtime"
    assert result.days_since is not None
    assert "source-file change" in result.detail


def test_staleness_ignores_known_artifact_directories_for_mtime(tmp_path: Path) -> None:
    """The artifact directory's own files must never set the mtime signal."""
    project = tmp_path / "project"
    project.mkdir()
    old_source = project / "main.py"
    old_source.write_text("print('hi')")
    old_time = time.time() - 1_000_000
    os.utime(old_source, (old_time, old_time))

    node_modules = project / "node_modules"
    node_modules.mkdir()
    (node_modules / "pkg.json").write_text("{}")  # freshly written, i.e. "now"

    result = estimate_staleness(str(project))

    assert result.known is True
    assert result.source == "source-mtime"
    # If node_modules' fresh file had counted, days_since would be ~0.
    assert result.days_since is not None
    assert result.days_since > 10


def test_staleness_reports_no_reliable_signal_without_git_or_source_files(
    tmp_path: Path,
) -> None:
    """No git repo, and the only file present lives inside a known artifact
    directory — so there is nothing left to derive a signal from."""
    project = tmp_path / "project"
    project.mkdir()
    node_modules = project / "node_modules"
    node_modules.mkdir()
    (node_modules / "pkg.json").write_text("{}")

    result = estimate_staleness(str(project))

    assert result.known is False
    assert result.source is None
    assert result.last_activity is None
    assert result.days_since is None
    assert "no reliable signal" in result.detail
    assert "no git repository" in result.detail
    assert "no source files found" in result.detail
