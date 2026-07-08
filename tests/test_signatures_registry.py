"""Golden-output tests for the artifact-signature registry (devklean.signatures)."""

from __future__ import annotations

from pathlib import Path

import pytest

from devklean.config.defaults import DEFAULT_TARGETS
from devklean.signatures import SIGNATURE_REGISTRY, RiskLevel, lookup, match_signature


def test_registry_covers_every_default_target() -> None:
    """Seeded 1:1 from DEFAULT_TARGETS — devklean's actual known artifact list."""
    assert set(SIGNATURE_REGISTRY) == set(DEFAULT_TARGETS)


@pytest.mark.parametrize("dir_name", sorted(SIGNATURE_REGISTRY))
def test_every_entry_has_fixed_fields(dir_name: str) -> None:
    signature = SIGNATURE_REGISTRY[dir_name]
    assert signature.dir_name == dir_name
    assert isinstance(signature.risk, RiskLevel)
    assert 0.0 <= signature.confidence <= 1.0
    assert signature.ecosystem
    assert signature.generated_by
    assert signature.regenerate_command
    assert signature.rationale


# Golden values pin the actual maintainer-assigned data so a change to any of
# them is a deliberate, reviewed edit rather than an accidental drift.
_GOLDEN = {
    "node_modules": ("Node.js (npm/yarn/pnpm)", RiskLevel.LOW, 0.98),
    "venv": ("Python (venv)", RiskLevel.LOW, 0.95),
    ".venv": ("Python (venv)", RiskLevel.LOW, 0.95),
    "env": ("Python (venv, legacy naming)", RiskLevel.MEDIUM, 0.75),
    "__pycache__": ("Python interpreter (CPython bytecode cache)", RiskLevel.LOW, 0.99),
    ".next": ("Next.js", RiskLevel.LOW, 0.95),
    "dist": ("Generic build tooling (bundler/compiler output)", RiskLevel.MEDIUM, 0.7),
    ".cache": ("Generic cache directory", RiskLevel.MEDIUM, 0.65),
}


def test_golden_table_covers_the_whole_registry() -> None:
    assert set(_GOLDEN) == set(SIGNATURE_REGISTRY)


@pytest.mark.parametrize("dir_name", sorted(_GOLDEN))
def test_golden_signature_values(dir_name: str) -> None:
    ecosystem, risk, confidence = _GOLDEN[dir_name]
    signature = lookup(dir_name)
    assert signature is not None
    assert signature.ecosystem == ecosystem
    assert signature.risk == risk
    assert signature.confidence == confidence


@pytest.mark.parametrize("dir_name", sorted(SIGNATURE_REGISTRY))
def test_match_signature_by_directory_fixture(tmp_path: Path, dir_name: str) -> None:
    """Golden-output test per signature: a real fixture directory resolves
    to exactly that signature and nothing else."""
    candidate = tmp_path / dir_name
    candidate.mkdir()

    matched = match_signature(str(candidate))

    assert matched is SIGNATURE_REGISTRY[dir_name]


def test_match_signature_returns_none_for_unrecognized_directory(tmp_path: Path) -> None:
    candidate = tmp_path / "totally_unknown_dir"
    candidate.mkdir()

    assert match_signature(str(candidate)) is None


def test_lookup_returns_none_for_unknown_name() -> None:
    assert lookup("totally_unknown_dir") is None


def test_signature_matches_uses_basename_not_full_path(tmp_path: Path) -> None:
    signature = lookup("node_modules")
    assert signature is not None
    nested = tmp_path / "a" / "b" / "node_modules"
    assert signature.matches(str(nested))
    assert not signature.matches(str(tmp_path / "a" / "node_modules" / "b"))
