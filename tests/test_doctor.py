"""Tests for the `devclean doctor` integrity repair command."""

from __future__ import annotations

import json
import subprocess
import sys
from argparse import Namespace
from pathlib import Path

from devklean.cli.commands.doctor import run_doctor


def _meta_dir(tmp_path: Path) -> Path:
    return tmp_path / "data" / "devklean" / "deletions"


def _valid(directory: Path, name: str, *, trash_path: str | None) -> None:
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
    }
    if trash_path is not None:
        payload["trash"] = {"path": trash_path}
    (directory / f"{name}.json").write_text(json.dumps(payload), encoding="utf-8")


def _corrupt(directory: Path, name: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f"{name}.json").write_text("{ not json", encoding="utf-8")


def _args(**kwargs) -> Namespace:
    return Namespace(yes=kwargs.get("yes", False))


def test_doctor_healthy_store(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data"))
    meta = _meta_dir(tmp_path)
    trash = tmp_path / "trash" / "node_modules"
    trash.mkdir(parents=True)
    _valid(meta, "a", trash_path=str(trash))

    code = run_doctor(_args(), None, None)

    out = capsys.readouterr().out
    assert code == 0
    assert "healthy" in out.lower()


def test_doctor_removes_corrupt_on_confirmation(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data"))
    meta = _meta_dir(tmp_path)
    _corrupt(meta, "bad")
    monkeypatch.setattr("builtins.input", lambda prompt: "y")

    code = run_doctor(_args(), None, None)

    out = capsys.readouterr().out
    assert code == 0
    assert not (meta / "bad.json").exists()
    assert "malformed JSON" in out
    assert "Removed" in out


def test_doctor_keeps_corrupt_when_declined(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data"))
    meta = _meta_dir(tmp_path)
    _corrupt(meta, "bad")
    monkeypatch.setattr("builtins.input", lambda prompt: "n")

    code = run_doctor(_args(), None, None)

    out = capsys.readouterr().out
    assert code == 0
    assert (meta / "bad.json").exists()
    assert "Kept" in out or "kept" in out


def test_doctor_yes_flag_skips_prompt(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data"))
    meta = _meta_dir(tmp_path)
    _corrupt(meta, "bad")

    def fail_input(prompt):
        raise AssertionError("should not prompt with --yes")

    monkeypatch.setattr("builtins.input", fail_input)

    code = run_doctor(_args(yes=True), None, None)

    assert code == 0
    assert not (meta / "bad.json").exists()


def test_doctor_reports_orphaned_but_keeps_them(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data"))
    meta = _meta_dir(tmp_path)
    _valid(meta, "gone", trash_path=str(tmp_path / "trash" / "missing"))
    monkeypatch.setattr("builtins.input", lambda prompt: "y")

    code = run_doctor(_args(), None, None)

    out = capsys.readouterr().out
    assert code == 0
    # orphaned record is reported...
    assert "ORPHAN" in out.upper()
    # ...but never removed by doctor
    assert (meta / "gone.json").exists()


def test_doctor_lists_corrupt_and_orphaned_separately(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data"))
    meta = _meta_dir(tmp_path)
    _corrupt(meta, "bad")
    _valid(meta, "gone", trash_path=str(tmp_path / "trash" / "missing"))
    monkeypatch.setattr("builtins.input", lambda prompt: "n")

    code = run_doctor(_args(), None, None)

    out = capsys.readouterr().out.upper()
    assert code == 0
    assert "CORRUPT" in out
    assert "ORPHAN" in out


def test_doctor_command_end_to_end(tmp_path) -> None:
    meta = _meta_dir(tmp_path)
    _corrupt(meta, "bad")

    env = {"XDG_DATA_HOME": str(tmp_path / "data"), "PATH": "/usr/bin:/bin"}
    result = subprocess.run(
        [sys.executable, "-m", "devklean", "doctor", "--yes"],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )

    assert result.returncode == 0
    assert "Removed" in result.stdout
    assert not (meta / "bad.json").exists()
