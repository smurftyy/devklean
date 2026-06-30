# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/smurftyy/devklean/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/smurftyy/devklean/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/smurftyy/devklean/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/smurftyy/devklean/releases/tag/v0.1.0
