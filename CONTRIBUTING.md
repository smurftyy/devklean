# Contributing to devklean

Thanks for your interest in improving devklean! Bug reports, feature ideas, and
pull requests are all welcome.

## Development setup

devklean targets Python 3.8+ and has no build-time dependencies beyond
[Hatchling](https://hatch.pypa.io/latest/).

```bash
git clone https://github.com/smurftyy/devklean.git
cd devklean
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
```

This installs devklean in editable mode plus the dev tools (pytest, ruff, mypy,
build).

## Running checks locally

Run the same checks CI runs, in the same order (lint first, it's fastest):

```bash
ruff check .              # lint
ruff format --check .     # formatting (drop --check to auto-format)
mypy                      # type check (src/devklean)
pytest                    # test suite
pytest --cov=devklean --cov-report=term-missing   # with coverage
```

Some tests are platform-specific (permissions, symlinks, mounted-drive
detection) and skip cleanly when not applicable, so the suite runs green on
Linux, macOS, and Windows.

## How we work

- **Tests first.** This codebase is built with TDD — add a failing test before
  the implementation, and keep the suite green. New behavior needs a test.
- **Keep safety/integrity logic centralized.** Path safety lives in
  `SafetyValidator`; metadata integrity in the `integrity`/`doctor` modules.
  Extend those rather than scattering checks.
- **Match the surrounding style.** Small, focused modules; type hints;
  `from __future__ import annotations`.

## Pull requests

Before opening a PR:

1. `ruff check .`, `ruff format --check .`, and `mypy` are clean.
2. `pytest` passes (ideally on your OS; CI covers the rest).
3. New or changed behavior has tests.
4. Add a note under `## [Unreleased]` in [CHANGELOG.md](CHANGELOG.md).

Keep PRs focused and describe the motivation. A short, imperative commit subject
(e.g. "add --json to history") is appreciated.

## Project layout

```
src/devklean/
  cli/          argument parsing, command dispatch, command handlers
  config/       TOML config loading, precedence, validation
  deletion/     strategies (send2trash), safety validator, metadata, integrity
  output/       renderers (text/json), console/theme/color, progress widgets
  scanner/      directory traversal and size computation
  logging_setup.py
tests/          pytest suite (mirrors the package)
```

## Releasing

Maintainers: see [RELEASING.md](RELEASING.md) for how to cut a release.
