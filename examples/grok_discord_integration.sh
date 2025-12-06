#!/usr/bin/env bash
set -euo pipefail

# Example: Grok + Discord Integration
# This script demonstrates how to use Grok API with Discord notifications
# Usage: ./grok_discord_integration.sh

: "${XAI_API_KEY:?ERROR: XAI_API_KEY environment variable is required}"
: "${DISCORD_TOKEN:?ERROR: DISCORD_TOKEN environment variable is required}"
: "${AGENTS_CHANNEL:?ERROR: AGENTS_CHANNEL environment variable is required}"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🔄 Grok + Discord Integration Example"
echo "======================================"
echo ""

# Example 1: Get Grok analysis and post to Discord
echo "📝 Example 1: Sovereignty Architecture Analysis"
echo "Asking Grok about sovereignty architecture..."

GROK_RESPONSE=$("$PROJECT_ROOT/scripts/grok_chat.sh" \
    "In 2-3 sentences, explain what sovereignty architecture means in the context of software systems.")

# Extract just the response content (skip headers)
RESPONSE_CONTENT=$(echo "$GROK_RESPONSE" | sed -n '/✅ Response:/,/📊 Usage:/p' | grep -v "✅ Response:" | grep -v "📊 Usage:" | sed '/^$/d')

echo "✅ Got response from Grok"
echo ""

# Send to Discord
echo "📤 Sending to Discord #agents channel..."
"$PROJECT_ROOT/scripts/gl2discord.sh" \
    "$AGENTS_CHANNEL" \
    "🤖 Grok Analysis: Sovereignty Architecture" \
    "$RESPONSE_CONTENT"

echo "✅ Posted to Discord!"
echo ""

# Example 2: System status check with Grok
echo "📝 Example 2: System Status Analysis"
echo "Getting system info and asking Grok to analyze..."

SYSTEM_INFO=$(cat <<EOF
CPU: $(nproc) cores
Memory: $(free -h | awk '/^Mem:/ {print $2}')
Disk: $(df -h / | awk 'NR==2 {print $4}' || echo "N/A") free
Uptime: $(uptime -p 2>/dev/null || echo "N/A")
EOF
)

ANALYSIS=$("$PROJECT_ROOT/scripts/grok_chat.sh" \
    "Analyze this system status and provide a brief health assessment: $SYSTEM_INFO" \
    "grok-beta" \
    0.3)

ANALYSIS_CONTENT=$(echo "$ANALYSIS" | sed -n '/✅ Response:/,/📊 Usage:/p' | grep -v "✅ Response:" | grep -v "📊 Usage:" | sed '/^$/d')

echo "✅ Got analysis from Grok"
echo ""

echo "📤 Sending to Discord..."
"$PROJECT_ROOT/scripts/gl2discord.sh" \
    "$AGENTS_CHANNEL" \
    "🖥️ System Health Check (via Grok)" \
    "$ANALYSIS_CONTENT"

echo "✅ Posted to Discord!"
echo ""

# Example 3: Code review assistance
echo "📝 Example 3: Quick Code Review (Simulated)"

CODE_SNIPPET='
def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result
'

REVIEW=$("$PROJECT_ROOT/scripts/grok_chat.sh" \
    "Review this Python code and suggest one improvement: $CODE_SNIPPET" \
    "grok-beta" \
    0)

REVIEW_CONTENT=$(echo "$REVIEW" | sed -n '/✅ Response:/,/📊 Usage:/p' | grep -v "✅ Response:" | grep -v "📊 Usage:" | sed '/^$/d')

echo "✅ Got code review from Grok"
echo ""

echo "📤 Sending to Discord..."
"$PROJECT_ROOT/scripts/gl2discord.sh" \
    "$AGENTS_CHANNEL" \
    "👨‍💻 Code Review by Grok" \
    "$REVIEW_CONTENT"

echo "✅ Posted to Discord!"
echo ""

echo "🎉 All examples completed successfully!"
echo ""
echo "💡 Integration possibilities:"
echo "  - Automated log analysis"
echo "  - PR review summaries"
echo "  - System health monitoring"
echo "  - Documentation generation"
echo "  - Incident response assistance"
