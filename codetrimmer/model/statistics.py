"""Processing statistics data model."""

from dataclasses import dataclass, field
from typing import Dict, List

from codetrimmer.error.codes import ErrorCode
from codetrimmer.model.file_result import FileProcessingResult


@dataclass
class ProcessingStatistics:
    """Statistics for a processing run.

    Attributes:
        files_processed: Total number of files processed
        files_modified: Number of files that were modified
        files_skipped: Number of files skipped (binary, etc.)
        files_with_errors: Number of files with errors
        total_bytes_trimmed: Total bytes trimmed
        total_execution_time_ms: Total execution time in milliseconds
        errors: Count of each error type encountered
        results: List of individual file results
    """

    files_processed: int = 0
    files_modified: int = 0
    files_skipped: int = 0
    files_with_errors: int = 0
    total_bytes_trimmed: int = 0
    total_execution_time_ms: int = 0
    errors: Dict[ErrorCode, int] = field(default_factory=dict)
    results: List[FileProcessingResult] = field(default_factory=list)

    def add_result(self, result: FileProcessingResult) -> None:
        """Add a file processing result.

        Args:
            result: The file processing result to add
        """
        self.results.append(result)
        self.files_processed += 1

        if result.was_modified:
            self.files_modified += 1
            self.total_bytes_trimmed += result.bytes_modified

        if result.error:
            self.files_with_errors += 1
            error_count = self.errors.get(result.error, 0)
            self.errors[result.error] = error_count + 1

    def add_skipped(self) -> None:
        """Increment the skipped files counter."""
        self.files_skipped += 1

    def set_execution_time(self, time_ms: int) -> None:
        """Set the total execution time.

        Args:
            time_ms: Execution time in milliseconds
        """
        self.total_execution_time_ms = time_ms

    def to_dict(self) -> Dict:
        """Convert statistics to dictionary for reporting.

        Returns:
            Dictionary representation of statistics
        """
        return {
            "files_processed": self.files_processed,
            "files_modified": self.files_modified,
            "files_skipped": self.files_skipped,
            "files_with_errors": self.files_with_errors,
            "total_bytes_trimmed": self.total_bytes_trimmed,
            "total_execution_time_ms": self.total_execution_time_ms,
            "errors": {
                error.code: count for error, count in self.errors.items()
            },
            "results": [
                {
                    "file_path": r.file_path,
                    "was_modified": r.was_modified,
                    "bytes_modified": r.bytes_modified,
                    "error": r.error.code if r.error else None,
                    "error_message": r.error_message,
                    "backup_path": r.backup_path,
                    "processing_time_ms": r.processing_time_ms,
                }
                for r in self.results
            ],
        }

    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"ProcessingStatistics(processed={self.files_processed}, "
            f"modified={self.files_modified}, skipped={self.files_skipped}, "
            f"errors={self.files_with_errors})"
        )
