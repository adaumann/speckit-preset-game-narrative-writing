#!/bin/bash

# ============================================================================
# Witchhunter Playwright Tests - Setup and Run Script
# ============================================================================

set -e

echo ""
echo "============================================================================"
echo "Witchhunter Playwright Test Suite - Setup & Execution"
echo "============================================================================"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ---- Check Node.js Installation ----
echo "[1/5] Checking Node.js installation..."

if ! command -v node &> /dev/null; then
    echo ""
    echo "❌ Node.js is NOT installed"
    echo ""
    echo "Please install Node.js from: https://nodejs.org/"
    echo "- Download v18 LTS or later"
    echo "- Run the installer"
    echo "- Restart your terminal"
    echo ""
    exit 1
fi

NODE_VERSION=$(node --version)
echo "✅ Node.js found: $NODE_VERSION"

# ---- Check npm Installation ----
echo "[2/5] Checking npm installation..."

if ! command -v npm &> /dev/null; then
    echo "❌ npm is NOT installed"
    exit 1
fi

NPM_VERSION=$(npm --version)
echo "✅ npm found: $NPM_VERSION"

# ---- Install Dependencies ----
echo "[3/5] Installing dependencies..."

if [ ! -d "node_modules" ]; then
    echo "Installing packages from package.json..."
    npm install
else
    echo "✅ Dependencies already installed"
fi

# ---- Verify Test Files ----
echo "[4/5] Verifying test files..."

MISSING=0

if [ ! -f "witchhunter.html" ]; then
    echo "⚠️  WARNING: witchhunter.html not found"
    echo ""
    echo "You need to compile the game with Tweego:"
    echo "  tweego witchhunter-*.twee -o witchhunter.html"
    echo ""
    MISSING=1
fi

for file in tests/helpers.ts tests/game-flow.spec.ts tests/dialogue.spec.ts tests/faction.spec.ts tests/spells-combat.spec.ts tests/inventory-quests.spec.ts; do
    if [ ! -f "$file" ]; then
        echo "❌ $file missing"
        MISSING=1
    fi
done

if [ $MISSING -eq 1 ] && [ -f "witchhunter.html" ]; then
    echo ""
    echo "⚠️  Some test files are missing. Please check and try again."
    exit 1
fi

echo "✅ All test files found"

# ---- Compile TypeScript ----
echo "[5/5] Compiling TypeScript..."

npx tsc --noEmit || {
    echo "⚠️  TypeScript compilation found errors (non-fatal)"
    echo "Attempting to run tests anyway..."
}

echo ""
echo "============================================================================"
echo "Ready to run tests!"
echo "============================================================================"
echo ""
echo "Command: npm test"
echo ""
echo "Options:"
echo "  npm test              - Run all tests (headless)"
echo "  npm run test:headed   - Run with browser visible"
echo "  npm run test:debug    - Debug mode"
echo "  npm run test:ui       - Interactive UI mode"
echo ""
echo "Running all tests now..."
echo "============================================================================"
echo ""

npm test

echo ""
echo "Tests complete!"
