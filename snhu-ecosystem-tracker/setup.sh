#!/bin/bash
# Setup script for SNHU Ecosystem Tracker

set -e

echo "================================"
echo "SNHU Ecosystem Tracker Setup"
echo "================================"
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.12 or higher."
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION found"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "⚠ Docker is not installed. Docker is required for containerization."
else
    DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
    echo "✓ Docker $DOCKER_VERSION found"
fi

# Check kubectl
if ! command -v kubectl &> /dev/null; then
    echo "⚠ kubectl is not installed. kubectl is required for Kubernetes deployment."
else
    KUBECTL_VERSION=$(kubectl version --client --short 2>/dev/null | cut -d' ' -f3 || echo "unknown")
    echo "✓ kubectl $KUBECTL_VERSION found"
fi

echo ""
echo "================================"
echo "Environment Configuration"
echo "================================"
echo ""

# Check for Grok API key
if [ -z "$GROK_API_KEY" ]; then
    echo "❌ GROK_API_KEY environment variable is not set."
    echo ""
    echo "Please set your Grok API key:"
    echo "  export GROK_API_KEY='your-grok-api-key'"
    echo ""
    echo "Get your API key from: https://x.ai/api"
    echo ""
    read -p "Do you want to enter your API key now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your Grok API key: " GROK_API_KEY
        export GROK_API_KEY
        echo "✓ GROK_API_KEY set"
    else
        echo "⚠ Skipping API key configuration"
    fi
else
    echo "✓ GROK_API_KEY is set"
fi

# Optional: Discord webhook
if [ -z "$DISCORD_WEBHOOK_URL" ]; then
    echo "⚠ DISCORD_WEBHOOK_URL not set (optional)"
else
    echo "✓ DISCORD_WEBHOOK_URL is set"
fi

echo ""
echo "================================"
echo "Installing Python Dependencies"
echo "================================"
echo ""

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo "✓ Dependencies installed"

echo ""
echo "================================"
echo "Validating Configuration"
echo "================================"
echo ""

echo "Validating YAML files..."
python3 -c "
import yaml
import sys

files = [
    'k8s/deployment.yaml',
    'k8s/configmap.yaml',
    'k8s/service.yaml',
    'k8s/secret.yaml',
    'k8s/cronjob.yaml',
    'k8s/pvc.yaml',
    'docker/docker-compose.yml',
    '.github/workflows/deploy.yml'
]

all_valid = True
for f in files:
    try:
        with open(f) as file:
            yaml.safe_load(file)
        print(f'✓ {f}')
    except Exception as e:
        print(f'✗ {f}: {e}')
        all_valid = False

if not all_valid:
    sys.exit(1)
"

echo ""
echo "Validating Python code..."
python3 -m py_compile src/main.py src/email_analyzer.py
echo "✓ Python code is valid"

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Replace placeholder values in configuration files:"
echo "   - Update Docker image name in k8s/*.yaml and .github/workflows/deploy.yml"
echo "   - Set Grok API key: kubectl create secret generic grok-secret --from-literal=api-key=\$GROK_API_KEY"
echo ""
echo "2. Test locally:"
echo "   source venv/bin/activate"
echo "   python src/main.py"
echo ""
echo "3. Or with Docker:"
echo "   docker build -t snhu-analyzer -f docker/Dockerfile ."
echo "   docker run -e GROK_API_KEY=\$GROK_API_KEY -p 8080:8080 snhu-analyzer"
echo ""
echo "4. Deploy to Kubernetes:"
echo "   kubectl apply -f k8s/"
echo ""
echo "5. Run batch analysis:"
echo "   export RUN_MODE=batch"
echo "   export INPUT_FILE=examples/sample_emails.csv"
echo "   python src/main.py"
echo ""
echo "For more information, see README.md"
echo ""
