"""Tests for ReportGenerator."""

import json
import os
import tempfile
from pathlib import Path

import pytest

from codetrimmer.error.codes import ErrorCode
from codetrimmer.model.file_result import FileProcessingResult
from codetrimmer.model.statistics import ProcessingStatistics
from codetrimmer.service.report_generator import ReportGenerator


class TestReportGenerator:
    """Tests for ReportGenerator class."""

    @pytest.fixture
    def sample_stats(self) -> ProcessingStatistics:
        """Create sample processing statistics."""
        stats = ProcessingStatistics()
        stats.add_result(
            FileProcessingResult(
                file_path="/path/to/file1.py",
                was_modified=True,
                bytes_modified=10,
                processing_time_ms=50,
            )
        )
        stats.add_result(
            FileProcessingResult(
                file_path="/path/to/file2.py",
                was_modified=False,
                processing_time_ms=20,
            )
        )
        stats.set_execution_time(100)
        return stats

    def test_export_json(self, sample_stats: ProcessingStatistics) -> None:
        """Test exporting to JSON."""
        generator = ReportGenerator()
        json_str = generator.export_json(sample_stats)

        data = json.loads(json_str)
        assert data["files_processed"] == 2
        assert data["files_modified"] == 1
        assert len(data["results"]) == 2

    def test_export_csv(self, sample_stats: ProcessingStatistics) -> None:
        """Test exporting to CSV."""
        generator = ReportGenerator()
        csv_str = generator.export_csv(sample_stats)

        lines = csv_str.strip().split("\n")
        assert len(lines) == 3  # Header + 2 data rows

        # Check header
        header = lines[0]
        assert "file_path" in header
        assert "was_modified" in header

    def test_export_sqlite(
        self, sample_stats: ProcessingStatistics, temp_dir: Path
    ) -> None:
        """Test exporting to SQLite."""
        generator = ReportGenerator()
        db_path = str(temp_dir / "report.db")

        generator.export_sqlite(sample_stats, db_path)

        assert Path(db_path).exists()

        # Verify database content
        import sqlite3

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM processing_runs")
        assert cursor.fetchone()[0] == 1

        cursor.execute("SELECT COUNT(*) FROM file_results")
        assert cursor.fetchone()[0] == 2

        conn.close()

    def test_save_report_json(
        self, sample_stats: ProcessingStatistics, temp_dir: Path
    ) -> None:
        """Test saving JSON report to file."""
        generator = ReportGenerator()
        output_path = str(temp_dir / "report.json")

        generator.save_report(sample_stats, output_path, "json")

        assert Path(output_path).exists()
        with open(output_path) as f:
            data = json.load(f)
            assert data["files_processed"] == 2

    def test_save_report_csv(
        self, sample_stats: ProcessingStatistics, temp_dir: Path
    ) -> None:
        """Test saving CSV report to file."""
        generator = ReportGenerator()
        output_path = str(temp_dir / "report.csv")

        generator.save_report(sample_stats, output_path, "csv")

        assert Path(output_path).exists()

    def test_invalid_format(
        self, sample_stats: ProcessingStatistics, temp_dir: Path
    ) -> None:
        """Test error on invalid format."""
        from codetrimmer.error.exceptions import CodeTrimmerException

        generator = ReportGenerator()
        output_path = str(temp_dir / "report.xml")

        with pytest.raises(CodeTrimmerException) as exc_info:
            generator.save_report(sample_stats, output_path, "xml")

        assert exc_info.value.error_code == ErrorCode.CT_0061

    def test_stats_with_errors(self) -> None:
        """Test report with error results."""
        stats = ProcessingStatistics()
        stats.add_result(
            FileProcessingResult(
                file_path="/path/to/file.py",
                was_modified=False,
                error=ErrorCode.CT_0011,
                error_message="Cannot read file",
            )
        )

        generator = ReportGenerator()
        json_str = generator.export_json(stats)

        data = json.loads(json_str)
        assert data["files_with_errors"] == 1
        assert data["results"][0]["error"] == "CT-0011"
