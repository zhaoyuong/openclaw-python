#!/bin/bash
# Run integration tests for OpenClaw

set -e

echo "========================================"
echo "OpenClaw - Integration Tests"
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

# Check if required services are running
echo "Checking required services..."

# Check for .env file with API keys
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Some integration tests may fail."
    echo "Copy .env.example to .env and fill in your API keys."
fi

# Run integration tests
echo ""
echo "Running integration tests..."
echo ""

pytest tests/integration/ \
    -v \
    --tb=short \
    --color=yes \
    --timeout=60 \
    "$@"

echo ""
echo "========================================"
echo "Integration tests complete!"
echo "========================================"
