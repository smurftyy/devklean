# devclean

Clean up common development artifacts (like `node_modules` and Python virtual environments) to reclaim disk space.

## Requirements

- Python 3.8+

## Quick Start

```bash
git clone <repo-url>
cd devclean
python3 devclean.py --dry-run
```

## Usage

```bash
python3 devclean.py [path] [--dry-run]
```

- `path` is optional. Defaults to the current directory.
- `--dry-run` lists what would be removed without deleting anything.

Example:

```bash
python3 devclean.py ~/code --dry-run
python3 devclean.py ~/code
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

## Notes

This is a local utility. Use at your own discretion on directories you control.
