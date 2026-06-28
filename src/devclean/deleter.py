import shutil

from devclean.formatting import BOLD, DIM, GREEN, RED, RESET, format_size


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
