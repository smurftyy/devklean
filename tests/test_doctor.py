"""Tests for the `devklean doctor` integrity repair command."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from argparse import Namespace
from io import StringIO
from pathlib import Path

from devklean.cli.commands.doctor import run_doctor
from devklean.output.console import Console
from devklean.output.text import TextRenderer


def _meta_dir(tmp_path: Path) -> Path:
    return tmp_path / "data" / "devklean" / "deletions"


def _valid(directory: Path, name: str, *, trash_path: str | None) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 4,
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
    _valid(meta, "a", trash_path=None)

    code = run_doctor(_args(), TextRenderer(), None)

    out = capsys.readouterr().out
    assert code == 0
    assert "healthy" in out.lower()


def test_doctor_uses_injected_renderer(tmp_path, monkeypatch) -> None:
    # C3 regression: doctor must write through the injected renderer's stream,
    # not construct its own Console pointed at sys.stdout.
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data"))
    _valid(_meta_dir(tmp_path), "a", trash_path=None)
    stream = StringIO()
    renderer = TextRenderer(console=Console(stream=stream))

    code = run_doctor(_args(), renderer, None)

    assert code == 0
    assert "healthy" in stream.getvalue().lower()


def test_doctor_removes_corrupt_on_confirmation(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data"))
    meta = _meta_dir(tmp_path)
    _corrupt(meta, "bad")
    monkeypatch.setattr("builtins.input", lambda prompt: "y")

    code = run_doctor(_args(), TextRenderer(), None)

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

    code = run_doctor(_args(), TextRenderer(), None)

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

    code = run_doctor(_args(yes=True), TextRenderer(), None)

    assert code == 0
    assert not (meta / "bad.json").exists()


def test_doctor_does_not_flag_records_with_missing_trash(tmp_path, monkeypatch, capsys) -> None:
    # Orphan detection was removed with the move to the native OS trash; a
    # record whose trashed item is gone is no longer reported as a problem.
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data"))
    meta = _meta_dir(tmp_path)
    _valid(meta, "gone", trash_path=str(tmp_path / "trash" / "missing"))

    code = run_doctor(_args(), TextRenderer(), None)

    out = capsys.readouterr().out
    assert code == 0
    assert "healthy" in out.lower()
    assert "ORPHAN" not in out.upper()
    assert (meta / "gone.json").exists()


def test_doctor_accepts_compressed_records(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data"))
    meta = _meta_dir(tmp_path)
    meta.mkdir(parents=True, exist_ok=True)
    (meta / "compressed.json").write_text(
        json.dumps(
            {
                "schema_version": 4,
                "deletion": {
                    "id": "compressed",
                    "run_id": "run1",
                    "timestamp": "2026-06-28T14:00:00+00:00",
                    "strategy": "trash",
                },
                "item": {
                    "original_path": "/tmp/compressed",
                    "display_name": "compressed",
                    "size": 100,
                },
                "archive": {"path": "/tmp/compressed.zip", "format": "zip"},
            }
        ),
        encoding="utf-8",
    )

    code = run_doctor(_args(), TextRenderer(), None)

    out = capsys.readouterr().out
    assert code == 0
    assert "healthy" in out.lower()


def test_doctor_command_end_to_end(tmp_path) -> None:
    meta = _meta_dir(tmp_path)
    _corrupt(meta, "bad")

    env = {**os.environ, "XDG_DATA_HOME": str(tmp_path / "data")}
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
