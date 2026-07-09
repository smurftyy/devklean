# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **`analyze [PATH]`** — scan for cleanable directories and cross-reference
  them against a new artifact-signature registry: buckets results into
  recognized (a known artifact type, with risk tier, confidence, and a
  staleness estimate for its parent project) and unrecognized (no registry
  entry, no verdict fabricated), flags project roots with conflicting
  package-manager lockfiles, and reports an overall workspace-health score
  (0-100). `--verbose` prints the scoring formula and its raw inputs.
- **`explain PATH`** — look up a single directory against the same
  signature registry and explain what it is: ecosystem, what generates it,
  how to regenerate it, risk tier, confidence, and the rationale behind the
  entry. An unrecognized path gets no risk/confidence verdict at all.
- Artifact-signature registry (`devklean.signatures`) backing both commands
  above — static, maintainer-assigned data (not inferred) covering
  `node_modules`, `venv`/`.venv`/`env`, `__pycache__`, `.next`, `dist`, and
  `.cache`.
- `--compress` flag (and matching `compress` config default) for `clean`:
  when set, eligible directories are archived into a sibling `.tar.gz` (or
  `.tar.zst`, via the `devklean[zstd]` extra) before being sent to trash,
  shrinking the footprint of large artifacts like `node_modules` or
  `.venv`. Compression is ordered for safety — archive, verify, send the
  archive to trash, and only then remove the original — so a failure at
  any step leaves the source directory untouched. New `compress_min_size`
  and `compress_format` config keys tune the size threshold and archive
  format. Metadata schema bumped to version 5 to record the archive path,
  format, and original/compressed sizes; restoring a compressed item
  currently requires unpacking the archive by hand after pulling it out of
  trash.

## [1.0.2] - 2026-07-01

### Changed

- Replaced `print()` calls in the console layer with `click.echo()` for improved
  Unicode and Windows terminal compatibility.
- Fixed `src/devklean/__main__.py` to correctly import `main` from
  `devklean.cli.main`.
- Made package `__init__.py` imports lazy to avoid pulling in `send2trash`
  during unrelated imports.
- Added `click` as a runtime dependency.
- Updated Windows guard test to work in subprocesses with `PYTHONPATH=src`.

## [1.0.1] - 2026-06-30

### Fixed

- Pressing Ctrl+C (e.g. at a `clean` confirmation prompt) now exits cleanly with
  a short `Aborted.` notice and exit code 130 (the Unix SIGINT convention)
  instead of dumping a `KeyboardInterrupt` traceback.
- `doctor` now flags records with an unrecognized `strategy` value as corrupt.
  Stores containing legacy strategy values (e.g. `"recording"`, `"rec"`) were
  previously reported as healthy; the only recognized strategy is `"trash"`.

## [1.0.0] - 2026-06-30

First stable release. No breaking changes to the CLI since `0.1.0`; this
release marks the API and behavior as stable.

### Added

- A default-command shorthand: running `devklean <path>` (or `devklean` with no
  arguments) is treated as a `scan`, so the most common operation needs no
  subcommand.
- Permission errors encountered while scanning are now tracked and surfaced in
  `--json` output.

### Changed

- Path resolution now honors `XDG_*` environment variables consistently across
  log, config, and deletion-metadata paths on all platforms.
  - Note: if you previously had `XDG_*` variables set, devklean may now resolve
    these paths to different locations than before; existing logs, config, and
    metadata in the old locations will not be migrated automatically.
- Console output is forced to UTF-8 on Windows to render the `✓`/`✗`/`⚠`
  symbols without raising `UnicodeEncodeError`.

### Fixed

- Non-interactive commands no longer crash on Windows. The `curses` import (a
  Unix-only module) is now loaded lazily, so `scan`, `clean`, `history`,
  `doctor`, and `restore` import and run on Windows.

### Known limitations

- Interactive mode (`-i` / `--interactive`) is **Linux/macOS only** because it
  depends on `curses`, which is unavailable on Windows. On Windows, `devklean
  clean -i` now prints a clear message and exits cleanly instead of raising an
  `ImportError`. All other commands work on Windows.

## [0.1.0] - 2026-06-28

First public pre-release.

### Added

- **Scanning** — discover cleanable directories (`node_modules`, `.venv`,
  `__pycache__`, `dist`, caches, and more) with size reporting; `scan` command
  with `--json` output.
- **Cleaning** — `clean` command moves items to the native operating-system
  trash (Recycle Bin on Windows, Trash on macOS, freedesktop trash on Linux) via
  `send2trash`, with a size summary and confirmation. Supports `--dry-run`,
  interactive selection (`-i`), `--allow-symlinks`, and `-y/--yes`.
- **History & recovery** — `history` lists past cleanup operations (timestamp,
  reclaimed size, strategy, item count) in text or `--json`. Recovery is done
  through the OS trash UI (the OS owns the trash); `restore` explains how.
- **Safety layer** — a centralized `SafetyValidator` blocks deletion of the
  filesystem root, home directory, mounted drive roots, protected system
  directories, and symlinks (opt in with `--allow-symlinks`); protected
  locations reached via a symlink (e.g. macOS `/etc`) are classified as
  protected and cannot be bypassed with `--allow-symlinks`. Large deletions
  (≥ 1 GiB by default) require typing `DELETE`.
- **Integrity** — `doctor` command detects corrupt metadata and removes only
  confirmed-corrupt records after confirmation; reads degrade gracefully and
  surface warnings.
- **Configuration** — TOML config with precedence project (`.devklean.toml`) >
  global (`~/.config/devklean/config.toml`) > built-in defaults; keys for
  `exclude`, `default_yes`, `theme`, `confirm_threshold`, targets, and ignores;
  validation warns on unknown keys / malformed TOML without crashing.
- **Logging** — structured, rotating file logs at
  `~/.cache/devklean/logs/latest.log`, separate from terminal output.
- **UX** — consistent `✓`/`✗`/`⚠` messaging, color that respects `NO_COLOR`,
  non-tty output, and a `theme` setting; polished interactive mode.
- **Performance** — `os.scandir`-based size computation and concurrent
  per-target sizing.
- **Packaging** — distributable via `pip`/`pipx`; MIT licensed.

[Unreleased]: https://github.com/smurftyy/devklean/compare/v1.0.2...HEAD
[1.0.2]: https://github.com/smurftyy/devklean/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/smurftyy/devklean/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/smurftyy/devklean/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/smurftyy/devklean/releases/tag/v0.1.0
