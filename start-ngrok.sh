#!/bin/bash
# Sovereignty-focused ngrok launcher with auto-replay capability
# Zero-trust, zero-cloud-for-dev, fully local god-mode webhook setup

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NGROK_CONFIG="${SCRIPT_DIR}/ngrok.yml"
NGROK_API="http://localhost:4040/api"
REPLAY_COUNT=5  # Number of recent failed webhooks to replay

echo "🚀 Starting Sovereignty Ngrok Setup..."
echo "================================================"

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok is not installed!"
    echo "📦 Install it from: https://ngrok.com/download"
    echo ""
    echo "Quick install:"
    echo "  macOS:    brew install ngrok/ngrok/ngrok"
    echo "  Linux:    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo 'deb https://ngrok-agent.s3.amazonaws.com buster main' | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok"
    echo "  Windows:  choco install ngrok"
    exit 1
fi

# Check if ngrok config exists
if [ ! -f "$NGROK_CONFIG" ]; then
    echo "❌ ngrok.yml not found at: $NGROK_CONFIG"
    echo "📝 Create it by copying ngrok.yml.example or follow the setup guide"
    exit 1
fi

# Kill any existing ngrok processes (sovereignty = clean slate)
echo "🧹 Cleaning up any existing ngrok processes..."
pkill -f ngrok || true
sleep 2

# Start ngrok with all tunnels
echo "🌐 Starting ngrok tunnels from config..."
ngrok start --all --config "$NGROK_CONFIG" > /tmp/ngrok.log 2>&1 &
NGROK_PID=$!

# Wait for ngrok to initialize
echo "⏳ Waiting for ngrok to initialize..."
for i in {1..10}; do
    if curl -s "$NGROK_API/tunnels" &> /dev/null; then
        echo "✅ Ngrok API is ready!"
        break
    fi
    if [ $i -eq 10 ]; then
        echo "❌ Ngrok failed to start. Check /tmp/ngrok.log"
        cat /tmp/ngrok.log
        exit 1
    fi
    sleep 1
done

# Display active tunnels
echo ""
echo "🔗 Active Tunnels:"
echo "================================================"
curl -s "$NGROK_API/tunnels" | jq -r '.tunnels[] | "  \(.name): \(.public_url)"' 2>/dev/null || echo "  (Unable to parse tunnel URLs)"

# Get event-gateway URL
EVENT_GATEWAY_URL=$(curl -s "$NGROK_API/tunnels" | jq -r '.tunnels[] | select(.name=="event-gateway") | .public_url' 2>/dev/null)
if [ -n "$EVENT_GATEWAY_URL" ]; then
    echo ""
    echo "📡 Event Gateway Webhook URL:"
    echo "  $EVENT_GATEWAY_URL/webhooks/github"
    echo ""
    echo "📋 Set this URL in your GitHub repository:"
    echo "  Settings → Webhooks → Add webhook"
    echo "  Payload URL: $EVENT_GATEWAY_URL/webhooks/github"
    echo "  Content type: application/json"
    echo "  Secret: (your GITHUB_WEBHOOK_SECRET)"
fi

# Auto-replay functionality for failed webhooks
echo ""
echo "🔄 Auto-replay: Checking for recent failed webhooks..."
sleep 2  # Give ngrok time to populate request history

# Replay recent failed requests (status >= 400)
FAILED_REQUESTS=$(curl -s "$NGROK_API/requests/http" | jq -r ".requests[] | select(.response.status >= 400) | .id" 2>/dev/null | head -$REPLAY_COUNT)

if [ -n "$FAILED_REQUESTS" ]; then
    echo "🔁 Found failed requests, replaying last $REPLAY_COUNT..."
    echo "$FAILED_REQUESTS" | while read -r req_id; do
        if [ -n "$req_id" ]; then
            echo "  ↻ Replaying request: $req_id"
            curl -s -X POST "$NGROK_API/requests/http/$req_id/replay" -H "Content-Type: application/json" > /dev/null 2>&1 || true
        fi
    done
    echo "✅ Replay complete!"
else
    echo "ℹ️  No failed requests to replay (clean slate!)"
fi

echo ""
echo "================================================"
echo "🎯 Ngrok Control Panel: http://localhost:4040"
echo "📊 Inspect webhooks, replay requests, debug in real-time"
echo ""
echo "💡 Tips:"
echo "  - Reserve a static domain at https://dashboard.ngrok.com/domains"
echo "  - Update ngrok.yml with your domain to avoid URL changes"
echo "  - Use 'make destroy' to nuke everything and start fresh"
echo ""
echo "🚀 Sovereign dev mode: ACTIVE"
echo "================================================"

# Keep script running (optional - comment out if you want it to exit)
echo ""
echo "Press Ctrl+C to stop ngrok..."
wait $NGROK_PID
