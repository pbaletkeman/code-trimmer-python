# Configuration Samples

This directory contains example configuration files for Code Trimmer. These files demonstrate different ways to configure the tool for various use cases.

## Table of Contents

- [Overview](#overview)
- [Configuration Files](#configuration-files)
- [YAML Configuration](#yaml-configuration)
- [JSON Configuration](#json-configuration)
- [Custom Rules](#custom-rules)
- [Quick Start](#quick-start)
- [Best Practices](#best-practices)

## Overview

Code Trimmer supports multiple configuration formats:

- **YAML** (`.codetrimmer.yaml`) - Human-readable, recommended format
- **JSON** (`.codetrimmer.json`) - Structured, programmatic format
- **Custom Rules** - Advanced regex-based transformations

Place configuration files in your project root, and Code Trimmer will automatically detect them.

## Configuration Files

### `.codetrimmer.yaml` (Recommended)

Human-readable YAML format - recommended for most projects.

**When to use:**

- Most projects
- Human-readable configuration
- Support for comments
- Easier version control reviews

**Key features:**

- Comments explain each option
- Clear structure with sections
- Support for complex patterns
- Easy to edit manually

**Location:** Root of project: `.codetrimmer.yaml`

**Example:**

```yaml
codetrimmer:
  include: "*.{py,js,ts,md}"
  exclude: "node_modules/**,dist/**"
  max-consecutive-blank-lines: 2
  ensure-final-newline: true
  trim-trailing-whitespace: true
  create-backups: true
  verbose: false
```

### `.codetrimmer.json`

JSON format - useful for programmatic configuration or tool integration.

**When to use:**

- Tool integration
- Programmatic generation
- Standardized tooling
- Web-based configuration

**Key features:**

- Structured format
- Easy to parse programmatically
- Integrates with build tools
- Supports validation schemas

**Location:** Root of project: `.codetrimmer.json`

**Example:**

```json
{
  "codetrimmer": {
    "include": "*.{py,js,ts}",
    "exclude": "node_modules/**",
    "max-consecutive-blank-lines": 2,
    "ensure-final-newline": true,
    "trim-trailing-whitespace": true
  }
}
```

### `sample-rules.yaml`

Advanced custom regex rules for specialized transformations.

**When to use:**

- Project-specific transformations
- Removing debug statements
- Normalizing patterns
- Enforcing code standards

**Key features:**

- Named rules with descriptions
- Regex pattern matching
- Custom replacements
- Chainable transformations

**Location:** Reference file: `docs/samples/sample-rules.yaml`

## YAML Configuration

### Configuration Options

```yaml
codetrimmer:
  # File Selection
  # ==============
  # Files to include (glob patterns, comma-separated)
  include: "*.{py,js,java,ts,jsx,tsx,md}"

  # Files to exclude (glob patterns)
  exclude: "node_modules/**,*.min.js,dist/**"

  # Include hidden files (starting with .)
  include-hidden: false

  # Follow symbolic links
  follow-symlinks: false

  # Whitespace Rules
  # ================
  # Maximum consecutive blank lines
  max-consecutive-blank-lines: 2

  # Ensure file ends with single newline
  ensure-final-newline: true

  # Trim trailing whitespace from lines
  trim-trailing-whitespace: true

  # Performance Limits
  # ==================
  # Maximum file size in bytes (default: 5MB)
  max-file-size: 5242880

  # Maximum number of files to process
  max-files: 1000

  # Disable all limits
  no-limits: false

  # Operation Modes
  # ================
  # Preview changes without modifying
  dry-run: false

  # Create .bak backup files
  create-backups: true

  # Stop on first error
  fail-fast: false

  # Output Options
  # ================
  # Detailed output
  verbose: false

  # Minimal output
  quiet: false

  # Disable colored output
  no-color: false
```

### Common Configurations

#### Python Project

```yaml
codetrimmer:
  include: "**/*.py"
  exclude: "venv/**,dist/**,build/**,.git/**"
  max-consecutive-blank-lines: 2
  ensure-final-newline: true
  trim-trailing-whitespace: true
  create-backups: true
```

#### Node.js/TypeScript Project

```yaml
codetrimmer:
  include: "**/*.{js,ts,jsx,tsx}"
  exclude: "node_modules/**,dist/**,build/**,coverage/**"
  max-consecutive-blank-lines: 2
  ensure-final-newline: true
  trim-trailing-whitespace: true
  create-backups: true
```

#### Documentation Project

```yaml
codetrimmer:
  include: "**/*.md"
  exclude: "node_modules/**"
  max-consecutive-blank-lines: 1
  ensure-final-newline: true
  trim-trailing-whitespace: true
  create-backups: true
  verbose: true
```

## JSON Configuration

### Basic Structure

```json
{
  "codetrimmer": {
    "include": "*.py",
    "exclude": "venv/**",
    "max-consecutive-blank-lines": 2,
    "ensure-final-newline": true,
    "trim-trailing-whitespace": true,
    "create-backups": true,
    "verbose": false
  }
}
```

### Schema Validation

Code Trimmer validates JSON configuration against a schema. This ensures:

- Required fields are present
- Values have correct types
- No unknown options are used
- Clear error messages if invalid

## Custom Rules

### Rule Structure

Each rule has:

- `name`: Unique identifier for the rule
- `pattern`: Regex pattern to match
- `replacement`: String to replace matches with
- `description`: Human-readable description

### Example Rules

#### Remove Python Debugging

```yaml
- name: "remove-debug-prints"
  pattern: 'print\s*\(\s*["\']DEBUG:'
  replacement: "# DEBUG: "
  description: "Comment out debug print statements"
```

#### Normalize Line Endings

```yaml
- name: "normalize-crlf"
  pattern: '\r\n'
  replacement: "\n"
  description: "Convert CRLF to LF"
```

#### Fix Common Typos

```yaml
- name: "fix-common-typo"
  pattern: "recieve"
  replacement: "receive"
  description: "Fix 'recieve' -> 'receive' typo"
```

### Advanced Patterns

#### Removing Code Blocks

```yaml
- name: "remove-commented-code"
  pattern: '^#\s*def\s+\w+\(.*?\):'
  replacement: ""
  description: "Remove commented-out function definitions"
```

#### Formatting Standards

```yaml
- name: "normalize-import-spacing"
  pattern: 'import\s{2,}'
  replacement: "import "
  description: "Fix spacing in import statements"
```

## Quick Start

### Using `.codetrimmer.yaml`

1. **Copy sample configuration:**

   ```bash
   cp docs/samples/.codetrimmer.yaml .
   ```

2. **Edit for your project:**

   ```bash
   # Modify include/exclude patterns
   # Adjust whitespace rules
   # Add custom rules if needed
   ```

3. **Preview changes:**

   ```bash
   codetrimmer trim . --dry-run
   ```

4. **Apply changes:**

   ```bash
   codetrimmer trim .
   ```

### Using `.codetrimmer.json`

1. **Copy sample configuration:**

   ```bash
   cp docs/samples/.codetrimmer.json .
   ```

2. **Edit for your project:**

   ```bash
   # Use JSON editor or text editor
   # Validate JSON syntax
   ```

3. **Preview changes:**

   ```bash
   codetrimmer trim . --dry-run
   ```

4. **Apply changes:**

   ```bash
   codetrimmer trim .
   ```

## Best Practices

### File Selection

- **Be specific with patterns:** `**/*.py` is better than `**/*`
- **Exclude build directories:** Always exclude `dist/`, `build/`, `node_modules/`
- **Exclude version control:** Add `.git/`, `.hg/`
- **Test patterns first:** Use `--dry-run` to verify what will be matched

```yaml
include: "**/*.{py,js,ts}"
exclude: "venv/**,dist/**,node_modules/**,.git/**"
```

### Whitespace Rules

- **Conservative settings:** Start with standard settings
- **Test gradually:** Make changes incrementally
- **Review diffs:** Always check what changed before committing
- **Use backups:** Always enable `create-backups: true` initially

```yaml
max-consecutive-blank-lines: 2
ensure-final-newline: true
trim-trailing-whitespace: true
```

### Custom Rules

- **Test rules carefully:** Rules modify code, test thoroughly
- **Document rules:** Add clear descriptions
- **Version control:** Commit rule changes with other code changes
- **Be conservative:** Avoid rules that remove semantically important content

```yaml
rules:
  - name: "my-rule"
    pattern: "find_this"
    replacement: "replace_with_this"
    description: "Clear description of what this rule does"
```

### Safety

- **Always backup:** Enable `create-backups: true`
- **Use dry-run:** Always preview changes first
- **Use version control:** Commit before running
- **Test on sample:** Test on a subset before full project

```yaml
create-backups: true
dry-run: true # Change to false after review
```

### Performance

- **Set appropriate limits:** Don't set `no-limits: true` without reason
- **Watch file count:** Monitor `max-files` for large projects
- **Monitor performance:** Use `verbose: true` during testing

```yaml
max-file-size: 5242880 # 5MB
max-files: 10000
no-limits: false
```

## Troubleshooting

### Files Not Being Processed

**Issue:** Expected files not included

**Solution:**

1. Check `include` pattern matches your files
2. Check `exclude` pattern doesn't match your files
3. Use `--dry-run --verbose` to see which files are processed
4. Verify glob patterns with examples

### Unexpected Changes

**Issue:** Files changed in unexpected ways

**Solution:**

1. Check custom rules carefully
2. Review regex patterns for side effects
3. Use `--dry-run` to preview
4. Test rules on sample files first
5. Consider simplifying rules

### Configuration Not Loading

**Issue:** Configuration file ignored

**Solution:**

1. Verify file is named correctly (`.codetrimmer.yaml` or `.codetrimmer.json`)
2. Verify file is in project root
3. Verify file format is valid
4. Use `--verbose` to see configuration loading

## See Also

- [Configuration Guide](../CONFIGURATION.md) - Complete documentation
- [CLI Reference](../CLI_REFERENCE.md) - Command-line options
- [Troubleshooting](../TROUBLESHOOTING.md) - Common issues and solutions
- [Architecture](../ARCHITECTURE.md) - How Code Trimmer works
