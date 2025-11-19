#!/bin/bash
# Test script to validate Grafana Cloud integration configurations

set -e

echo "🧪 Testing Grafana Cloud Integration Configurations"
echo "===================================================="
echo ""

# Test 1: Validate YAML syntax
echo "1️⃣  Testing docker-compose.obs.yml syntax..."
if python3 -c "import yaml; yaml.safe_load(open('docker-compose.obs.yml'))" 2>&1; then
    echo "   ✅ docker-compose.obs.yml is valid YAML"
else
    echo "   ❌ docker-compose.obs.yml has syntax errors"
    exit 1
fi
echo ""

# Test 2: Validate prometheus.yml syntax
echo "2️⃣  Testing prometheus.yml syntax..."
if python3 -c "import yaml; yaml.safe_load(open('monitoring/prometheus.yml'))" 2>&1; then
    echo "   ✅ prometheus.yml is valid YAML"
else
    echo "   ❌ prometheus.yml has syntax errors"
    exit 1
fi
echo ""

# Test 3: Check Alloy config exists
echo "3️⃣  Testing Alloy configuration..."
if [ -f "monitoring/alloy-config.alloy" ]; then
    echo "   ✅ alloy-config.alloy exists"
    # Check for required components
    if grep -q "prometheus.remote_write" monitoring/alloy-config.alloy && \
       grep -q "prometheus.scrape" monitoring/alloy-config.alloy && \
       grep -q "loki.write" monitoring/alloy-config.alloy; then
        echo "   ✅ alloy-config.alloy contains required components"
    else
        echo "   ❌ alloy-config.alloy missing required components"
        exit 1
    fi
else
    echo "   ❌ alloy-config.alloy not found"
    exit 1
fi
echo ""

# Test 4: Check deployment script
echo "4️⃣  Testing deployment script..."
if [ -x "deploy-grafana-cloud.sh" ]; then
    echo "   ✅ deploy-grafana-cloud.sh is executable"
else
    echo "   ❌ deploy-grafana-cloud.sh is not executable"
    exit 1
fi
echo ""

# Test 5: Check documentation
echo "5️⃣  Testing documentation..."
if [ -f "GRAFANA_CLOUD_INTEGRATION.md" ]; then
    echo "   ✅ GRAFANA_CLOUD_INTEGRATION.md exists"
    # Check for key sections
    if grep -q "Quick Setup" GRAFANA_CLOUD_INTEGRATION.md && \
       grep -q "Architecture Options" GRAFANA_CLOUD_INTEGRATION.md && \
       grep -q "Troubleshooting" GRAFANA_CLOUD_INTEGRATION.md; then
        echo "   ✅ Documentation contains required sections"
    else
        echo "   ⚠️  Documentation may be missing some sections"
    fi
else
    echo "   ❌ GRAFANA_CLOUD_INTEGRATION.md not found"
    exit 1
fi
echo ""

# Test 6: Check .env.example
echo "6️⃣  Testing environment configuration..."
if grep -q "GRAFANA_CLOUD_API_TOKEN" .env.example && \
   grep -q "GRAFANA_CLOUD_PROMETHEUS_URL" .env.example && \
   grep -q "GRAFANA_CLOUD_LOKI_URL" .env.example; then
    echo "   ✅ .env.example contains Grafana Cloud variables"
else
    echo "   ❌ .env.example missing Grafana Cloud variables"
    exit 1
fi
echo ""

# Test 7: Check Prometheus remote_write config
echo "7️⃣  Testing Prometheus remote_write configuration..."
if grep -q "remote_write:" monitoring/prometheus.yml && \
   grep -q "GRAFANA_CLOUD_PROMETHEUS_URL" monitoring/prometheus.yml && \
   grep -q "basic_auth:" monitoring/prometheus.yml; then
    echo "   ✅ Prometheus configured with remote_write"
else
    echo "   ❌ Prometheus remote_write configuration incomplete"
    exit 1
fi
echo ""

# Test 8: Check docker-compose service definitions
echo "8️⃣  Testing docker-compose service definitions..."
if grep -q "alloy:" docker-compose.obs.yml && \
   grep -q "grafana/alloy" docker-compose.obs.yml; then
    echo "   ✅ Alloy service defined in docker-compose"
else
    echo "   ❌ Alloy service not found in docker-compose"
    exit 1
fi
echo ""

# Test 9: Check README updates
echo "9️⃣  Testing README updates..."
if grep -q "Grafana Cloud" README.md && \
   grep -q "GRAFANA_CLOUD_INTEGRATION.md" README.md; then
    echo "   ✅ README updated with Grafana Cloud references"
else
    echo "   ⚠️  README may not reference Grafana Cloud integration"
fi
echo ""

echo "✅ All tests passed!"
echo ""
echo "🚀 Integration is ready for deployment"
echo "   Run: ./deploy-grafana-cloud.sh"
echo ""
