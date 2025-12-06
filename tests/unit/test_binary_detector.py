"""Tests for BinaryFileDetector."""

from pathlib import Path

import pytest

from codetrimmer.model.binary_detector import BinaryFileDetector


class TestBinaryFileDetector:
    """Tests for BinaryFileDetector class."""

    def test_detect_binary_file(self, sample_binary_file: Path) -> None:
        """Test detecting binary file by content."""
        assert BinaryFileDetector.is_binary(sample_binary_file) is True

    def test_detect_text_file(self, sample_text_file: Path) -> None:
        """Test detecting text file."""
        assert BinaryFileDetector.is_binary(sample_text_file) is False

    def test_detect_by_extension_binary(self, temp_dir: Path) -> None:
        """Test detecting binary by extension."""
        binary_path = temp_dir / "image.jpg"
        binary_path.touch()
        assert BinaryFileDetector.is_binary_by_extension(binary_path) is True

    def test_detect_by_extension_text(self, temp_dir: Path) -> None:
        """Test detecting text by extension."""
        text_path = temp_dir / "code.py"
        text_path.touch()
        assert BinaryFileDetector.is_binary_by_extension(text_path) is False

    def test_binary_extensions(self, temp_dir: Path) -> None:
        """Test various binary extensions."""
        binary_extensions = [
            ".jpg", ".png", ".gif", ".exe", ".dll",
            ".zip", ".pdf", ".mp3", ".mp4",
        ]
        for ext in binary_extensions:
            path = temp_dir / f"file{ext}"
            path.touch()
            assert BinaryFileDetector.is_binary_by_extension(path) is True

    def test_text_extensions(self, temp_dir: Path) -> None:
        """Test various text extensions."""
        text_extensions = [".py", ".js", ".java", ".md", ".txt", ".html"]
        for ext in text_extensions:
            path = temp_dir / f"file{ext}"
            path.touch()
            assert BinaryFileDetector.is_binary_by_extension(path) is False

    def test_should_skip_binary(self, sample_binary_file: Path) -> None:
        """Test should_skip for binary file."""
        assert BinaryFileDetector.should_skip(sample_binary_file) is True

    def test_should_not_skip_text(self, sample_text_file: Path) -> None:
        """Test should_skip for text file."""
        assert BinaryFileDetector.should_skip(sample_text_file) is False

    def test_non_existent_file(self, temp_dir: Path) -> None:
        """Test handling non-existent file."""
        non_existent = temp_dir / "nonexistent.txt"
        # Should return True (assume binary) if file can't be read
        assert BinaryFileDetector.is_binary(non_existent) is True

    def test_file_with_null_byte(self, temp_dir: Path) -> None:
        """Test detecting file with null byte."""
        file_path = temp_dir / "mixed.txt"
        file_path.write_bytes(b"Hello\x00World")
        assert BinaryFileDetector.is_binary(file_path) is True

    def test_empty_file(self, temp_dir: Path) -> None:
        """Test empty file detection."""
        empty_file = temp_dir / "empty.txt"
        empty_file.touch()
        assert BinaryFileDetector.is_binary(empty_file) is False

    def test_string_path_input(self, sample_text_file: Path) -> None:
        """Test with string path input."""
        assert BinaryFileDetector.is_binary(str(sample_text_file)) is False
