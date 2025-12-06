"""Tests for error codes."""

import pytest

from codetrimmer.error.codes import ErrorCode


class TestErrorCode:
    """Tests for ErrorCode enum."""

    def test_error_code_values(self) -> None:
        """Test that error codes have expected values."""
        assert ErrorCode.CT_0001.code == "CT-0001"
        assert ErrorCode.CT_0001.title == "Invalid configuration file"
        assert "invalid" in ErrorCode.CT_0001.description.lower()

    def test_error_code_str(self) -> None:
        """Test string representation of error codes."""
        error = ErrorCode.CT_0010
        assert str(error) == "CT-0010: File not found"

    def test_configuration_errors(self) -> None:
        """Test configuration error codes."""
        config_errors = [
            ErrorCode.CT_0001,
            ErrorCode.CT_0002,
            ErrorCode.CT_0003,
            ErrorCode.CT_0004,
            ErrorCode.CT_0005,
        ]
        for error in config_errors:
            assert error.code.startswith("CT-000")

    def test_file_operation_errors(self) -> None:
        """Test file operation error codes."""
        file_errors = [
            ErrorCode.CT_0010,
            ErrorCode.CT_0011,
            ErrorCode.CT_0012,
            ErrorCode.CT_0013,
            ErrorCode.CT_0014,
            ErrorCode.CT_0015,
            ErrorCode.CT_0016,
        ]
        for error in file_errors:
            assert error.code.startswith("CT-001")

    def test_backup_errors(self) -> None:
        """Test backup/restore error codes."""
        backup_errors = [
            ErrorCode.CT_0040,
            ErrorCode.CT_0041,
            ErrorCode.CT_0042,
            ErrorCode.CT_0043,
        ]
        for error in backup_errors:
            assert error.code.startswith("CT-004")

    def test_hook_errors(self) -> None:
        """Test hook generation error codes."""
        hook_errors = [
            ErrorCode.CT_0050,
            ErrorCode.CT_0051,
            ErrorCode.CT_0052,
        ]
        for error in hook_errors:
            assert error.code.startswith("CT-005")

    def test_report_errors(self) -> None:
        """Test report error codes."""
        report_errors = [
            ErrorCode.CT_0060,
            ErrorCode.CT_0061,
            ErrorCode.CT_0062,
            ErrorCode.CT_0063,
        ]
        for error in report_errors:
            assert error.code.startswith("CT-006")

    def test_general_errors(self) -> None:
        """Test general error codes."""
        general_errors = [
            ErrorCode.CT_0090,
            ErrorCode.CT_0091,
            ErrorCode.CT_0092,
        ]
        for error in general_errors:
            assert error.code.startswith("CT-009")

    def test_all_codes_unique(self) -> None:
        """Test that all error codes are unique."""
        codes = [e.code for e in ErrorCode]
        assert len(codes) == len(set(codes))

    def test_all_titles_non_empty(self) -> None:
        """Test that all error titles are non-empty."""
        for error in ErrorCode:
            assert error.title
            assert len(error.title) > 0

    def test_all_descriptions_non_empty(self) -> None:
        """Test that all error descriptions are non-empty."""
        for error in ErrorCode:
            assert error.description
            assert len(error.description) > 0
