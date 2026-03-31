#!/usr/bin/env python3
"""
devclean — scan and remove node_modules / venvs to reclaim disk space
usage: python3 devclean.py [path] [--dry-run]
"""

import os
import sys
import shutil
import argparse
import curses

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

def scan(root):
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

    return found

def print_summary(found):
    total_size = sum(s for _, _, s in found)

    print(f"{'TYPE':<18} {'SIZE':>8}  {'PATH'}")
    print(f"{DIM}{'─'*70}{RESET}")

    for path, name, size in sorted(found, key=lambda x: -x[2]):
        label = TARGETS.get(name, name)
        color = RED if size > 50 * 1024 * 1024 else YELLOW
        print(f"{DIM}{label:<18}{RESET} {color}{format_size(size):>8}{RESET}  {DIM}{path}{RESET}")

    print(f"{DIM}{'─'*70}{RESET}")
    print(f"{'TOTAL':<18} {BOLD}{RED}{format_size(total_size):>8}{RESET}\n")

    return total_size

def delete_items(items, total_size):
    deleted = 0
    failed = 0

    print()
    for path, _, _ in items:
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

def run_standard(found, dry_run):
    total_size = print_summary(found)

    if dry_run:
        print(f"{YELLOW}[dry-run] nothing deleted.{RESET}\n")
        return

    confirm = input(f"{BOLD}Delete all {len(found)} director{'y' if len(found)==1 else 'ies'}? {DIM}(y/N){RESET} ").strip().lower()
    if confirm != "y":
        print(f"\n{DIM}Aborted. Nothing deleted.{RESET}\n")
        return

    delete_items(found, total_size)

def truncate(text, max_len):
    if max_len <= 0:
        return ""
    if len(text) <= max_len:
        return text
    if max_len <= 3:
        return text[:max_len]
    return text[:max_len - 3] + "..."

def interactive_ui(stdscr, items, dry_run):
    curses.curs_set(0)
    stdscr.keypad(True)

    selected = [False] * len(items)
    idx = 0
    top = 0

    while True:
        stdscr.erase()
        height, width = stdscr.getmaxyx()

        header = "devclean interactive - SPACE select | A all | D none | ENTER confirm | Q/ESC quit"
        stdscr.addnstr(0, 0, truncate(header, width), width)

        list_top = 1
        list_height = max(0, height - 3)
        footer_y = height - 1

        if len(items) == 0:
            stdscr.addnstr(list_top, 0, "No matching directories found.", width)
        else:
            if idx < top:
                top = idx
            if idx >= top + list_height:
                top = idx - list_height + 1

            for row in range(list_height):
                i = top + row
                if i >= len(items):
                    break
                item = items[i]
                mark = "x" if selected[i] else " "
                line = f"[{mark}] {item['label']:<18} {format_size(item['size']):>8} {item['path']}"
                line = truncate(line, width)
                if i == idx:
                    stdscr.addnstr(list_top + row, 0, line, width, curses.A_REVERSE)
                else:
                    stdscr.addnstr(list_top + row, 0, line, width)

        selected_count = sum(1 for s in selected if s)
        selected_size = sum(items[i]["size"] for i, s in enumerate(selected) if s)
        footer = f"Selected: {selected_count}/{len(items)}  Total: {format_size(selected_size)}"
        if dry_run:
            footer += "  [dry-run]"
        stdscr.addnstr(footer_y, 0, truncate(footer, width), width)

        stdscr.refresh()

        key = stdscr.getch()
        if key in (ord("q"), ord("Q"), 27):
            return None
        if key in (curses.KEY_UP,):
            if idx > 0:
                idx -= 1
        elif key in (curses.KEY_DOWN,):
            if idx < len(items) - 1:
                idx += 1
        elif key == ord(" "):
            if len(items) > 0:
                selected[idx] = not selected[idx]
        elif key in (ord("a"), ord("A")):
            selected = [True] * len(items)
        elif key in (ord("d"), ord("D")):
            selected = [False] * len(items)
        elif key in (curses.KEY_ENTER, 10, 13):
            return [i for i, s in enumerate(selected) if s]

def run_interactive(found, dry_run):
    items = [
        {
            "path": path,
            "name": name,
            "size": size,
            "label": TARGETS.get(name, name),
        }
        for path, name, size in sorted(found, key=lambda x: -x[2])
    ]

    selected_indices = curses.wrapper(interactive_ui, items, dry_run)
    if selected_indices is None:
        print(f"\n{DIM}Aborted. Nothing deleted.{RESET}\n")
        return

    selected = [items[i] for i in selected_indices]
    if not selected:
        print(f"\n{DIM}No items selected. Nothing deleted.{RESET}\n")
        return

    total_size = sum(item["size"] for item in selected)
    selected_paths = [(item["path"], item["name"], item["size"]) for item in selected]

    if dry_run:
        print(f"{YELLOW}[dry-run] {len(selected)} director{'y' if len(selected)==1 else 'ies'} selected, nothing deleted.{RESET}\n")
        return

    delete_items(selected_paths, total_size)

def main():
    parser = argparse.ArgumentParser(
        description="Scan and remove node_modules/venvs to reclaim disk space."
    )
    parser.add_argument(
        "--version",
        action="version",
        version="devclean v1.1.0"
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
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Interactively select items to delete"
    )
    args = parser.parse_args()

    root = os.path.abspath(args.path)
    if not os.path.isdir(root):
        print(f"{RED}Error: '{root}' is not a directory.{RESET}")
        sys.exit(1)

    found = scan(root)
    if not found:
        print(f"{GREEN}✓ Nothing to clean.{RESET}\n")
        return

    if args.interactive:
        run_interactive(found, args.dry_run)
    else:
        run_standard(found, args.dry_run)

if __name__ == "__main__":
    main()
