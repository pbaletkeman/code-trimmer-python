"""Application constants for Code Trimmer."""


class AppConstants:
    """Application-wide constants."""

    # Application info
    APP_NAME = "codetrimmer"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "A file formatting and whitespace normalization utility"

    # Default configuration values
    DEFAULT_INCLUDE = "*"
    DEFAULT_EXCLUDE = ""
    DEFAULT_MAX_CONSECUTIVE_BLANK_LINES = 2
    DEFAULT_MAX_FILE_SIZE = 5242880  # 5MB in bytes
    DEFAULT_MAX_FILES = 50
    DEFAULT_CONFIG_FILE = ".codetrimmer.yaml"
    DEFAULT_REPORT_OUTPUT = "codetrimmer-report.json"
    DEFAULT_BACKUP_EXTENSION = ".bak"

    # File buffer size for reading
    BUFFER_SIZE = 8192

    # Binary file extensions
    BINARY_EXTENSIONS = frozenset([
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico", ".webp",
        ".mp3", ".mp4", ".wav", ".avi", ".mov", ".mkv", ".flv",
        ".exe", ".dll", ".so", ".dylib", ".bin", ".com", ".msi",
        ".zip", ".rar", ".7z", ".gz", ".tar", ".jar", ".war", ".ear",
        ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
        ".class", ".o", ".pyc", ".pyo", ".swp", ".swo",
        ".git", ".lock", ".cache",
    ])

    # Report formats
    REPORT_FORMATS = frozenset(["json", "csv", "sqlite"])

    # Hook types
    HOOK_TYPES = frozenset(["bash", "batch", "powershell"])
