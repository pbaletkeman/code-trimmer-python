"""Custom exceptions for Code Trimmer."""

from typing import Optional

from codetrimmer.error.codes import ErrorCode


class CodeTrimmerException(Exception):
    """Exception class for Code Trimmer operations.

    Provides structured error information including error code,
    cause, and suggestions for resolution.
    """

    def __init__(
        self,
        error_code: ErrorCode,
        cause: Optional[str] = None,
        suggestion: Optional[str] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            error_code: The error code enum value
            cause: Optional cause of the error
            suggestion: Optional suggestion for resolution
        """
        self.error_code = error_code
        self.cause = cause
        self.suggestion = suggestion
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        """Format the full error message."""
        parts = [f"[{self.error_code.code}] {self.error_code.title}"]
        parts.append(f"Description: {self.error_code.description}")

        if self.cause:
            parts.append(f"Cause: {self.cause}")

        if self.suggestion:
            parts.append(f"Suggestion: {self.suggestion}")

        return "\n".join(parts)

    def __str__(self) -> str:
        """Return string representation of the exception."""
        return self._format_message()

    def __repr__(self) -> str:
        """Return detailed representation of the exception."""
        return (
            f"CodeTrimmerException(error_code={self.error_code!r}, "
            f"cause={self.cause!r}, suggestion={self.suggestion!r})"
        )
