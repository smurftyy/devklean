# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-06-28

First public pre-release.

### Added

- **Scanning** — discover cleanable directories (`node_modules`, `.venv`,
  `__pycache__`, `dist`, caches, and more) with size reporting; `scan` command
  with `--json` output.
- **Cleaning** — `clean` command moves items to the system trash (not permanent
  deletion), with a size summary and confirmation. Supports `--dry-run`,
  interactive selection (`-i`), `--allow-symlinks`, and `-y/--yes`.
- **Restore & history** — `restore` recovers trashed items; `history` lists past
  cleanup operations (timestamp, reclaimed size, strategy, item count) in text
  or `--json`.
- **Safety layer** — a centralized `SafetyValidator` blocks deletion of the
  filesystem root, home directory, mounted drive roots, protected system
  directories, and symlinks (opt in with `--allow-symlinks`). Large deletions
  (≥ 1 GiB by default) require typing `DELETE`.
- **Recovery & integrity** — `doctor` command detects corrupt and orphaned
  metadata, removing only confirmed-corrupt records after confirmation; reads
  degrade gracefully and surface warnings.
- **Configuration** — TOML config with precedence project (`.devklean.toml`) >
  global (`~/.config/devklean/config.toml`) > built-in defaults; keys for
  `exclude`, `default_yes`, `theme`, `confirm_threshold`, targets, and ignores;
  validation warns on unknown keys / malformed TOML without crashing.
- **Logging** — structured, rotating file logs at
  `~/.cache/devklean/logs/latest.log`, separate from terminal output.
- **UX** — consistent `✓`/`✗`/`⚠` messaging, color that respects `NO_COLOR`,
  non-tty output, and a `theme` setting; progress spinners/bars; polished
  interactive mode.
- **Performance** — `os.scandir`-based size computation and concurrent
  per-target sizing.
- **Packaging** — distributable via `pip`/`pipx`; MIT licensed.

[Unreleased]: https://github.com/smurftyy/devklean/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/smurftyy/devklean/releases/tag/v0.1.0
