"""Default configuration values for Code Trimmer."""

from codetrimmer.config.models import TrimmerConfig, CodeTrimmerConfig


def get_default_config() -> TrimmerConfig:
    """Get default configuration values.

    Returns:
        TrimmerConfig with default values
    """
    return TrimmerConfig()


def get_default_runtime_config() -> CodeTrimmerConfig:
    """Get default runtime configuration values.

    Returns:
        CodeTrimmerConfig with default values
    """
    return CodeTrimmerConfig()
