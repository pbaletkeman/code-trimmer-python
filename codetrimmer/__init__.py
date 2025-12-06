"""
Code Trimmer - A file formatting and whitespace normalization utility.

This is the Python 3.14+ implementation of Code Trimmer.
For documentation, see ./docs/
"""

__version__ = "1.0.0"
__author__ = "Pete Letkeman"
__email__ = "pete@letkeman.ca"

from codetrimmer.error.codes import ErrorCode
from codetrimmer.error.exceptions import CodeTrimmerException

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "ErrorCode",
    "CodeTrimmerException",
]
