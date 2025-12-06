"""File processing service."""

import fnmatch
import logging
import os
import shutil
import time
from pathlib import Path
from typing import List, Optional

from codetrimmer.config.loader import ConfigurationLoader
from codetrimmer.config.models import CodeTrimmerConfig
from codetrimmer.error.codes import ErrorCode
from codetrimmer.error.exceptions import CodeTrimmerException
from codetrimmer.model.binary_detector import BinaryFileDetector
from codetrimmer.model.file_result import FileProcessingResult
from codetrimmer.model.statistics import ProcessingStatistics
from codetrimmer.service.diff_generator import DiffGenerator
from codetrimmer.service.trimmer import FileTrimmer
from codetrimmer.util.constants import AppConstants

logger = logging.getLogger(__name__)


class FileProcessingService:
    """Main orchestrator for file processing operations."""

    def __init__(self, config: Optional[CodeTrimmerConfig] = None) -> None:
        """Initialize the service.

        Args:
            config: Optional runtime configuration
        """
        self.config = config or CodeTrimmerConfig()
        self.config_loader = ConfigurationLoader()
        self.diff_generator = DiffGenerator()
        self.stats = ProcessingStatistics()

    def process_directory(self, directory: str) -> ProcessingStatistics:
        """Process all files in a directory.

        Args:
            directory: Path to directory to process

        Returns:
            Processing statistics
        """
        start_time = time.time()
        dir_path = Path(directory)

        if not dir_path.exists():
            raise CodeTrimmerException(
                ErrorCode.CT_0010,
                f"Directory not found: {directory}",
                "Verify the directory path exists",
            )

        if not dir_path.is_dir():
            raise CodeTrimmerException(
                ErrorCode.CT_0014,
                f"Path is not a directory: {directory}",
                "Provide a valid directory path",
            )

        # Discover files
        files = self._discover_files(dir_path)
        logger.info("Found %d files to process", len(files))

        # Apply file limit
        if not self.config.no_limits and len(files) > self.config.max_files:
            files = files[: self.config.max_files]
            logger.warning(
                "Limiting to %d files (use --no-limits to process all)",
                self.config.max_files,
            )

        # Process each file
        for file_path in files:
            if self.config.fail_fast and self.stats.files_with_errors > 0:
                logger.warning("Stopping due to --fail-fast")
                break

            result = self.process_file(file_path)
            self.stats.add_result(result)

        end_time = time.time()
        self.stats.set_execution_time(int((end_time - start_time) * 1000))

        return self.stats

    def process_file(self, file_path: Path) -> FileProcessingResult:
        """Process a single file.

        Args:
            file_path: Path to file to process

        Returns:
            File processing result
        """
        start_time = time.time()
        result = FileProcessingResult(file_path=str(file_path))

        try:
            # Check if binary
            if BinaryFileDetector.should_skip(file_path):
                result.error = ErrorCode.CT_0016
                result.error_message = "Binary file skipped"
                self.stats.add_skipped()
                return result

            # Check file size
            file_size = file_path.stat().st_size
            if not self.config.no_limits and file_size > self.config.max_file_size:
                result.error = ErrorCode.CT_0015
                result.error_message = f"File too large: {file_size} bytes"
                return result

            # Read file content
            try:
                original_content = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                # Try with latin-1 as fallback
                try:
                    original_content = file_path.read_text(encoding="latin-1")
                except Exception as e:
                    result.error = ErrorCode.CT_0011
                    result.error_message = str(e)
                    return result

            # Trim content
            trimmer = FileTrimmer(original_content, self.config)
            trim_result = trimmer.trim()

            # Check if modified
            if trim_result.content != original_content:
                result.was_modified = True
                result.bytes_modified = abs(
                    len(original_content) - len(trim_result.content)
                )

                # Generate diff if requested
                if self.config.diff and self.config.dry_run:
                    diff = self.diff_generator.generate_diff(
                        original_content,
                        trim_result.content,
                        str(file_path),
                    )
                    if self.config.verbose:
                        print(diff)

                # Write changes if not dry run
                if not self.config.dry_run:
                    # Create backup if requested
                    if self.config.create_backups:
                        backup_path = self._create_backup(file_path)
                        result.backup_path = str(backup_path)

                    # Write modified content
                    try:
                        file_path.write_text(
                            trim_result.content, encoding="utf-8"
                        )
                    except IOError as e:
                        result.error = ErrorCode.CT_0012
                        result.error_message = str(e)
                        return result

        except PermissionError as e:
            result.error = ErrorCode.CT_0013
            result.error_message = str(e)

        except Exception as e:
            result.error = ErrorCode.CT_0090
            result.error_message = str(e)
            logger.exception("Unexpected error processing %s", file_path)

        end_time = time.time()
        result.processing_time_ms = int((end_time - start_time) * 1000)

        return result

    def _discover_files(self, directory: Path) -> List[Path]:
        """Discover files to process in directory.

        Args:
            directory: Directory to search

        Returns:
            List of file paths to process
        """
        files = []

        for root, dirs, filenames in os.walk(directory, followlinks=self.config.follow_symlinks):
            # Skip hidden directories if not included
            if not self.config.include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith(".")]

            root_path = Path(root)

            for filename in filenames:
                # Skip hidden files if not included
                if not self.config.include_hidden and filename.startswith("."):
                    continue

                file_path = root_path / filename

                # Check include pattern
                if not self._matches_pattern(filename, self.config.include):
                    continue

                # Check exclude pattern
                if self.config.exclude and self._matches_pattern(
                    filename, self.config.exclude
                ):
                    continue

                files.append(file_path)

        return sorted(files)

    def _matches_pattern(self, filename: str, pattern: str) -> bool:
        """Check if filename matches glob pattern.

        Args:
            filename: Filename to check
            pattern: Glob pattern (supports comma-separated patterns)

        Returns:
            True if filename matches pattern
        """
        if pattern == "*":
            return True

        # Handle comma-separated patterns
        patterns = [p.strip() for p in pattern.split(",")]

        for p in patterns:
            # Handle brace expansion like "*.{java,py,js}"
            if "{" in p and "}" in p:
                # Simple brace expansion
                prefix, rest = p.split("{", 1)
                options, suffix = rest.split("}", 1)
                for opt in options.split(","):
                    if fnmatch.fnmatch(filename, prefix + opt + suffix):
                        return True
            elif fnmatch.fnmatch(filename, p):
                return True

        return False

    def _create_backup(self, file_path: Path) -> Path:
        """Create a backup of the file.

        Args:
            file_path: Path to file to backup

        Returns:
            Path to backup file

        Raises:
            CodeTrimmerException: If backup creation fails
        """
        backup_path = file_path.with_suffix(
            file_path.suffix + AppConstants.DEFAULT_BACKUP_EXTENSION
        )

        try:
            shutil.copy2(file_path, backup_path)
            return backup_path
        except IOError as e:
            raise CodeTrimmerException(
                ErrorCode.CT_0040,
                f"Failed to create backup: {e}",
                "Check disk space and permissions",
            ) from e
