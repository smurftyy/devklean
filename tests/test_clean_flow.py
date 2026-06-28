"""Tests for the clean command's confirmation/threshold/dry-run flow."""

from __future__ import annotations

from dataclasses import dataclass, field

from devklean.cli.commands.clean import run_standard
from devklean.models import CleanableItem, DeleteResult


@dataclass
class _Renderer:
    dry_run_selected_calls: int = 0
    aborted_calls: int = 0
    result: DeleteResult | None = None
    prompts: list = field(default_factory=list)

    def scan_summary(self, items) -> int:
        return sum(i.size for i in items)

    def dry_run_selected(self, count: int) -> None:
        self.dry_run_selected_calls += 1

    def dry_run_nothing_deleted(self) -> None:
        self.dry_run_selected_calls += 1

    def aborted(self) -> None:
        self.aborted_calls += 1

    def confirm_prompt(self, count: int, total_size: int = 0) -> str:
        self.prompts.append((count, total_size))
        return "prompt? "

    def deletion_result(self, result: DeleteResult) -> None:
        self.result = result


def _install_delete_recorder(monkeypatch) -> list[bool]:
    """Replace clean.delete_items with a recorder; returns the call log."""
    calls: list[bool] = []

    def _fake(items, total_size, **kwargs) -> DeleteResult:
        calls.append(True)
        return DeleteResult(deleted=tuple(i.path for i in items), failed=(), total_size=total_size)

    monkeypatch.setattr("devklean.cli.commands.clean.delete_items", _fake)
    return calls


def _items(size: int):
    return [CleanableItem(f"/p/{size}", "node_modules", size, "Node.js")]


def test_dry_run_skips_deletion(monkeypatch) -> None:
    renderer = _Renderer()
    calls = _install_delete_recorder(monkeypatch)
    monkeypatch.setattr("builtins.input", lambda p: (_ for _ in ()).throw(AssertionError()))

    run_standard(renderer, _items(100), dry_run=True)

    assert renderer.dry_run_selected_calls == 1
    assert calls == []
    assert renderer.result is None


def test_default_yes_below_threshold_skips_prompt(monkeypatch) -> None:
    renderer = _Renderer()
    calls = _install_delete_recorder(monkeypatch)

    def fail_input(p):
        raise AssertionError("should not prompt with default_yes below threshold")

    monkeypatch.setattr("builtins.input", fail_input)

    run_standard(
        renderer,
        _items(100),
        dry_run=False,
        default_yes=True,
        confirm_threshold=1024**3,
    )

    assert calls == [True]
    assert renderer.result is not None


def test_below_threshold_without_default_yes_prompts(monkeypatch) -> None:
    renderer = _Renderer()
    calls = _install_delete_recorder(monkeypatch)
    monkeypatch.setattr("builtins.input", lambda p: "y")

    run_standard(
        renderer,
        _items(100),
        dry_run=False,
        default_yes=False,
        confirm_threshold=1024**3,
    )

    assert renderer.prompts == [(1, 100)]
    assert calls == [True]


def test_large_deletion_requires_typed_delete_even_with_default_yes(monkeypatch) -> None:
    renderer = _Renderer()
    calls = _install_delete_recorder(monkeypatch)
    answers = iter(["DELETE"])
    monkeypatch.setattr("builtins.input", lambda p: next(answers))

    run_standard(
        renderer,
        _items(2 * 1024**3),
        dry_run=False,
        default_yes=True,
        confirm_threshold=1024**3,
    )

    # the plain y/N prompt was NOT used; the typed gate ran instead
    assert renderer.prompts == []
    assert calls == [True]


def test_large_deletion_aborts_when_not_confirmed(monkeypatch) -> None:
    renderer = _Renderer()
    calls = _install_delete_recorder(monkeypatch)
    monkeypatch.setattr("builtins.input", lambda p: "nope")

    run_standard(
        renderer,
        _items(2 * 1024**3),
        dry_run=False,
        default_yes=True,
        confirm_threshold=1024**3,
    )

    assert calls == []
    assert renderer.aborted_calls == 1
