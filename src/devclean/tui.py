from __future__ import annotations

import curses
from typing import List, Optional

from devclean.deleter import delete_items
from devclean.formatting import DIM, YELLOW, format_size, truncate
from devclean.models import CleanableItem


def interactive_ui(stdscr, items: List[CleanableItem], dry_run: bool) -> Optional[List[int]]:
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
                line = f"[{mark}] {item.display_label:<18} {format_size(item.size):>8} {item.path}"
                line = truncate(line, width)
                if i == idx:
                    stdscr.addnstr(list_top + row, 0, line, width, curses.A_REVERSE)
                else:
                    stdscr.addnstr(list_top + row, 0, line, width)

        selected_count = sum(1 for s in selected if s)
        selected_size = sum(items[i].size for i, s in enumerate(selected) if s)
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


def run_interactive(found: List[CleanableItem], dry_run: bool) -> None:
    items = sorted(found, key=lambda x: -x.size)

    selected_indices = curses.wrapper(interactive_ui, items, dry_run)
    if selected_indices is None:
        print(f"\n{DIM}Aborted. Nothing deleted.{RESET}\n")
        return

    selected = [items[i] for i in selected_indices]
    if not selected:
        print(f"\n{DIM}No items selected. Nothing deleted.{RESET}\n")
        return

    total_size = sum(item.size for item in selected)

    if dry_run:
        print(f"{YELLOW}[dry-run] {len(selected)} director{'y' if len(selected)==1 else 'ies'} selected, nothing deleted.{RESET}\n")
        return

    delete_items(selected, total_size)
