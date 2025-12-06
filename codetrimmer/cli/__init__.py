"""CLI module for Code Trimmer."""

from codetrimmer.cli.commands import cli, trim, generate_hook, undo
from codetrimmer.cli.options import TrimOptions
from codetrimmer.cli.output import OutputHandler

__all__ = [
    "cli",
    "trim",
    "generate_hook",
    "undo",
    "TrimOptions",
    "OutputHandler",
]
