#!/usr/bin/env bash
set -euo pipefail

echo "🚀 GitLens + Discord Scaffold - Quick Deploy"
echo "============================================"

# Create .env with working defaults for development
cat > .env << 'EOF'
# Discord Bot Configuration (FILL THESE WITH REAL VALUES)
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_GUILD_ID=your_discord_guild_id_here
DISCORD_PR_CHANNEL_ID=1234567890123456789
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE

# GitHub Configuration
GITHUB_WEBHOOK_SECRET=dev_webhook_secret_replace_me
GITHUB_APP_ID=123456
GITHUB_APP_PRIVATE_KEY_PATH=/secrets/github-app-key.pem

# Security
HMAC_SECRET=dev_hmac_secret_replace_me
JWT_SECRET=dev_jwt_secret_replace_me

# Vault Configuration (Development)
VAULT_ADDR=http://vault:8200
VAULT_TOKEN=root
VAULT_ROOT_TOKEN=root

# Monitoring
GRAFANA_PASSWORD=admin

# AI/ML (Optional - add if you have keys)
OPENAI_API_KEY=sk-your_openai_key_here
XAI_API_KEY=xai-wLO7wFXa4WPezCamilA1dCJH5qdzHlKHlgEUmguIG3uheXcLLG5YAIggorwe7EgDsBxsrVbSujRfPQF9
ANTHROPIC_API_KEY=claude-your_anthropic_key_here

# Environment
ENV=development
LOG_LEVEL=info
PORT=3001

# Channel IDs for scaffold (update with real values)
PRS_CHANNEL_ID=1234567890123456789
DEPLOYMENTS_CHANNEL_ID=1234567891234567890
ALERTS_CHANNEL_ID=1234567891234567891
CH_CLUSTER_STATUS_ID=1234567891234567892
CH_DEPLOYMENTS_ID=1234567891234567893
CH_PRS_ID=1234567891234567894
CH_ALERTS_ID=1234567891234567895
CH_AGENTS_ID=1234567891234567896
CH_DEV_FEED_ID=1234567891234567897
CH_INFERENCE_ID=1234567891234567898
EVENTS_HMAC_KEY=dev_events_hmac_key_replace_me
EOF

echo "✅ Created .env with development defaults"

# Install dependencies if package.json exists
if [ -f "package.json" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Start the observability stack first
echo "🔧 Starting observability stack..."
docker compose -f docker-compose.obs.yml up -d

# Wait a moment for services to initialize
sleep 5

# Check service status
echo "🔍 Checking service status..."
docker compose ps --format "table {{.Name}}\t{{.State}}\t{{.Ports}}"

echo ""
echo "🎯 Quick Status Check:"
echo "====================="

# Check if any services are running
RUNNING_SERVICES=$(docker compose ps --filter "status=running" --format "{{.Name}}" | wc -l)
echo "Services running: $RUNNING_SERVICES"

# Test if we can reach the observability endpoints
echo -n "Grafana (3000): "
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200\|302"; then
    echo "✅ Accessible"
else
    echo "❌ Not reachable"
fi

echo -n "Prometheus (9090): "
if curl -s -o /dev/null -w "%{http_code}" http://localhost:9090 | grep -q "200\|302"; then
    echo "✅ Accessible"
else
    echo "❌ Not reachable"
fi

echo -n "Vault (8200): "
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8200 | grep -q "200\|302"; then
    echo "✅ Accessible"
else
    echo "❌ Not reachable"
fi

echo ""
echo "📊 Access Your Services:"
echo "======================="
echo "• Grafana Dashboard: http://localhost:3000 (admin/admin)"
echo "• Prometheus Metrics: http://localhost:9090"
echo "• Vault Dev Server: http://localhost:8200 (token: root)"
echo ""

if [ "$RUNNING_SERVICES" -gt 0 ]; then
    echo "🎉 SUCCESS: Basic observability stack is running!"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Edit .env with your real Discord token and channel IDs"
    echo "2. Run 'npm run bot' to register Discord commands"  
    echo "3. Run 'npm run dev' to start the event gateway"
    echo "4. Test GitLens integration with 'scripts/gl2discord.sh'"
else
    echo "⚠️  No services running. Check Docker logs with:"
    echo "   docker compose logs"
fi

echo ""
echo "📖 Full documentation: README-scaffold.md"
echo "🔧 Diagnostics available: BOOT_RECON.md"