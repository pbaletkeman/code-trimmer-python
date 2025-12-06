"""Report generation service."""

import csv
import io
import json
import logging
import sqlite3
from pathlib import Path

from codetrimmer.error.codes import ErrorCode
from codetrimmer.error.exceptions import CodeTrimmerException
from codetrimmer.model.statistics import ProcessingStatistics

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Service for generating processing reports.

    Supports JSON, CSV, and SQLite output formats.
    """

    def export_json(self, stats: ProcessingStatistics) -> str:
        """Export statistics to JSON format.

        Args:
            stats: Processing statistics

        Returns:
            JSON string
        """
        return json.dumps(stats.to_dict(), indent=2)

    def export_csv(self, stats: ProcessingStatistics) -> str:
        """Export statistics to CSV format.

        Args:
            stats: Processing statistics

        Returns:
            CSV string
        """
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow([
            "file_path",
            "was_modified",
            "bytes_modified",
            "error_code",
            "error_message",
            "backup_path",
            "processing_time_ms",
        ])

        # Write data rows
        for result in stats.results:
            writer.writerow([
                result.file_path,
                result.was_modified,
                result.bytes_modified,
                result.error.code if result.error else "",
                result.error_message,
                result.backup_path or "",
                result.processing_time_ms,
            ])

        return output.getvalue()

    def export_sqlite(
        self,
        stats: ProcessingStatistics,
        db_path: str,
    ) -> None:
        """Export statistics to SQLite database.

        Args:
            stats: Processing statistics
            db_path: Path to SQLite database file

        Raises:
            CodeTrimmerException: If database operation fails
        """
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Create tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS processing_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    files_processed INTEGER,
                    files_modified INTEGER,
                    files_skipped INTEGER,
                    files_with_errors INTEGER,
                    total_bytes_trimmed INTEGER,
                    total_execution_time_ms INTEGER
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS file_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER,
                    file_path TEXT,
                    was_modified INTEGER,
                    bytes_modified INTEGER,
                    error_code TEXT,
                    error_message TEXT,
                    backup_path TEXT,
                    processing_time_ms INTEGER,
                    FOREIGN KEY (run_id) REFERENCES processing_runs (id)
                )
            """)

            # Insert run summary
            cursor.execute("""
                INSERT INTO processing_runs (
                    files_processed, files_modified, files_skipped,
                    files_with_errors, total_bytes_trimmed, total_execution_time_ms
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                stats.files_processed,
                stats.files_modified,
                stats.files_skipped,
                stats.files_with_errors,
                stats.total_bytes_trimmed,
                stats.total_execution_time_ms,
            ))

            run_id = cursor.lastrowid

            # Insert file results
            for result in stats.results:
                cursor.execute("""
                    INSERT INTO file_results (
                        run_id, file_path, was_modified, bytes_modified,
                        error_code, error_message, backup_path, processing_time_ms
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    run_id,
                    result.file_path,
                    1 if result.was_modified else 0,
                    result.bytes_modified,
                    result.error.code if result.error else None,
                    result.error_message,
                    result.backup_path,
                    result.processing_time_ms,
                ))

            conn.commit()
            conn.close()

            logger.info("Report exported to SQLite: %s", db_path)

        except sqlite3.Error as e:
            raise CodeTrimmerException(
                ErrorCode.CT_0063,
                f"SQLite error: {e}",
                "Check database path and permissions",
            ) from e

    def save_report(
        self,
        stats: ProcessingStatistics,
        output_path: str,
        format: str = "json",
    ) -> None:
        """Save report to file.

        Args:
            stats: Processing statistics
            output_path: Path to output file
            format: Report format (json, csv, sqlite)

        Raises:
            CodeTrimmerException: If report generation fails
        """
        try:
            if format == "json":
                content = self.export_json(stats)
                Path(output_path).write_text(content, encoding="utf-8")
            elif format == "csv":
                content = self.export_csv(stats)
                Path(output_path).write_text(content, encoding="utf-8")
            elif format == "sqlite":
                self.export_sqlite(stats, output_path)
            else:
                raise CodeTrimmerException(
                    ErrorCode.CT_0061,
                    f"Invalid report format: {format}",
                    "Use json, csv, or sqlite",
                )

            logger.info("Report saved to: %s", output_path)

        except IOError as e:
            raise CodeTrimmerException(
                ErrorCode.CT_0060,
                f"Failed to save report: {e}",
                "Check disk space and permissions",
            ) from e

    async def send_to_endpoint(
        self,
        stats: ProcessingStatistics,
        url: str,
    ) -> None:
        """Send report to HTTP endpoint.

        Args:
            stats: Processing statistics
            url: HTTP endpoint URL

        Raises:
            CodeTrimmerException: If sending fails
        """
        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=stats.to_dict(),
                    headers={"Content-Type": "application/json"},
                ) as response:
                    if response.status >= 400:
                        raise CodeTrimmerException(
                            ErrorCode.CT_0062,
                            f"HTTP error {response.status}",
                            "Check endpoint URL and availability",
                        )

            logger.info("Report sent to endpoint: %s", url)

        except ImportError:
            raise CodeTrimmerException(
                ErrorCode.CT_0062,
                "aiohttp not installed",
                "Install with: pip install codetrimmer[http]",
            )
        except Exception as e:
            raise CodeTrimmerException(
                ErrorCode.CT_0062,
                f"Failed to send report: {e}",
                "Check endpoint URL and network connection",
            ) from e
