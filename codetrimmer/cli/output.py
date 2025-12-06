"""CLI output handler."""

import sys


from codetrimmer.model.statistics import ProcessingStatistics
from codetrimmer.util.color import ColorOutput


class OutputHandler:
    """Handler for CLI output with color support."""

    def __init__(
        self,
        quiet: bool = False,
        verbose: bool = False,
        no_color: bool = False,
        disable_color_for_pipe: bool = True,
    ) -> None:
        """Initialize output handler.

        Args:
            quiet: If True, minimize output
            verbose: If True, show detailed output
            no_color: If True, disable colors
            disable_color_for_pipe: If True, disable colors when piped
        """
        self.quiet = quiet
        self.verbose = verbose
        self.color = ColorOutput(no_color, disable_color_for_pipe)

    def print(self, message: str = "") -> None:
        """Print message if not in quiet mode.

        Args:
            message: Message to print
        """
        if not self.quiet:
            print(message)

    def print_verbose(self, message: str) -> None:
        """Print message if in verbose mode.

        Args:
            message: Message to print
        """
        if self.verbose:
            print(message)

    def print_error(self, message: str) -> None:
        """Print error message to stderr.

        Args:
            message: Error message
        """
        print(self.color.error(f"Error: {message}"), file=sys.stderr)

    def print_warning(self, message: str) -> None:
        """Print warning message.

        Args:
            message: Warning message
        """
        if not self.quiet:
            print(self.color.warning(f"Warning: {message}"))

    def print_success(self, message: str) -> None:
        """Print success message.

        Args:
            message: Success message
        """
        if not self.quiet:
            print(self.color.success(message))

    def print_info(self, message: str) -> None:
        """Print info message.

        Args:
            message: Info message
        """
        if not self.quiet:
            print(self.color.info(message))

    def print_file_modified(self, file_path: str, bytes_changed: int) -> None:
        """Print file modification message.

        Args:
            file_path: Path to modified file
            bytes_changed: Number of bytes changed
        """
        if self.verbose:
            msg = f"  {self.color.green('✓')} {file_path} ({bytes_changed} bytes)"
            print(msg)

    def print_file_skipped(self, file_path: str, reason: str) -> None:
        """Print file skipped message.

        Args:
            file_path: Path to skipped file
            reason: Reason for skipping
        """
        if self.verbose:
            msg = f"  {self.color.yellow('○')} {file_path} ({reason})"
            print(msg)

    def print_file_error(self, file_path: str, error: str) -> None:
        """Print file error message.

        Args:
            file_path: Path to file with error
            error: Error message
        """
        msg = f"  {self.color.red('✗')} {file_path}: {error}"
        print(msg, file=sys.stderr)

    def print_statistics(self, stats: ProcessingStatistics) -> None:
        """Print processing statistics.

        Args:
            stats: Processing statistics
        """
        if self.quiet:
            return

        print()
        print(self.color.bold("Summary:"))
        print(f"  Files processed: {stats.files_processed}")
        print(f"  Files modified:  {self.color.green(str(stats.files_modified))}")
        print(f"  Files skipped:   {stats.files_skipped}")

        if stats.files_with_errors > 0:
            print(
                f"  Files with errors: {self.color.red(str(stats.files_with_errors))}"
            )

        print(f"  Bytes trimmed:   {stats.total_bytes_trimmed}")
        print(f"  Time:            {stats.total_execution_time_ms}ms")

    def print_dry_run_notice(self) -> None:
        """Print dry-run mode notice."""
        if not self.quiet:
            print(self.color.cyan("Dry-run mode: no files will be modified"))
            print()

    def print_header(self, directory: str) -> None:
        """Print processing header.

        Args:
            directory: Directory being processed
        """
        if not self.quiet:
            print(self.color.bold(f"Processing: {directory}"))
            print()
