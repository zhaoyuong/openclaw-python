#!/bin/bash
# OpenClaw Command Test Script

cd "$(dirname "$0")"

echo "🧪 OpenClaw Command Tests"
echo "===================="
echo ""

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m'

# Check if Gateway is running
if ! lsof -i :18789 | grep -q LISTEN; then
    echo -e "${YELLOW}⚠️  Gateway is not running${NC}"
    echo "Please start the Gateway first:"
    echo "  /Users/openbot/.local/bin/uv run openclaw gateway run"
    echo ""
fi

echo -e "${BLUE}1️⃣  Testing agent run command${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "$ openclaw agent run -m 'Hello, please introduce yourself'"
echo ""
/Users/openbot/.local/bin/uv run openclaw agent run -m "Hello, please introduce yourself"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo -e "${BLUE}2️⃣  View skills list${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
/Users/openbot/.local/bin/uv run openclaw skills list | head -20
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo -e "${BLUE}3️⃣  View tools list${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
/Users/openbot/.local/bin/uv run openclaw tools list | head -20
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo -e "${BLUE}4️⃣  View configuration${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
/Users/openbot/.local/bin/uv run openclaw config path
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo -e "${BLUE}5️⃣  View channel status${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
/Users/openbot/.local/bin/uv run openclaw channels status
echo ""

echo -e "${GREEN}✅ Tests complete${NC}"
echo ""
echo "Common commands:"
echo "  • Chat: openclaw agent run -m 'your message'"
echo "  • Skills: openclaw skills list"
echo "  • Tools: openclaw tools list"
echo "  • Status: openclaw gateway status"
echo "  • Help: openclaw --help"
