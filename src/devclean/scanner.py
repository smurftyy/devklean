import os

from devclean.formatting import BOLD, CYAN, DIM, RESET

TARGETS = {
    "node_modules": "Node.js",
    "venv": "Python venv",
    ".venv": "Python venv",
    "env": "Python env",
    "__pycache__": "Python cache",
    ".next": "Next.js build",
    "dist": "Build output",
    ".cache": "Cache",
}


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
