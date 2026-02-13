#!/bin/bash
# Run unit tests for OpenClaw

set -e

echo "========================================"
echo "OpenClaw - Unit Tests"
echo "========================================"
echo ""

# Change to project root
cd "$(dirname "$0")/.."

# Check if pytest is available
if ! command -v pytest &> /dev/null; then
    echo "Error: pytest not found. Please install test dependencies:"
    echo "  pip install -e '.[test]'"
    exit 1
fi

# Run unit tests
echo "Running unit tests..."
echo ""

pytest tests/unit/ \
    -v \
    --tb=short \
    --color=yes \
    "$@"

echo ""
echo "========================================"
echo "Unit tests complete!"
echo "========================================"
