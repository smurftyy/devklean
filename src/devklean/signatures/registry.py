"""Static, deterministic registry of known development-artifact signatures.

This is the single source of truth ``devklean explain`` and ``devklean
analyze`` read from. Every field on every entry is fixed data written by a
maintainer — there is no model call, heuristic scoring pass, or runtime
inference anywhere in this file. ``risk`` and ``confidence`` are looked up
verbatim for a matched entry; an unmatched path gets no entry and therefore
no verdict, by construction (``lookup``/``match_signature`` return ``None``
rather than fabricating one).

Matching reuses the exact signal ``scan_tree`` (``devklean.scanner.scanner``)
already uses to find cleanable directories: the directory's basename against
a fixed set of known names (``devklean.config.defaults.DEFAULT_TARGETS``).
This module does not walk the filesystem itself.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum


class RiskLevel(Enum):
    """Fixed risk tier for deleting a matched artifact directory."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    @property
    def weight(self) -> float:
        """Fixed reclaim-safety weight used only by the workspace-health formula.

        Not a probability and not derived from the ``confidence`` score — a
        separate, hand-assigned constant so the health formula (see
        ``devklean.signatures.health``) stays traceable to this table.
        """
        return _RISK_WEIGHTS[self]


_RISK_WEIGHTS: dict[RiskLevel, float] = {
    RiskLevel.LOW: 1.0,
    RiskLevel.MEDIUM: 0.6,
    RiskLevel.HIGH: 0.2,
}


@dataclass(frozen=True)
class ArtifactSignature:
    """A fixed description of one artifact-directory type.

    ``confidence`` is a fixed fraction (0.0-1.0) reflecting how unambiguous
    ``dir_name`` is as a signal on its own — e.g. ``__pycache__`` is a
    reserved CPython name (very high confidence); ``.cache`` is reused by
    many unrelated tools (lower confidence). It is maintainer-assigned, not
    computed.
    """

    dir_name: str
    ecosystem: str
    generated_by: str
    regenerate_command: str
    risk: RiskLevel
    confidence: float
    rationale: str

    def matches(self, path: str) -> bool:
        """True if ``path``'s basename is this signature's directory name."""
        return os.path.basename(os.path.normpath(path)) == self.dir_name


# Seeded 1:1 from devklean.config.defaults.DEFAULT_TARGETS — the directory
# names devklean's scanner already treats as cleanable. A built-in target
# without a matching entry here is not an error: it simply falls into the
# "not recognized" bucket in `analyze`/`explain` output instead of a second,
# divergent list of "things devklean knows about".
SIGNATURE_REGISTRY: dict[str, ArtifactSignature] = {
    "node_modules": ArtifactSignature(
        dir_name="node_modules",
        ecosystem="Node.js (npm/yarn/pnpm)",
        generated_by="npm install / yarn install / pnpm install, from package.json and a lockfile",
        regenerate_command="npm install (or yarn install / pnpm install, matching your lockfile)",
        risk=RiskLevel.LOW,
        confidence=0.98,
        rationale=(
            "Directory name is npm/Node's own convention; contents are fully "
            "reproducible from package.json plus a lockfile."
        ),
    ),
    "venv": ArtifactSignature(
        dir_name="venv",
        ecosystem="Python (venv)",
        generated_by="python -m venv, populated via pip from a requirements/lock file",
        regenerate_command="python -m venv venv && venv/bin/pip install -r requirements.txt",
        risk=RiskLevel.LOW,
        confidence=0.95,
        rationale=(
            "Standard virtualenv layout (pyvenv.cfg, bin/lib); reproducible from a "
            "requirements file, though the exact install set depends on which file "
            "was originally used."
        ),
    ),
    ".venv": ArtifactSignature(
        dir_name=".venv",
        ecosystem="Python (venv)",
        generated_by="python -m venv, populated via pip from a requirements/lock file",
        regenerate_command="python -m venv .venv && .venv/bin/pip install -r requirements.txt",
        risk=RiskLevel.LOW,
        confidence=0.95,
        rationale=(
            "Standard virtualenv layout (pyvenv.cfg, bin/lib); reproducible from a "
            "requirements file, though the exact install set depends on which file "
            "was originally used."
        ),
    ),
    "env": ArtifactSignature(
        dir_name="env",
        ecosystem="Python (venv, legacy naming)",
        generated_by="python -m venv, populated via pip from a requirements/lock file",
        regenerate_command="python -m venv env && env/bin/pip install -r requirements.txt",
        risk=RiskLevel.MEDIUM,
        confidence=0.75,
        rationale=(
            "'env' is a less specific convention than venv/.venv and is sometimes "
            "used for unrelated environment-variable directories, so the match is "
            "less certain."
        ),
    ),
    "__pycache__": ArtifactSignature(
        dir_name="__pycache__",
        ecosystem="Python interpreter (CPython bytecode cache)",
        generated_by="CPython automatically, on any import",
        regenerate_command=(
            "none needed — recreated automatically the next time the module is imported"
        ),
        risk=RiskLevel.LOW,
        confidence=0.99,
        rationale=(
            "Name is reserved by CPython itself; contents are always .pyc bytecode "
            "with zero authored content."
        ),
    ),
    ".next": ArtifactSignature(
        dir_name=".next",
        ecosystem="Next.js",
        generated_by="next build / next dev, from the project's Next.js source",
        regenerate_command="next build (or next dev, which regenerates dev artifacts on the fly)",
        risk=RiskLevel.LOW,
        confidence=0.95,
        rationale=(
            "Directory name is Next.js's own build-output convention; reproducible "
            "from source via the Next.js CLI."
        ),
    ),
    "dist": ArtifactSignature(
        dir_name="dist",
        ecosystem="Generic build tooling (bundler/compiler output)",
        generated_by="whatever build step the project defines (webpack, tsc, vite, build.sh, ...)",
        regenerate_command="run the project's documented build command (e.g. npm run build)",
        risk=RiskLevel.MEDIUM,
        confidence=0.7,
        rationale=(
            "'dist' is a widely shared convention across many toolchains rather than "
            "one tool's signature — usually build output, but devklean cannot prove "
            "which build command produced it."
        ),
    ),
    ".cache": ArtifactSignature(
        dir_name=".cache",
        ecosystem="Generic cache directory",
        generated_by=(
            "varies by tool — bundlers, test runners, and linters all use .cache differently"
        ),
        regenerate_command=(
            "no single command — recreated automatically the next time the owning tool runs"
        ),
        risk=RiskLevel.MEDIUM,
        confidence=0.65,
        rationale=(
            "Extremely generic name reused by many unrelated tools; usually safe to "
            "remove, but devklean cannot identify which tool owns it or how quickly "
            "it regenerates."
        ),
    ),
}


def lookup(name: str) -> ArtifactSignature | None:
    """Look up a signature by exact directory name. No fuzzy matching."""
    return SIGNATURE_REGISTRY.get(name)


def match_signature(path: str) -> ArtifactSignature | None:
    """Resolve a filesystem path to a signature by directory-name match.

    Uses the same name-based signal as ``scan_tree`` (basename membership in
    a fixed set) — not a second walker, not a heuristic classifier. Returns
    ``None`` on no match; callers must not substitute a guessed verdict.
    """
    name = os.path.basename(os.path.normpath(path))
    return SIGNATURE_REGISTRY.get(name)
