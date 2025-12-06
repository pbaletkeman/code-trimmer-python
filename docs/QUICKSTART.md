# Quick Start Guide

Get started with Code Trimmer Python in 5 minutes.

## Installation

### From PyPI (Recommended)

```bash
pip install codetrimmer
```

### From Source

```bash
git clone https://github.com/pbaletkeman/code-trimmer-python.git
cd code-trimmer-python
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Basic Usage

### 1. Trim Files in Directory

```bash
# Process current directory
codetrimmer trim .

# Process specific directory
codetrimmer trim /path/to/project
```

### 2. Preview Changes (Dry-run)

```bash
codetrimmer trim . --dry-run
```

### 3. See Detailed Diff

```bash
codetrimmer trim . --dry-run --diff --verbose
```

### 4. Process Specific Files

```bash
# Only Python files
codetrimmer trim . --include "*.py"

# Exclude test files
codetrimmer trim . --exclude "*_test.py"
```

### 5. Create Configuration File

Create `.codetrimmer.yaml` in your project:

```yaml
codetrimmer:
  include: "*.{py,js,java,md}"
  exclude: "node_modules/**,*.min.js"
  max-consecutive-blank-lines: 2
  ensure-final-newline: true
  trim-trailing-whitespace: true
  create-backups: true
```

## Common Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview changes without modifying files |
| `--verbose` | Show detailed output |
| `--quiet` | Minimal output |
| `--no-color` | Disable colored output |
| `--create-backups/--no-create-backups` | Enable/disable backup creation |

## Git Integration

Generate a pre-commit hook:

```bash
codetrimmer generate-hook .
```

This creates `.git/hooks/pre-commit` that runs Code Trimmer on staged files.

## Undo Changes

Restore files from backups:

```bash
codetrimmer undo .
```

## Next Steps

- Read the [Configuration Guide](./CONFIGURATION.md)
- See all [CLI Options](./CLI_REFERENCE.md)
- Check [Error Codes](./ERROR_CODES.md) for troubleshooting
