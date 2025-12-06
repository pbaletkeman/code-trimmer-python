"""Configuration loading utilities for Code Trimmer."""

import json
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from codetrimmer.config.models import CodeTrimmerConfig, TrimRule, TrimmerConfig
from codetrimmer.error.codes import ErrorCode
from codetrimmer.error.exceptions import CodeTrimmerException

logger = logging.getLogger(__name__)

CONFIG_FILE_NAMES = [".codetrimmer.yaml", ".codetrimmer.yml", ".codetrimmer.json"]


class ConfigurationLoader:
    """Service for loading and validating configuration files.

    Supports both YAML and JSON formats.
    """

    def load_configuration(self, directory: str) -> TrimmerConfig:
        """Load configuration from default locations.

        Searches for .codetrimmer.yaml, .codetrimmer.yml, or .codetrimmer.json
        in the given directory.

        Args:
            directory: Directory to search for config files

        Returns:
            Loaded configuration or default if none found
        """
        dir_path = Path(directory)

        for config_name in CONFIG_FILE_NAMES:
            config_path = dir_path / config_name
            if config_path.exists():
                logger.info("Loading configuration from: %s", config_path)
                return self.load_from_file(config_path)

        logger.info("No configuration file found, using defaults")
        return TrimmerConfig()

    def load_from_file(self, config_path: Path) -> TrimmerConfig:
        """Load configuration from a specific file path.

        Args:
            config_path: Path to the config file

        Returns:
            Loaded configuration

        Raises:
            CodeTrimmerException: If file cannot be loaded or is invalid
        """
        if not config_path.exists():
            raise CodeTrimmerException(
                ErrorCode.CT_0002,
                f"File not found: {config_path}",
                "Verify the configuration file exists at the specified path",
            )

        try:
            content = config_path.read_text(encoding="utf-8")
            filename = config_path.name.lower()

            if filename.endswith(".json"):
                config = self._load_from_json(content)
            else:
                config = self._load_from_yaml(content)

            self.validate_configuration(config)
            return config

        except IOError as e:
            raise CodeTrimmerException(
                ErrorCode.CT_0011,
                f"Cannot read configuration file: {e}",
                "Check file permissions and encoding",
            ) from e

    def _load_from_json(self, json_content: str) -> TrimmerConfig:
        """Load configuration from JSON string.

        Args:
            json_content: JSON content string

        Returns:
            Parsed configuration
        """
        try:
            data = json.loads(json_content)
            return self._dict_to_config(data)
        except json.JSONDecodeError as e:
            raise CodeTrimmerException(
                ErrorCode.CT_0001,
                f"Invalid JSON format: {e}",
                "Verify JSON syntax using a validator",
            ) from e

    def _load_from_yaml(self, yaml_content: str) -> TrimmerConfig:
        """Load configuration from YAML string.

        Args:
            yaml_content: YAML content string

        Returns:
            Parsed configuration
        """
        try:
            data = yaml.safe_load(yaml_content)
            if data is None:
                return TrimmerConfig()
            return self._dict_to_config(data)
        except yaml.YAMLError as e:
            raise CodeTrimmerException(
                ErrorCode.CT_0001,
                f"Invalid YAML format: {e}",
                "Verify YAML syntax and indentation",
            ) from e

    def _dict_to_config(self, data: Dict[str, Any]) -> TrimmerConfig:
        """Convert dictionary to TrimmerConfig.

        Args:
            data: Dictionary from parsed YAML/JSON

        Returns:
            TrimmerConfig instance
        """
        # Handle nested 'codetrimmer' key
        if "codetrimmer" in data:
            data = data["codetrimmer"]

        # Convert hyphenated keys to underscores
        normalized = {}
        for key, value in data.items():
            normalized_key = key.replace("-", "_")
            normalized[normalized_key] = value

        # Parse rules
        rules = []
        if "rules" in normalized:
            for rule_data in normalized["rules"]:
                rule_normalized = {
                    k.replace("-", "_"): v for k, v in rule_data.items()
                }
                rules.append(TrimRule(**rule_normalized))
            normalized["rules"] = rules

        # Create config with only known fields
        config_fields = {
            "include", "exclude", "include_hidden", "follow_symlinks",
            "max_consecutive_blank_lines", "ensure_final_newline",
            "trim_trailing_whitespace", "max_file_size", "max_files",
            "no_limits", "dry_run", "create_backups", "fail_fast",
            "verbose", "quiet", "no_color", "disable_color_for_pipe",
            "report", "report_output", "report_endpoint", "diff", "rules",
        }

        filtered = {k: v for k, v in normalized.items() if k in config_fields}
        return TrimmerConfig(**filtered)

    def validate_configuration(self, config: TrimmerConfig) -> None:
        """Validate the loaded configuration.

        Args:
            config: Configuration to validate

        Raises:
            CodeTrimmerException: If validation fails
        """
        if config.max_file_size < 0:
            raise CodeTrimmerException(
                ErrorCode.CT_0003,
                "max_file_size must be non-negative",
                "Set max_file_size to a positive value or 0 for unlimited",
            )

        if config.max_files < 0:
            raise CodeTrimmerException(
                ErrorCode.CT_0003,
                "max_files must be non-negative",
                "Set max_files to a positive value or 0 for unlimited",
            )

        if config.max_consecutive_blank_lines < 0:
            raise CodeTrimmerException(
                ErrorCode.CT_0003,
                "max_consecutive_blank_lines must be non-negative",
                "Set max_consecutive_blank_lines to 0 or higher",
            )

        # Validate custom rules
        for rule in config.rules:
            self._validate_rule(rule)

    def _validate_rule(self, rule: TrimRule) -> None:
        """Validate a custom trimming rule.

        Args:
            rule: Rule to validate

        Raises:
            CodeTrimmerException: If rule is invalid
        """
        if not rule.name or not rule.name.strip():
            raise CodeTrimmerException(
                ErrorCode.CT_0004,
                "Rule name is required",
                "Add a 'name' field to the rule definition",
            )

        if not rule.pattern or not rule.pattern.strip():
            raise CodeTrimmerException(
                ErrorCode.CT_0004,
                f"Rule pattern is required for rule: {rule.name}",
                "Add a 'pattern' field with a valid regex",
            )

        try:
            re.compile(rule.pattern)
        except re.error as e:
            raise CodeTrimmerException(
                ErrorCode.CT_0005,
                f"Invalid regex pattern in rule '{rule.name}': {e}",
                "Fix the regex pattern syntax",
            ) from e

    def load_env_vars(self) -> Dict[str, Any]:
        """Load configuration from environment variables.

        Environment variables are prefixed with CODETRIMMER_.

        Returns:
            Dictionary of configuration values from environment
        """
        env_config: Dict[str, Any] = {}
        prefix = "CODETRIMMER_"

        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower().replace("_", "_")
                env_config[config_key] = self._parse_env_value(value)

        return env_config

    def _parse_env_value(self, value: str) -> Any:
        """Parse environment variable value to appropriate type.

        Args:
            value: String value from environment

        Returns:
            Parsed value (bool, int, or string)
        """
        # Boolean
        if value.lower() in ("true", "1", "yes", "on"):
            return True
        if value.lower() in ("false", "0", "no", "off"):
            return False

        # Integer
        try:
            return int(value)
        except ValueError:
            pass

        return value

    def apply_configuration(
        self,
        source: TrimmerConfig,
        target: CodeTrimmerConfig,
    ) -> None:
        """Apply configuration from source to target.

        Args:
            source: Source configuration
            target: Target configuration to update
        """
        target.include = source.include
        target.exclude = source.exclude
        target.include_hidden = source.include_hidden
        target.follow_symlinks = source.follow_symlinks
        target.max_consecutive_blank_lines = source.max_consecutive_blank_lines
        target.ensure_final_newline = source.ensure_final_newline
        target.trim_trailing_whitespace = source.trim_trailing_whitespace
        target.max_file_size = source.max_file_size
        target.max_files = source.max_files
        target.no_limits = source.no_limits
        target.dry_run = source.dry_run
        target.create_backups = source.create_backups
        target.fail_fast = source.fail_fast
        target.verbose = source.verbose
        target.quiet = source.quiet
        target.no_color = source.no_color
        target.rules = source.rules.copy()

    def merge_configs(
        self,
        file_config: TrimmerConfig,
        env_config: Dict[str, Any],
        cli_options: Optional[Dict[str, Any]] = None,
    ) -> CodeTrimmerConfig:
        """Merge configurations with priority: CLI > Env > File > Defaults.

        Args:
            file_config: Configuration from file
            env_config: Configuration from environment variables
            cli_options: Configuration from CLI options

        Returns:
            Merged configuration
        """
        result = CodeTrimmerConfig()
        self.apply_configuration(file_config, result)

        # Apply environment config
        for key, value in env_config.items():
            if hasattr(result, key):
                setattr(result, key, value)

        # Apply CLI options (highest priority)
        if cli_options:
            for key, value in cli_options.items():
                if value is not None and hasattr(result, key):
                    setattr(result, key, value)

        return result
