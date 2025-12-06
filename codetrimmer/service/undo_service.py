"""Undo/restore service for backup files."""

import logging
import shutil
from pathlib import Path
from typing import Dict, List

from codetrimmer.error.codes import ErrorCode
from codetrimmer.error.exceptions import CodeTrimmerException
from codetrimmer.util.constants import AppConstants

logger = logging.getLogger(__name__)


class UndoService:
    """Service for restoring files from backups."""

    BACKUP_EXTENSION = AppConstants.DEFAULT_BACKUP_EXTENSION

    def restore_directory(
        self,
        directory: str,
        recursive: bool = True,
    ) -> Dict[str, bool]:
        """Restore all .bak files in a directory.

        Args:
            directory: Directory to search for backup files
            recursive: If True, search subdirectories

        Returns:
            Dictionary mapping file paths to restore success status
        """
        dir_path = Path(directory)

        if not dir_path.exists():
            raise CodeTrimmerException(
                ErrorCode.CT_0010,
                f"Directory not found: {directory}",
                "Verify the directory path exists",
            )

        # Find all backup files
        backup_files = self._find_backup_files(dir_path, recursive)
        logger.info("Found %d backup files", len(backup_files))

        results = {}
        for backup_file in backup_files:
            original_file = self._get_original_path(backup_file)
            try:
                success = self.restore_file(str(original_file))
                results[str(original_file)] = success
            except Exception as e:
                logger.error("Failed to restore %s: %s", original_file, e)
                results[str(original_file)] = False

        return results

    def restore_file(self, file_path: str) -> bool:
        """Restore a single file from backup.

        Args:
            file_path: Path to the original file

        Returns:
            True if restore was successful

        Raises:
            CodeTrimmerException: If restore fails
        """
        original_path = Path(file_path)
        backup_path = Path(file_path + self.BACKUP_EXTENSION)

        if not backup_path.exists():
            raise CodeTrimmerException(
                ErrorCode.CT_0042,
                f"Backup file not found: {backup_path}",
                "Verify the backup file exists",
            )

        try:
            # Validate backup file
            if backup_path.stat().st_size == 0:
                raise CodeTrimmerException(
                    ErrorCode.CT_0043,
                    f"Backup file is empty: {backup_path}",
                    "Backup file may be corrupted",
                )

            # Restore the file
            shutil.copy2(backup_path, original_path)

            # Remove backup after successful restore
            backup_path.unlink()

            logger.info("Restored %s from backup", original_path)
            return True

        except IOError as e:
            raise CodeTrimmerException(
                ErrorCode.CT_0041,
                f"Failed to restore file: {e}",
                "Check file permissions",
            ) from e

    def _find_backup_files(
        self,
        directory: Path,
        recursive: bool,
    ) -> List[Path]:
        """Find all backup files in directory.

        Args:
            directory: Directory to search
            recursive: If True, search subdirectories

        Returns:
            List of backup file paths
        """
        pattern = f"*{self.BACKUP_EXTENSION}"

        if recursive:
            return list(directory.rglob(pattern))
        else:
            return list(directory.glob(pattern))

    def _get_original_path(self, backup_path: Path) -> Path:
        """Get original file path from backup path.

        Args:
            backup_path: Path to backup file

        Returns:
            Path to original file
        """
        # Remove .bak extension
        original_name = backup_path.name
        if original_name.endswith(self.BACKUP_EXTENSION):
            original_name = original_name[: -len(self.BACKUP_EXTENSION)]

        return backup_path.parent / original_name

    def list_backup_files(
        self,
        directory: str,
        recursive: bool = True,
    ) -> List[str]:
        """List all backup files in a directory.

        Args:
            directory: Directory to search
            recursive: If True, search subdirectories

        Returns:
            List of backup file paths as strings
        """
        dir_path = Path(directory)

        if not dir_path.exists():
            return []

        backup_files = self._find_backup_files(dir_path, recursive)
        return [str(f) for f in backup_files]

    def cleanup_backups(
        self,
        directory: str,
        recursive: bool = True,
    ) -> int:
        """Remove all backup files in a directory.

        Args:
            directory: Directory to clean
            recursive: If True, search subdirectories

        Returns:
            Number of backup files removed
        """
        dir_path = Path(directory)

        if not dir_path.exists():
            return 0

        backup_files = self._find_backup_files(dir_path, recursive)
        count = 0

        for backup_file in backup_files:
            try:
                backup_file.unlink()
                count += 1
                logger.debug("Removed backup: %s", backup_file)
            except IOError as e:
                logger.warning("Failed to remove backup %s: %s", backup_file, e)

        logger.info("Removed %d backup files", count)
        return count
