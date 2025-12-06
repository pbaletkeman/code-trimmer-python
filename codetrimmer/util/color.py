"""ANSI color output utilities for terminal."""

import os
import sys


# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
UNDERLINE = "\033[4m"

# Foreground colors
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# Bright foreground colors
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"


class ColorOutput:
    """Utility class for colored terminal output."""

    def __init__(
        self,
        no_color: bool = False,
        disable_for_pipe: bool = True,
    ) -> None:
        """Initialize color output.

        Args:
            no_color: If True, disable all colors
            disable_for_pipe: If True, disable colors when output is piped
        """
        self._no_color = no_color
        self._disable_for_pipe = disable_for_pipe

    def _is_color_enabled(self) -> bool:
        """Check if color output is enabled."""
        if self._no_color:
            return False

        if self._disable_for_pipe and not sys.stdout.isatty():
            return False

        # Check for NO_COLOR environment variable
        if os.environ.get("NO_COLOR"):
            return False

        return True

    def _colorize(self, text: str, color_code: str) -> str:
        """Apply color code to text if colors are enabled."""
        if not self._is_color_enabled():
            return text
        return f"{color_code}{text}{RESET}"

    def red(self, text: str) -> str:
        """Apply red color to text."""
        return self._colorize(text, RED)

    def green(self, text: str) -> str:
        """Apply green color to text."""
        return self._colorize(text, GREEN)

    def yellow(self, text: str) -> str:
        """Apply yellow color to text."""
        return self._colorize(text, YELLOW)

    def blue(self, text: str) -> str:
        """Apply blue color to text."""
        return self._colorize(text, BLUE)

    def cyan(self, text: str) -> str:
        """Apply cyan color to text."""
        return self._colorize(text, CYAN)

    def magenta(self, text: str) -> str:
        """Apply magenta color to text."""
        return self._colorize(text, MAGENTA)

    def bold(self, text: str) -> str:
        """Apply bold style to text."""
        return self._colorize(text, BOLD)

    def dim(self, text: str) -> str:
        """Apply dim style to text."""
        return self._colorize(text, DIM)

    def success(self, text: str) -> str:
        """Apply success (green) color to text."""
        return self._colorize(text, BRIGHT_GREEN)

    def error(self, text: str) -> str:
        """Apply error (red) color to text."""
        return self._colorize(text, BRIGHT_RED)

    def warning(self, text: str) -> str:
        """Apply warning (yellow) color to text."""
        return self._colorize(text, BRIGHT_YELLOW)

    def info(self, text: str) -> str:
        """Apply info (cyan) color to text."""
        return self._colorize(text, BRIGHT_CYAN)

    @staticmethod
    def strip_colors(text: str) -> str:
        """Remove all ANSI color codes from text.

        Args:
            text: Text potentially containing ANSI codes

        Returns:
            Text with all ANSI codes removed
        """
        import re
        ansi_escape = re.compile(r"\033\[[0-9;]*m")
        return ansi_escape.sub("", text)


def red(text: str) -> str:
    """Apply red color to text (module-level function)."""
    return f"{RED}{text}{RESET}"


def green(text: str) -> str:
    """Apply green color to text (module-level function)."""
    return f"{GREEN}{text}{RESET}"


def yellow(text: str) -> str:
    """Apply yellow color to text (module-level function)."""
    return f"{YELLOW}{text}{RESET}"


def cyan(text: str) -> str:
    """Apply cyan color to text (module-level function)."""
    return f"{CYAN}{text}{RESET}"


def bold(text: str) -> str:
    """Apply bold style to text (module-level function)."""
    return f"{BOLD}{text}{RESET}"


def strip_colors(text: str) -> str:
    """Remove all ANSI color codes from text (module-level function)."""
    return ColorOutput.strip_colors(text)
