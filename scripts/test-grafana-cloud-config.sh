#!/bin/bash
# Test script for Grafana Cloud integration configuration
# Validates all configuration files and connections

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🧪 Testing Grafana Cloud Integration Configuration"
echo "=================================================="
echo ""

# Test 1: Check if configuration files exist
echo "📁 Test 1: Checking configuration files..."
required_files=(
    "monitoring/prometheus.yml"
    "monitoring/grafana/provisioning/datasources/datasources.yml"
    "GRAFANA_CLOUD_INTEGRATION.md"
    ".env.example"
)

all_files_exist=true
for file in "${required_files[@]}"; do
    if [ -f "$PROJECT_ROOT/$file" ]; then
        echo "  ✅ $file exists"
    else
        echo "  ❌ $file NOT FOUND"
        all_files_exist=false
    fi
done

if [ "$all_files_exist" = false ]; then
    echo ""
    echo "❌ Some required files are missing"
    exit 1
fi

echo "  ✅ All required files exist"
echo ""

# Test 2: Validate YAML syntax
echo "📝 Test 2: Validating YAML syntax..."

if command -v python3 &> /dev/null; then
    # Test prometheus.yml
    if python3 -c "import yaml; yaml.safe_load(open('$PROJECT_ROOT/monitoring/prometheus.yml'))" 2>/dev/null; then
        echo "  ✅ monitoring/prometheus.yml - valid YAML"
    else
        echo "  ❌ monitoring/prometheus.yml - invalid YAML"
        exit 1
    fi
    
    # Test datasources.yml
    if python3 -c "import yaml; yaml.safe_load(open('$PROJECT_ROOT/monitoring/grafana/provisioning/datasources/datasources.yml'))" 2>/dev/null; then
        echo "  ✅ datasources.yml - valid YAML"
    else
        echo "  ❌ datasources.yml - invalid YAML"
        exit 1
    fi
else
    echo "  ⚠️  Python3 not available, skipping YAML validation"
fi

echo ""

# Test 3: Check for Grafana Cloud configuration in Prometheus
echo "🔍 Test 3: Checking Prometheus remote_write configuration..."

if grep -q "remote_write:" "$PROJECT_ROOT/monitoring/prometheus.yml"; then
    echo "  ✅ remote_write configuration found"
else
    echo "  ❌ remote_write configuration NOT found"
    exit 1
fi

if grep -q "prometheus-prod-56-prod-us-east-2.grafana.net/api/prom/push" "$PROJECT_ROOT/monitoring/prometheus.yml"; then
    echo "  ✅ Grafana Cloud endpoint configured"
else
    echo "  ❌ Grafana Cloud endpoint NOT configured"
    exit 1
fi

if grep -q "GRAFANA_CLOUD_API_TOKEN" "$PROJECT_ROOT/monitoring/prometheus.yml"; then
    echo "  ✅ API token environment variable reference found"
else
    echo "  ❌ API token environment variable NOT found"
    exit 1
fi

echo ""

# Test 4: Check for Grafana Cloud datasource
echo "🔍 Test 4: Checking Grafana datasource configuration..."

if grep -q "Grafana Cloud" "$PROJECT_ROOT/monitoring/grafana/provisioning/datasources/datasources.yml"; then
    echo "  ✅ Grafana Cloud datasource configured"
else
    echo "  ❌ Grafana Cloud datasource NOT configured"
    exit 1
fi

echo ""

# Test 5: Validate Prometheus configuration with promtool (if Docker available)
echo "🐳 Test 5: Validating Prometheus configuration with promtool..."

if command -v docker &> /dev/null && docker info &> /dev/null; then
    cd "$PROJECT_ROOT"
    
    validation_output=$(docker run --rm --entrypoint /bin/promtool \
        -v "$(pwd)/monitoring:/etc/prometheus:ro" \
        -e GRAFANA_CLOUD_API_TOKEN="test_token" \
        prom/prometheus:v2.55.0 \
        check config /etc/prometheus/prometheus.yml 2>&1)
    
    if echo "$validation_output" | grep -q "SUCCESS.*is valid prometheus config"; then
        echo "  ✅ Prometheus configuration is valid"
    else
        echo "  ❌ Prometheus configuration validation failed"
        echo "$validation_output"
        exit 1
    fi
else
    echo "  ⚠️  Docker not available, skipping promtool validation"
fi

echo ""

# Test 6: Check environment variables in .env.example
echo "📋 Test 6: Checking .env.example for Grafana Cloud variables..."

required_vars=(
    "GRAFANA_CLOUD_INSTANCE_ID"
    "GRAFANA_CLOUD_API_TOKEN"
    "GRAFANA_CLOUD_PROMETHEUS_URL"
    "GRAFANA_CLOUD_REMOTE_WRITE_URL"
)

all_vars_present=true
for var in "${required_vars[@]}"; do
    if grep -q "^${var}=" "$PROJECT_ROOT/.env.example"; then
        echo "  ✅ $var found in .env.example"
    else
        echo "  ❌ $var NOT found in .env.example"
        all_vars_present=false
    fi
done

if [ "$all_vars_present" = false ]; then
    echo ""
    echo "❌ Some required environment variables are missing from .env.example"
    exit 1
fi

echo ""

# Test 7: Verify setup script exists and is executable
echo "🔧 Test 7: Checking setup script..."

if [ -f "$PROJECT_ROOT/scripts/setup-grafana-cloud.sh" ]; then
    echo "  ✅ setup-grafana-cloud.sh exists"
    
    if [ -x "$PROJECT_ROOT/scripts/setup-grafana-cloud.sh" ]; then
        echo "  ✅ setup-grafana-cloud.sh is executable"
    else
        echo "  ⚠️  setup-grafana-cloud.sh is not executable (run: chmod +x scripts/setup-grafana-cloud.sh)"
    fi
else
    echo "  ❌ setup-grafana-cloud.sh NOT found"
    exit 1
fi

echo ""

# Summary
echo "=================================================="
echo "✅ All configuration tests passed!"
echo ""
echo "📚 Next Steps:"
echo "   1. Set your Grafana Cloud API token in .env"
echo "   2. Run: ./scripts/setup-grafana-cloud.sh"
echo "   3. Start the stack: docker-compose -f docker-compose.obs.yml up -d"
echo "   4. Check logs: docker logs prometheus"
echo ""
echo "📖 Full documentation: $PROJECT_ROOT/GRAFANA_CLOUD_INTEGRATION.md"
echo "=================================================="
