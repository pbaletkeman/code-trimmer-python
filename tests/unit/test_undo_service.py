"""Tests for UndoService."""

from pathlib import Path

import pytest

from codetrimmer.error.codes import ErrorCode
from codetrimmer.error.exceptions import CodeTrimmerException
from codetrimmer.service.undo_service import UndoService


class TestUndoService:
    """Tests for UndoService class."""

    def test_restore_file(self, temp_dir: Path) -> None:
        """Test restoring a file from backup."""
        # Create original and backup
        original = temp_dir / "test.txt"
        backup = temp_dir / "test.txt.bak"

        backup.write_text("original content")
        original.write_text("modified content")

        # Restore
        service = UndoService()
        result = service.restore_file(str(original))

        assert result is True
        assert original.read_text() == "original content"
        assert not backup.exists()

    def test_restore_no_backup(self, temp_dir: Path) -> None:
        """Test error when backup doesn't exist."""
        original = temp_dir / "test.txt"
        original.write_text("content")

        service = UndoService()

        with pytest.raises(CodeTrimmerException) as exc_info:
            service.restore_file(str(original))

        assert exc_info.value.error_code == ErrorCode.CT_0042

    def test_restore_directory(self, temp_dir: Path) -> None:
        """Test restoring all files in a directory."""
        # Create originals and backups
        for i in range(3):
            original = temp_dir / f"file{i}.txt"
            backup = temp_dir / f"file{i}.txt.bak"
            backup.write_text(f"original {i}")
            original.write_text(f"modified {i}")

        service = UndoService()
        results = service.restore_directory(str(temp_dir))

        assert len(results) == 3
        assert all(success for success in results.values())

    def test_list_backup_files(self, temp_dir: Path) -> None:
        """Test listing backup files."""
        # Create backup files
        for i in range(3):
            (temp_dir / f"file{i}.txt.bak").write_text(f"backup {i}")

        service = UndoService()
        backups = service.list_backup_files(str(temp_dir))

        assert len(backups) == 3
        assert all(b.endswith(".bak") for b in backups)

    def test_cleanup_backups(self, temp_dir: Path) -> None:
        """Test cleaning up backup files."""
        # Create backup files
        for i in range(3):
            (temp_dir / f"file{i}.txt.bak").write_text(f"backup {i}")

        service = UndoService()
        count = service.cleanup_backups(str(temp_dir))

        assert count == 3

        # Verify all backups are gone
        remaining = list(temp_dir.glob("*.bak"))
        assert len(remaining) == 0

    def test_restore_empty_directory(self, temp_dir: Path) -> None:
        """Test restoring from empty directory."""
        service = UndoService()
        results = service.restore_directory(str(temp_dir))

        assert len(results) == 0

    def test_restore_nonexistent_directory(self) -> None:
        """Test error on non-existent directory."""
        service = UndoService()

        with pytest.raises(CodeTrimmerException) as exc_info:
            service.restore_directory("/nonexistent/path")

        assert exc_info.value.error_code == ErrorCode.CT_0010

    def test_restore_subdirectories(self, temp_dir: Path) -> None:
        """Test recursive restore in subdirectories."""
        subdir = temp_dir / "subdir"
        subdir.mkdir()

        # Create backup in subdir
        backup = subdir / "file.txt.bak"
        original = subdir / "file.txt"
        backup.write_text("original")
        original.write_text("modified")

        service = UndoService()
        results = service.restore_directory(str(temp_dir), recursive=True)

        assert len(results) == 1
        assert original.read_text() == "original"
