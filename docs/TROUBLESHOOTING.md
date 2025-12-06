# Troubleshooting Guide

Common issues and solutions for Code Trimmer Python.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Configuration Issues](#configuration-issues)
3. [File Processing Issues](#file-processing-issues)
4. [Performance Issues](#performance-issues)
5. [Git Hook Issues](#git-hook-issues)
6. [Report Generation Issues](#report-generation-issues)

## Installation Issues

### Q: ModuleNotFoundError: No module named 'codetrimmer'

**Solution:**

```bash
pip install codetrimmer
# or for development
pip install -e .
```

### Q: Command 'codetrimmer' not found

**Solution:**

1. Ensure the package is installed
2. Check if pip's bin directory is in PATH
3. Try running as module: `python -m codetrimmer`

### Q: Dependency conflicts

**Solution:**

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Unix
venv\Scripts\activate     # Windows

# Install fresh
pip install codetrimmer
```

## Configuration Issues

### Q: Configuration file not being loaded

**Solution:**

1. Ensure file is named `.codetrimmer.yaml` or `.codetrimmer.json`
2. File must be in the project root or specified with `--config`
3. Check file permissions

### Q: YAML parsing error

**Solution:**

1. Validate YAML syntax at https://yamlint.com
2. Use proper indentation (2 spaces recommended)
3. Quote strings with special characters

**Example of correct YAML:**

```yaml
codetrimmer:
  include: "*.{py,js}"
  max-consecutive-blank-lines: 2
```

### Q: Invalid regex pattern error

**Solution:**

1. Test regex at https://regex101.com
2. Use raw strings: `pattern: '\s+$'`
3. Escape backslashes in JSON: `"pattern": "\\s+$"`

## File Processing Issues

### Q: Files not being processed

**Possible causes and solutions:**

1. **Pattern mismatch:**

   ```bash
   # Use verbose to see what's being matched
   codetrimmer trim . --verbose
   ```

2. **Hidden files:**

   ```bash
   # Include hidden files
   codetrimmer trim . --include-hidden
   ```

3. **Binary detection:**
   - Binary files are automatically skipped
   - Check if files contain null bytes

### Q: "File too large" error

**Solution:**

```bash
# Increase limit
codetrimmer trim . --max-file-size 10485760  # 10MB

# Or disable limits
codetrimmer trim . --no-limits
```

### Q: "Permission denied" error

**Solution:**

1. Check file permissions: `ls -la filename`
2. Run with appropriate user
3. Skip problematic files with `--exclude`

### Q: Encoding errors

**Solution:**

- Code Trimmer tries UTF-8 first, then Latin-1
- For other encodings, convert files first:

  ```bash
  iconv -f ISO-8859-1 -t UTF-8 file.txt > file_utf8.txt
  ```

### Q: Files modified incorrectly

**Solution:**

1. Use `--dry-run --diff` to preview changes
2. Enable backups: `--create-backups`
3. Restore from backups: `codetrimmer undo .`

## Performance Issues

### Q: Processing is slow

**Solution:**

1. Limit files:

   ```bash
   codetrimmer trim . --max-files 100
   ```

2. Exclude large directories:

   ```bash
   codetrimmer trim . --exclude "node_modules/**,venv/**"
   ```

3. Process specific file types:

   ```bash
   codetrimmer trim . --include "*.py"
   ```

### Q: Out of memory

**Solution:**

1. Process smaller batches:

   ```bash
   codetrimmer trim . --max-files 50
   ```

2. Limit file sizes:

   ```bash
   codetrimmer trim . --max-file-size 1048576  # 1MB
   ```

## Git Hook Issues

### Q: "Git directory not found" error

**Solution:**

1. Run from repository root
2. Initialize Git: `git init`
3. Specify correct path: `codetrimmer generate-hook /path/to/repo`

### Q: "Hook already exists" error

**Solution:**

```bash
# Force overwrite
codetrimmer generate-hook . --force

# Or backup existing hook first
cp .git/hooks/pre-commit .git/hooks/pre-commit.backup
```

### Q: Hook not running

**Solution:**

1. Check hook is executable:

   ```bash
   chmod +x .git/hooks/pre-commit
   ```

2. Verify codetrimmer is installed globally or in PATH

3. Check hook script for errors:

   ```bash
   bash -x .git/hooks/pre-commit
   ```

### Q: Hook blocking commits

**Solution:**

1. Run trimmer manually first:

   ```bash
   codetrimmer trim .
   ```

2. Bypass hook temporarily:

   ```bash
   git commit --no-verify
   ```

## Report Generation Issues

### Q: "Invalid report format" error

**Solution:**
Use valid format: `json`, `csv`, or `sqlite`

```bash
codetrimmer trim . --report json
```

### Q: SQLite database error

**Solution:**

1. Check write permissions on output path
2. Ensure parent directory exists
3. Verify disk space

### Q: HTTP endpoint failed

**Solution:**

1. Verify URL is correct and accessible
2. Check network connectivity
3. Ensure endpoint accepts POST requests
4. Install aiohttp: `pip install codetrimmer[http]`

## Getting More Help

1. **Verbose output:**

   ```bash
   codetrimmer trim . --verbose
   ```

2. **Check version:**

   ```bash
   codetrimmer --version
   ```

3. **Command help:**

   ```bash
   codetrimmer trim --help
   ```

4. **Report bugs:**

   - GitHub Issues: https://github.com/pbaletkeman/code-trimmer-python/issues
   - Include error message, command used, and Python version
