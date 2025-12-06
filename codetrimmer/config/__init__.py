"""Configuration module for Code Trimmer."""

from codetrimmer.config.models import TrimmerConfig, TrimRule, CodeTrimmerConfig
from codetrimmer.config.defaults import get_default_config
from codetrimmer.config.loader import ConfigurationLoader

__all__ = [
    "TrimmerConfig",
    "TrimRule",
    "CodeTrimmerConfig",
    "get_default_config",
    "ConfigurationLoader",
]
