"""File processing result data model."""

from dataclasses import dataclass
from typing import Optional

from codetrimmer.error.codes import ErrorCode


@dataclass
class FileProcessingResult:
    """Result of processing a single file.

    Attributes:
        file_path: Path to the processed file
        was_modified: Whether the file was modified
        bytes_modified: Number of bytes changed
        error: Optional error code if processing failed
        error_message: Error message if processing failed
        backup_path: Path to backup file if created
        processing_time_ms: Time taken to process in milliseconds
    """

    file_path: str
    was_modified: bool = False
    bytes_modified: int = 0
    error: Optional[ErrorCode] = None
    error_message: str = ""
    backup_path: Optional[str] = None
    processing_time_ms: int = 0

    def is_success(self) -> bool:
        """Check if processing was successful."""
        return self.error is None

    def is_error(self) -> bool:
        """Check if processing resulted in an error."""
        return self.error is not None

    def __repr__(self) -> str:
        """Return string representation."""
        status = "modified" if self.was_modified else "unchanged"
        if self.error:
            status = f"error: {self.error.code}"
        return f"FileProcessingResult({self.file_path!r}, {status})"
