#!/bin/bash
# Setup Grafana Cloud Integration for Strategickhaos Sovereignty Architecture
# This script helps configure Grafana Cloud credentials and validates the setup

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

echo "🌥️  Grafana Cloud Setup for Strategickhaos Sovereignty Architecture"
echo "================================================================"
echo ""

# Check if .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Error: .env file not found at $ENV_FILE"
    echo "Creating .env from .env.example..."
    cp "$PROJECT_ROOT/.env.example" "$ENV_FILE"
fi

# Function to update or add environment variable
update_env_var() {
    local key=$1
    local value=$2
    local file=$3
    
    if grep -q "^${key}=" "$file"; then
        # Update existing variable (macOS and Linux compatible)
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s|^${key}=.*|${key}=${value}|" "$file"
        else
            sed -i "s|^${key}=.*|${key}=${value}|" "$file"
        fi
    else
        # Add new variable
        echo "${key}=${value}" >> "$file"
    fi
}

# Prompt for Grafana Cloud API token
echo "📝 Please enter your Grafana Cloud API Token:"
echo "   (Generate at: https://grafana.com/orgs/me1010101/access-policies)"
echo ""
read -r -p "API Token: " GRAFANA_API_TOKEN

if [ -z "$GRAFANA_API_TOKEN" ]; then
    echo "❌ Error: API token cannot be empty"
    exit 1
fi

# Update .env file with Grafana Cloud configuration
echo ""
echo "✏️  Updating .env file..."

update_env_var "GRAFANA_CLOUD_INSTANCE_ID" "2786173" "$ENV_FILE"
update_env_var "GRAFANA_CLOUD_API_TOKEN" "$GRAFANA_API_TOKEN" "$ENV_FILE"
update_env_var "GRAFANA_CLOUD_PROMETHEUS_URL" "https://prometheus-prod-56-prod-us-east-2.grafana.net/api/prom" "$ENV_FILE"
update_env_var "GRAFANA_CLOUD_REMOTE_WRITE_URL" "https://prometheus-prod-56-prod-us-east-2.grafana.net/api/prom/push" "$ENV_FILE"

echo "✅ Environment file updated"

# Test connectivity to Grafana Cloud
echo ""
echo "🔍 Testing connection to Grafana Cloud..."

response=$(curl -s -o /dev/null -w "%{http_code}" \
    --user "2786173:$GRAFANA_API_TOKEN" \
    "https://prometheus-prod-56-prod-us-east-2.grafana.net/api/prom/api/v1/labels" || echo "000")

if [ "$response" = "200" ]; then
    echo "✅ Successfully connected to Grafana Cloud!"
elif [ "$response" = "401" ]; then
    echo "❌ Authentication failed. Please check your API token."
    echo "   Make sure the token has MetricsPublisher permissions."
    exit 1
elif [ "$response" = "000" ]; then
    echo "⚠️  Could not connect to Grafana Cloud. Check your internet connection."
    exit 1
else
    echo "⚠️  Unexpected response: HTTP $response"
    echo "   You may need to verify your configuration manually."
fi

# Check if Docker is running
echo ""
echo "🐳 Checking Docker status..."
if ! docker info > /dev/null 2>&1; then
    echo "⚠️  Docker is not running. Please start Docker to deploy the stack."
    exit 0
fi

echo "✅ Docker is running"

# Offer to restart Prometheus with new configuration
echo ""
read -r -p "Would you like to restart Prometheus with the new configuration? (y/n): " restart_prometheus

if [[ "$restart_prometheus" =~ ^[Yy]$ ]]; then
    echo ""
    echo "🔄 Restarting Prometheus..."
    
    cd "$PROJECT_ROOT"
    
    # Check if using docker-compose or docker-compose.obs.yml
    if docker-compose -f docker-compose.obs.yml ps prometheus > /dev/null 2>&1; then
        docker-compose -f docker-compose.obs.yml restart prometheus
        echo "✅ Prometheus restarted (using docker-compose.obs.yml)"
    elif docker-compose ps prometheus > /dev/null 2>&1; then
        docker-compose restart prometheus
        echo "✅ Prometheus restarted (using docker-compose.yml)"
    else
        echo "⚠️  Prometheus container not found. You may need to start it manually:"
        echo "   docker-compose -f docker-compose.obs.yml up -d prometheus"
    fi
    
    # Wait a few seconds and check logs
    echo ""
    echo "📋 Checking Prometheus logs for remote_write status..."
    sleep 3
    
    if docker ps | grep -q prometheus; then
        docker logs prometheus 2>&1 | grep -i "remote_write" | tail -5 || echo "No remote_write logs found yet (this is normal on first start)"
    fi
fi

echo ""
echo "================================================================"
echo "✅ Grafana Cloud Setup Complete!"
echo ""
echo "📚 Next Steps:"
echo "   1. View your metrics at: https://grafana.com/orgs/me1010101"
echo "   2. Check Prometheus status: http://localhost:9090"
echo "   3. Read the full documentation: $PROJECT_ROOT/GRAFANA_CLOUD_INTEGRATION.md"
echo ""
echo "🔍 To verify metrics are being sent:"
echo "   docker logs prometheus 2>&1 | grep remote_write"
echo ""
echo "================================================================"
