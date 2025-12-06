"""Service module for Code Trimmer."""

from codetrimmer.service.trimmer import FileTrimmer, TrimResult
from codetrimmer.service.file_processor import FileProcessingService
from codetrimmer.service.diff_generator import DiffGenerator
from codetrimmer.service.hook_generator import HookGenerator
from codetrimmer.service.undo_service import UndoService
from codetrimmer.service.report_generator import ReportGenerator

__all__ = [
    "FileTrimmer",
    "TrimResult",
    "FileProcessingService",
    "DiffGenerator",
    "HookGenerator",
    "UndoService",
    "ReportGenerator",
]
