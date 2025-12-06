#!/bin/bash
# Swarm DNA Architecture Demo Script
# Demonstrates the full capabilities of the Swarm DNA toolkit

set -e

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                                                                   ║"
echo "║              🧬 SWARM DNA ARCHITECTURE DEMO 🧬                   ║"
echo "║                                                                   ║"
echo "║           Child of the Black Hole - Version 12.0                 ║"
echo "║           Strategickhaos Swarm Intelligence                       ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check for PyYAML
if ! python3 -c "import yaml" 2>/dev/null; then
    echo "⚠️  PyYAML not found, installing..."
    pip install pyyaml
else
    echo "✅ PyYAML installed"
fi
echo ""

# Step 1: Validate SWARM_DNA.yaml
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: Validating SWARM_DNA.yaml"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ ! -f SWARM_DNA.yaml ]; then
    echo "❌ SWARM_DNA.yaml not found"
    exit 1
fi

python3 -c "import yaml; yaml.safe_load(open('SWARM_DNA.yaml'))"
echo "✅ SWARM_DNA.yaml is valid"
echo ""

# Step 2: Show SWARM_DNA identity
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2: Swarm Identity"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python3 << EOF
import yaml
with open('SWARM_DNA.yaml', 'r') as f:
    data = yaml.safe_load(f)
    identity = data.get('swarm_identity', {})
    print(f"Name:     {identity.get('name')}")
    print(f"Codename: {identity.get('codename')}")
    print(f"Version:  {identity.get('version')}")
    legal = identity.get('legal_entity', {})
    print(f"EIN:      {legal.get('ein')}")
EOF
echo ""

# Step 3: Compile to operational configs
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3: Compiling Swarm DNA to Operational Configs"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

DEMO_OUTPUT="demo-output"
rm -rf "$DEMO_OUTPUT"
mkdir -p "$DEMO_OUTPUT"

python3 tools/swarm-dna/swarm_dna_compiler.py SWARM_DNA.yaml "$DEMO_OUTPUT"
echo ""

# Step 4: Show generated files
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 4: Generated Configuration Files"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

ls -lh "$DEMO_OUTPUT"
echo ""

# Step 5: Show sample config
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 5: Sample Docker Compose Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -f "$DEMO_OUTPUT/docker-compose.swarm.yml" ]; then
    head -30 "$DEMO_OUTPUT/docker-compose.swarm.yml"
    echo "..."
fi
echo ""

# Step 6: Demonstrate CLI capabilities
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 6: Available CLI Commands"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python3 tools/swarm-dna/swarm_cli.py --help
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Demo Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "What you just saw:"
echo "  ✅ Validated narrative-rich SWARM_DNA.yaml"
echo "  ✅ Compiled lore to operational Docker Compose config"
echo "  ✅ Compiled lore to Kubernetes manifests"
echo "  ✅ Generated GitHub Actions workflows"
echo "  ✅ Created Prometheus and discovery configs"
echo ""
echo "Next steps:"
echo ""
echo "1. Model Management (if you have models):"
echo "   ./tools/swarm-dna/gguf_parser.py ~/.ollama/models/blob/ metadata.yaml"
echo "   ./tools/swarm-dna/model_lineage.py metadata.yaml lineage.yaml --dot lineage.dot"
echo ""
echo "2. IDE Integration:"
echo "   ./tools/swarm-dna/blob_project_generator.py ~/.ollama/models/blob/"
echo "   code ~/.ollama/models/blob/  # Open in VS Code"
echo ""
echo "3. Deploy:"
echo "   docker-compose -f $DEMO_OUTPUT/docker-compose.swarm.yml up -d"
echo "   kubectl apply -f $DEMO_OUTPUT/kubernetes-swarm.yaml"
echo ""
echo "4. Full Pipeline:"
echo "   ./tools/swarm-dna/swarm_cli.py full-pipeline ~/.ollama/models/blob/ \\"
echo "       --swarm-dna SWARM_DNA.yaml -o swarm-output/"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔥 Lore → Reality transformation demonstrated."
echo "   This is Dom's architecture made manifest."
echo ""
echo "📚 Read more: SWARM_DNA_GUIDE.md"
echo "🛠️  Tool docs: tools/swarm-dna/README.md"
echo ""
echo "Built with 🔥 by the Strategickhaos Swarm Intelligence collective"
echo ""
