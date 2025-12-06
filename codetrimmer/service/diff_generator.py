"""Unified diff generator service."""

from dataclasses import dataclass
from enum import Enum
from typing import List


class DiffLineType(Enum):
    """Type of diff line."""

    CONTEXT = " "
    ADDED = "+"
    REMOVED = "-"


@dataclass
class DiffLine:
    """Represents a single line in a diff."""

    line_type: DiffLineType
    content: str
    line_number: int

    def __str__(self) -> str:
        """Return string representation."""
        return f"{self.line_type.value}{self.content}"


@dataclass
class DiffHunk:
    """Represents a diff hunk with context."""

    orig_start: int
    orig_count: int
    mod_start: int
    mod_count: int
    lines: List[DiffLine]

    def __str__(self) -> str:
        """Return string representation."""
        header = f"@@ -{self.orig_start},{self.orig_count} +{self.mod_start},{self.mod_count} @@\n"
        body = "\n".join(str(line) for line in self.lines)
        return header + body


class DiffGenerator:
    """Service for generating unified diff output."""

    CONTEXT_LINES = 3

    def generate_diff(
        self,
        original_content: str,
        modified_content: str,
        file_name: str,
    ) -> str:
        """Generate a unified diff between original and modified content.

        Args:
            original_content: Original file content
            modified_content: Modified content
            file_name: File name for the diff header

        Returns:
            Unified diff as string
        """
        if original_content == modified_content:
            return ""

        original_lines = original_content.split("\n")
        modified_lines = modified_content.split("\n")

        diff_lines = [f"--- a/{file_name}", f"+++ b/{file_name}"]

        hunks = self._compute_hunks(original_lines, modified_lines)
        for hunk in hunks:
            diff_lines.append(str(hunk))

        return "\n".join(diff_lines) + "\n"

    def _compute_hunks(
        self,
        original: List[str],
        modified: List[str],
    ) -> List[DiffHunk]:
        """Compute diff hunks between two line arrays.

        Args:
            original: Original lines
            modified: Modified lines

        Returns:
            List of diff hunks
        """
        all_changes = self._compute_lcs(original, modified)

        if not all_changes:
            return []

        return self._build_hunks(all_changes)

    def _compute_lcs(
        self,
        original: List[str],
        modified: List[str],
    ) -> List[DiffLine]:
        """Compute longest common subsequence based diff.

        Args:
            original: Original lines
            modified: Modified lines

        Returns:
            List of diff lines
        """
        result = []
        orig_idx = 0
        mod_idx = 0

        while orig_idx < len(original) or mod_idx < len(modified):
            if orig_idx >= len(original):
                # Only additions remain
                result.append(
                    DiffLine(DiffLineType.ADDED, modified[mod_idx], mod_idx + 1)
                )
                mod_idx += 1
            elif mod_idx >= len(modified):
                # Only deletions remain
                result.append(
                    DiffLine(DiffLineType.REMOVED, original[orig_idx], orig_idx + 1)
                )
                orig_idx += 1
            elif original[orig_idx] == modified[mod_idx]:
                # Lines match
                result.append(
                    DiffLine(DiffLineType.CONTEXT, original[orig_idx], orig_idx + 1)
                )
                orig_idx += 1
                mod_idx += 1
            else:
                # Lines differ
                change_type = self._find_next_match(
                    original, modified, orig_idx, mod_idx
                )

                if change_type == "modification":
                    result.append(
                        DiffLine(
                            DiffLineType.REMOVED, original[orig_idx], orig_idx + 1
                        )
                    )
                    result.append(
                        DiffLine(DiffLineType.ADDED, modified[mod_idx], mod_idx + 1)
                    )
                    orig_idx += 1
                    mod_idx += 1
                elif change_type == "deletion":
                    result.append(
                        DiffLine(
                            DiffLineType.REMOVED, original[orig_idx], orig_idx + 1
                        )
                    )
                    orig_idx += 1
                else:  # addition
                    result.append(
                        DiffLine(DiffLineType.ADDED, modified[mod_idx], mod_idx + 1)
                    )
                    mod_idx += 1

        return result

    def _find_next_match(
        self,
        original: List[str],
        modified: List[str],
        orig_idx: int,
        mod_idx: int,
    ) -> str:
        """Find the next matching line to determine change type.

        Args:
            original: Original lines
            modified: Modified lines
            orig_idx: Current original index
            mod_idx: Current modified index

        Returns:
            "modification", "deletion", or "addition"
        """
        # Look ahead to find if next original matches current modified
        if (
            orig_idx + 1 < len(original)
            and original[orig_idx + 1] == modified[mod_idx]
        ):
            return "deletion"

        # Look ahead to find if current original matches next modified
        if (
            mod_idx + 1 < len(modified)
            and original[orig_idx] == modified[mod_idx + 1]
        ):
            return "addition"

        return "modification"

    def _build_hunks(self, all_changes: List[DiffLine]) -> List[DiffHunk]:
        """Build hunks from diff lines.

        Args:
            all_changes: All diff lines

        Returns:
            List of diff hunks
        """
        hunks = []
        hunk_start = -1
        current_hunk_lines: List[DiffLine] = []
        last_change_index = -self.CONTEXT_LINES - 1

        for i, line in enumerate(all_changes):
            if line.line_type != DiffLineType.CONTEXT:
                # Handle change line
                if (
                    hunk_start == -1
                    or i - last_change_index > self.CONTEXT_LINES * 2
                ):
                    # Start new hunk
                    if current_hunk_lines:
                        hunks.append(
                            self._create_hunk(current_hunk_lines, hunk_start)
                        )
                        current_hunk_lines = []

                    context_start = max(0, i - self.CONTEXT_LINES)
                    hunk_start = context_start

                    # Add context lines before
                    for j in range(context_start, i):
                        current_hunk_lines.append(all_changes[j])

                last_change_index = i

            if hunk_start != -1:
                if (
                    line.line_type != DiffLineType.CONTEXT
                    or i - last_change_index <= self.CONTEXT_LINES
                ):
                    current_hunk_lines.append(line)
                elif i - last_change_index == self.CONTEXT_LINES + 1:
                    # End of context after change
                    hunks.append(self._create_hunk(current_hunk_lines, hunk_start))
                    current_hunk_lines = []
                    hunk_start = -1

        # Handle remaining hunk
        if current_hunk_lines:
            hunks.append(self._create_hunk(current_hunk_lines, hunk_start))

        return hunks

    def _create_hunk(
        self,
        lines: List[DiffLine],
        start_line: int,
    ) -> DiffHunk:
        """Create a diff hunk from lines.

        Args:
            lines: Diff lines
            start_line: Starting line number

        Returns:
            DiffHunk instance
        """
        orig_start = start_line + 1
        orig_count = 0
        mod_start = start_line + 1
        mod_count = 0

        for line in lines:
            if line.line_type == DiffLineType.REMOVED:
                orig_count += 1
            elif line.line_type == DiffLineType.ADDED:
                mod_count += 1
            else:  # CONTEXT
                orig_count += 1
                mod_count += 1

        return DiffHunk(orig_start, orig_count, mod_start, mod_count, lines)
