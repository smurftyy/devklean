#!/usr/bin/env python3
"""
devclean — scan and remove node_modules / venvs to reclaim disk space
usage: python3 devclean.py [path] [--dry-run]
"""

import os
import sys
import shutil
import argparse

# ANSI colors
CYAN   = "\033[36m"
GREEN  = "\033[32m"
RED    = "\033[31m"
YELLOW = "\033[33m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

TARGETS = {
    "node_modules": "Node.js",
    "venv":         "Python venv",
    ".venv":        "Python venv",
    "env":          "Python env",
    "__pycache__":  "Python cache",
    ".next":        "Next.js build",
    "dist":         "Build output",
    ".cache":       "Cache",
}

def format_size(size_bytes):
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def get_dir_size(path):
    total = 0
    try:
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    total += os.path.getsize(fp)
                except (OSError, FileNotFoundError):
                    pass
    except PermissionError:
        pass
    return total

def scan(root, dry_run):
    found = []

    print(f"\n{BOLD}{CYAN}devclean{RESET} {DIM}scanning {root}...{RESET}\n")

    for dirpath, dirnames, _ in os.walk(root, topdown=True):
        # Prune already-found targets from further traversal
        dirnames[:] = [
            d for d in dirnames
            if os.path.join(dirpath, d) not in [f[0] for f in found]
        ]

        for dirname in list(dirnames):
            if dirname in TARGETS:
                full_path = os.path.join(dirpath, dirname)
                size = get_dir_size(full_path)
                found.append((full_path, dirname, size))
                dirnames.remove(dirname)  # don't recurse into it

    if not found:
        print(f"{GREEN}✓ Nothing to clean.{RESET}\n")
        return

    total_size = sum(s for _, _, s in found)

    print(f"{'TYPE':<18} {'SIZE':>8}  {'PATH'}")
    print(f"{DIM}{'─'*70}{RESET}")

    for path, name, size in sorted(found, key=lambda x: -x[2]):
        label = TARGETS.get(name, name)
        color = RED if size > 50 * 1024 * 1024 else YELLOW
        print(f"{DIM}{label:<18}{RESET} {color}{format_size(size):>8}{RESET}  {DIM}{path}{RESET}")

    print(f"{DIM}{'─'*70}{RESET}")
    print(f"{'TOTAL':<18} {BOLD}{RED}{format_size(total_size):>8}{RESET}\n")

    if dry_run:
        print(f"{YELLOW}[dry-run] nothing deleted.{RESET}\n")
        return

    confirm = input(f"{BOLD}Delete all {len(found)} director{'y' if len(found)==1 else 'ies'}? {DIM}(y/N){RESET} ").strip().lower()
    if confirm != "y":
        print(f"\n{DIM}Aborted. Nothing deleted.{RESET}\n")
        return

    deleted = 0
    failed  = 0

    print()
    for path, name, size in found:
        try:
            shutil.rmtree(path)
            print(f"  {GREEN}✓{RESET} {DIM}{path}{RESET}")
            deleted += 1
        except Exception as e:
            print(f"  {RED}✗{RESET} {path} — {e}")
            failed += 1

    print(f"\n{GREEN}{BOLD}Cleaned {deleted} director{'y' if deleted==1 else 'ies'}, freed ~{format_size(total_size)}.{RESET}")
    if failed:
        print(f"{RED}{failed} failed.{RESET}")
    print()

def main():
    parser = argparse.ArgumentParser(
        description="Scan and remove node_modules/venvs to reclaim disk space."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Root directory to scan (default: current directory)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without deleting anything"
    )
    args = parser.parse_args()

    root = os.path.abspath(args.path)
    if not os.path.isdir(root):
        print(f"{RED}Error: '{root}' is not a directory.{RESET}")
        sys.exit(1)

    scan(root, args.dry_run)

if __name__ == "__main__":
    main()