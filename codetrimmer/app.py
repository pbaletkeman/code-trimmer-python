"""Application bootstrap for Code Trimmer."""

import logging

from typing import Optional

from codetrimmer import __version__
from codetrimmer.cli.commands import main as cli_main
from codetrimmer.config.loader import ConfigurationLoader
from codetrimmer.config.models import CodeTrimmerConfig
from codetrimmer.service.file_processor import FileProcessingService


def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    """Configure logging for the application.

    Args:
        verbose: If True, set DEBUG level
        quiet: If True, set ERROR level only
    """
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


class CodeTrimmerApp:
    """Main application class for Code Trimmer.

    Provides programmatic access to Code Trimmer functionality.
    """

    def __init__(self, config: Optional[CodeTrimmerConfig] = None) -> None:
        """Initialize the application.

        Args:
            config: Optional runtime configuration
        """
        self.config = config or CodeTrimmerConfig()
        self.config_loader = ConfigurationLoader()

    def process_directory(self, directory: str) -> dict:
        """Process files in a directory.

        Args:
            directory: Path to directory to process

        Returns:
            Dictionary with processing statistics
        """
        service = FileProcessingService(self.config)
        stats = service.process_directory(directory)
        return stats.to_dict()

    def load_config(self, directory: str) -> CodeTrimmerConfig:
        """Load configuration from directory.

        Args:
            directory: Directory to search for config files

        Returns:
            Loaded configuration
        """
        file_config = self.config_loader.load_configuration(directory)
        self.config_loader.apply_configuration(file_config, self.config)
        return self.config

    @staticmethod
    def get_version() -> str:
        """Get application version.

        Returns:
            Version string
        """
        return __version__


def main() -> None:
    """Main entry point."""
    cli_main()


if __name__ == "__main__":
    main()
