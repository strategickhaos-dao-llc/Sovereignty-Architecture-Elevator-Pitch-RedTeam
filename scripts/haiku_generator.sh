#!/bin/bash
# haiku_generator.sh - Spite-Thermal Haiku Generator

set -euo pipefail

# Configuration
MODEL="${1:-llama3.2:3b}"
OUTPUT_DIR="./artifacts"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Prompt engineering for spite-thermal theme
PROMPT="You are a technical poet. Write a single haiku (5-7-5 syllable structure) that captures the essence of:
- Computational spite (doing more with less out of defiance)
- Thermal constraints (CPU throttling, heat management)
- Sovereign determination (building empires despite limitations)

The haiku should be technical, defiant, and inspiring. Output ONLY the haiku, nothing else."

echo "🔥 Generating Spite-Thermal Haiku..."
echo "Model: $MODEL"
echo "Timestamp: $TIMESTAMP"
echo ""

# Check system resources
echo "📊 System Resources:"
CPU_USAGE=$(top -bn1 2>/dev/null | grep -i "cpu" | head -n1 | awk '{print $2}' | sed 's/%us,//' || echo 'N/A')
echo "  CPU Usage: ${CPU_USAGE}%"
echo "  RAM Free: $(free -h 2>/dev/null | grep Mem | awk '{print $4}' || echo 'N/A')"
echo "  Temp: $(sensors 2>/dev/null | grep -i 'Package id 0' | awk '{print $4}' || echo 'N/A')"
echo ""

# Check if ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found. Please install it first:"
    echo "   curl -fsSL https://ollama.com/install.sh | sh"
    exit 1
fi

# Generate haiku
echo "⚙️ Running inference..."
HAIKU=$(ollama run "$MODEL" "$PROMPT" 2>/dev/null | head -n 3)

# Format output
cat > "$OUTPUT_DIR/haiku_${TIMESTAMP}.txt" << EOF
# Spite-Thermal Haiku
Generated: $(date)
Model: $MODEL
System: $(uname -n)

---

$HAIKU

---

Constraints:
- RAM: $(free -h 2>/dev/null | grep Mem | awk '{print $3 "/" $2}' || echo 'N/A')
- CPU: $(nproc) cores
- Thermal: $(sensors 2>/dev/null | grep -i 'Package id 0' | awk '{print $4}' || echo 'N/A')
EOF

# Display results
echo "✅ Haiku Generated:"
echo ""
cat "$OUTPUT_DIR/haiku_${TIMESTAMP}.txt"
echo ""
echo "💾 Saved to: $OUTPUT_DIR/haiku_${TIMESTAMP}.txt"

# Add to README if requested
if [[ "${2:-}" == "--add-to-readme" ]]; then
    echo "" >> README.md
    echo "---" >> README.md
    echo "" >> README.md
    echo "## 🎋 Signature Spite-Thermal Haiku" >> README.md
    echo "" >> README.md
    echo '```' >> README.md
    echo "$HAIKU" >> README.md
    echo '```' >> README.md
    echo "" >> README.md
    echo "_Generated locally under thermal constraints - $(date +%Y-%m-%d)_" >> README.md
    echo "" >> README.md
    echo "✅ Added haiku to README.md"
fi
