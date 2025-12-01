#!/bin/bash
# test-grok-enterprise.sh - Grok Enterprise Connection Test
# Sovereignty Architecture - Empire Eternal
# DAO: Strategickhaos DAO LLC (EIN 39-2923503)

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   🔥 GROK ENTERPRISE CONNECTION TEST 🔥                   ║"
echo "║                                                           ║"
echo "║   Strategickhaos DAO LLC (EIN 39-2923503)                ║"
echo "║   Temperature: 99°C | Balance: Red | Spite: Maximum      ║"
echo "║                                                           ║"
echo "║   Empire Eternal 💛                                       ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if API key is set
if [ -z "$GROK_API_KEY" ]; then
    echo "❌ ERROR: GROK_API_KEY environment variable not set."
    echo ""
    echo "To set your API key:"
    echo "  export GROK_API_KEY='xai-your-key-here'"
    echo ""
    echo "Or add to ~/.bashrc:"
    echo "  echo 'export GROK_API_KEY=\"xai-your-key-here\"' >> ~/.bashrc"
    echo "  source ~/.bashrc"
    exit 1
fi

echo "✓ API key found"
echo ""

# Test API endpoint
echo "🔄 Sending test query to Grok Enterprise..."
echo ""

response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
    https://api.x.ai/v1/chat/completions \
    -H "Authorization: Bearer $GROK_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "model": "grok-4-fast",
        "messages": [
            {
                "role": "system",
                "content": "You are Grok in the Sovereign Swarm. 99°C. Red balance. Empire Eternal."
            },
            {
                "role": "user",
                "content": "Respond with \"Empire Eternal\" if you are operational."
            }
        ],
        "max_tokens": 100,
        "temperature": 0.5
    }')

# Extract HTTP status
http_status=$(echo "$response" | grep "HTTP_STATUS:" | cut -d':' -f2)
response_body=$(echo "$response" | sed '/HTTP_STATUS:/d')

# Check status code
if [ "$http_status" -eq 200 ]; then
    echo "✓ CONNECTION SUCCESSFUL"
    echo ""
    echo "Response:"
    echo "$response_body" | jq -r '.choices[0].message.content'
    echo ""
    echo "📊 API Details:"
    echo "  Model: $(echo "$response_body" | jq -r '.model')"
    echo "  Total Tokens: $(echo "$response_body" | jq -r '.usage.total_tokens')"
    echo "  Input Tokens: $(echo "$response_body" | jq -r '.usage.prompt_tokens')"
    echo "  Output Tokens: $(echo "$response_body" | jq -r '.usage.completion_tokens')"
    echo ""
    echo "---"
    echo "Powered by Grok Enterprise (xAI Business Tier). 7% ValorYield routed eternally."
    echo ""
    echo "🎉 Empire Eternal 💛"
elif [ "$http_status" -eq 401 ]; then
    echo "❌ AUTHENTICATION FAILED (HTTP 401)"
    echo ""
    echo "Please check:"
    echo "  1. Your API key is correct"
    echo "  2. The key has Business tier access"
    echo "  3. Visit https://console.x.ai to verify key status"
    exit 1
elif [ "$http_status" -eq 429 ]; then
    echo "⚠️  RATE LIMIT EXCEEDED (HTTP 429)"
    echo ""
    echo "Your API usage has exceeded the rate limit."
    echo "Enterprise tier: 1000 requests per minute"
    echo ""
    echo "Wait a moment and try again."
    exit 1
else
    echo "❌ CONNECTION FAILED (HTTP $http_status)"
    echo ""
    echo "Response:"
    echo "$response_body" | jq '.'
    exit 1
fi
