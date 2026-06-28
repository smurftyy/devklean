from __future__ import annotations

import shutil

from devclean.formatting import BOLD, DIM, GREEN, RED, RESET, format_size
from devclean.models import CleanableItem


def delete_items(items: list[CleanableItem], total_size: int) -> None:
    deleted = 0
    failed = 0

    print()
    for item in items:
        try:
            shutil.rmtree(item.path)
            print(f"  {GREEN}✓{RESET} {DIM}{item.path}{RESET}")
            deleted += 1
        except Exception as e:
            print(f"  {RED}✗{RESET} {item.path} — {e}")
            failed += 1

    print(f"\n{GREEN}{BOLD}Cleaned {deleted} director{'y' if deleted==1 else 'ies'}, freed ~{format_size(total_size)}.{RESET}")
    if failed:
        print(f"{RED}{failed} failed.{RESET}")
    print()
