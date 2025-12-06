"""Tests for CLI commands."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from codetrimmer.cli.commands import cli, trim, generate_hook, undo


class TestCliCommands:
    """Tests for CLI commands."""

    @pytest.fixture
    def runner(self) -> CliRunner:
        """Create a CLI runner."""
        return CliRunner()

    def test_cli_help(self, runner: CliRunner) -> None:
        """Test CLI help output."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Code Trimmer" in result.output

    def test_cli_version(self, runner: CliRunner) -> None:
        """Test CLI version output."""
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "1.0.0" in result.output

    def test_trim_help(self, runner: CliRunner) -> None:
        """Test trim command help."""
        result = runner.invoke(cli, ["trim", "--help"])
        assert result.exit_code == 0
        assert "dry-run" in result.output.lower()
        assert "include" in result.output.lower()

    def test_trim_dry_run(self, runner: CliRunner, temp_dir: Path) -> None:
        """Test trim in dry-run mode."""
        # Create a test file
        test_file = temp_dir / "test.txt"
        test_file.write_text("Hello World   \n")

        result = runner.invoke(cli, ["trim", str(temp_dir), "--dry-run"])
        assert result.exit_code == 0
        assert "Dry-run" in result.output or "dry" in result.output.lower()

    def test_trim_with_verbose(
        self, runner: CliRunner, temp_dir: Path
    ) -> None:
        """Test trim with verbose output."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Hello   \n")

        result = runner.invoke(
            cli, ["trim", str(temp_dir), "--dry-run", "--verbose"]
        )
        assert result.exit_code == 0

    def test_trim_with_quiet(self, runner: CliRunner, temp_dir: Path) -> None:
        """Test trim with quiet output."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Hello   \n")

        result = runner.invoke(
            cli, ["trim", str(temp_dir), "--dry-run", "--quiet"]
        )
        # Quiet mode should have minimal output
        assert result.exit_code == 0

    def test_trim_nonexistent_dir(self, runner: CliRunner) -> None:
        """Test trim on non-existent directory."""
        result = runner.invoke(cli, ["trim", "/nonexistent/path"])
        assert result.exit_code != 0

    def test_generate_hook_help(self, runner: CliRunner) -> None:
        """Test generate-hook command help."""
        result = runner.invoke(cli, ["generate-hook", "--help"])
        assert result.exit_code == 0
        assert "force" in result.output.lower()

    def test_generate_hook_no_git(self, runner: CliRunner, temp_dir: Path) -> None:
        """Test generate-hook without .git directory."""
        result = runner.invoke(cli, ["generate-hook", str(temp_dir)])
        assert result.exit_code != 0
        assert "git" in result.output.lower() or "Error" in result.output

    def test_generate_hook_with_git(
        self, runner: CliRunner, git_repo: Path
    ) -> None:
        """Test generate-hook with .git directory."""
        result = runner.invoke(cli, ["generate-hook", str(git_repo)])
        assert result.exit_code == 0
        assert "generated" in result.output.lower() or "hook" in result.output.lower()

    def test_undo_help(self, runner: CliRunner) -> None:
        """Test undo command help."""
        result = runner.invoke(cli, ["undo", "--help"])
        assert result.exit_code == 0
        assert "backup" in result.output.lower() or "restore" in result.output.lower()

    def test_undo_no_backups(self, runner: CliRunner, temp_dir: Path) -> None:
        """Test undo with no backup files."""
        result = runner.invoke(cli, ["undo", str(temp_dir)])
        assert result.exit_code == 0
        assert "no backup" in result.output.lower()

    def test_undo_with_backups(self, runner: CliRunner, temp_dir: Path) -> None:
        """Test undo with backup files."""
        # Create backup file
        original = temp_dir / "test.txt"
        backup = temp_dir / "test.txt.bak"
        original.write_text("modified")
        backup.write_text("original")

        result = runner.invoke(cli, ["undo", str(temp_dir)])
        assert result.exit_code == 0
        assert "restored" in result.output.lower()

    def test_trim_with_no_color(
        self, runner: CliRunner, temp_dir: Path
    ) -> None:
        """Test trim with --no-color."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Hello   \n")

        result = runner.invoke(
            cli, ["trim", str(temp_dir), "--dry-run", "--no-color"]
        )
        # Should not contain ANSI escape codes
        assert "\033[" not in result.output
        assert result.exit_code == 0
