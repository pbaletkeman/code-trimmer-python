"""CLI commands for Code Trimmer."""

import logging
import sys
from pathlib import Path
from typing import Optional

import click

from codetrimmer import __version__
from codetrimmer.cli.output import OutputHandler
from codetrimmer.config.loader import ConfigurationLoader
from codetrimmer.config.models import CodeTrimmerConfig
from codetrimmer.error.exceptions import CodeTrimmerException
from codetrimmer.service.file_processor import FileProcessingService
from codetrimmer.service.hook_generator import HookGenerator
from codetrimmer.service.report_generator import ReportGenerator
from codetrimmer.service.undo_service import UndoService

logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version=__version__, prog_name="codetrimmer")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Code Trimmer - A file formatting and whitespace normalization utility.

    Process source code files to remove unnecessary whitespace,
    enforce consistent formatting rules, and optionally create backups.
    """
    ctx.ensure_object(dict)


@cli.command()
@click.argument("directory", default=".", type=click.Path(exists=True))
@click.option("--include", default="*", help="File glob pattern to include")
@click.option("--exclude", default="", help="File glob pattern to exclude")
@click.option("--include-hidden", is_flag=True, help="Include hidden files")
@click.option("--follow-symlinks", is_flag=True, help="Follow symbolic links")
@click.option(
    "--max-consecutive-blank-lines",
    default=2,
    type=int,
    help="Maximum consecutive blank lines",
)
@click.option(
    "--ensure-final-newline/--no-ensure-final-newline",
    default=True,
    help="Ensure file ends with newline",
)
@click.option(
    "--trim-trailing-whitespace/--no-trim-trailing-whitespace",
    default=True,
    help="Trim trailing whitespace",
)
@click.option(
    "--max-file-size",
    default=5242880,
    type=int,
    help="Max file size in bytes",
)
@click.option(
    "--max-files",
    default=50,
    type=int,
    help="Max files to process",
)
@click.option("--no-limits", is_flag=True, help="Disable all limits")
@click.option("--dry-run", is_flag=True, help="Preview changes without modifying")
@click.option(
    "--create-backups/--no-create-backups",
    default=True,
    help="Create .bak backup files",
)
@click.option("--fail-fast", is_flag=True, help="Stop on first error")
@click.option("--verbose", "-v", is_flag=True, help="Detailed output")
@click.option("--quiet", "-q", is_flag=True, help="Minimal output")
@click.option("--no-color", is_flag=True, help="Disable colored output")
@click.option(
    "--disable-color-for-pipe/--no-disable-color-for-pipe",
    default=True,
    help="Disable colors when piped",
)
@click.option("--config", type=click.Path(), help="Config file path")
@click.option(
    "--report",
    type=click.Choice(["json", "csv", "sqlite"]),
    help="Report format",
)
@click.option(
    "--report-output",
    default="codetrimmer-report.json",
    help="Report file path",
)
@click.option("--report-endpoint", help="HTTP endpoint for reports")
@click.option("--diff", is_flag=True, help="Show diff in dry-run")
@click.pass_context
def trim(
    ctx: click.Context,
    directory: str,
    include: str,
    exclude: str,
    include_hidden: bool,
    follow_symlinks: bool,
    max_consecutive_blank_lines: int,
    ensure_final_newline: bool,
    trim_trailing_whitespace: bool,
    max_file_size: int,
    max_files: int,
    no_limits: bool,
    dry_run: bool,
    create_backups: bool,
    fail_fast: bool,
    verbose: bool,
    quiet: bool,
    no_color: bool,
    disable_color_for_pipe: bool,
    config: Optional[str],
    report: Optional[str],
    report_output: str,
    report_endpoint: Optional[str],
    diff: bool,
) -> None:
    """Trim whitespace from files in DIRECTORY.

    Processes files to remove trailing whitespace, reduce consecutive
    blank lines, and ensure files end with a newline.
    """
    output = OutputHandler(quiet, verbose, no_color, disable_color_for_pipe)

    try:
        # Load configuration
        config_loader = ConfigurationLoader()

        if config:
            file_config = config_loader.load_from_file(Path(config))
        else:
            file_config = config_loader.load_configuration(directory)

        # Create runtime configuration
        runtime_config = CodeTrimmerConfig(
            include=include,
            exclude=exclude,
            include_hidden=include_hidden,
            follow_symlinks=follow_symlinks,
            max_consecutive_blank_lines=max_consecutive_blank_lines,
            ensure_final_newline=ensure_final_newline,
            trim_trailing_whitespace=trim_trailing_whitespace,
            max_file_size=max_file_size,
            max_files=max_files,
            no_limits=no_limits,
            dry_run=dry_run,
            create_backups=create_backups,
            fail_fast=fail_fast,
            verbose=verbose,
            quiet=quiet,
            no_color=no_color,
            disable_color_for_pipe=disable_color_for_pipe,
            report=report,
            report_output=report_output,
            report_endpoint=report_endpoint,
            diff=diff,
            input_directory=directory,
            rules=file_config.rules,
        )

        # Print header
        output.print_header(directory)

        if dry_run:
            output.print_dry_run_notice()

        # Process files
        service = FileProcessingService(runtime_config)
        stats = service.process_directory(directory)

        # Print results
        for result in stats.results:
            if result.was_modified:
                output.print_file_modified(result.file_path, result.bytes_modified)
            elif result.error:
                if result.error.code == "CT-0016":
                    output.print_file_skipped(result.file_path, "binary")
                else:
                    output.print_file_error(result.file_path, result.error_message)

        output.print_statistics(stats)

        # Generate report
        if report:
            report_gen = ReportGenerator()
            report_gen.save_report(stats, report_output, report)
            output.print_info(f"Report saved to: {report_output}")

        # Exit with error code if there were errors
        if stats.files_with_errors > 0:
            sys.exit(1)

    except CodeTrimmerException as e:
        output.print_error(str(e))
        sys.exit(1)
    except Exception as e:
        output.print_error(f"Unexpected error: {e}")
        logger.exception("Unexpected error")
        sys.exit(1)


@cli.command("generate-hook")
@click.argument("directory", default=".", type=click.Path(exists=True))
@click.option("--force", is_flag=True, help="Overwrite existing hook")
@click.option("--verbose", "-v", is_flag=True, help="Detailed output")
@click.option("--quiet", "-q", is_flag=True, help="Minimal output")
@click.option("--no-color", is_flag=True, help="Disable colored output")
def generate_hook(
    directory: str,
    force: bool,
    verbose: bool,
    quiet: bool,
    no_color: bool,
) -> None:
    """Generate a Git pre-commit hook for DIRECTORY.

    Creates a pre-commit hook that runs Code Trimmer on staged files
    before each commit.
    """
    output = OutputHandler(quiet, verbose, no_color)

    try:
        generator = HookGenerator()
        hook_path = generator.generate_pre_commit_hook(directory, force)

        output.print_success(f"Pre-commit hook generated: {hook_path}")
        output.print_info("Hook will run Code Trimmer on staged files before commits.")

    except CodeTrimmerException as e:
        output.print_error(str(e))
        sys.exit(1)
    except Exception as e:
        output.print_error(f"Unexpected error: {e}")
        sys.exit(1)


@cli.command()
@click.argument("directory", default=".", type=click.Path(exists=True))
@click.option("--undo-dir", type=click.Path(), help="Directory with backup files")
@click.option("--verbose", "-v", is_flag=True, help="Detailed output")
@click.option("--quiet", "-q", is_flag=True, help="Minimal output")
@click.option("--no-color", is_flag=True, help="Disable colored output")
def undo(
    directory: str,
    undo_dir: Optional[str],
    verbose: bool,
    quiet: bool,
    no_color: bool,
) -> None:
    """Restore files from backups in DIRECTORY.

    Finds all .bak files and restores the original files.
    """
    output = OutputHandler(quiet, verbose, no_color)

    try:
        service = UndoService()
        target_dir = undo_dir or directory

        # List backup files first
        backup_files = service.list_backup_files(target_dir)

        if not backup_files:
            output.print_info("No backup files found.")
            return

        output.print(f"Found {len(backup_files)} backup file(s)")

        # Restore files
        results = service.restore_directory(target_dir)

        success_count = sum(1 for v in results.values() if v)
        fail_count = len(results) - success_count

        output.print()
        output.print_success(f"Restored: {success_count} file(s)")

        if fail_count > 0:
            output.print_error(f"Failed: {fail_count} file(s)")
            sys.exit(1)

    except CodeTrimmerException as e:
        output.print_error(str(e))
        sys.exit(1)
    except Exception as e:
        output.print_error(f"Unexpected error: {e}")
        sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
