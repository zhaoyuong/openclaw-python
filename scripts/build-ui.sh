#!/bin/bash
# Build UI assets for OpenClaw Python

set -e

cd "$(dirname "$0")/.."

echo "🔨 Building OpenClaw Control UI..."

# Check if pnpm is installed
if ! command -v pnpm &> /dev/null; then
    echo "❌ pnpm not found. Installing pnpm..."
    npm install -g pnpm
fi

# Build UI
cd ui
echo "📦 Installing dependencies..."
pnpm install

echo "🏗️  Building UI..."
pnpm build

echo "✅ UI build complete! Files in ui/dist/"
