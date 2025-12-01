#!/bin/bash
# Grafana Cloud Integration Deployment Script
# Deploys AI-powered observability for Strategickhaos Sovereignty Architecture

set -e

echo "🚀 Grafana Cloud Integration - Sovereignty Architecture"
echo "========================================================"

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "📝 Please edit .env and add your Grafana Cloud credentials:"
    echo "   - GRAFANA_CLOUD_API_TOKEN"
    echo "   - GRAFANA_CLOUD_PROMETHEUS_URL"
    echo "   - GRAFANA_CLOUD_PROMETHEUS_USER"
    echo ""
    echo "Get your credentials at: https://grafana.com/profile/api-keys"
    echo ""
    read -p "Press Enter after updating .env to continue..."
fi

# Load environment variables
source .env

# Check if required variables are set
if [ -z "$GRAFANA_CLOUD_API_TOKEN" ] || [ "$GRAFANA_CLOUD_API_TOKEN" == "your_grafana_cloud_api_token" ]; then
    echo "❌ Error: GRAFANA_CLOUD_API_TOKEN not set in .env"
    echo "Please update .env with your actual Grafana Cloud API token"
    exit 1
fi

echo "✅ Environment variables loaded"
echo ""

# Deployment mode selection
echo "Select deployment mode:"
echo "1) Grafana Alloy (Recommended - Modern OpenTelemetry collector)"
echo "2) Prometheus + Remote Write (Traditional approach)"
echo "3) Both (Full observability stack)"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo "🚀 Deploying Grafana Alloy..."
        docker-compose -f docker-compose.obs.yml up -d alloy redis vault
        MODE="alloy"
        ;;
    2)
        echo "🚀 Deploying Prometheus with Remote Write..."
        docker-compose -f docker-compose.obs.yml up -d prometheus redis vault
        MODE="prometheus"
        ;;
    3)
        echo "🚀 Deploying Full Observability Stack..."
        docker-compose -f docker-compose.obs.yml up -d prometheus alloy grafana loki redis vault
        MODE="full"
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo ""
echo "🔍 Checking service health..."

if [ "$MODE" == "alloy" ] || [ "$MODE" == "full" ]; then
    if curl -s http://localhost:12345/ready > /dev/null; then
        echo "✅ Alloy is ready"
        echo "   UI: http://localhost:12345"
    else
        echo "⚠️  Alloy may not be ready yet. Check logs: docker-compose -f docker-compose.obs.yml logs alloy"
    fi
fi

if [ "$MODE" == "prometheus" ] || [ "$MODE" == "full" ]; then
    if curl -s http://localhost:9090/-/ready > /dev/null; then
        echo "✅ Prometheus is ready"
        echo "   UI: http://localhost:9090"
    else
        echo "⚠️  Prometheus may not be ready yet. Check logs: docker-compose -f docker-compose.obs.yml logs prometheus"
    fi
fi

# Provide next steps
echo ""
echo "✨ Deployment complete!"
echo ""
echo "📊 Next Steps:"
echo ""
echo "1. Verify metrics are flowing:"
echo "   - Open your Grafana Cloud instance: ${GRAFANA_CLOUD_INSTANCE_URL:-https://yourorg.grafana.net}"
echo "   - Navigate to Explore"
echo "   - Query: up{source=\"sovereignty-architecture\"}"
echo ""
echo "2. Import dashboards:"
echo "   - Search for 'Docker', 'PostgreSQL', 'Redis' integrations"
echo "   - Use pre-built dashboards from Grafana Cloud"
echo ""
echo "3. Set up alerts:"
echo "   - Configure Grafana Cloud OnCall"
echo "   - Link to Discord webhook for notifications"
echo ""
echo "4. Explore AI features:"
echo "   - Grafana Asserts for root cause analysis"
echo "   - SLO management for service objectives"
echo "   - Anomaly detection with ML"
echo ""
echo "📚 Full guide: GRAFANA_CLOUD_INTEGRATION.md"
echo ""
echo "🔧 Useful commands:"
echo "   - View logs: docker-compose -f docker-compose.obs.yml logs -f"
echo "   - Stop services: docker-compose -f docker-compose.obs.yml down"
echo "   - Check status: docker-compose -f docker-compose.obs.yml ps"
echo ""
echo "🆘 Troubleshooting:"
echo "   - If metrics don't appear, check your API token is valid"
echo "   - Verify URLs match your Grafana Cloud instance"
echo "   - Check logs for authentication errors"
echo ""
