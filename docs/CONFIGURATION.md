# Configuration Guide

Code Trimmer supports configuration via YAML files, JSON files, environment variables, and CLI options.

## Configuration Priority

Configuration sources are applied in this order (highest priority first):

1. CLI options
2. Environment variables
3. Configuration file
4. Default values

## Configuration File

### YAML Format (Recommended)

Create `.codetrimmer.yaml` in your project root:

```yaml
codetrimmer:
  # File filtering
  include: "*.{py,js,java,md}"
  exclude: "node_modules/**,*.min.js,dist/**"
  include-hidden: false
  follow-symlinks: false

  # Whitespace rules
  max-consecutive-blank-lines: 2
  ensure-final-newline: true
  trim-trailing-whitespace: true

  # Performance limits
  max-file-size: 5242880  # 5MB in bytes
  max-files: 50
  no-limits: false

  # Operation modes
  dry-run: false
  create-backups: true
  fail-fast: false

  # Output options
  verbose: false
  quiet: false
  no-color: false

  # Custom rules
  rules:
    - name: "remove-trailing-spaces"
      pattern: '\s+$'
      replacement: ""
      description: "Remove trailing whitespace"
```

### JSON Format

Create `.codetrimmer.json`:

```json
{
  "codetrimmer": {
    "include": "*.py",
    "exclude": "*.pyc",
    "max-consecutive-blank-lines": 2,
    "ensure-final-newline": true,
    "create-backups": true
  }
}
```

## Configuration Options

### File Filtering

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `include` | string | `*` | File glob pattern to include |
| `exclude` | string | (empty) | File glob pattern to exclude |
| `include-hidden` | bool | false | Include hidden files |
| `follow-symlinks` | bool | false | Follow symbolic links |

### Whitespace Rules

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `max-consecutive-blank-lines` | int | 2 | Maximum consecutive blank lines |
| `ensure-final-newline` | bool | true | Ensure file ends with newline |
| `trim-trailing-whitespace` | bool | true | Trim trailing whitespace |

### Performance Limits

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `max-file-size` | int | 5242880 | Max file size in bytes (5MB) |
| `max-files` | int | 50 | Max files to process |
| `no-limits` | bool | false | Disable all limits |

### Operation Modes

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `dry-run` | bool | false | Preview without modifying |
| `create-backups` | bool | true | Create `.bak` backup files |
| `fail-fast` | bool | false | Stop on first error |

### Output Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `verbose` | bool | false | Detailed output |
| `quiet` | bool | false | Minimal output |
| `no-color` | bool | false | Disable colored output |

## Environment Variables

All options can be set via environment variables prefixed with `CODETRIMMER_`:

```bash
export CODETRIMMER_MAX_FILES=100
export CODETRIMMER_VERBOSE=true
export CODETRIMMER_DRY_RUN=true
```

## Custom Rules

Define regex-based rules in your configuration:

```yaml
codetrimmer:
  rules:
    - name: "remove-debug-prints"
      pattern: 'print\(.*debug.*\)'
      replacement: ""
      description: "Remove debug print statements"

    - name: "normalize-quotes"
      pattern: "\"([^\"]*)\""
      replacement: "'\\1'"
      description: "Convert double quotes to single"
```

### Rule Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique rule identifier |
| `pattern` | Yes | Regex pattern to match |
| `replacement` | No | Replacement string (empty = remove) |
| `description` | No | Description of what the rule does |
