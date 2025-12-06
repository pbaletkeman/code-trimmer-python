@echo off
REM Batch script to build Code Trimmer wheel
REM Usage: build-wheel.bat

setlocal enabledelayedexpansion

echo.
echo Code Trimmer Wheel Build Script
echo ================================
echo.

REM Check Python
echo Checking Python version...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found. Please install Python 3.11+
    exit /b 1
)

python --version
echo.

REM Setup venv if needed
if not exist ".venv" (
    echo Setting up virtual environment...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment
        exit /b 1
    )
    echo.
)

REM Activate venv
call .venv\Scripts\activate.bat

REM Install build deps
echo Installing build dependencies...
python -m pip install --upgrade build wheel setuptools >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Failed to install build dependencies
    exit /b 1
)
echo.

REM Build wheel
echo Building wheel...
cd /d "%~dp0\.."
python -m build --wheel
if %errorlevel% neq 0 (
    echo Error: Build failed
    exit /b 1
)

echo.
echo Build completed successfully!
echo.
echo Wheel output in: dist\
dir dist\*.whl
echo.
echo Install with:
echo   pip install dist\codetrimmer-*.whl
echo.

exit /b 0
