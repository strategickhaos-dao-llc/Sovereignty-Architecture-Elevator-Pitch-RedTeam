#!/bin/bash
# Quick launch script for TRS Multi-Agent Chess System

set -e

echo "================================================"
echo "TRS Multi-Agent Chess System"
echo "================================================"
echo ""

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama is not running!"
    echo "Please start Ollama first:"
    echo "  ollama serve"
    exit 1
fi

echo "✅ Ollama is running"

# Check if model is available
if ! ollama list | grep -q "llama3.2:3b"; then
    echo "⚠️  Model llama3.2:3b not found"
    echo "Pulling model (this may take a while)..."
    ollama pull llama3.2:3b
fi

echo "✅ Model llama3.2:3b is available"
echo ""

# Check Python dependencies
if ! python3 -c "import chess" 2>/dev/null; then
    echo "⚠️  Python dependencies not installed"
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

echo "✅ Dependencies installed"
echo ""

# Create logs directory
mkdir -p logs

echo "🚀 Starting TRS Multi-Agent Chess System..."
echo ""
echo "WebSocket server will be available at: ws://localhost:8765"
echo "Press Ctrl+C to stop"
echo ""

# Run the system
python3 main.py
