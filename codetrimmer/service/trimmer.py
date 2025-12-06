"""File trimming service."""

import re
from dataclasses import dataclass
from typing import List

from codetrimmer.config.models import CodeTrimmerConfig, TrimRule


@dataclass
class TrimResult:
    """Result of a trim operation.

    Attributes:
        content: The trimmed content
        lines_trimmed: Number of lines with trailing whitespace removed
        blank_lines_removed: Number of excessive blank lines removed
    """

    content: str
    lines_trimmed: int = 0
    blank_lines_removed: int = 0


class FileTrimmer:
    """Service for trimming whitespace from file content."""

    def __init__(self, content: str, config: CodeTrimmerConfig) -> None:
        """Initialize the trimmer.

        Args:
            content: The file content to trim
            config: Configuration options
        """
        self.content = content
        self.config = config

    def trim(self) -> TrimResult:
        """Apply all trimming rules to the content.

        Returns:
            TrimResult with modified content and statistics
        """
        result = self.content
        lines_trimmed = 0
        blank_lines_removed = 0

        # Trim trailing whitespace from lines
        if self.config.trim_trailing_whitespace:
            result, lines_trimmed = self._trim_trailing_whitespace(result)

        # Reduce excessive blank lines
        result, blank_lines_removed = self._reduce_consecutive_blank_lines(result)

        # Apply custom rules
        if self.config.rules:
            result = self._apply_custom_rules(result, self.config.rules)

        # Ensure final newline
        if self.config.ensure_final_newline:
            result = self._ensure_final_newline(result)

        return TrimResult(result, lines_trimmed, blank_lines_removed)

    def _trim_trailing_whitespace(self, text: str) -> tuple[str, int]:
        """Trim trailing whitespace from all lines.

        Args:
            text: Text to process

        Returns:
            Tuple of (processed text, number of lines trimmed)
        """
        lines = text.split("\n")
        trimmed_count = 0
        result_lines = []

        for line in lines:
            trimmed = line.rstrip()
            if trimmed != line:
                trimmed_count += 1
            result_lines.append(trimmed)

        return "\n".join(result_lines), trimmed_count

    def _reduce_consecutive_blank_lines(self, text: str) -> tuple[str, int]:
        """Reduce consecutive blank lines to the maximum allowed.

        Args:
            text: Text to process

        Returns:
            Tuple of (processed text, number of blank lines removed)
        """
        lines = text.split("\n")
        max_blank = self.config.max_consecutive_blank_lines
        result_lines = []
        consecutive_blank = 0
        removed_count = 0

        for line in lines:
            if line.strip() == "":
                consecutive_blank += 1
                if consecutive_blank <= max_blank:
                    result_lines.append(line)
                else:
                    removed_count += 1
            else:
                consecutive_blank = 0
                result_lines.append(line)

        return "\n".join(result_lines), removed_count

    def _apply_custom_rules(self, text: str, rules: List[TrimRule]) -> str:
        """Apply custom regex-based rules.

        Args:
            text: Text to process
            rules: List of custom rules to apply

        Returns:
            Processed text
        """
        result = text
        for rule in rules:
            try:
                result = re.sub(rule.pattern, rule.replacement, result)
            except re.error:
                # Skip invalid patterns (should be validated earlier)
                continue
        return result

    def _ensure_final_newline(self, text: str) -> str:
        """Ensure the file ends with exactly one newline.

        Args:
            text: Text to process

        Returns:
            Text with single final newline
        """
        if not text:
            return "\n"

        # Remove all trailing newlines
        text = text.rstrip("\n")

        # Add single newline
        return text + "\n"

    @staticmethod
    def trim_line(line: str) -> str:
        """Trim trailing whitespace from a single line.

        Args:
            line: Line to trim

        Returns:
            Trimmed line
        """
        return line.rstrip()
