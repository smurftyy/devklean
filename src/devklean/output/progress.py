from __future__ import annotations

import itertools
import os
import sys
import threading
from typing import TextIO

_SPINNER_FRAMES = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"


def progress_enabled(stream: TextIO) -> bool:
    """Progress is shown only on an interactive tty with NO_COLOR unset."""
    if os.environ.get("NO_COLOR") is not None:
        return False
    isatty = getattr(stream, "isatty", None)
    return bool(isatty and isatty())


class Spinner:
    """Indeterminate spinner animated on a background thread.

    A no-op when disabled (non-tty / NO_COLOR / JSON mode), so it never
    pollutes piped output. Writes to stderr by default.
    """

    def __init__(
        self,
        stream: TextIO | None = None,
        label: str = "",
        enabled: bool | None = None,
        interval: float = 0.1,
    ) -> None:
        self._stream = stream if stream is not None else sys.stderr
        self._label = label
        self._enabled = enabled if enabled is not None else progress_enabled(self._stream)
        self._interval = interval
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()
        self._lock = threading.Lock()

    def _write_frame(self, frame: str) -> None:
        with self._lock:
            self._stream.write(f"\r{frame} {self._label}")
            self._stream.flush()

    def start(self) -> Spinner:
        if not self._enabled:
            return self
        self._write_frame(_SPINNER_FRAMES[0])
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()
        return self

    def _spin(self) -> None:
        for frame in itertools.cycle(_SPINNER_FRAMES[1:]):
            if self._stop.wait(self._interval):
                return
            self._write_frame(frame)

    def update(self, label: str) -> None:
        self._label = label

    def stop(self) -> None:
        if not self._enabled:
            return
        self._stop.set()
        if self._thread is not None:
            self._thread.join()
        with self._lock:
            self._stream.write("\r\033[K")  # clear the spinner line
            self._stream.flush()

    def __enter__(self) -> Spinner:
        return self.start()

    def __exit__(self, *exc) -> None:
        self.stop()


class ProgressBar:
    """Determinate progress bar for batches of known size."""

    def __init__(
        self,
        total: int,
        stream: TextIO | None = None,
        label: str = "",
        enabled: bool | None = None,
        width: int = 8,
    ) -> None:
        self._total = total
        self._stream = stream if stream is not None else sys.stderr
        self._label = label
        self._enabled = enabled if enabled is not None else progress_enabled(self._stream)
        self._width = width
        self._count = 0

    def render(self, count: int) -> str:
        if self._total <= 0:
            filled = self._width
        else:
            filled = int(self._width * count / self._total)
        bar = "#" * filled + "-" * (self._width - filled)
        return f"{self._label} [{bar}] {count}/{self._total}".strip()

    def advance(self, n: int = 1) -> None:
        self._count += n
        if not self._enabled:
            return
        self._stream.write("\r" + self.render(self._count))
        self._stream.flush()

    def close(self) -> None:
        if not self._enabled:
            return
        self._stream.write("\r\033[K")
        self._stream.flush()

    def __enter__(self) -> ProgressBar:
        return self

    def __exit__(self, *exc) -> None:
        self.close()
