"""Tests for the restore command's graceful degradation."""

from __future__ import annotations

import json
from pathlib import Path

from devklean.cli.commands.restore import run_restore


def _meta_dir(tmp_path: Path) -> Path:
    return tmp_path / "data" / "devklean" / "deletions"


def _valid(directory: Path, name: str, trash_path: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 3,
        "deletion": {
            "id": name,
            "run_id": "run1",
            "timestamp": "2026-06-28T14:00:00+00:00",
            "strategy": "trash",
        },
        "item": {"original_path": f"/tmp/{name}", "display_name": name, "size": 100},
        "trash": {"path": str(trash_path)},
    }
    (directory / f"{name}.json").write_text(json.dumps(payload), encoding="utf-8")


def test_restore_degrades_gracefully_and_warns_about_corrupt(
    tmp_path, monkeypatch, capsys
) -> None:
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data"))
    meta = _meta_dir(tmp_path)
    trash = tmp_path / "trash" / "node_modules"
    trash.mkdir(parents=True)
    _valid(meta, "a", trash)
    (meta / "bad.json").write_text("{ broken", encoding="utf-8")

    # cancel at the selection prompt
    monkeypatch.setattr("builtins.input", lambda prompt: "")

    code = run_restore(object(), None, None)

    out = capsys.readouterr().out
    assert code == 0
    # the valid entry is still listed (recovered what it could)
    assert "a" in out
    # and the corruption is surfaced with a pointer to doctor
    assert "corrupt" in out
    assert "doctor" in out
