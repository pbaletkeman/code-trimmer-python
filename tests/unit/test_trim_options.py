"""Tests for TrimOptions."""

import pytest

from codetrimmer.cli.options import TrimOptions


class TestTrimOptions:
    """Tests for TrimOptions class."""

    def test_default_values(self) -> None:
        """Test default option values."""
        options = TrimOptions()

        assert options.input_directory == "."
        assert options.include == "*"
        assert options.exclude == ""
        assert options.max_consecutive_blank_lines == 2
        assert options.max_file_size == 5242880
        assert options.max_files == 50
        assert options.dry_run is False
        assert options.create_backups is True
        assert options.verbose is False
        assert options.quiet is False

    def test_include_file_type(self) -> None:
        """Test including file types."""
        options = TrimOptions()
        options.include_file_type(".py")
        options.include_file_type(".js")

        assert options.is_file_type_included(".py")
        assert options.is_file_type_included(".js")
        assert not options.is_file_type_included(".java")

    def test_exclude_file_type(self) -> None:
        """Test excluding file types."""
        options = TrimOptions()
        options.exclude_file_type(".pyc")
        options.exclude_file_type(".class")

        assert options.is_file_type_excluded(".pyc")
        assert options.is_file_type_excluded(".class")
        assert not options.is_file_type_excluded(".py")

    def test_from_click_context(self) -> None:
        """Test creating from Click context."""
        ctx = {
            "directory": "/path/to/dir",
            "include": "*.py",
            "exclude": "*.pyc",
            "dry_run": True,
            "verbose": True,
            "max_files": 100,
        }

        options = TrimOptions.from_click_context(ctx)

        assert options.input_directory == "/path/to/dir"
        assert options.include == "*.py"
        assert options.exclude == "*.pyc"
        assert options.dry_run is True
        assert options.verbose is True
        assert options.max_files == 100

    def test_str_representation(self) -> None:
        """Test string representation."""
        options = TrimOptions(
            input_directory="/test",
            dry_run=True,
            verbose=True,
        )

        str_repr = str(options)
        assert "TrimOptions" in str_repr
        assert "/test" in str_repr
        assert "dry_run=True" in str_repr

    def test_empty_included_types(self) -> None:
        """Test that empty included types includes all."""
        options = TrimOptions()

        # When no types are explicitly included, all types are included
        assert options.is_file_type_included(".any")
        assert options.is_file_type_included(".extension")
