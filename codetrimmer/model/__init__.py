"""Model module for Code Trimmer."""

from codetrimmer.model.binary_detector import BinaryFileDetector
from codetrimmer.model.file_result import FileProcessingResult
from codetrimmer.model.statistics import ProcessingStatistics

__all__ = [
    "BinaryFileDetector",
    "FileProcessingResult",
    "ProcessingStatistics",
]
