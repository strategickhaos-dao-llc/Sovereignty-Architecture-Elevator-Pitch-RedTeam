#!/bin/bash
# Quick Start Script for Neural Heir Evolution System
# Ensures dependencies are installed and provides easy launch commands

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🧬 Neural Heir Evolution System - Quick Start"
echo "=" | tr -d '\n' && printf '%.0s=' {1..60} && echo ""
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION detected"

# Install dependencies if needed
if ! python3 -c "import httpx" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt --user
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi

echo ""
echo "Available Commands:"
echo "=" | tr -d '\n' && printf '%.0s=' {1..60} && echo ""
echo ""
echo "1. Basic Evolution (MVP):"
echo "   python3 evolution_engine.py"
echo ""
echo "2. Nuclear Evolution (All Level 10 features):"
echo "   python3 evolution_nuclear.py --generations 100 --population 20"
echo ""
echo "3. Run Tests:"
echo "   python3 test_evolution.py"
echo ""
echo "4. Monitor Progress (in another terminal):"
echo "   tail -f evolution_ledger.jsonl | jq '{generation, avg_fitness, best_fitness}'"
echo ""
echo "5. View Lineage Report:"
echo "   python3 -c 'from lineage import visualize_evolution_progress; visualize_evolution_progress()'"
echo ""
echo "=" | tr -d '\n' && printf '%.0s=' {1..60} && echo ""
echo ""

# Offer to run tests
read -p "Run tests now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Running tests..."
    python3 test_evolution.py
    echo ""
fi

# Offer to start basic evolution
read -p "Start basic evolution now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🚀 Starting evolution engine..."
    echo "Press Ctrl+C to stop"
    echo ""
    python3 evolution_engine.py
fi
