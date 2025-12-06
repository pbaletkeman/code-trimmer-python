"""Error codes for Code Trimmer operations.

Format: CT-XXXX where X is a digit.
"""

from enum import Enum


class ErrorCode(Enum):
    """Error codes for Code Trimmer operations."""

    # Configuration errors (CT-0001 to CT-0005)
    CT_0001 = ("CT-0001", "Invalid configuration file", "Configuration file format is invalid")
    CT_0002 = ("CT-0002", "Configuration file not found", "Specified config file does not exist")
    CT_0003 = ("CT-0003", "Invalid configuration value", "Configuration value is out of range")
    CT_0004 = ("CT-0004", "Invalid rule definition", "Custom rule is malformed or missing fields")
    CT_0005 = ("CT-0005", "Invalid regex pattern", "Regex pattern in rule is invalid")

    # File operation errors (CT-0010 to CT-0016)
    CT_0010 = ("CT-0010", "File not found", "Specified file or directory does not exist")
    CT_0011 = ("CT-0011", "File read error", "Cannot read file contents")
    CT_0012 = ("CT-0012", "File write error", "Cannot write to file")
    CT_0013 = ("CT-0013", "Permission denied", "Insufficient permissions to access file")
    CT_0014 = ("CT-0014", "Directory not accessible", "Cannot access or traverse directory")
    CT_0015 = ("CT-0015", "File too large", "File exceeds maximum size limit")
    CT_0016 = ("CT-0016", "Binary file skipped", "Binary file detected and skipped")

    # Backup/Restore errors (CT-0040 to CT-0043)
    CT_0040 = ("CT-0040", "Backup creation failed", "Failed to create backup file")
    CT_0041 = ("CT-0041", "Restore failed", "Failed to restore from backup")
    CT_0042 = ("CT-0042", "Backup file missing", "Backup file not found for restore")
    CT_0043 = ("CT-0043", "Backup file corrupted", "Backup file is corrupted or invalid")

    # Hook generation errors (CT-0050 to CT-0052)
    CT_0050 = ("CT-0050", "Hook generation failed", "Failed to generate pre-commit hook")
    CT_0051 = ("CT-0051", "Git directory not found", ".git directory not found in path")
    CT_0052 = ("CT-0052", "Hook already exists", "Pre-commit hook already exists")

    # Report errors (CT-0060 to CT-0063)
    CT_0060 = ("CT-0060", "Report generation failed", "Failed to generate report")
    CT_0061 = ("CT-0061", "Invalid report format", "Unsupported report format specified")
    CT_0062 = ("CT-0062", "Report endpoint failed", "Failed to send report to endpoint")
    CT_0063 = ("CT-0063", "SQLite database error", "Error writing to SQLite database")

    # General errors (CT-0090 to CT-0092)
    CT_0090 = ("CT-0090", "Unknown error", "An unexpected error occurred")
    CT_0091 = ("CT-0091", "Operation cancelled", "Operation was cancelled by user")
    CT_0092 = ("CT-0092", "Disk full", "Insufficient disk space for operation")

    def __init__(self, code: str, title: str, description: str) -> None:
        """Initialize error code.

        Args:
            code: The error code string (e.g., "CT-0001")
            title: Short title describing the error
            description: Detailed description of the error
        """
        self._code = code
        self._title = title
        self._description = description

    @property
    def code(self) -> str:
        """Get the error code string."""
        return self._code

    @property
    def title(self) -> str:
        """Get the error title."""
        return self._title

    @property
    def description(self) -> str:
        """Get the error description."""
        return self._description

    def __str__(self) -> str:
        """Return string representation of error code."""
        return f"{self._code}: {self._title}"
