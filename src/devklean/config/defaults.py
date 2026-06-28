"""Built-in default target definitions."""

from __future__ import annotations

DEFAULT_TARGETS: dict[str, str] = {
    "node_modules": "Node.js",
    "venv": "Python venv",
    ".venv": "Python venv",
    "env": "Python env",
    "__pycache__": "Python cache",
    ".next": "Next.js build",
    "dist": "Build output",
    ".cache": "Cache",
}
