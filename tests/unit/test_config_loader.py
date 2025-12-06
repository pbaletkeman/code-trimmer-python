"""Tests for ConfigurationLoader."""

import json
from pathlib import Path

import pytest
import yaml

from codetrimmer.config.loader import ConfigurationLoader
from codetrimmer.config.models import TrimmerConfig, TrimRule
from codetrimmer.error.codes import ErrorCode
from codetrimmer.error.exceptions import CodeTrimmerException


class TestConfigurationLoader:
    """Tests for ConfigurationLoader class."""

    def test_load_default_config(self, temp_dir: Path) -> None:
        """Test loading default config when no file exists."""
        loader = ConfigurationLoader()
        config = loader.load_configuration(str(temp_dir))

        assert config.include == "*"
        assert config.max_consecutive_blank_lines == 2
        assert config.ensure_final_newline is True

    def test_load_yaml_config(self, yaml_config_file: Path) -> None:
        """Test loading YAML configuration."""
        loader = ConfigurationLoader()
        config = loader.load_from_file(yaml_config_file)

        assert config.include == "*.py"
        assert config.exclude == "*.pyc"
        assert config.max_consecutive_blank_lines == 2
        assert len(config.rules) == 1
        assert config.rules[0].name == "test-rule"

    def test_load_json_config(self, json_config_file: Path) -> None:
        """Test loading JSON configuration."""
        loader = ConfigurationLoader()
        config = loader.load_from_file(json_config_file)

        assert config.include == "*.py"
        assert config.exclude == "*.pyc"

    def test_config_file_not_found(self, temp_dir: Path) -> None:
        """Test error when config file not found."""
        loader = ConfigurationLoader()
        non_existent = temp_dir / "nonexistent.yaml"

        with pytest.raises(CodeTrimmerException) as exc_info:
            loader.load_from_file(non_existent)

        assert exc_info.value.error_code == ErrorCode.CT_0002

    def test_invalid_yaml_format(self, temp_dir: Path) -> None:
        """Test error on invalid YAML."""
        loader = ConfigurationLoader()
        invalid_file = temp_dir / ".codetrimmer.yaml"
        invalid_file.write_text("invalid: yaml: content: [")

        with pytest.raises(CodeTrimmerException) as exc_info:
            loader.load_from_file(invalid_file)

        assert exc_info.value.error_code == ErrorCode.CT_0001

    def test_invalid_json_format(self, temp_dir: Path) -> None:
        """Test error on invalid JSON."""
        loader = ConfigurationLoader()
        invalid_file = temp_dir / ".codetrimmer.json"
        invalid_file.write_text("{invalid json}")

        with pytest.raises(CodeTrimmerException) as exc_info:
            loader.load_from_file(invalid_file)

        assert exc_info.value.error_code == ErrorCode.CT_0001

    def test_validate_negative_max_file_size(self) -> None:
        """Test validation of negative max_file_size."""
        loader = ConfigurationLoader()
        config = TrimmerConfig(max_file_size=-1)

        with pytest.raises(CodeTrimmerException) as exc_info:
            loader.validate_configuration(config)

        assert exc_info.value.error_code == ErrorCode.CT_0003

    def test_validate_negative_max_files(self) -> None:
        """Test validation of negative max_files."""
        loader = ConfigurationLoader()
        config = TrimmerConfig(max_files=-1)

        with pytest.raises(CodeTrimmerException) as exc_info:
            loader.validate_configuration(config)

        assert exc_info.value.error_code == ErrorCode.CT_0003

    def test_validate_rule_missing_name(self) -> None:
        """Test validation of rule with missing name."""
        loader = ConfigurationLoader()
        config = TrimmerConfig(
            rules=[TrimRule(name="", pattern="test")]
        )

        with pytest.raises(CodeTrimmerException) as exc_info:
            loader.validate_configuration(config)

        assert exc_info.value.error_code == ErrorCode.CT_0004

    def test_validate_rule_missing_pattern(self) -> None:
        """Test validation of rule with missing pattern."""
        loader = ConfigurationLoader()
        config = TrimmerConfig(
            rules=[TrimRule(name="test", pattern="")]
        )

        with pytest.raises(CodeTrimmerException) as exc_info:
            loader.validate_configuration(config)

        assert exc_info.value.error_code == ErrorCode.CT_0004

    def test_validate_rule_invalid_regex(self) -> None:
        """Test validation of rule with invalid regex."""
        loader = ConfigurationLoader()
        config = TrimmerConfig(
            rules=[TrimRule(name="test", pattern="[invalid")]
        )

        with pytest.raises(CodeTrimmerException) as exc_info:
            loader.validate_configuration(config)

        assert exc_info.value.error_code == ErrorCode.CT_0005

    def test_load_env_vars(self, monkeypatch) -> None:
        """Test loading configuration from environment variables."""
        loader = ConfigurationLoader()

        monkeypatch.setenv("CODETRIMMER_MAX_FILES", "100")
        monkeypatch.setenv("CODETRIMMER_VERBOSE", "true")

        env_config = loader.load_env_vars()

        assert env_config.get("max_files") == 100
        assert env_config.get("verbose") is True

    def test_merge_configs(self) -> None:
        """Test merging configurations."""
        loader = ConfigurationLoader()

        file_config = TrimmerConfig(
            include="*.py",
            max_files=10,
        )
        env_config = {"max_files": 50}
        cli_options = {"verbose": True}

        result = loader.merge_configs(file_config, env_config, cli_options)

        assert result.include == "*.py"
        assert result.max_files == 50  # Env overrides file
        assert result.verbose is True  # CLI overrides all
