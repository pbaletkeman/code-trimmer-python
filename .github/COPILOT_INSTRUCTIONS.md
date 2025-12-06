# Copilot Instructions for Code Trimmer

This file provides guidance for GitHub Copilot and other AI assistants contributing to the Code Trimmer project.

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture & Code Organization](#architecture--code-organization)
  - [Module Structure](#module-structure)
  - [Key Design Principles](#key-design-principles)
- [Coding Standards](#coding-standards)
  - [Code Style](#code-style)
  - [Example Function](#example-function)
  - [Testing](#testing)
- [When Contributing](#when-contributing)
  - [Before Making Changes](#before-making-changes)
  - [When Adding Features](#when-adding-features)
  - [When Fixing Bugs](#when-fixing-bugs)
- [Common Tasks](#common-tasks)
  - [Add a New Trim Rule](#add-a-new-trim-rule)
  - [Handle a New Error](#handle-a-new-error)
  - [Update Configuration Schema](#update-configuration-schema)
- [Testing Guidance](#testing-guidance)
  - [Running Tests](#running-tests)
  - [Writing Tests](#writing-tests)
- [Documentation Guidelines](#documentation-guidelines)
  - [When to Document](#when-to-document)
  - [Documentation Standards](#documentation-standards)
- [Review Checklist](#review-checklist)
- [Useful Commands](#useful-commands)
- [Getting Help](#getting-help)
- [Philosophy](#philosophy)

## Project Overview

**Code Trimmer** is a Python CLI tool for normalizing whitespace and formatting in source code files. It provides:

- Trailing whitespace removal
- Trailing newline normalization
- Empty line management between functions
- Configuration via YAML or JSON
- Git pre-commit hook generation
- Undo/rollback functionality

**Key Constraints:**

- Python 3.11+
- No external dependencies beyond: click, pyyaml, pydantic, colorama
- Cross-platform (Linux, macOS, Windows)
- MIT Licensed

## Architecture & Code Organization

### Module Structure

```text
codetrimmer/
├── app.py                   # CLI entry point
├── cli/                     # CLI command handling
│   ├── commands.py          # Command implementations
│   ├── options.py           # CLI options
│   └── output.py            # Output formatting
├── config/                  # Configuration handling
│   ├── loader.py            # Load YAML/JSON configs
│   ├── models.py            # Pydantic configuration models
│   └── defaults.py          # Default configuration values
├── service/                 # Business logic
│   ├── trimmer.py           # Core trimming logic
│   ├── file_processor.py    # File I/O operations
│   ├── diff_generator.py    # Generate diffs for dry-run
│   ├── report_generator.py  # Generate reports
│   ├── hook_generator.py    # Generate pre-commit hooks
│   └── undo_service.py      # Backup/restore logic
├── model/                   # Data models
│   ├── file_result.py       # File processing results
│   ├── statistics.py        # Statistics aggregation
│   └── binary_detector.py   # Detect binary files
├── error/                   # Error handling
│   ├── exceptions.py        # Custom exceptions
│   └── codes.py             # Error codes and messages
└── util/                    # Utilities
    ├── color.py             # Color output
    └── constants.py         # Project constants
```

### Key Design Principles

1. **Separation of Concerns**

   - CLI layer (app.py, cli/) handles user input
   - Service layer handles business logic
   - Model layer defines data structures
   - Config layer manages configuration

2. **Safe Operations**

   - Always create backups before modification
   - Validate all inputs
   - Use dry-run for previews
   - Support undo operations

3. **Configuration-Driven**
   - All behavior controlled via config files
   - Sensible defaults provided
   - Schema validation with Pydantic
   - Support for both YAML and JSON

## Coding Standards

### Code Style

- Follow PEP 8
- Use type hints throughout
- 88-character line length (Black formatter compatible)
- Docstrings for all public functions/classes
- Comments explain "why", not "what"

### Example Function

```python
def process_file(file_path: str, options: TrimOptions) -> FileResult:
    """
    Process a single file with trimming rules.

    Args:
        file_path: Path to file to process
        options: Trimming configuration options

    Returns:
        FileResult with modification details

    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If file can't be read
    """
    if not Path(file_path).exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Implementation...
```

### Testing

Unit tests in `tests/unit/`

- Integration tests in `tests/integration/`
- Use pytest framework
- Aim for >80% coverage
- Test both happy path and error cases

## When Contributing

### Before Making Changes

1. **Check existing code:** Review similar functionality
2. **Understand the architecture:** Know where code belongs
3. **Follow patterns:** Use existing patterns as template
4. **Consider backwards compatibility:** Don't break existing behavior
5. **Plan for testing:** Write tests alongside code

### When Adding Features

1. **Add configuration option** (if user-facing):

   - Define in config/models.py
   - Add defaults in config/defaults.py
   - Document in docs/CONFIGURATION.md

2. **Add CLI command** (if user-facing):

   - Implement in cli/commands.py
   - Add options in cli/options.py
   - Update docs/CLI_REFERENCE.md
   - Add tests in tests/unit/test_cli_commands.py

3. **Add service function** (internal logic):

   - Implement in appropriate service module
   - Use type hints
   - Add docstrings
   - Test thoroughly

4. **Error handling:**
   - Use custom exceptions from error/exceptions.py
   - Reference error codes from error/codes.py
   - Provide helpful error messages

### When Fixing Bugs

1. **Add test case first** that reproduces the bug
2. **Fix the bug** with minimal changes
3. **Verify the test passes**
4. **Run full test suite** to catch regressions
5. **Update documentation** if behavior changed

## Common Tasks

### Add a New Trim Rule

1. Add configuration option to `config/models.py`:

   ```python
   class TrimOptions(BaseModel):
       # ... existing options ...
       new_rule: bool = True  # With default value
   ```

2. Implement rule in `service/trimmer.py`:

   ```python
   def _apply_new_rule(self, lines: List[str]) -> List[str]:
       """Apply the new trimming rule."""
       # Implementation
       return lines
   ```

3. Call in `trim_content` method

4. Add test in `tests/unit/test_file_trimmer.py`

5. Update documentation:
   - `docs/CONFIGURATION.md` - Explain the option
   - `docs/CLI_REFERENCE.md` - Add to commands
   - `docs/samples/` - Add example configuration

### Handle a New Error

1. Add error code to `error/codes.py`:

   ```python
   class ErrorCode(Enum):
       # ... existing ...
       NEW_ERROR = ("NEW_001", "Description of error")
   ```

2. Create exception in `error/exceptions.py`:

   ```python
   class NewException(CodeTrimmerException):
       """Description of when this occurs."""
       pass
   ```

3. Raise where appropriate with context

4. Document in `docs/ERROR_CODES.md`

### Update Configuration Schema

1. Modify `config/models.py` with new field
2. Update `config/defaults.py` with default value
3. Add validation logic if needed
4. Update `docs/CONFIGURATION.md`
5. Add test in `tests/unit/test_config_loader.py`

## Testing Guidance

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=codetrimmer --cov-report=html

# Run specific test file
pytest tests/unit/test_file_trimmer.py

# Run specific test
pytest tests/unit/test_file_trimmer.py::test_trailing_whitespace
```

### Writing Tests

```python
def test_new_functionality():
    """Test description of what is being tested."""
    # Arrange - Set up test data
    input_data = "test data"
    expected = "expected result"

    # Act - Call the function
    result = function_under_test(input_data)

    # Assert - Verify results
    assert result == expected
```

## Documentation Guidelines

### When to Document

- New CLI commands → update `docs/CLI_REFERENCE.md`
- Configuration options → update `docs/CONFIGURATION.md`
- Architecture changes → update `docs/ARCHITECTURE.md`
- Error codes → update `docs/ERROR_CODES.md`
- Troubleshooting info → update `docs/TROUBLESHOOTING.md`
- Automation/integration → update `AGENTS.md`

### Documentation Standards

- Use clear, technical language
- Include examples where helpful
- Keep it up-to-date with code
- Link to related documentation
- Include table of contents for docs >100 lines

## Review Checklist

Before submitting a PR:

- [ ] Code follows PEP 8 and project standards
- [ ] Type hints added to all functions
- [ ] Docstrings written for public APIs
- [ ] Tests written and passing
- [ ] Code coverage maintained or improved
- [ ] No breaking changes without discussion
- [ ] Documentation updated
- [ ] Backwards compatibility preserved
- [ ] Error handling comprehensive
- [ ] Edge cases considered

## Useful Commands

```bash
# Format code
black codetrimmer tests

# Run linting
pylint codetrimmer

# Run type checking
mypy codetrimmer

# Generate test coverage report
pytest --cov=codetrimmer --cov-report=html

# Run dry-run to preview changes
codetrimmer trim . --dry-run

# Generate diff
codetrimmer trim . --dry-run --diff
```

## Getting Help

- **Architecture questions:** See `docs/ARCHITECTURE.md`
- **CLI usage:** See `docs/CLI_REFERENCE.md`
- **Configuration:** See `docs/CONFIGURATION.md`
- **Errors:** See `docs/ERROR_CODES.md`
- **Troubleshooting:** See `docs/TROUBLESHOOTING.md`
- **Automation:** See `AGENTS.md`
- **Code examples:** See `docs/samples/`

## Philosophy

Code Trimmer aims to be:

- **Simple:** Easy to understand and use
- **Safe:** Provides backups and undo
- **Reliable:** Consistent, predictable behavior
- **Flexible:** Highly configurable
- **Portable:** Works across platforms
- **Maintainable:** Clean, well-documented code

When in doubt, prioritize simplicity and safety over cleverness.
