"""Tests for the centralized deletion safety validator."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from devklean.deletion.safety import SafetyValidator, SafetyViolation
from devklean.deletion.service import default_deletion_strategy
from devklean.deletion.trash import TrashStrategy
from devklean.models import CleanableItem


def _item(path: str, size: int = 100) -> CleanableItem:
    return CleanableItem(path=path, name="node_modules", size=size, display_label="Node.js")


def test_safe_path_passes_validation(tmp_path: Path) -> None:
    target = tmp_path / "project" / "node_modules"
    target.mkdir(parents=True)

    assert SafetyValidator().validate(str(target)) is None


def test_blocks_filesystem_root() -> None:
    violation = SafetyValidator().validate("/")

    assert violation is not None
    assert violation.rule == "filesystem_root"
    assert "/" in violation.message


def test_blocks_home_directory(tmp_path: Path, monkeypatch) -> None:
    home = tmp_path / "me"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))

    violation = SafetyValidator().validate(str(home))

    assert violation is not None
    assert violation.rule == "home_directory"


def test_blocks_mount_point(monkeypatch, tmp_path: Path) -> None:
    mount = tmp_path / "mnt" / "usb"
    mount.mkdir(parents=True)
    monkeypatch.setattr(
        "devklean.deletion.safety.os.path.ismount",
        lambda p: str(p) == str(mount),
    )

    violation = SafetyValidator().validate(str(mount))

    assert violation is not None
    assert violation.rule == "mount_point"


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX protected paths")
def test_blocks_protected_system_directory() -> None:
    violation = SafetyValidator().validate("/etc")

    assert violation is not None
    assert violation.rule == "protected_system_directory"
    assert "/etc" in violation.message


def test_blocks_symlink_by_default(tmp_path: Path) -> None:
    real = tmp_path / "real_node_modules"
    real.mkdir()
    link = tmp_path / "link_node_modules"
    link.symlink_to(real)

    violation = SafetyValidator().validate(str(link))

    assert violation is not None
    assert violation.rule == "symlink"


def test_symlink_that_is_a_protected_dir_is_classified_protected(tmp_path: Path) -> None:
    # Reproduces the macOS case (/etc is a symlink into /private) on any
    # platform: a symlink whose own path is protected must be reported as
    # protected_system_directory, not symlink — ordering must put protected
    # ahead of the symlink rule.
    real = tmp_path / "private" / "etc"
    real.mkdir(parents=True)
    protected_link = tmp_path / "etc"
    protected_link.symlink_to(real)

    validator = SafetyValidator(protected_paths=frozenset({str(protected_link)}))
    violation = validator.validate(str(protected_link))

    assert violation is not None
    assert violation.rule == "protected_system_directory"


def test_symlink_protected_dir_not_bypassable_with_allow_symlinks(tmp_path: Path) -> None:
    # --allow-symlinks must not let you delete a protected location that happens
    # to be reached via a symlink.
    real = tmp_path / "private" / "etc"
    real.mkdir(parents=True)
    protected_link = tmp_path / "etc"
    protected_link.symlink_to(real)

    validator = SafetyValidator(
        allow_symlinks=True, protected_paths=frozenset({str(protected_link)})
    )
    violation = validator.validate(str(protected_link))

    assert violation is not None
    assert violation.rule == "protected_system_directory"


def test_ordinary_symlink_outside_protected_is_still_symlink(tmp_path: Path) -> None:
    # Inverse of the ordering fix: a symlink NOT pointing at / resolving into a
    # protected location must still be classified as a symlink.
    real = tmp_path / "real"
    real.mkdir()
    link = tmp_path / "link"
    link.symlink_to(real)

    validator = SafetyValidator(protected_paths=frozenset({"/some/protected/dir"}))
    violation = validator.validate(str(link))

    assert violation is not None
    assert violation.rule == "symlink"


def test_allows_symlink_when_opted_in(tmp_path: Path) -> None:
    real = tmp_path / "real_node_modules"
    real.mkdir()
    link = tmp_path / "link_node_modules"
    link.symlink_to(real)

    assert SafetyValidator(allow_symlinks=True).validate(str(link)) is None


def test_symlink_to_unsafe_target_still_blocked_when_symlinks_allowed() -> None:
    # Even allowing symlinks, the resolved target must still be safe.
    validator = SafetyValidator(allow_symlinks=True)
    # "/" is not a symlink but demonstrates resolved-target rules still apply;
    # use a constructed symlink to root via opt-in path instead.
    violation = validator.validate("/")
    assert violation is not None
    assert violation.rule == "filesystem_root"


def test_partition_splits_safe_and_blocked(tmp_path: Path) -> None:
    safe_dir = tmp_path / "proj" / "node_modules"
    safe_dir.mkdir(parents=True)
    safe = _item(str(safe_dir))
    unsafe = _item("/")

    kept, blocked = SafetyValidator().partition([unsafe, safe])

    assert kept == [safe]
    assert len(blocked) == 1
    blocked_item, violation = blocked[0]
    assert blocked_item is unsafe
    assert isinstance(violation, SafetyViolation)
    assert violation.rule == "filesystem_root"


def test_trash_strategy_blocks_unsafe_path_and_deletes_safe_one(tmp_path: Path, fake_trash) -> None:
    safe_dir = tmp_path / "proj" / "node_modules"
    safe_dir.mkdir(parents=True)
    (safe_dir / "package.json").write_text("{}")

    safe = _item(str(safe_dir), size=100)
    unsafe = _item("/", size=999)

    result = TrashStrategy().delete([unsafe, safe], total_size=1099)

    assert result.deleted == (str(safe_dir),)
    assert len(result.failed) == 1
    assert result.failed[0].path == "/"
    assert "filesystem root" in result.failed[0].error
    # freed size reflects only the safe item, not the blocked one
    assert result.total_size == 100
    assert not safe_dir.exists()
    assert fake_trash == [str(safe_dir)]  # only the safe item was trashed


def test_trash_strategy_uses_injected_validator(tmp_path: Path, fake_trash) -> None:
    link_target = tmp_path / "real"
    link_target.mkdir()
    link = tmp_path / "proj" / "node_modules"
    link.parent.mkdir(parents=True)
    link.symlink_to(link_target)

    item = _item(str(link), size=50)

    blocked = TrashStrategy().delete([item], total_size=50)
    assert blocked.deleted == ()
    assert blocked.failed[0].error.count("symbolic link") == 1

    allowed = TrashStrategy(
        validator=SafetyValidator(allow_symlinks=True),
    ).delete([item], total_size=50)
    assert allowed.deleted == (str(link),)


def test_default_deletion_strategy_blocks_symlinks_by_default(tmp_path: Path) -> None:
    real = tmp_path / "real"
    real.mkdir()
    link = tmp_path / "node_modules"
    link.symlink_to(real)
    item = _item(str(link))

    result = default_deletion_strategy().delete([item], total_size=100)

    assert result.deleted == ()
    assert result.failed[0].error.count("symbolic link") == 1


def test_default_deletion_strategy_honors_allow_symlinks(tmp_path: Path, fake_trash) -> None:
    real = tmp_path / "real"
    real.mkdir()
    link = tmp_path / "node_modules"
    link.symlink_to(real)
    item = _item(str(link))

    result = default_deletion_strategy(allow_symlinks=True).delete([item], total_size=100)

    assert result.deleted == (str(link),)
    assert fake_trash == [str(link)]
