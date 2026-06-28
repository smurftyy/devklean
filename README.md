# devclean

Clean up common development artifacts (like `node_modules` and Python virtual environments) to reclaim disk space.

## Requirements

- Python 3.8+

## Quick Start

```bash
git clone <repo-url>
cd devclean
python3 -m pip install .
devclean --dry-run
```

## Install

```bash
python3 -m pip install .
python3 -m pip install -e .
```

## Usage

```bash
devclean [path] [--dry-run] [--interactive]
python3 -m devclean [path] [--dry-run] [--interactive]
```

- `path` is optional. Defaults to the current directory.
- `--dry-run` lists what would be removed without deleting anything.
- `-i, --interactive` opens a curses-based TUI to select specific items.

Example:

```bash
devclean ~/code --dry-run
devclean ~/code
devclean ~/code --interactive
devclean ~/code --interactive --dry-run
```

## What It Cleans

- `node_modules`
- `venv`, `.venv`, `env`
- `__pycache__`
- `.next`
- `dist`
- `.cache`

## Safety

- Shows a size summary before deleting.
- Prompts for confirmation before removal.
- Handles permission errors gracefully.

## Interactive TUI

Use `-i`/`--interactive` to pick exactly what to delete:

- Arrow keys to move
- SPACE to toggle selection
- `A` select all / `D` deselect all
- ENTER to confirm and delete selected items
- `Q` or ESC to quit without deleting
- Live total for selected size at the bottom

## Notes

This is a local utility. Use at your own discretion on directories you control.
