#!/usr/bin/env bash
set -e

echo "Testing Grafana Cloud integration configuration..."
echo

echo "1. Validate Prometheus config"
if command -v docker &> /dev/null && docker compose ps prometheus | grep -q "Up"; then
  docker compose exec prometheus promtool check config /etc/prometheus/prometheus.yml
  echo "✓ Prometheus config is valid"
else
  echo "⚠ Prometheus is not running. Start with: docker compose up -d prometheus"
fi

echo
echo "2. Check if remote_write is configured"
if grep -q "prometheus-prod-56-prod-us-east-2" monitoring/prometheus.yml; then
  echo "✓ remote_write configured"
else
  echo "✗ remote_write missing"
  exit 1
fi

echo
echo "3. Check if GRAFANA_CLOUD_API_TOKEN is set in .env"
if grep -q "GRAFANA_CLOUD_API_TOKEN=" .env 2>/dev/null && ! grep -q "GRAFANA_CLOUD_API_TOKEN=glc_XXX" .env; then
  echo "✓ GRAFANA_CLOUD_API_TOKEN is set"
else
  echo "⚠ GRAFANA_CLOUD_API_TOKEN not set or using example value"
  echo "  Run ./scripts/setup-grafana-cloud.sh to configure"
fi

echo
echo "4. Check if Grafana Cloud datasource is configured"
if grep -q "Grafana Cloud - me1010101-prom" monitoring/grafana/provisioning/datasources/datasources.yml; then
  echo "✓ Grafana Cloud datasource configured"
else
  echo "✗ Grafana Cloud datasource missing"
  exit 1
fi

echo
echo "All checks passed! 🚀"
echo
echo "Next steps:"
echo "1. Ensure GRAFANA_CLOUD_API_TOKEN is set in .env"
echo "2. Start/restart services: docker compose up -d"
echo "3. Check Prometheus targets: http://localhost:9090/targets"
echo "4. View metrics in Grafana Cloud: https://me1010101.grafana.net"
