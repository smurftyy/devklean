# Phase 5 — Release & Ecosystem Design

Packaging, CI, documentation, and release-prep groundwork so the maintainer can
cut `v0.1.0` themselves. No git tags, no PyPI uploads, no GitHub releases are
performed here.

## Decisions (confirmed)

- **Build backend:** migrate to **Hatchling**. Delete the hand-rolled
  `build_backend.py`. `pyproject.toml` becomes the single source of truth;
  version is read from `src/devklean/_version.py` via Hatchling's version hook,
  so a release bump remains a one-line change in one file.
- **License:** **MIT**. Add a `LICENSE` file (© 2026 smurftyy) and an SPDX
  `license = "MIT"` expression with `license-files`.
- **Version:** reset `_version.py` to **0.1.0** (first public pre-release).
- **Identity:** author `smurftyy <oladapooloyede185@gmail.com>`; badge/project
  URLs target `github.com/smurftyy/devklean` (repo to be renamed to match the
  package). PyPI distribution + console script name: `devklean`.

## §1 Packaging

Rewrite `pyproject.toml`:

- `[build-system]` → `requires = ["hatchling"]`, `build-backend = "hatchling.build"`.
- `[project]`: `name="devklean"`, `dynamic=["version"]`, description, `readme`,
  `requires-python=">=3.8"`, `license="MIT"`, `license-files=["LICENSE"]`,
  `authors`, `keywords`, `classifiers` (MIT, Beta, Console, supported Pythons),
  `dependencies` (tomli marker), `[project.optional-dependencies].dev`
  (pytest, pytest-cov, ruff, mypy, build), `[project.scripts].devklean`,
  `[project.urls]` (Homepage, Repository, Issues, Changelog).
- `[tool.hatch.version] path = "src/devklean/_version.py"`.
- `[tool.hatch.build.targets.wheel] packages = ["src/devklean"]`.
- Keep `[tool.pytest.ini_options]` and `[tool.coverage.*]`; add `[tool.ruff]`
  and `[tool.mypy]`.
- Delete `build_backend.py`.

Verify: `python -m build` produces a wheel + sdist; the wheel METADATA includes
author, description, project URLs, MIT license; `pipx install ./dist/*.whl`
(or an isolated venv) exposes a working `devklean` console script. Add a small
packaging test asserting the version is single-sourced and the entry point
imports.

**pipx compatibility:** the tool depends only on stdlib + `tomli` (<3.11); the
console script is a normal entry point; no assumptions about being importable
from a system environment. Nothing should break under pipx isolation — verified
by installing the built wheel into a clean venv and running `devklean --version`.

## §2 GitHub Actions

Replace `.github/workflows/test.yml` with `ci.yml` and add `release.yml`.

- **`ci.yml`** (push/PR to main/dev):
  - `lint` job (fails fast): ruff check + ruff format --check + mypy. Runs once
    on the newest Python before the heavier matrix.
  - `test` job (needs: lint): matrix of `{ubuntu, macos, windows} ×
    {3.8 … 3.12}`, installs `.[dev]`, runs pytest with coverage. This exercises
    the Phase 4 platform-aware tests across OSes.
  - `build` job (needs: lint): `python -m build`, then `twine check dist/*` to
    catch metadata regressions.
  - Each job commented with its purpose.
- **`release.yml`** (on tag `v*.*.*`):
  - Build job, then publish via **PyPI Trusted Publishing (OIDC)** using
    `pypa/gh-action-pypi-publish` with `permissions: id-token: write` and a
    `pypi` environment. A commented fallback block shows the
    `password: ${{ secrets.PYPI_API_TOKEN }}` token method. No real secrets are
    wired; only the secret name is referenced.

## §3 Documentation

- **README.md** (rewrite): one-line description; shields.io badges (CI, PyPI
  version, license, Python versions) pointing at `smurftyy/devklean`;
  Install (`pip` + `pipx`); Commands reference (every command + flag with
  examples: `scan`, `clean` incl. `--dry-run`/`-i`/`--allow-symlinks`/`-y`,
  `restore`, `history` incl. `--json`, `doctor` incl. `--yes`); realistic
  before/after usage output; clearly-marked screenshot/GIF placeholders; FAQ
  drawn from real behavior (safety blocks, large-deletion DELETE gate, excludes,
  config precedence + `.devklean.toml`, log location, dry-run, NO_COLOR/themes).
- **CONTRIBUTING.md**: dev setup (`pip install -e ".[dev]"`), running
  tests/ruff/mypy locally, PR expectations (tests + lint green, TDD,
  conventional-ish commits), project layout pointer.
- **CHANGELOG.md**: Keep a Changelog format with an `## [Unreleased]` section
  and a seeded `## [0.1.0]` summary of Phases 1–5.

## §4 Release prep

- `_version.py` is the single source of truth (Hatchling reads it; README/docs
  reference it generically, never hardcode).
- **RELEASING.md**: step-by-step — bump `_version.py`, update CHANGELOG
  (`Unreleased` → version + date), commit, tag `vX.Y.Z`, push tag → triggers
  `release.yml` → Trusted Publishing to PyPI; pre-flight checklist (CI green,
  `python -m build`, `twine check`). Reference only — no tags created here.

## Out of scope / flagged

- Whether the GitHub repo is actually renamed `devclean → devklean` (URLs assume
  yes). The console script and PyPI name are `devklean` regardless.
- Real PyPI name registration and secret/environment configuration are the
  maintainer's to do.
- Full mypy strictness: config starts pragmatic (non-strict, `src/devklean`
  only) to keep CI green; tightening is future work.

## Files

**Added:** `.github/workflows/ci.yml`, `.github/workflows/release.yml`,
`LICENSE`, `CONTRIBUTING.md`, `CHANGELOG.md`, `RELEASING.md`,
`tests/test_packaging.py`.
**Modified:** `pyproject.toml`, `src/devklean/_version.py`, `README.md`.
**Removed:** `build_backend.py`, `.github/workflows/test.yml`.
