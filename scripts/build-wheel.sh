#!/bin/bash
# Bash script to build Code Trimmer wheel
# Usage: ./build-wheel.sh [OPTIONS]

set -e

# Colors for output
SUCCESS="\033[0;32m"
ERROR="\033[0;31m"
WARNING="\033[1;33m"
INFO="\033[0;36m"
NC="\033[0m" # No Color

# Script variables
CLEAN=false
SKIP_VENV=false
VERBOSE=false
PYTHON_CMD="python3"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Helper functions
info() {
    echo -e "${INFO}$@${NC}"
}

success() {
    echo -e "${SUCCESS}✓ $@${NC}"
}

error() {
    echo -e "${ERROR}✗ $@${NC}"
}

warning() {
    echo -e "${WARNING}⚠ $@${NC}"
}

show_help() {
    cat << EOF
Code Trimmer Wheel Build Script

Usage: ./build-wheel.sh [OPTIONS]

Options:
    --help          Show this help message
    --clean         Clean build artifacts before building
    --skip-venv     Skip virtual environment creation
    --verbose       Verbose output
    --python CMD    Python command to use (default: python3)

Examples:
    ./build-wheel.sh
    ./build-wheel.sh --clean
    ./build-wheel.sh --python python3.11 --verbose
EOF
}

check_python() {
    info "Checking Python version..."

    if ! command -v "$PYTHON_CMD" &> /dev/null; then
        error "Python ($PYTHON_CMD) not found"
        exit 1
    fi

    VERSION=$("$PYTHON_CMD" --version 2>&1 | awk '{print $2}')
    success "Python version: $VERSION"

    # Check if 3.11+
    MAJOR=$(echo "$VERSION" | cut -d. -f1)
    MINOR=$(echo "$VERSION" | cut -d. -f2)

    if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 11 ]); then
        error "Python 3.11+ required, found $VERSION"
        exit 1
    fi
}

setup_venv() {
    if [ "$SKIP_VENV" = true ]; then
        info "Skipping venv creation"
        return 0
    fi

    info "Setting up virtual environment..."

    if [ -d ".venv" ]; then
        if [ "$CLEAN" = true ]; then
            warning "Removing old venv..."
            rm -rf .venv
        else
            info "Using existing venv"
            return 0
        fi
    fi

    "$PYTHON_CMD" -m venv .venv
    source .venv/bin/activate
    success "Virtual environment created and activated"
}

install_deps() {
    info "Installing build dependencies..."

    if [ "$VERBOSE" = true ]; then
        python -m pip install --upgrade build wheel setuptools
    else
        python -m pip install --upgrade build wheel setuptools > /dev/null 2>&1
    fi

    success "Build dependencies installed"
}

clean_artifacts() {
    warning "Cleaning build artifacts..."

    rm -rf "$PROJECT_ROOT/build"
    rm -rf "$PROJECT_ROOT/dist"
    rm -rf "$PROJECT_ROOT"/*.egg-info

    success "Cleaned"
}

build_wheel() {
    info "Building wheel..."

    cd "$PROJECT_ROOT"

    if [ "$VERBOSE" = true ]; then
        python -m build --wheel
    else
        python -m build --wheel > /dev/null 2>&1
    fi

    success "Wheel built successfully"
}

show_output() {
    local wheel=$(find "$PROJECT_ROOT/dist" -name "*.whl" -type f | head -1)

    if [ -n "$wheel" ]; then
        success "Build completed!"
        info "\nOutput:"
        info "  Location: $wheel"
        info "  Size: $(du -h "$wheel" | cut -f1)"
        info "\nInstall with:"
        info "  pip install \"$wheel\""
    else
        warning "Could not find wheel in dist/"
    fi
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --help)
            show_help
            exit 0
            ;;
        --clean)
            CLEAN=true
            shift
            ;;
        --skip-venv)
            SKIP_VENV=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --python)
            PYTHON_CMD="$2"
            shift 2
            ;;
        *)
            error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Main execution
main() {
    info "Code Trimmer Wheel Build Script"
    info "================================"
    info ""

    check_python

    cd "$SCRIPT_DIR/.."

    setup_venv
    install_deps

    if [ "$CLEAN" = true ]; then
        clean_artifacts
    fi

    build_wheel
    show_output

    success "\nBuild successful!"
}

# Run main
main "$@"
