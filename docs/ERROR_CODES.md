# Error Codes Reference

Complete list of error codes and their solutions.

## Configuration Errors (CT-0001 to CT-0005)

### CT-0001: Invalid configuration file

**Description:** Configuration file format is invalid.

**Cause:** YAML or JSON syntax error in the configuration file.

**Solution:**
1. Validate YAML syntax using a YAML linter
2. Check for proper indentation
3. Ensure all strings are properly quoted

### CT-0002: Configuration file not found

**Description:** Specified config file does not exist.

**Cause:** The `--config` path points to a non-existent file.

**Solution:**
1. Verify the file path is correct
2. Check file permissions
3. Use absolute path if relative path isn't working

### CT-0003: Invalid configuration value

**Description:** Configuration value is out of range.

**Cause:** A numeric value is negative or invalid.

**Solution:**
1. Check that `max-file-size` is non-negative
2. Check that `max-files` is non-negative
3. Check that `max-consecutive-blank-lines` is non-negative

### CT-0004: Invalid rule definition

**Description:** Custom rule is malformed or missing fields.

**Cause:** A rule in the `rules` section is missing required fields.

**Solution:**
1. Ensure each rule has a `name` field
2. Ensure each rule has a `pattern` field
3. Check rule field names for typos

### CT-0005: Invalid regex pattern

**Description:** Regex pattern in rule is invalid.

**Cause:** The `pattern` field contains invalid regex syntax.

**Solution:**
1. Test the regex pattern in a regex tester
2. Escape special characters properly
3. Use raw strings in YAML (`pattern: '\s+'`)

## File Operation Errors (CT-0010 to CT-0016)

### CT-0010: File not found

**Description:** Specified file or directory does not exist.

**Cause:** The directory or file path is invalid.

**Solution:**
1. Verify the path exists
2. Check for typos in the path
3. Use absolute paths

### CT-0011: File read error

**Description:** Cannot read file contents.

**Cause:** File encoding issues or read permissions.

**Solution:**
1. Check file permissions
2. Try specifying file encoding
3. Verify file is not locked by another process

### CT-0012: File write error

**Description:** Cannot write to file.

**Cause:** Write permissions or disk space issues.

**Solution:**
1. Check file write permissions
2. Verify disk has free space
3. Check if file is read-only

### CT-0013: Permission denied

**Description:** Insufficient permissions to access file.

**Cause:** User doesn't have required permissions.

**Solution:**
1. Run with appropriate permissions
2. Check file ownership
3. Use `sudo` if necessary (with caution)

### CT-0014: Directory not accessible

**Description:** Cannot access or traverse directory.

**Cause:** Directory permissions or invalid path.

**Solution:**
1. Check directory permissions
2. Verify path is a directory, not a file
3. Check for broken symlinks

### CT-0015: File too large

**Description:** File exceeds maximum size limit.

**Cause:** File is larger than `max-file-size`.

**Solution:**
1. Use `--no-limits` to process large files
2. Increase `max-file-size` in config
3. Process the file separately

### CT-0016: Binary file skipped

**Description:** Binary file detected and skipped.

**Cause:** File was detected as binary (contains null bytes).

**Solution:**
- This is expected behavior
- Binary files are automatically skipped to prevent corruption
- No action required

## Backup/Restore Errors (CT-0040 to CT-0043)

### CT-0040: Backup creation failed

**Description:** Failed to create backup file.

**Cause:** Disk full or permission issues.

**Solution:**
1. Check available disk space
2. Verify write permissions
3. Use `--no-create-backups` if backups not needed

### CT-0041: Restore failed

**Description:** Failed to restore from backup.

**Cause:** File permission or I/O error.

**Solution:**
1. Check file permissions
2. Verify backup file isn't corrupted
3. Restore manually if needed

### CT-0042: Backup file missing

**Description:** Backup file not found for restore.

**Cause:** The `.bak` file doesn't exist.

**Solution:**
1. Verify backup was created
2. Check the correct directory
3. Backups may have been cleaned up

### CT-0043: Backup file corrupted

**Description:** Backup file is corrupted or invalid.

**Cause:** Backup file is empty or damaged.

**Solution:**
1. Use version control to restore
2. Restore from other backup source
3. Re-process the file

## Hook Generation Errors (CT-0050 to CT-0052)

### CT-0050: Hook generation failed

**Description:** Failed to generate pre-commit hook.

**Cause:** I/O error writing hook file.

**Solution:**
1. Check write permissions on `.git/hooks/`
2. Verify disk space
3. Create hooks directory manually if missing

### CT-0051: Git directory not found

**Description:** .git directory not found in path.

**Cause:** Not running in a Git repository.

**Solution:**
1. Initialize a Git repository with `git init`
2. Run from the repository root
3. Specify correct directory path

### CT-0052: Hook already exists

**Description:** Pre-commit hook already exists.

**Cause:** A pre-commit hook file is already present.

**Solution:**
1. Use `--force` to overwrite
2. Manually backup existing hook
3. Merge hooks manually

## Report Errors (CT-0060 to CT-0063)

### CT-0060: Report generation failed

**Description:** Failed to generate report.

**Cause:** I/O error writing report file.

**Solution:**
1. Check write permissions
2. Verify disk space
3. Check output path is valid

### CT-0061: Invalid report format

**Description:** Unsupported report format specified.

**Cause:** Invalid `--report` option value.

**Solution:**
1. Use valid format: `json`, `csv`, or `sqlite`
2. Check for typos

### CT-0062: Report endpoint failed

**Description:** Failed to send report to endpoint.

**Cause:** Network error or invalid URL.

**Solution:**
1. Verify endpoint URL
2. Check network connectivity
3. Ensure endpoint accepts POST requests

### CT-0063: SQLite database error

**Description:** Error writing to SQLite database.

**Cause:** Database file access error.

**Solution:**
1. Check database file permissions
2. Verify disk space
3. Ensure path is writable

## General Errors (CT-0090 to CT-0092)

### CT-0090: Unknown error

**Description:** An unexpected error occurred.

**Cause:** Unhandled exception.

**Solution:**
1. Check the error message for details
2. Run with `--verbose` for more info
3. Report bug if reproducible

### CT-0091: Operation cancelled

**Description:** Operation was cancelled by user.

**Cause:** User interrupted with Ctrl+C.

**Solution:**
- No action required
- Re-run the command to complete

### CT-0092: Disk full

**Description:** Insufficient disk space for operation.

**Cause:** Disk is full.

**Solution:**
1. Free up disk space
2. Use `--no-create-backups` to save space
3. Process fewer files at once
