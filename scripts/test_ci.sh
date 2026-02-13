#!/bin/bash
# CI/CD test script for OpenClaw
# Runs full test suite with coverage and quality checks

set -e

echo "========================================"
echo "OpenClaw - CI/CD Test Pipeline"
echo "========================================"
echo ""

# Change to project root
cd "$(dirname "$0")/.."

# Track overall status
OVERALL_STATUS=0

# 1. Run tests with coverage
echo "Step 1: Running tests with coverage..."
echo "========================================"
echo ""

if pytest tests/ \
    --cov=openclaw \
    --cov-report=term-missing \
    --cov-report=xml \
    --cov-fail-under=70 \
    -v \
    --tb=short; then
    echo "✅ Tests passed with adequate coverage"
else
    echo "❌ Tests failed or coverage insufficient"
    OVERALL_STATUS=1
fi

echo ""

# 2. Run linting if available
echo "Step 2: Running code quality checks..."
echo "========================================"
echo ""

if command -v ruff &> /dev/null; then
    echo "Running ruff linter..."
    if ruff check openclaw/; then
        echo "✅ Linting passed"
    else
        echo "⚠️  Linting issues found"
        OVERALL_STATUS=1
    fi
else
    echo "⚠️  ruff not installed, skipping linting"
fi

echo ""

# 3. Run type checking if available
echo "Step 3: Running type checks..."
echo "========================================"
echo ""

if command -v mypy &> /dev/null; then
    echo "Running mypy type checker..."
    if mypy openclaw/ --ignore-missing-imports --no-strict-optional; then
        echo "✅ Type checking passed"
    else
        echo "⚠️  Type checking issues found"
        # Don't fail on type errors for now
    fi
else
    echo "⚠️  mypy not installed, skipping type checking"
fi

echo ""

# 4. Check formatting if available
echo "Step 4: Checking code formatting..."
echo "========================================"
echo ""

if command -v black &> /dev/null; then
    echo "Running black formatter check..."
    if black --check openclaw/ tests/; then
        echo "✅ Code formatting is correct"
    else
        echo "⚠️  Code formatting issues found"
        echo "Run: black openclaw/ tests/"
        # Don't fail on formatting for now
    fi
else
    echo "⚠️  black not installed, skipping formatting check"
fi

echo ""

# 5. Check import sorting if available
echo "Step 5: Checking import sorting..."
echo "========================================"
echo ""

if command -v isort &> /dev/null; then
    echo "Running isort check..."
    if isort --check-only openclaw/ tests/; then
        echo "✅ Import sorting is correct"
    else
        echo "⚠️  Import sorting issues found"
        echo "Run: isort openclaw/ tests/"
        # Don't fail on import sorting for now
    fi
else
    echo "⚠️  isort not installed, skipping import sorting check"
fi

echo ""

# Final summary
echo "========================================"
echo "CI/CD Pipeline Summary"
echo "========================================"
echo ""

if [ $OVERALL_STATUS -eq 0 ]; then
    echo "✅ All critical checks passed!"
    echo ""
    echo "Pipeline Status: SUCCESS"
else
    echo "❌ Some critical checks failed"
    echo ""
    echo "Pipeline Status: FAILURE"
fi

echo "========================================"

exit $OVERALL_STATUS
