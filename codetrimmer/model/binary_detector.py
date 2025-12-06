"""Binary file detection utilities."""

from pathlib import Path
from typing import Union

from codetrimmer.util.constants import AppConstants


class BinaryFileDetector:
    """Utility class for detecting binary files."""

    BUFFER_SIZE = AppConstants.BUFFER_SIZE
    BINARY_EXTENSIONS = AppConstants.BINARY_EXTENSIONS

    @classmethod
    def is_binary(cls, path: Union[str, Path]) -> bool:
        """Detect if a file is binary by checking for null bytes.

        Checks the first 8KB of the file for null bytes.

        Args:
            path: Path to the file to check

        Returns:
            True if the file appears to be binary, False if text
        """
        file_path = Path(path)

        try:
            with open(file_path, "rb") as f:
                buffer = f.read(cls.BUFFER_SIZE)

            # Check for null bytes
            if b"\x00" in buffer:
                return True

            return False

        except IOError:
            # If we can't read it, assume it's binary to be safe
            return True

    @classmethod
    def is_binary_by_extension(cls, path: Union[str, Path]) -> bool:
        """Check if a file is likely binary based on extension.

        Args:
            path: Path to the file to check

        Returns:
            True if the file extension suggests it's binary
        """
        file_path = Path(path)
        filename = file_path.name.lower()

        for ext in cls.BINARY_EXTENSIONS:
            if filename.endswith(ext):
                return True

        return False

    @classmethod
    def should_skip(cls, path: Union[str, Path]) -> bool:
        """Check if a file should be skipped (is binary).

        Combines extension check and content check.

        Args:
            path: Path to the file to check

        Returns:
            True if the file should be skipped
        """
        file_path = Path(path)

        # First check by extension (faster)
        if cls.is_binary_by_extension(file_path):
            return True

        # Then check content
        return cls.is_binary(file_path)
