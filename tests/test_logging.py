"""Tests for file-based structured logging."""

from __future__ import annotations

import logging

from devklean.logging_setup import (
    configure_logging,
    get_log_path,
    get_logger,
    log_invocation,
)


def test_log_path_respects_xdg_cache_home(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    path = get_log_path()
    assert path == tmp_path / "cache" / "devklean" / "logs" / "latest.log"


def test_configure_logging_creates_log_file(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    configure_logging()
    get_logger().info("hello-from-test")

    log_file = tmp_path / "cache" / "devklean" / "logs" / "latest.log"
    assert log_file.is_file()
    assert "hello-from-test" in log_file.read_text(encoding="utf-8")


def test_logging_does_not_write_to_stdout(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    configure_logging()
    get_logger().info("file-only-message")

    captured = capsys.readouterr()
    assert "file-only-message" not in captured.out
    assert "file-only-message" not in captured.err


def test_log_invocation_records_command(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    configure_logging()
    log_invocation(["devklean", "clean", "/proj"], "clean")

    log_file = tmp_path / "cache" / "devklean" / "logs" / "latest.log"
    text = log_file.read_text(encoding="utf-8")
    assert "clean" in text


def test_configure_logging_is_idempotent(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    configure_logging()
    configure_logging()
    handlers = get_logger().handlers
    assert len(handlers) == 1


def test_delete_items_logs_deletion(tmp_path, monkeypatch, fake_trash) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    configure_logging()

    from devklean.deletion import delete_items
    from devklean.deletion.metadata import MetadataManager
    from devklean.models import CleanableItem

    target = tmp_path / "proj" / "node_modules"
    target.mkdir(parents=True)
    item = CleanableItem(str(target), "node_modules", 100, "Node.js")

    delete_items(
        [item],
        100,
        metadata_manager=MetadataManager(storage_dir=tmp_path / "meta"),
    )

    text = (tmp_path / "cache" / "devklean" / "logs" / "latest.log").read_text(encoding="utf-8")
    assert "node_modules" in text
    assert "deleted" in text.lower()


def test_configure_logging_never_raises_on_filesystem_error(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))

    def boom(*args, **kwargs):
        raise OSError("disk full")

    monkeypatch.setattr("devklean.logging_setup.Path.mkdir", boom)
    # Must not raise — logging failure must never break the CLI.
    configure_logging()


def test_logger_does_not_propagate_to_root(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    configure_logging()
    assert get_logger().propagate is False
    assert isinstance(get_logger().handlers[0], logging.Handler)
