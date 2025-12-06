"""Configuration data models for Code Trimmer."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TrimRule:
    """A custom trimming rule definition.

    Attributes:
        name: Name of the rule
        pattern: Regex pattern to match
        replacement: Replacement string
        description: Description of what the rule does
    """

    name: str
    pattern: str
    replacement: str = ""
    description: str = ""


@dataclass
class TrimmerConfig:
    """Configuration loaded from .codetrimmer.yaml or .codetrimmer.json.

    This represents the configuration file structure.
    """

    # File filtering
    include: str = "*"
    exclude: str = ""
    include_hidden: bool = False
    follow_symlinks: bool = False

    # Whitespace rules
    max_consecutive_blank_lines: int = 2
    ensure_final_newline: bool = True
    trim_trailing_whitespace: bool = True

    # Performance limits
    max_file_size: int = 5242880  # 5MB in bytes
    max_files: int = 50
    no_limits: bool = False

    # Operation modes
    dry_run: bool = False
    create_backups: bool = True
    fail_fast: bool = False

    # Output options
    verbose: bool = False
    quiet: bool = False
    no_color: bool = False
    disable_color_for_pipe: bool = True

    # Reporting
    report: Optional[str] = None
    report_output: str = "codetrimmer-report.json"
    report_endpoint: Optional[str] = None

    # Diff output
    diff: bool = False

    # Custom rules
    rules: List[TrimRule] = field(default_factory=list)


@dataclass
class CodeTrimmerConfig:
    """Runtime configuration for Code Trimmer application.

    This combines configuration from files, environment variables,
    and CLI options.
    """

    # File filtering
    include: str = "*"
    exclude: str = ""
    include_hidden: bool = False
    follow_symlinks: bool = False

    # Whitespace rules
    max_consecutive_blank_lines: int = 2
    ensure_final_newline: bool = True
    trim_trailing_whitespace: bool = True

    # Performance limits
    max_file_size: int = 5242880  # 5MB in bytes
    max_files: int = 50
    no_limits: bool = False

    # Operation modes
    dry_run: bool = False
    create_backups: bool = True
    fail_fast: bool = False

    # Output options
    verbose: bool = False
    quiet: bool = False
    no_color: bool = False
    disable_color_for_pipe: bool = True

    # Reporting
    report: Optional[str] = None
    report_output: str = "codetrimmer-report.json"
    report_endpoint: Optional[str] = None

    # Diff output
    diff: bool = False

    # Custom rules
    rules: List[TrimRule] = field(default_factory=list)

    # Input/Output directories
    input_directory: str = "."
    output_directory: Optional[str] = None

    # Config file path
    config_path: Optional[str] = None

    def is_trim_trailing_whitespace(self) -> bool:
        """Check if trailing whitespace trimming is enabled."""
        return self.trim_trailing_whitespace

    def is_ensure_final_newline(self) -> bool:
        """Check if final newline enforcement is enabled."""
        return self.ensure_final_newline

    def get_max_consecutive_blank_lines(self) -> int:
        """Get maximum consecutive blank lines allowed."""
        return self.max_consecutive_blank_lines
