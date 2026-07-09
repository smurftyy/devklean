"""Tests for `devklean explain`."""

from __future__ import annotations

import re
import subprocess
import sys
from argparse import Namespace
from pathlib import Path

import pytest

from devklean.cli.commands.explain import run_explain
from devklean.output.text import TextRenderer
from devklean.signatures import SIGNATURE_REGISTRY, match_signature


def _args(path: str) -> Namespace:
    return Namespace(path=path)


@pytest.mark.parametrize("dir_name", sorted(SIGNATURE_REGISTRY))
def test_explain_golden_output_per_signature(tmp_path: Path, capsys, dir_name: str) -> None:
    """Golden-output test: every field printed is the matched signature's own,
    verbatim — nothing generated freeform."""
    candidate = tmp_path / dir_name
    candidate.mkdir()
    signature = SIGNATURE_REGISTRY[dir_name]

    code = run_explain(_args(str(candidate)), TextRenderer(), None)

    out = capsys.readouterr().out
    assert code == 0
    assert signature.ecosystem in out
    assert signature.generated_by in out
    assert signature.regenerate_command in out
    assert signature.risk.value in out
    assert f"{signature.confidence:.2f}" in out
    assert signature.rationale in out


def test_explain_unrecognized_path_gives_no_verdict(tmp_path: Path, capsys) -> None:
    mystery = tmp_path / "mystery_dir"
    mystery.mkdir()

    code = run_explain(_args(str(mystery)), TextRenderer(), None)

    out = capsys.readouterr().out
    assert code == 0
    assert "not recognized" in out.lower()

    # Hard constraint: an unrecognized path must never receive a fabricated
    # risk or confidence value. Check for the risk-level words and a
    # confidence-shaped number as whole tokens, since tmp_path itself
    # legitimately contains digits (e.g. pytest's tmp dir numbering).
    assert re.search(r"\b(low|medium|high)\b", out, re.IGNORECASE) is None
    assert re.search(r"\b0\.\d{2}\b", out) is None


def test_explain_invalid_directory_returns_error(tmp_path: Path, capsys) -> None:
    code = run_explain(_args(str(tmp_path / "does-not-exist")), TextRenderer(), None)

    out = capsys.readouterr().out
    assert code == 1
    assert "not a directory" in out


def test_explain_unrecognized_path_matches_no_registry_entry(tmp_path: Path) -> None:
    mystery = tmp_path / "mystery_dir"
    mystery.mkdir()

    assert match_signature(str(mystery)) is None


def test_explain_command_end_to_end(tmp_path: Path) -> None:
    node_modules = tmp_path / "node_modules"
    node_modules.mkdir()

    result = subprocess.run(
        [sys.executable, "-m", "devklean", "explain", str(node_modules)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Node.js" in result.stdout
    assert "risk:" in result.stdout
    assert "confidence:" in result.stdout


def test_explain_requires_path_argument() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "devklean", "explain"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
