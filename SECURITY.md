# Security Policy

## Table of Contents

- [Supported Versions](#supported-versions)
- [Reporting a Vulnerability](#reporting-a-vulnerability)
- [Security Best Practices](#security-best-practices)
- [Dependencies](#dependencies)
- [Data Handling](#data-handling)

## Supported Versions

| Version | Supported | Status          |
| ------- | --------- | --------------- |
| 1.0.x   | ✅ Yes    | Current release |
| < 1.0   | ❌ No     | Not supported   |

We support the latest released version. Security patches are released for critical vulnerabilities.

## Reporting a Vulnerability

**Do not disclose security vulnerabilities publicly.** Instead:

1. **Email your report** to the project maintainer at `pbaletkeman@github.com`
2. **Include the following information:**

   - Description of the vulnerability
   - Steps to reproduce (if applicable)
   - Potential impact
   - Suggested fix (if available)
   - Your name/contact information for follow-up

3. **What to expect:**

   - Acknowledgment within 48 hours
   - Investigation and assessment
   - Coordinated disclosure once patched
   - Credit in release notes (if desired)

4. **Timeline:**
   - Critical vulnerabilities: Patch within 7 days
   - High severity: Patch within 14 days
   - Medium/Low: Included in next release

## Security Best Practices

### File Processing

- **Input Validation:** All file paths are validated before processing
- **Safe Deletion:** Backup files created before any modifications
- **Permission Preservation:** File permissions are maintained during processing
- **Binary Detection:** Non-text files are automatically detected and skipped

### Configuration

- **Configuration Validation:** All configuration is validated against defined schemas
- **Sensitive Data:** Never log sensitive configuration values
- **File Permissions:** Configuration files should have appropriate read permissions

### Git Integration

- **Pre-commit Hooks:** Generated hooks are safely installed to `.git/hooks/`
- **Hook Validation:** All generated scripts are validated before execution
- **Reversibility:** Hooks can be easily removed or updated

## Dependencies

### Direct Dependencies

- **click** (>=8.0.0): CLI framework - [security advisory search](https://pypi.org/project/click/)
- **pyyaml** (>=6.0): YAML parsing - [security advisory search](https://pypi.org/project/pyyaml/)
- **pydantic** (>=2.0.0): Data validation - [security advisory search](https://pypi.org/project/pydantic/)
- **colorama** (>=0.4.6): Cross-platform colors - [security advisory search](https://pypi.org/project/colorama/)

### Dependency Security

We regularly scan dependencies for known vulnerabilities:

- Run `pip-audit` to check for vulnerable dependencies: `pip install pip-audit && pip-audit`
- Check specific packages: `python -m pip index versions PACKAGE_NAME`
- Review [PyPI security advisories](https://pypi.org/project/pip-audit/)

### Development Dependencies

- **black**: Code formatter
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting

## Data Handling

### What Code Trimmer Processes

- **Local Files Only:** This tool processes files on your local filesystem
- **No Network Transmission:** File contents are never transmitted over the network
- **No Tracking:** No usage data or telemetry is collected
- **No Logging of Content:** File content is not logged; only file paths and operations are tracked

### What You Should Know

1. **Backups:** Ensure you have backups of important files before running trim operations
2. **Version Control:** Use Git or another VCS for version control
3. **Undo Feature:** The undo feature requires backup files to exist
4. **Configuration Files:** Keep configuration files secure if they contain paths to sensitive locations

### Safe Usage Recommendations

1. **Always use version control** before running bulk operations
2. **Test with `--dry-run` flag** to preview changes before applying
3. **Use Git hooks carefully** and review generated scripts
4. **Review configuration files** for correct patterns and exclusions
5. **Regularly backup** important source files

## Security Configuration

### Recommended `.codetrimmer.yaml` Practices

```yaml
# ✅ Good: Explicit includes/excludes
rules:
  trailing_whitespace: true
  trailing_newlines: true

exclude:
  # Never trim generated files or third-party code
  - "**/node_modules/**"
  - "**/.venv/**"
  - "**/dist/**"
  - "**/build/**"

include:
  # Only process code files
  - "**/*.py"
  - "**/*.js"
  - "**/*.ts"
```

```yaml
# ❌ Avoid: Overly broad patterns
exclude:
  - ".gitignore" # Too vague - be specific
```

## Security Audit Checklist

Before using in production, verify:

- [ ] Configuration file is reviewed and correct
- [ ] Exclude patterns cover generated and third-party code
- [ ] Backup strategy is in place
- [ ] Dry-run preview looks correct
- [ ] Team is aware of the tool's behavior
- [ ] Version control history is clean
- [ ] Dependencies are up to date

## Vulnerability Disclosure

If you discover a vulnerability, please report it responsibly:

1. Do not open a public GitHub issue
2. Do not post about it on social media
3. Email the maintainer directly
4. Allow time for a patch before public disclosure

## License

This security policy is part of the Code Trimmer project, licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Additional Resources

- [OWASP Security Best Practices](https://owasp.org/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [PyPI Security Advisories](https://pypi.org/advisories/)
- [Common Vulnerabilities and Exposures (CVE)](https://cve.mitre.org/)
