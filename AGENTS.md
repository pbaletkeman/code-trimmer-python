# AI Agents & Automation Guide

This guide explains how to use Code Trimmer with AI agents and automation systems, including best practices for integrating with GitHub Actions, LLMs, and other autonomous tools.

## Table of Contents

- [Overview](#overview)
- [Integration with GitHub Actions](#integration-with-github-actions)
- [LLM Integration](#llm-integration)
- [API-First Usage](#api-first-usage)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

Code Trimmer is designed to be automation-friendly:

- **CLI-First Design:** All functionality is accessible via command-line interface
- **Predictable Output:** Deterministic behavior with consistent formatting
- **Exit Codes:** Clear success/failure indicators for automation
- **Dry-Run Mode:** Preview changes before applying (critical for automation)
- **Configuration:** YAML-based configuration for reproducible behavior

## Integration with GitHub Actions

### Basic Workflow Example

```yaml
name: Code Trimming

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  trim:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install Code Trimmer
        run: pip install code-trimmer

      - name: Preview changes (dry-run)
        run: codetrimmer trim . --dry-run

      - name: Apply trimming
        run: codetrimmer trim .

      - name: Commit changes
        run: |
          git config user.name "Code Trimmer Bot"
          git config user.email "bot@example.com"
          git add .
          git commit -m "chore: apply code trimming" || echo "No changes needed"
          git push
```

### Pre-commit Hook Workflow

```yaml
name: Setup Pre-commit Hook

on: [push]

jobs:
  setup-hook:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install Code Trimmer
        run: pip install code-trimmer

      - name: Generate pre-commit hook
        run: codetrimmer generate-hook .

      - name: Commit hook
        run: |
          git config user.name "Code Trimmer Bot"
          git config user.email "bot@example.com"
          git add .git/hooks/pre-commit
          git commit -m "chore: update pre-commit hook" || echo "No changes"
          git push
```

## LLM Integration

### Using Code Trimmer with Language Models

Code Trimmer output is optimized for LLM processing:

#### Example: Preparing Code for Analysis

```bash
# Generate diff for LLM review
codetrimmer trim . --dry-run --format json > analysis.json

# Use in Python with LLM API
```

```python
import json
import subprocess
from anthropic import Anthropic

client = Anthropic()

# Get trimming diff
result = subprocess.run(
    ["codetrimmer", "trim", ".", "--dry-run", "--format", "json"],
    capture_output=True,
    text=True
)

diff_data = json.loads(result.stdout)

# Send to LLM for review
message = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": f"""Review these code trimming changes and identify any potential issues:

{json.dumps(diff_data, indent=2)}

Are there any changes that look problematic or unexpected?"""
        }
    ]
)

print(message.content[0].text)
```

### Integration Best Practices

1. **Always use dry-run first** before applying automated changes
2. **Review diffs** with LLMs before committing
3. **Store configuration** in version control
4. **Log all changes** for audit trails
5. **Test in staging** before production

## API-First Usage

### Using Code Trimmer as a Module

```python
from codetrimmer.service.trimmer import Trimmer
from codetrimmer.service.file_processor import FileProcessor
from codetrimmer.model.file_result import FileResult
from codetrimmer.config.models import TrimOptions

# Configure trimming options
options = TrimOptions(
    trailing_whitespace=True,
    trailing_newlines=True,
    empty_lines_between_functions=True,
)

# Create trimmer instance
trimmer = Trimmer(options)

# Process files
results = []
for file_path in ["src/main.py", "src/utils.py"]:
    result = trimmer.trim_file(file_path)
    results.append(result)

# Handle results
for result in results:
    if result.modified:
        print(f"Modified: {result.file_path}")
        print(f"Changes: {result.lines_removed} lines removed")
```

### Integration Example: Custom Automation

```python
from pathlib import Path
from codetrimmer.service.trimmer import Trimmer
from codetrimmer.config.loader import ConfigLoader
from codetrimmer.model.file_result import FileResult

class CodeTrimmerAgent:
    def __init__(self, config_path: str = ".codetrimmer.yaml"):
        self.config = ConfigLoader.load(config_path)
        self.trimmer = Trimmer(self.config.options)

    def process_repository(self, repo_path: str) -> dict:
        """Process entire repository and return statistics."""
        stats = {
            "total_files": 0,
            "modified_files": 0,
            "total_lines_removed": 0,
            "errors": []
        }

        for file_path in Path(repo_path).rglob("*"):
            if file_path.is_file() and self._should_process(file_path):
                try:
                    result = self.trimmer.trim_file(str(file_path))
                    stats["total_files"] += 1

                    if result.modified:
                        stats["modified_files"] += 1
                        stats["total_lines_removed"] += result.lines_removed

                except Exception as e:
                    stats["errors"].append({
                        "file": str(file_path),
                        "error": str(e)
                    })

        return stats

    def _should_process(self, file_path: Path) -> bool:
        """Check if file should be processed based on config."""
        # Implement your logic
        return file_path.suffix in [".py", ".js", ".ts"]
```

## Best Practices

### For Automation Systems

1. **Use Dry-Run Mode**

   ```bash
   codetrimmer trim . --dry-run
   ```

2. **Store Configuration in VCS**

   ```yaml
   # .codetrimmer.yaml - always commit this
   rules:
     trailing_whitespace: true
     trailing_newlines: true
   ```

3. **Implement Rollback Strategy**

   ```bash
   # Create backup before running
   codetrimmer trim . --create-backup

   # If needed, rollback
   codetrimmer undo .
   ```

4. **Log All Operations**

   ```bash
   codetrimmer trim . --verbose > trim_$(date +%s).log
   ```

5. **Schedule Safely**
   - Run during off-peak hours
   - Allow time for review before deployment
   - Set up notifications for failures

### For LLM Integration

1. **Provide Context**

   ```python
   # Tell the LLM about your configuration
   with open(".codetrimmer.yaml") as f:
       config = f.read()

   prompt = f"""
   Here's our code trimming configuration:
   {config}

   Review these changes...
   """
   ```

2. **Validate Before Applying**

   - Always get human confirmation for automation
   - Use LLM feedback to refine configuration
   - Document exceptions and special cases

3. **Maintain Audit Trail**
   - Log all automated changes
   - Track LLM decisions
   - Enable rollback

## Troubleshooting

### Common Issues with Automation

#### Issue: Hook not executing

```bash
# Verify hook exists and is executable
ls -la .git/hooks/pre-commit

# Make sure it's executable
chmod +x .git/hooks/pre-commit

# Test it manually
./.git/hooks/pre-commit
```

#### Issue: Changes not applied in CI

```bash
# Check configuration is committed
git ls-files .codetrimmer.yaml

# Verify Python version compatibility
python --version  # Should be 3.11+

# Test locally first
codetrimmer trim . --dry-run
```

#### Issue: LLM receiving inconsistent output

```bash
# Ensure deterministic output
codetrimmer trim . --dry-run --format json

# Verify configuration is stable
cat .codetrimmer.yaml
```

## Examples

See [docs/samples/](docs/samples/) for:

- `.codetrimmer.json` - JSON configuration example
- `.codetrimmer.yaml` - YAML configuration example
- `sample-rules.yaml` - Complex rules example

## Further Reading

- [CLI Reference](docs/CLI_REFERENCE.md) - Complete command documentation
- [Configuration Guide](docs/CONFIGURATION.md) - Configuration options
- [Architecture](docs/ARCHITECTURE.md) - Internal design
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [LLM Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)
