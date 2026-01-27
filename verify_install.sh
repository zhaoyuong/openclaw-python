#!/bin/bash

echo "========================================"
echo "ClawdBot Python - Installation Verification"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# Check if Poetry is installed
echo ""
echo "Checking Poetry..."
if command -v poetry &> /dev/null; then
    POETRY_VERSION=$(poetry --version 2>&1 | awk '{print $3}')
    echo "✓ Poetry version: $POETRY_VERSION"
else
    echo "⚠ Poetry not installed (optional, can use pip)"
fi

# Check directory structure
echo ""
echo "Checking project structure..."
if [ -f "pyproject.toml" ]; then
    echo "✓ pyproject.toml found"
else
    echo "✗ pyproject.toml missing"
fi

if [ -d "clawdbot" ]; then
    echo "✓ clawdbot/ directory found"
else
    echo "✗ clawdbot/ directory missing"
fi

if [ -d "tests" ]; then
    echo "✓ tests/ directory found"
else
    echo "✗ tests/ directory missing"
fi

if [ -d "skills" ]; then
    echo "✓ skills/ directory found"
else
    echo "✗ skills/ directory missing"
fi

if [ -d "extensions" ]; then
    echo "✓ extensions/ directory found"
else
    echo "✗ extensions/ directory missing"
fi

# Count files
echo ""
echo "Counting files..."
PY_FILES=$(find clawdbot -name "*.py" | wc -l | tr -d ' ')
echo "✓ Python files in clawdbot/: $PY_FILES"

TEST_FILES=$(find tests -name "*.py" | wc -l | tr -d ' ')
echo "✓ Test files: $TEST_FILES"

SKILL_FILES=$(find skills -name "SKILL.md" | wc -l | tr -d ' ')
echo "✓ Skill files: $SKILL_FILES"

PLUGIN_FILES=$(find extensions -name "plugin.json" | wc -l | tr -d ' ')
echo "✓ Plugin manifests: $PLUGIN_FILES"

# Check key files
echo ""
echo "Checking key files..."
key_files=(
    "README.md"
    "QUICKSTART.md"
    "CHANGELOG.md"
    "CONTRIBUTING.md"
    "LICENSE"
    "Makefile"
    ".gitignore"
    "clawdbot/__init__.py"
    "clawdbot/gateway/server.py"
    "clawdbot/agents/runtime.py"
    "clawdbot/cli/main.py"
    "clawdbot/web/app.py"
)

for file in "${key_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
    else
        echo "✗ $file missing"
    fi
done

echo ""
echo "========================================"
echo "Installation verification complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Install dependencies: poetry install (or pip install -e .)"
echo "2. Set API key: export ANTHROPIC_API_KEY='your-key'"
echo "3. Run onboarding: clawdbot onboard"
echo "4. Start gateway: clawdbot gateway start"
echo "5. Open Web UI: http://localhost:8080 (after running: make run-web)"
echo ""
