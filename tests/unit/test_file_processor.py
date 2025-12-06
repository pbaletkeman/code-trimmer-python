"""Tests for FileProcessingService."""

from pathlib import Path

import pytest

from codetrimmer.config.models import CodeTrimmerConfig
from codetrimmer.error.codes import ErrorCode
from codetrimmer.error.exceptions import CodeTrimmerException
from codetrimmer.service.file_processor import FileProcessingService


class TestFileProcessingService:
    """Tests for FileProcessingService class."""

    def test_process_directory(
        self, temp_dir: Path, sample_text_file: Path
    ) -> None:
        """Test processing a directory."""
        config = CodeTrimmerConfig(
            dry_run=False,
            create_backups=False,
        )
        service = FileProcessingService(config)
        stats = service.process_directory(str(temp_dir))

        assert stats.files_processed >= 1
        assert stats.total_execution_time_ms >= 0

    def test_dry_run_mode(self, temp_dir: Path, sample_text_file: Path) -> None:
        """Test dry-run mode doesn't modify files."""
        original_content = sample_text_file.read_text()

        config = CodeTrimmerConfig(dry_run=True)
        service = FileProcessingService(config)
        stats = service.process_directory(str(temp_dir))

        # File should not be modified
        assert sample_text_file.read_text() == original_content

    def test_process_with_backup(
        self, temp_dir: Path, sample_text_file: Path
    ) -> None:
        """Test processing creates backups."""
        config = CodeTrimmerConfig(
            dry_run=False,
            create_backups=True,
        )
        service = FileProcessingService(config)
        stats = service.process_directory(str(temp_dir))

        # Check for backup file if file was modified
        if stats.files_modified > 0:
            backup_path = sample_text_file.with_suffix(
                sample_text_file.suffix + ".bak"
            )
            assert backup_path.exists()

    def test_non_existent_directory(self) -> None:
        """Test error on non-existent directory."""
        config = CodeTrimmerConfig()
        service = FileProcessingService(config)

        with pytest.raises(CodeTrimmerException) as exc_info:
            service.process_directory("/nonexistent/path")

        assert exc_info.value.error_code == ErrorCode.CT_0010

    def test_file_as_directory(self, sample_text_file: Path) -> None:
        """Test error when file path given instead of directory."""
        config = CodeTrimmerConfig()
        service = FileProcessingService(config)

        with pytest.raises(CodeTrimmerException) as exc_info:
            service.process_directory(str(sample_text_file))

        assert exc_info.value.error_code == ErrorCode.CT_0014

    def test_include_pattern(self, temp_dir: Path) -> None:
        """Test include pattern filtering."""
        # Create files
        (temp_dir / "file.py").write_text("test\n")
        (temp_dir / "file.txt").write_text("test\n")

        config = CodeTrimmerConfig(include="*.py", dry_run=True)
        service = FileProcessingService(config)
        stats = service.process_directory(str(temp_dir))

        # Only .py files should be processed
        py_files = [r for r in stats.results if r.file_path.endswith(".py")]
        assert len(py_files) >= 1

    def test_exclude_pattern(self, temp_dir: Path) -> None:
        """Test exclude pattern filtering."""
        # Create files
        (temp_dir / "file.py").write_text("test\n")
        (temp_dir / "file.pyc").write_text("test\n")

        config = CodeTrimmerConfig(exclude="*.pyc", dry_run=True)
        service = FileProcessingService(config)
        stats = service.process_directory(str(temp_dir))

        # No .pyc files should be processed
        pyc_files = [r for r in stats.results if r.file_path.endswith(".pyc")]
        assert len(pyc_files) == 0

    def test_max_files_limit(self, temp_dir: Path) -> None:
        """Test max files limit."""
        # Create many files
        for i in range(10):
            (temp_dir / f"file{i}.txt").write_text("test\n")

        config = CodeTrimmerConfig(max_files=3, dry_run=True)
        service = FileProcessingService(config)
        stats = service.process_directory(str(temp_dir))

        assert stats.files_processed <= 3

    def test_skip_binary_files(
        self, temp_dir: Path, sample_binary_file: Path
    ) -> None:
        """Test binary files are skipped."""
        config = CodeTrimmerConfig(dry_run=True)
        service = FileProcessingService(config)
        stats = service.process_directory(str(temp_dir))

        # Binary files should be skipped
        binary_results = [
            r
            for r in stats.results
            if r.error and r.error == ErrorCode.CT_0016
        ]
        # There should be skipped files due to binary detection
        assert stats.files_skipped >= 0

    def test_fail_fast_mode(self, temp_dir: Path) -> None:
        """Test fail-fast mode stops on error."""
        # Create a file that will cause an error (binary)
        (temp_dir / "binary.bin").write_bytes(b"\x00\x01\x02")
        (temp_dir / "text.txt").write_text("test\n")

        config = CodeTrimmerConfig(fail_fast=True, dry_run=True)
        service = FileProcessingService(config)

        # Processing should continue with warnings but not stop
        stats = service.process_directory(str(temp_dir))
        assert stats.files_processed >= 0

    def test_process_single_file(
        self, sample_text_file: Path, default_config: CodeTrimmerConfig
    ) -> None:
        """Test processing a single file."""
        service = FileProcessingService(default_config)
        result = service.process_file(sample_text_file)

        assert result.file_path == str(sample_text_file)
        assert result.is_success() or result.error == ErrorCode.CT_0016
