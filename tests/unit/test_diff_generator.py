"""Tests for DiffGenerator."""

import pytest

from codetrimmer.service.diff_generator import DiffGenerator, DiffLineType


class TestDiffGenerator:
    """Tests for DiffGenerator class."""

    def test_identical_content(self) -> None:
        """Test diff with identical content."""
        generator = DiffGenerator()
        diff = generator.generate_diff("content\n", "content\n", "file.txt")
        assert diff == ""

    def test_simple_change(self) -> None:
        """Test diff with simple change."""
        generator = DiffGenerator()
        original = "Hello\n"
        modified = "Hello World\n"

        diff = generator.generate_diff(original, modified, "file.txt")

        assert "--- a/file.txt" in diff
        assert "+++ b/file.txt" in diff
        assert "-Hello" in diff
        assert "+Hello World" in diff

    def test_line_addition(self) -> None:
        """Test diff with added lines."""
        generator = DiffGenerator()
        original = "Line 1\n"
        modified = "Line 1\nLine 2\n"

        diff = generator.generate_diff(original, modified, "file.txt")

        assert "+Line 2" in diff

    def test_line_removal(self) -> None:
        """Test diff with removed lines."""
        generator = DiffGenerator()
        original = "Line 1\nLine 2\n"
        modified = "Line 1\n"

        diff = generator.generate_diff(original, modified, "file.txt")

        assert "-Line 2" in diff

    def test_multiple_changes(self) -> None:
        """Test diff with multiple changes."""
        generator = DiffGenerator()
        original = "Line 1\nLine 2\nLine 3\n"
        modified = "Line 1\nModified\nLine 3\nLine 4\n"

        diff = generator.generate_diff(original, modified, "file.txt")

        assert "-Line 2" in diff
        assert "+Modified" in diff
        assert "+Line 4" in diff

    def test_diff_header(self) -> None:
        """Test diff header format."""
        generator = DiffGenerator()
        diff = generator.generate_diff("a\n", "b\n", "test.py")

        assert "--- a/test.py" in diff
        assert "+++ b/test.py" in diff

    def test_hunk_header(self) -> None:
        """Test diff hunk header format."""
        generator = DiffGenerator()
        diff = generator.generate_diff("old\n", "new\n", "file.txt")

        # Should contain @@ markers
        assert "@@" in diff

    def test_diff_line_types(self) -> None:
        """Test DiffLineType enum."""
        assert DiffLineType.CONTEXT.value == " "
        assert DiffLineType.ADDED.value == "+"
        assert DiffLineType.REMOVED.value == "-"

    def test_empty_files(self) -> None:
        """Test diff between empty and non-empty."""
        generator = DiffGenerator()
        diff = generator.generate_diff("", "content\n", "file.txt")

        assert "+content" in diff

    def test_whitespace_changes(self) -> None:
        """Test diff with whitespace-only changes."""
        generator = DiffGenerator()
        original = "Hello World   \n"
        modified = "Hello World\n"

        diff = generator.generate_diff(original, modified, "file.txt")

        assert diff != ""  # Should detect the difference
