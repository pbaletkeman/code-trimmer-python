"""Tests for HookGenerator."""

from pathlib import Path

import pytest

from codetrimmer.error.codes import ErrorCode
from codetrimmer.error.exceptions import CodeTrimmerException
from codetrimmer.service.hook_generator import HookGenerator


class TestHookGenerator:
    """Tests for HookGenerator class."""

    def test_generate_hook(self, git_repo: Path) -> None:
        """Test generating pre-commit hook."""
        generator = HookGenerator()
        hook_path = generator.generate_pre_commit_hook(str(git_repo))

        assert hook_path.exists()
        content = hook_path.read_text()
        assert "#!/bin/bash" in content
        assert "codetrimmer" in content

    def test_generate_hook_no_git(self, temp_dir: Path) -> None:
        """Test error when no .git directory."""
        generator = HookGenerator()

        with pytest.raises(CodeTrimmerException) as exc_info:
            generator.generate_pre_commit_hook(str(temp_dir))

        assert exc_info.value.error_code == ErrorCode.CT_0051

    def test_hook_already_exists(self, git_repo: Path) -> None:
        """Test error when hook already exists."""
        generator = HookGenerator()

        # Create first hook
        generator.generate_pre_commit_hook(str(git_repo))

        # Try to create again without force
        with pytest.raises(CodeTrimmerException) as exc_info:
            generator.generate_pre_commit_hook(str(git_repo))

        assert exc_info.value.error_code == ErrorCode.CT_0052

    def test_force_overwrite(self, git_repo: Path) -> None:
        """Test force overwriting existing hook."""
        generator = HookGenerator()

        # Create first hook
        generator.generate_pre_commit_hook(str(git_repo))

        # Overwrite with force
        hook_path = generator.generate_pre_commit_hook(str(git_repo), force=True)
        assert hook_path.exists()

    def test_windows_hooks_generated(self, git_repo: Path) -> None:
        """Test Windows hook files are generated."""
        generator = HookGenerator()
        generator.generate_pre_commit_hook(str(git_repo))

        hooks_dir = git_repo / ".git" / "hooks"
        batch_hook = hooks_dir / "pre-commit.bat"
        ps1_hook = hooks_dir / "pre-commit.ps1"

        assert batch_hook.exists()
        assert ps1_hook.exists()

    def test_batch_hook_content(self, git_repo: Path) -> None:
        """Test batch hook content."""
        generator = HookGenerator()
        generator.generate_pre_commit_hook(str(git_repo))

        hooks_dir = git_repo / ".git" / "hooks"
        batch_hook = hooks_dir / "pre-commit.bat"
        content = batch_hook.read_text()

        assert "@echo off" in content
        assert "codetrimmer" in content

    def test_powershell_hook_content(self, git_repo: Path) -> None:
        """Test PowerShell hook content."""
        generator = HookGenerator()
        generator.generate_pre_commit_hook(str(git_repo))

        hooks_dir = git_repo / ".git" / "hooks"
        ps1_hook = hooks_dir / "pre-commit.ps1"
        content = ps1_hook.read_text()

        assert "Write-Host" in content
        assert "codetrimmer" in content
