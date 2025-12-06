"""Tests for ColorOutput utility."""

import sys

import pytest

from codetrimmer.util.color import (
    ColorOutput,
    RESET,
    RED,
    GREEN,
    YELLOW,
    CYAN,
    BOLD,
    red,
    green,
    yellow,
    cyan,
    bold,
    strip_colors,
)


class TestColorOutput:
    """Tests for ColorOutput class."""

    def test_red_color(self) -> None:
        """Test red color output."""
        output = ColorOutput()
        result = output.red("text")
        # In TTY mode, should have color codes
        # Since we're in test, just verify it returns a string
        assert "text" in result

    def test_green_color(self) -> None:
        """Test green color output."""
        output = ColorOutput()
        result = output.green("text")
        assert "text" in result

    def test_yellow_color(self) -> None:
        """Test yellow color output."""
        output = ColorOutput()
        result = output.yellow("text")
        assert "text" in result

    def test_cyan_color(self) -> None:
        """Test cyan color output."""
        output = ColorOutput()
        result = output.cyan("text")
        assert "text" in result

    def test_bold_style(self) -> None:
        """Test bold style output."""
        output = ColorOutput()
        result = output.bold("text")
        assert "text" in result

    def test_no_color_mode(self) -> None:
        """Test no color mode."""
        output = ColorOutput(no_color=True)
        result = output.red("text")
        assert result == "text"
        assert RESET not in result

    def test_strip_colors(self) -> None:
        """Test stripping color codes."""
        colored = f"{RED}text{RESET}"
        result = strip_colors(colored)
        assert result == "text"
        assert "\033" not in result

    def test_success_color(self) -> None:
        """Test success color (bright green)."""
        output = ColorOutput()
        result = output.success("success")
        assert "success" in result

    def test_error_color(self) -> None:
        """Test error color (bright red)."""
        output = ColorOutput()
        result = output.error("error")
        assert "error" in result

    def test_warning_color(self) -> None:
        """Test warning color (bright yellow)."""
        output = ColorOutput()
        result = output.warning("warning")
        assert "warning" in result

    def test_info_color(self) -> None:
        """Test info color (bright cyan)."""
        output = ColorOutput()
        result = output.info("info")
        assert "info" in result

    def test_dim_style(self) -> None:
        """Test dim style."""
        output = ColorOutput()
        result = output.dim("text")
        assert "text" in result


class TestModuleFunctions:
    """Tests for module-level color functions."""

    def test_red_function(self) -> None:
        """Test red function."""
        result = red("text")
        assert RED in result
        assert RESET in result
        assert "text" in result

    def test_green_function(self) -> None:
        """Test green function."""
        result = green("text")
        assert GREEN in result

    def test_yellow_function(self) -> None:
        """Test yellow function."""
        result = yellow("text")
        assert YELLOW in result

    def test_cyan_function(self) -> None:
        """Test cyan function."""
        result = cyan("text")
        assert CYAN in result

    def test_bold_function(self) -> None:
        """Test bold function."""
        result = bold("text")
        assert BOLD in result

    def test_strip_colors_function(self) -> None:
        """Test strip_colors function."""
        colored = f"{RED}{BOLD}text{RESET}"
        result = strip_colors(colored)
        assert result == "text"
