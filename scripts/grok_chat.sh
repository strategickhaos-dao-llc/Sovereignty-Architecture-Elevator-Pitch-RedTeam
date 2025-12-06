#!/usr/bin/env bash
set -euo pipefail

# Grok (x.ai) Chat Completions Script
# Usage: ./grok_chat.sh "Your prompt here"
# Requires: XAI_API_KEY environment variable

: "${XAI_API_KEY:?ERROR: XAI_API_KEY environment variable is required}"

PROMPT="${1:-Testing. Just say hi and hello world and nothing else.}"
MODEL="${2:-grok-beta}"
TEMPERATURE="${3:-0}"
STREAM="${4:-false}"

echo "🤖 Grok API Chat Completion"
echo "======================================"
echo "Model: $MODEL"
echo "Temperature: $TEMPERATURE"
echo "Prompt: $PROMPT"
echo "======================================"
echo ""

RESPONSE=$(curl -s https://api.x.ai/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $XAI_API_KEY" \
    -d "$(jq -n \
        --arg model "$MODEL" \
        --arg prompt "$PROMPT" \
        --argjson temp "$TEMPERATURE" \
        --argjson stream "$(echo $STREAM | tr '[:upper:]' '[:lower:]')" \
        '{
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant for the Sovereignty Architecture project."
                },
                {
                    "role": "user",
                    "content": $prompt
                }
            ],
            "model": $model,
            "stream": $stream,
            "temperature": $temp
        }')")

# Check if request was successful
if echo "$RESPONSE" | jq -e '.error' > /dev/null 2>&1; then
    echo "❌ Error from Grok API:"
    echo "$RESPONSE" | jq -r '.error.message // .error'
    exit 1
fi

# Extract and display the response
if echo "$RESPONSE" | jq -e '.choices[0].message.content' > /dev/null 2>&1; then
    echo "✅ Response:"
    echo "$RESPONSE" | jq -r '.choices[0].message.content'
    echo ""
    echo "📊 Usage:"
    echo "$RESPONSE" | jq -r '.usage | "  Prompt tokens: \(.prompt_tokens)\n  Completion tokens: \(.completion_tokens)\n  Total tokens: \(.total_tokens)"'
else
    echo "⚠️  Unexpected response format:"
    echo "$RESPONSE" | jq '.'
fi
