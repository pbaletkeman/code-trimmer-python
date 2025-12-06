# Code Trimmer Python

A file formatting and whitespace normalization utility for source code.

**This is the Python 3.11+ implementation of Code Trimmer.**

For detailed documentation, see [`./docs/`](./docs/).

## Features

- **Multi-format configuration** - YAML/JSON configuration files
- **Regex-based custom rules** - Extensible formatting rules
- **Binary file detection** - Intelligent skipping of binary files
- **Comprehensive error codes** - 45+ error types with actionable messages
- **Advanced reporting** - JSON/CSV/SQLite output formats
- **Git integration** - Pre-commit hook generation
- **Undo/restore capability** - Backup management
- **Rich CLI experience** - Color output, progress, dry-run modes

## Quick Start

### Installation

```bash
pip install codetrimmer
```

### Basic Usage

```bash
# Trim files in current directory
codetrimmer trim .

# Dry-run mode (preview changes)
codetrimmer trim . --dry-run

# Process specific file types
codetrimmer trim . --include "*.py,*.js"

# Verbose output
codetrimmer trim . --verbose
```

### Generate Pre-commit Hook

```bash
codetrimmer generate-hook .
```

### Undo Changes

```bash
codetrimmer undo .
```

## Configuration

Create a `.codetrimmer.yaml` file in your project root:

```yaml
codetrimmer:
  include: "*.{py,js,java}"
  exclude: "*.min.js,node_modules/**"
  max-consecutive-blank-lines: 2
  ensure-final-newline: true
  trim-trailing-whitespace: true
  create-backups: true
```

## Documentation

- [Quick Start Guide](./docs/QUICKSTART.md)
- [Configuration Reference](./docs/CONFIGURATION.md)
- [CLI Reference](./docs/CLI_REFERENCE.md)
- [Error Codes](./docs/ERROR_CODES.md)
- [Architecture](./docs/ARCHITECTURE.md)
- [Troubleshooting](./docs/TROUBLESHOOTING.md)

## Requirements

- Python 3.11+
- click >= 8.0.0
- pyyaml >= 6.0
- pydantic >= 2.0.0
- colorama >= 0.4.6

## License

MIT License

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.
