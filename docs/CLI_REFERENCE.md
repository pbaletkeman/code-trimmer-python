# CLI Reference

Complete command-line interface reference for Code Trimmer.

## Global Options

```bash
codetrimmer [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.
```

## Commands

### trim

Trim whitespace from files in a directory.

```bash
codetrimmer trim [OPTIONS] [DIRECTORY]
```

**Arguments:**
- `DIRECTORY` - Directory to process (default: current directory)

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--include` | TEXT | `*` | File glob pattern to include |
| `--exclude` | TEXT | | File glob pattern to exclude |
| `--include-hidden` | FLAG | | Include hidden files |
| `--follow-symlinks` | FLAG | | Follow symbolic links |
| `--max-consecutive-blank-lines` | INT | 2 | Maximum consecutive blank lines |
| `--ensure-final-newline/--no-ensure-final-newline` | | true | Ensure file ends with newline |
| `--trim-trailing-whitespace/--no-trim-trailing-whitespace` | | true | Trim trailing whitespace |
| `--max-file-size` | INT | 5242880 | Max file size in bytes |
| `--max-files` | INT | 50 | Max files to process |
| `--no-limits` | FLAG | | Disable all limits |
| `--dry-run` | FLAG | | Preview changes without modifying |
| `--create-backups/--no-create-backups` | | true | Create .bak backup files |
| `--fail-fast` | FLAG | | Stop on first error |
| `-v, --verbose` | FLAG | | Detailed output |
| `-q, --quiet` | FLAG | | Minimal output |
| `--no-color` | FLAG | | Disable colored output |
| `--disable-color-for-pipe/--no-disable-color-for-pipe` | | true | Disable colors when piped |
| `--config` | PATH | | Config file path |
| `--report` | CHOICE | | Report format: json/csv/sqlite |
| `--report-output` | TEXT | codetrimmer-report.json | Report file path |
| `--report-endpoint` | TEXT | | HTTP endpoint for reports |
| `--diff` | FLAG | | Show diff in dry-run |

**Examples:**

```bash
# Basic usage
codetrimmer trim .

# Dry-run with diff
codetrimmer trim . --dry-run --diff --verbose

# Only Python files
codetrimmer trim . --include "*.py"

# Generate JSON report
codetrimmer trim . --report json --report-output report.json

# Custom config file
codetrimmer trim . --config /path/to/.codetrimmer.yaml
```

### generate-hook

Generate a Git pre-commit hook.

```bash
codetrimmer generate-hook [OPTIONS] [DIRECTORY]
```

**Arguments:**
- `DIRECTORY` - Git repository directory (default: current directory)

**Options:**

| Option | Type | Description |
|--------|------|-------------|
| `--force` | FLAG | Overwrite existing hook |
| `-v, --verbose` | FLAG | Detailed output |
| `-q, --quiet` | FLAG | Minimal output |
| `--no-color` | FLAG | Disable colored output |

**Examples:**

```bash
# Generate hook
codetrimmer generate-hook .

# Force overwrite
codetrimmer generate-hook . --force
```

### undo

Restore files from backups.

```bash
codetrimmer undo [OPTIONS] [DIRECTORY]
```

**Arguments:**
- `DIRECTORY` - Directory with backup files (default: current directory)

**Options:**

| Option | Type | Description |
|--------|------|-------------|
| `--undo-dir` | PATH | Directory with backup files |
| `-v, --verbose` | FLAG | Detailed output |
| `-q, --quiet` | FLAG | Minimal output |
| `--no-color` | FLAG | Disable colored output |

**Examples:**

```bash
# Restore all backups in current directory
codetrimmer undo .

# Restore from specific directory
codetrimmer undo --undo-dir /path/to/backups
```

## Exit Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | Error (files with errors or other failures) |

## Pattern Syntax

The `--include` and `--exclude` options support glob patterns:

- `*` - Match any characters
- `?` - Match single character
- `**` - Match directories recursively
- `{a,b}` - Match either a or b

**Examples:**

```bash
# Multiple extensions
--include "*.{py,js,java}"

# Exclude directories
--exclude "node_modules/**,dist/**"

# Multiple patterns
--include "*.py" --exclude "*_test.py"
```
