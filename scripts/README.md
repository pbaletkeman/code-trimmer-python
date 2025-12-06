# Python Wheel Build Scripts

This directory contains scripts to build Code Trimmer into a Python wheel file and documentation for the build process.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Requirements](#requirements)
- [Build Scripts](#build-scripts)
- [Output](#output)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)

## Overview

A Python wheel is a binary package format that can be installed quickly without requiring compilation. These scripts automate the process of building Code Trimmer into a distributable wheel file.

**Benefits of wheels:**

- Fast installation (no compilation needed)
- Reproducible builds
- Can be published to PyPI
- Works across different Python installations
- Easier CI/CD integration

## Quick Start

### On Windows (PowerShell)

```powershell
cd scripts
.\build-wheel.ps1
```

### On Windows (Batch)

```batch
cd scripts
build-wheel.bat
```

### On macOS/Linux (Bash)

```bash
cd scripts
./build-wheel.sh
```

### Output

The built wheel will be in `dist/`:

```text
codetrimmer-1.0.0-py3-none-any.whl
```

## Requirements

### System Requirements

- Python 3.11 or higher
- pip (Python package installer)
- Virtual environment (recommended but optional)

### Python Packages

The following packages are installed automatically by the scripts:

- `build` - Modern Python build frontend
- `wheel` - Wheel package format
- `setuptools` - Package building tools

These are standard build tools and are safe to install globally or in a virtual environment.

## Build Scripts

### Windows PowerShell: `build-wheel.ps1`

Full-featured build script for PowerShell (Windows).

**Features:**

- Validates Python version (3.11+)
- Creates isolated virtual environment
- Installs build dependencies
- Builds the wheel
- Displays output location
- Error handling and reporting

**Usage:**

```powershell
.\build-wheel.ps1
```

**Options:**

```powershell
# Clean previous build artifacts
.\build-wheel.ps1 -Clean

# Skip venv creation (use existing)
.\build-wheel.ps1 -SkipVenv

# Specify output directory
.\build-wheel.ps1 -OutputDir "C:\temp\builds"

# Verbose output
.\build-wheel.ps1 -Verbose
```

### Windows Batch: `build-wheel.bat`

Simple batch script for command prompt (Windows).

**Features:**

- Python version check
- Dependency installation
- Wheel building
- Basic error handling

**Usage:**

```batch
build-wheel.bat
```

### Unix/Linux/macOS: `build-wheel.sh`

Bash script for Unix-like systems.

**Features:**

- Python version validation
- Virtual environment support
- Dependency management
- Clean build process
- Detailed logging

**Usage:**

```bash
# Make executable (first time only)
chmod +x build-wheel.sh

# Run the script
./build-wheel.sh
```

**Options:**

```bash
# Display help
./build-wheel.sh --help

# Clean before building
./build-wheel.sh --clean

# Use specific Python version
./build-wheel.sh --python python3.11

# Verbose mode
./build-wheel.sh --verbose
```

## Output

### Wheel File Location

Wheels are built to `../dist/`:

```text
project-root/
├── dist/
│   ├── codetrimmer-1.0.0-py3-none-any.whl
│   └── codetrimmer-1.0.0.tar.gz  (source distribution)
├── scripts/
│   ├── build-wheel.sh
│   ├── build-wheel.bat
│   ├── build-wheel.ps1
│   └── README.md (this file)
└── ...
```

### Wheel Contents

You can inspect the wheel contents:

```bash
# List wheel contents
python -m zipfile -l ../dist/codetrimmer-1.0.0-py3-none-any.whl

# Extract to inspect
python -m zipfile -e ../dist/codetrimmer-1.0.0-py3-none-any.whl /tmp/inspect
```

### Installing the Wheel

After building, install locally for testing:

```bash
pip install ../dist/codetrimmer-1.0.0-py3-none-any.whl
```

Verify installation:

```bash
codetrimmer --version
codetrimmer --help
```

## Troubleshooting

### Issue: "Python not found" or "Python version too old"

**Solution:**

- Ensure Python 3.11+ is installed
- Check PATH includes Python executable
- Use full path to Python: `C:\Python311\python.exe`

**Verify:**

```bash
python --version  # Should show 3.11+
```

### Issue: "Permission denied" on bash script

**Solution:**

```bash
chmod +x build-wheel.sh
./build-wheel.sh
```

### Issue: "Module not found" during build

**Solution:**

- Ensure dependencies are installed: `pip install build wheel`
- Try cleaning and rebuilding:
  - PowerShell: `.\build-wheel.ps1 -Clean`
  - Bash: `./build-wheel.sh --clean`

### Issue: "Virtual environment error"

**Solution:**

- Delete old `.venv` directory
- Run with `-SkipVenv` flag and use existing venv
- Or create new venv manually:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### Issue: Build succeeds but wheel is not in dist/

**Possible causes:**

- Check working directory
- Look for build output in current directory
- Run with verbose flag for details

## Advanced Usage

### Building Without Virtual Environment

Using existing Python environment:

**PowerShell:**

```powershell
.\build-wheel.ps1 -SkipVenv
```

**Bash:**

```bash
./build-wheel.sh --skip-venv
```

### Custom Output Directory

**PowerShell:**

```powershell
.\build-wheel.ps1 -OutputDir "D:\builds"
```

**Bash:**

```bash
./build-wheel.sh --output /custom/path
```

### Clean Build (Remove Old Artifacts)

**PowerShell:**

```powershell
.\build-wheel.ps1 -Clean
```

**Bash:**

```bash
./build-wheel.sh --clean
```

### Continuous Build (Watch for Changes)

Create a simple watch script:

```bash
while true; do
  clear
  ./build-wheel.sh
  echo "Waiting for changes... (Ctrl+C to stop)"
  sleep 5
done
```

### Building for Distribution

After building, prepare for PyPI:

```bash
# Build both wheel and source distribution
python -m build

# Upload to PyPI test (requires account and token)
python -m twine upload --repository testpypi dist/codetrimmer-*.whl

# Upload to production PyPI
python -m twine upload dist/codetrimmer-*.whl
```

## Build Process Details

### What the Scripts Do

1. **Verify Python Version:**

   - Checks that Python 3.11+ is available
   - Exits if version is too old

2. **Prepare Environment:**

   - Creates isolated virtual environment (recommended)
   - Installs build tools (build, wheel, setuptools)

3. **Install Project:**

   - Installs project in development mode
   - Validates configuration

4. **Build Wheel:**

   - Compiles Python files
   - Generates metadata
   - Creates `.whl` file in `dist/`

5. **Verify Output:**
   - Confirms wheel was created
   - Displays location and details

### Build Configuration

The build process uses `pyproject.toml` which defines:

- Project metadata (name, version, description)
- Dependencies (click, pyyaml, pydantic, colorama)
- Build system (setuptools)
- Entry points (CLI commands)
- Build options

No configuration is needed for these scripts—they use `pyproject.toml` automatically.

## Testing the Build

After building, thoroughly test the wheel:

```bash
# Create test environment
python -m venv test-env
source test-env/bin/activate  # or test-env\Scripts\activate

# Install wheel
pip install ../dist/codetrimmer-*.whl

# Test CLI
codetrimmer --version
codetrimmer --help
codetrimmer trim --help

# Run basic functionality
codetrimmer trim . --dry-run
```

## Performance

### Build Time

Typical build times:

- Clean build: 10-30 seconds
- Incremental build: 5-15 seconds
- Depends on system performance and network

### Wheel Size

```text
codetrimmer-1.0.0-py3-none-any.whl:  ~500 KB (with dependencies)
                                     ~100 KB (without dependencies)
```

## Best Practices

1. **Always test the wheel after building:**

   - Use in fresh environment
   - Test all CLI commands
   - Verify functionality

2. **Keep virtual environments clean:**

   - Remove old venvs before rebuilding
   - Use `--clean` flag when needed

3. **Document your build:**

   - Note build time and machine
   - Record Python version used
   - Keep build logs if needed

4. **Automate in CI/CD:**
   - Use scripts in GitHub Actions or similar
   - Test on multiple Python versions
   - Automate PyPI upload process

## Next Steps

- [Distribution Guide](../docs/DISTRIBUTION.md) - Publishing to PyPI
- [Project Architecture](../docs/ARCHITECTURE.md) - Technical details
- [Contributing Guide](../CONTRIBUTING.md) - How to contribute

## Support

For issues with the build scripts:

1. Check [Troubleshooting](#troubleshooting) section
2. Verify Python version and dependencies
3. Try clean build: `--clean` flag
4. Review build output for specific errors
5. File an issue on GitHub with build output

## License

These scripts are part of the Code Trimmer project, licensed under MIT License. See [LICENSE](../LICENSE) for details.
