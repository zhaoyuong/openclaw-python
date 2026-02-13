#!/bin/bash
# Generate test coverage report for OpenClaw

set -e

echo "========================================"
echo "OpenClaw - Coverage Report"
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

# Check if coverage is available
if ! python3 -m pytest --cov --help &> /dev/null; then
    echo "Error: pytest-cov not found. Installing..."
    pip install pytest-cov
fi

# Run tests with coverage
echo "Running tests with coverage analysis..."
echo ""

pytest tests/ \
    --cov=openclaw \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-report=xml \
    --cov-fail-under=70 \
    -v \
    "$@"

EXIT_CODE=$?

echo ""
echo "========================================"
echo "Coverage Report Generated"
echo "========================================"
echo ""
echo "HTML Report: htmlcov/index.html"
echo "XML Report: coverage.xml"
echo ""

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Coverage target met (70%+)"
    
    # Open HTML report if on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo ""
        echo "Opening coverage report in browser..."
        open htmlcov/index.html
    fi
else
    echo "❌ Coverage below threshold or tests failed"
fi

echo "========================================"

exit $EXIT_CODE
