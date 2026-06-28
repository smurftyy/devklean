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


class _Strategy:
    name = "rec"

    def __init__(self) -> None:
        self.called = False

    def delete(self, items, total_size: int, dry_run: bool = False) -> DeleteResult:
        self.called = True
        return DeleteResult(deleted=tuple(i.path for i in items), failed=(), total_size=total_size)


def _items(size: int):
    return [CleanableItem(f"/p/{size}", "node_modules", size, "Node.js")]


def test_dry_run_skips_deletion(monkeypatch) -> None:
    renderer, strategy = _Renderer(), _Strategy()
    monkeypatch.setattr("builtins.input", lambda p: (_ for _ in ()).throw(AssertionError()))

    run_standard(renderer, _items(100), dry_run=True, deletion_strategy=strategy)

    assert renderer.dry_run_selected_calls == 1
    assert strategy.called is False
    assert renderer.result is None


def test_default_yes_below_threshold_skips_prompt(monkeypatch) -> None:
    renderer, strategy = _Renderer(), _Strategy()

    def fail_input(p):
        raise AssertionError("should not prompt with default_yes below threshold")

    monkeypatch.setattr("builtins.input", fail_input)

    run_standard(
        renderer,
        _items(100),
        dry_run=False,
        deletion_strategy=strategy,
        default_yes=True,
        confirm_threshold=1024**3,
    )

    assert strategy.called is True
    assert renderer.result is not None


def test_below_threshold_without_default_yes_prompts(monkeypatch) -> None:
    renderer, strategy = _Renderer(), _Strategy()
    monkeypatch.setattr("builtins.input", lambda p: "y")

    run_standard(
        renderer,
        _items(100),
        dry_run=False,
        deletion_strategy=strategy,
        default_yes=False,
        confirm_threshold=1024**3,
    )

    assert renderer.prompts == [(1, 100)]
    assert strategy.called is True


def test_large_deletion_requires_typed_delete_even_with_default_yes(monkeypatch) -> None:
    renderer, strategy = _Renderer(), _Strategy()
    answers = iter(["DELETE"])
    monkeypatch.setattr("builtins.input", lambda p: next(answers))

    run_standard(
        renderer,
        _items(2 * 1024**3),
        dry_run=False,
        deletion_strategy=strategy,
        default_yes=True,
        confirm_threshold=1024**3,
    )

    # the plain y/N prompt was NOT used; the typed gate ran instead
    assert renderer.prompts == []
    assert strategy.called is True


def test_large_deletion_aborts_when_not_confirmed(monkeypatch) -> None:
    renderer, strategy = _Renderer(), _Strategy()
    monkeypatch.setattr("builtins.input", lambda p: "nope")

    run_standard(
        renderer,
        _items(2 * 1024**3),
        dry_run=False,
        deletion_strategy=strategy,
        default_yes=True,
        confirm_threshold=1024**3,
    )

    assert strategy.called is False
    assert renderer.aborted_calls == 1
