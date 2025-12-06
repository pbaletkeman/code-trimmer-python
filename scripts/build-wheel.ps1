# PowerShell script to build Code Trimmer wheel
# Usage: .\build-wheel.ps1

param(
    [switch]$Clean,
    [switch]$SkipVenv,
    [switch]$Verbose,
    [string]$OutputDir = "dist",
    [string]$PythonVersion = "3.11"
)

# Set error handling
$ErrorActionPreference = "Stop"
$WarningPreference = "Continue"

# Colors for output
$SUCCESS = "Green"
$ERROR_COLOR = "Red"
$WARNING = "Yellow"
$INFO = "Cyan"

function Write-Success { Write-Host $args -ForegroundColor $SUCCESS }
function Write-Error-Color { Write-Host $args -ForegroundColor $ERROR_COLOR }
function Write-Warning-Color { Write-Host $args -ForegroundColor $WARNING }
function Write-Info { Write-Host $args -ForegroundColor $INFO }

function Check-Python {
    Write-Info "Checking Python version..."

    $version = & python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Color "Python not found. Please install Python 3.11+"
        exit 1
    }

    # Parse version
    if ($version -match "Python (\d+)\.(\d+)") {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]

        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 11)) {
            Write-Error-Color "Python 3.11+ required. Found: $version"
            exit 1
        }

        Write-Success "✓ Python version: $version"
    }
}

function Setup-Venv {
    if ($SkipVenv) {
        Write-Info "Skipping venv creation (using current environment)"
        return
    }

    Write-Info "Setting up virtual environment..."

    if (Test-Path ".venv") {
        if ($Clean) {
            Write-Warning-Color "Removing old venv..."
            Remove-Item -Recurse -Force ".venv" | Out-Null
        } else {
            Write-Info "Using existing venv"
            return
        }
    }

    & python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Color "Failed to create venv"
        exit 1
    }

    & .venv\Scripts\Activate.ps1
    Write-Success "✓ Venv created and activated"
}

function Install-BuildDeps {
    Write-Info "Installing build dependencies..."

    & python -m pip install --upgrade build wheel setuptools
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Color "Failed to install build dependencies"
        exit 1
    }

    Write-Success "✓ Build dependencies installed"
}

function Clean-BuildArtifacts {
    Write-Warning-Color "Cleaning build artifacts..."

    if (Test-Path "build") {
        Remove-Item -Recurse -Force "build" | Out-Null
    }

    if (Test-Path "dist") {
        Remove-Item -Recurse -Force "dist" | Out-Null
    }

    if (Test-Path "*.egg-info") {
        Remove-Item -Recurse -Force "*.egg-info" | Out-Null
    }

    Write-Success "✓ Cleaned"
}

function Build-Wheel {
    $projectRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Leaf
    Write-Info "Building wheel for $projectRoot..."

    # Go to project root
    Push-Location (Split-Path $PSScriptRoot -Parent)

    if ($Verbose) {
        & python -m build --wheel
    } else {
        & python -m build --wheel 2>&1 | Out-Null
    }

    if ($LASTEXITCODE -ne 0) {
        Write-Error-Color "Build failed"
        Pop-Location
        exit 1
    }

    Pop-Location
    Write-Success "✓ Wheel built successfully"
}

function Show-Output {
    $wheelPath = Get-ChildItem -Path (Join-Path (Split-Path $PSScriptRoot -Parent) "dist") -Filter "*.whl" | Select-Object -First 1

    if ($wheelPath) {
        Write-Success "✓ Build completed!"
        Write-Info "`nOutput:"
        Write-Info "  Location: $($ wheelPath.FullName)"
        Write-Info "  Size: $('{0:N2}' -f ($wheelPath.Length / 1MB)) MB"
        Write-Info "`nInstall with:"
        Write-Info "  pip install `"$($wheelPath.FullName)`""
    } else {
        Write-Warning-Color "Could not find wheel in dist/"
    }
}

# Main execution
try {
    Write-Info "Code Trimmer Wheel Build Script"
    Write-Info "================================="
    Write-Info ""

    Check-Python
    Setup-Venv
    Install-BuildDeps

    if ($Clean) {
        Clean-BuildArtifacts
    }

    Build-Wheel
    Show-Output

    Write-Success "`nBuild successful!"
}
catch {
    Write-Error-Color "Build failed: $_"
    exit 1
}
