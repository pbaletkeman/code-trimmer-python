"""Pytest configuration and fixtures."""

import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest

from codetrimmer.config.models import CodeTrimmerConfig, TrimmerConfig, TrimRule


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_text_file(temp_dir: Path) -> Path:
    """Create a sample text file with trailing whitespace."""
    file_path = temp_dir / "sample.txt"
    file_path.write_text("Hello World   \nLine 2  \n\n\n\nLine 3\n")
    return file_path


@pytest.fixture
def sample_python_file(temp_dir: Path) -> Path:
    """Create a sample Python file."""
    file_path = temp_dir / "sample.py"
    file_path.write_text("""def hello():   
    print("Hello")  
    
    
    
    return True
""")
    return file_path


@pytest.fixture
def sample_binary_file(temp_dir: Path) -> Path:
    """Create a sample binary file."""
    file_path = temp_dir / "sample.bin"
    file_path.write_bytes(b"\x00\x01\x02\x03\x04\x05")
    return file_path


@pytest.fixture
def default_config() -> CodeTrimmerConfig:
    """Create a default configuration."""
    return CodeTrimmerConfig()


@pytest.fixture
def trimmer_config() -> TrimmerConfig:
    """Create a default TrimmerConfig."""
    return TrimmerConfig()


@pytest.fixture
def config_with_rules() -> TrimmerConfig:
    """Create a configuration with custom rules."""
    return TrimmerConfig(
        rules=[
            TrimRule(
                name="remove-trailing-spaces",
                pattern=r"\s+$",
                replacement="",
                description="Remove trailing whitespace",
            ),
        ]
    )


@pytest.fixture
def yaml_config_file(temp_dir: Path) -> Path:
    """Create a sample YAML configuration file."""
    file_path = temp_dir / ".codetrimmer.yaml"
    file_path.write_text("""codetrimmer:
  include: "*.py"
  exclude: "*.pyc"
  max-consecutive-blank-lines: 2
  ensure-final-newline: true
  trim-trailing-whitespace: true
  create-backups: true
  rules:
    - name: "test-rule"
      pattern: "foo"
      replacement: "bar"
      description: "Replace foo with bar"
""")
    return file_path


@pytest.fixture
def json_config_file(temp_dir: Path) -> Path:
    """Create a sample JSON configuration file."""
    file_path = temp_dir / ".codetrimmer.json"
    file_path.write_text("""{
  "codetrimmer": {
    "include": "*.py",
    "exclude": "*.pyc",
    "max-consecutive-blank-lines": 2,
    "ensure-final-newline": true,
    "trim-trailing-whitespace": true,
    "create-backups": true
  }
}""")
    return file_path


@pytest.fixture
def git_repo(temp_dir: Path) -> Path:
    """Create a mock git repository."""
    git_dir = temp_dir / ".git"
    git_dir.mkdir()
    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir()
    return temp_dir
