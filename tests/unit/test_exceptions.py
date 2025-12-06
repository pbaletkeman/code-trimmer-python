"""Tests for CodeTrimmerException."""

import pytest

from codetrimmer.error.codes import ErrorCode
from codetrimmer.error.exceptions import CodeTrimmerException


class TestCodeTrimmerException:
    """Tests for CodeTrimmerException class."""

    def test_exception_with_code_only(self) -> None:
        """Test exception with just error code."""
        exc = CodeTrimmerException(ErrorCode.CT_0001)
        assert exc.error_code == ErrorCode.CT_0001
        assert exc.cause is None
        assert exc.suggestion is None

    def test_exception_with_cause(self) -> None:
        """Test exception with cause."""
        exc = CodeTrimmerException(
            ErrorCode.CT_0010,
            cause="File not found: test.txt",
        )
        assert "File not found" in str(exc)
        assert exc.cause == "File not found: test.txt"

    def test_exception_with_suggestion(self) -> None:
        """Test exception with suggestion."""
        exc = CodeTrimmerException(
            ErrorCode.CT_0002,
            suggestion="Check the file path",
        )
        assert "Check the file path" in str(exc)
        assert exc.suggestion == "Check the file path"

    def test_exception_full_message(self) -> None:
        """Test exception with all fields."""
        exc = CodeTrimmerException(
            ErrorCode.CT_0011,
            cause="Permission denied",
            suggestion="Run as administrator",
        )
        message = str(exc)
        assert "[CT-0011]" in message
        assert "File read error" in message
        assert "Permission denied" in message
        assert "Run as administrator" in message

    def test_exception_repr(self) -> None:
        """Test exception repr."""
        exc = CodeTrimmerException(
            ErrorCode.CT_0001,
            cause="test cause",
            suggestion="test suggestion",
        )
        repr_str = repr(exc)
        assert "CodeTrimmerException" in repr_str
        assert "CT_0001" in repr_str

    def test_exception_is_exception(self) -> None:
        """Test that CodeTrimmerException is an Exception."""
        exc = CodeTrimmerException(ErrorCode.CT_0001)
        assert isinstance(exc, Exception)

    def test_exception_can_be_raised(self) -> None:
        """Test that exception can be raised and caught."""
        with pytest.raises(CodeTrimmerException) as exc_info:
            raise CodeTrimmerException(ErrorCode.CT_0010, cause="test")

        assert exc_info.value.error_code == ErrorCode.CT_0010

    def test_exception_message_formatting(self) -> None:
        """Test that exception message is properly formatted."""
        exc = CodeTrimmerException(
            ErrorCode.CT_0003,
            cause="Value out of range",
            suggestion="Use a value between 0 and 100",
        )
        message = str(exc)
        lines = message.split("\n")

        # Check structure
        assert any("[CT-0003]" in line for line in lines)
        assert any("Description:" in line for line in lines)
        assert any("Cause:" in line for line in lines)
        assert any("Suggestion:" in line for line in lines)
