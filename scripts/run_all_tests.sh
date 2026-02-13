#!/bin/bash
# Run all tests (unit + integration) for OpenClaw

set -e

echo "========================================"
echo "OpenClaw - Full Test Suite"
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

# Run all tests
echo "Running all tests (unit + integration)..."
echo ""

pytest tests/ \
    -v \
    --tb=short \
    --color=yes \
    --timeout=60 \
    "$@"

EXIT_CODE=$?

echo ""
echo "========================================"
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Some tests failed (exit code: $EXIT_CODE)"
fi
echo "========================================"

exit $EXIT_CODE
