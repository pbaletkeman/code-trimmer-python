"""CLI options for Code Trimmer."""

from dataclasses import dataclass, field
from typing import Optional, Set


@dataclass
class TrimOptions:
    """Configuration options for the code trimmer.

    Mirrors the CLI options and can be built from Click context.
    """

    # Input/output paths
    input_directory: str = "."
    output_directory: Optional[str] = None

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
    max_file_size: int = 5242880  # 5MB
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

    # Configuration
    config: Optional[str] = None

    # Reporting
    report: Optional[str] = None
    report_output: str = "codetrimmer-report.json"
    report_endpoint: Optional[str] = None

    # Diff output
    diff: bool = False

    # Included/excluded file types (built from patterns)
    included_file_types: Set[str] = field(default_factory=set)
    excluded_file_types: Set[str] = field(default_factory=set)

    def include_file_type(self, file_type: str) -> None:
        """Add a file type to the inclusion list.

        Args:
            file_type: File type extension to include
        """
        self.included_file_types.add(file_type)

    def exclude_file_type(self, file_type: str) -> None:
        """Add a file type to the exclusion list.

        Args:
            file_type: File type extension to exclude
        """
        self.excluded_file_types.add(file_type)

    def is_file_type_included(self, file_type: str) -> bool:
        """Check if a file type is included.

        Args:
            file_type: File type to check

        Returns:
            True if file type is included
        """
        if not self.included_file_types:
            return True
        return file_type in self.included_file_types

    def is_file_type_excluded(self, file_type: str) -> bool:
        """Check if a file type is excluded.

        Args:
            file_type: File type to check

        Returns:
            True if file type is excluded
        """
        return file_type in self.excluded_file_types

    @classmethod
    def from_click_context(cls, ctx: dict) -> "TrimOptions":
        """Create TrimOptions from Click context parameters.

        Args:
            ctx: Click context parameters dictionary

        Returns:
            TrimOptions instance
        """
        return cls(
            input_directory=ctx.get("directory", "."),
            include=ctx.get("include", "*"),
            exclude=ctx.get("exclude", ""),
            include_hidden=ctx.get("include_hidden", False),
            follow_symlinks=ctx.get("follow_symlinks", False),
            max_consecutive_blank_lines=ctx.get("max_consecutive_blank_lines", 2),
            ensure_final_newline=ctx.get("ensure_final_newline", True),
            trim_trailing_whitespace=ctx.get("trim_trailing_whitespace", True),
            max_file_size=ctx.get("max_file_size", 5242880),
            max_files=ctx.get("max_files", 50),
            no_limits=ctx.get("no_limits", False),
            dry_run=ctx.get("dry_run", False),
            create_backups=ctx.get("create_backups", True),
            fail_fast=ctx.get("fail_fast", False),
            verbose=ctx.get("verbose", False),
            quiet=ctx.get("quiet", False),
            no_color=ctx.get("no_color", False),
            disable_color_for_pipe=ctx.get("disable_color_for_pipe", True),
            config=ctx.get("config"),
            report=ctx.get("report"),
            report_output=ctx.get("report_output", "codetrimmer-report.json"),
            report_endpoint=ctx.get("report_endpoint"),
            diff=ctx.get("diff", False),
        )

    def __str__(self) -> str:
        """Return string representation."""
        return (
            f"TrimOptions(input={self.input_directory!r}, "
            f"dry_run={self.dry_run}, verbose={self.verbose})"
        )
