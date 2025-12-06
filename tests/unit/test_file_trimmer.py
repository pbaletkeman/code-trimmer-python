"""Tests for FileTrimmer."""

import pytest

from codetrimmer.config.models import CodeTrimmerConfig, TrimRule
from codetrimmer.service.trimmer import FileTrimmer, TrimResult


class TestFileTrimmer:
    """Tests for FileTrimmer class."""

    def test_trim_trailing_whitespace(self, default_config: CodeTrimmerConfig) -> None:
        """Test trimming trailing whitespace."""
        content = "Hello World   \nLine 2  \nLine 3\n"
        trimmer = FileTrimmer(content, default_config)
        result = trimmer.trim()

        assert "Hello World   " not in result.content
        assert "Line 2  " not in result.content
        assert result.lines_trimmed >= 2

    def test_reduce_blank_lines(self, default_config: CodeTrimmerConfig) -> None:
        """Test reducing consecutive blank lines."""
        content = "Line 1\n\n\n\n\nLine 2\n"
        trimmer = FileTrimmer(content, default_config)
        result = trimmer.trim()

        # Count blank lines in result
        blank_count = 0
        prev_blank = False
        consecutive = 0
        max_consecutive = 0

        for line in result.content.split("\n"):
            if line.strip() == "":
                consecutive += 1
                max_consecutive = max(max_consecutive, consecutive)
            else:
                consecutive = 0

        assert max_consecutive <= default_config.max_consecutive_blank_lines

    def test_ensure_final_newline(self, default_config: CodeTrimmerConfig) -> None:
        """Test ensuring final newline."""
        content = "Hello World"
        trimmer = FileTrimmer(content, default_config)
        result = trimmer.trim()

        assert result.content.endswith("\n")

    def test_no_final_newline_when_disabled(self) -> None:
        """Test no final newline when disabled."""
        config = CodeTrimmerConfig(ensure_final_newline=False)
        content = "Hello World"
        trimmer = FileTrimmer(content, config)
        result = trimmer.trim()

        # Content shouldn't change if no other issues
        assert result.content == "Hello World"

    def test_apply_custom_rules(self) -> None:
        """Test applying custom regex rules."""
        config = CodeTrimmerConfig(
            rules=[
                TrimRule(name="foo-to-bar", pattern="foo", replacement="bar")
            ]
        )
        content = "foo and foo again\n"
        trimmer = FileTrimmer(content, config)
        result = trimmer.trim()

        assert "foo" not in result.content
        assert "bar and bar again" in result.content

    def test_empty_content(self, default_config: CodeTrimmerConfig) -> None:
        """Test trimming empty content."""
        content = ""
        trimmer = FileTrimmer(content, default_config)
        result = trimmer.trim()

        # Should have at least a newline
        assert result.content == "\n"

    def test_already_clean_content(self, default_config: CodeTrimmerConfig) -> None:
        """Test content that doesn't need trimming."""
        content = "Clean content\nNo trailing spaces\n"
        trimmer = FileTrimmer(content, default_config)
        result = trimmer.trim()

        assert result.content == content
        assert result.lines_trimmed == 0
        assert result.blank_lines_removed == 0

    def test_multiple_trailing_newlines(self, default_config: CodeTrimmerConfig) -> None:
        """Test handling multiple trailing newlines."""
        content = "Content\n\n\n\n"
        trimmer = FileTrimmer(content, default_config)
        result = trimmer.trim()

        # Should end with exactly one newline
        assert result.content.endswith("\n")
        assert not result.content.endswith("\n\n")

    def test_trim_line_static_method(self) -> None:
        """Test static trim_line method."""
        assert FileTrimmer.trim_line("Hello   ") == "Hello"
        assert FileTrimmer.trim_line("  Hello  ") == "  Hello"
        assert FileTrimmer.trim_line("\t\t") == ""

    def test_trim_result_dataclass(self) -> None:
        """Test TrimResult dataclass."""
        result = TrimResult(content="test\n", lines_trimmed=5, blank_lines_removed=2)

        assert result.content == "test\n"
        assert result.lines_trimmed == 5
        assert result.blank_lines_removed == 2

    def test_disable_trailing_whitespace_trimming(self) -> None:
        """Test disabling trailing whitespace trimming."""
        config = CodeTrimmerConfig(trim_trailing_whitespace=False)
        content = "Hello World   \n"
        trimmer = FileTrimmer(content, config)
        result = trimmer.trim()

        # Trailing whitespace should be preserved
        assert "Hello World   " in result.content

    def test_custom_max_blank_lines(self) -> None:
        """Test custom max consecutive blank lines setting."""
        config = CodeTrimmerConfig(max_consecutive_blank_lines=1)
        content = "Line 1\n\n\n\nLine 2\n"
        trimmer = FileTrimmer(content, config)
        result = trimmer.trim()

        # Should have at most 1 consecutive blank line
        lines = result.content.split("\n")
        consecutive = 0
        max_consecutive = 0

        for line in lines:
            if line.strip() == "":
                consecutive += 1
                max_consecutive = max(max_consecutive, consecutive)
            else:
                consecutive = 0

        assert max_consecutive <= 1
