#!/bin/bash
# OpenClaw Python Test Runner Script

cd "$(dirname "$0")"

echo "🧪 OpenClaw Python Test Suite"
echo "=============================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

# Use uv run python -m pytest
PYTEST="/Users/openbot/.local/bin/uv run python -m pytest"

# Options
VERBOSE="-v"
MARKERS=""
COVERAGE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --unit)
            echo -e "${BLUE}Running unit tests...${NC}"
            MARKERS="-m unit"
            shift
            ;;
        --integration)
            echo -e "${BLUE}Running integration tests...${NC}"
            MARKERS="-m integration"
            shift
            ;;
        --cov)
            echo -e "${BLUE}Generating coverage report...${NC}"
            COVERAGE="--cov=openclaw --cov-report=term-missing"
            shift
            ;;
        --fast)
            echo -e "${BLUE}Skipping slow tests...${NC}"
            MARKERS="-m 'not slow'"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            shift
            ;;
    esac
done

# Run tests
echo -e "${BLUE}Executing tests...${NC}"
$PYTEST $VERBOSE $MARKERS $COVERAGE tests/

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ All tests passed!${NC}"
else
    echo ""
    echo -e "${RED}❌ Tests failed (exit code: $EXIT_CODE)${NC}"
fi

exit $EXIT_CODE
