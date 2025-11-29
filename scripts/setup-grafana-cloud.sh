#!/bin/bash
set -e

echo "Setting up Grafana Cloud integration for instance me1010101-prom (2786173)"
echo

read -p "Enter your Grafana Cloud API token (MetricsPublisher role): " -s TOKEN
echo

# Write to .env if not exist
if ! grep -q "GRAFANA_CLOUD_API_TOKEN" .env 2>/dev/null; then
  echo "GRAFANA_CLOUD_API_TOKEN=$TOKEN" >> .env
  echo "Token saved to .env"
else
  # Use sed in a cross-platform way
  if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/^GRAFANA_CLOUD_API_TOKEN=.*/GRAFANA_CLOUD_API_TOKEN=$TOKEN/" .env
  else
    sed -i "s/^GRAFANA_CLOUD_API_TOKEN=.*/GRAFANA_CLOUD_API_TOKEN=$TOKEN/" .env
  fi
  echo "Token updated in .env"
fi

echo
echo "Restarting Prometheus..."
docker compose restart prometheus

echo
echo "Integration complete. Test with ./scripts/test-grafana-cloud-config.sh"
