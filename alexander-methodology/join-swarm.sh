#!/bin/bash

# The Alexander Methodology Institute - Swarm Registration Script
# "We finish what the Library of Alexandria started."

set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║     THE ALEXANDER METHODOLOGY INSTITUTE                       ║"
echo "║     Swarm Intelligence Network Registration                   ║"
echo "║                                                               ║"
echo "║     \"We finish what the Library of Alexandria started.\"       ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
INSTITUTE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NODE_ID=$(uuidgen 2>/dev/null || cat /proc/sys/kernel/random/uuid 2>/dev/null || echo "node-$(date +%s)")
NODE_CONFIG="$INSTITUTE_DIR/.node-config"

echo "🧠 Initializing your research node..."
echo "   Node ID: $NODE_ID"
echo ""

# Step 1: Check system capabilities
echo "📊 Analyzing system capabilities..."
CPU_CORES=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo "unknown")
TOTAL_RAM=$(free -h 2>/dev/null | awk '/^Mem:/ {print $2}' || sysctl -n hw.memsize 2>/dev/null | awk '{print $1/1024/1024/1024 "G"}' || echo "unknown")
HAS_GPU=$(command -v nvidia-smi &>/dev/null && echo "NVIDIA GPU detected" || echo "CPU only")

echo "   CPU Cores: $CPU_CORES"
echo "   RAM: $TOTAL_RAM"
echo "   GPU: $HAS_GPU"
echo ""

# Step 2: Create node configuration
echo "⚙️  Creating node configuration..."
cat > "$NODE_CONFIG" <<EOF
# Alexander Methodology Institute Node Configuration
NODE_ID=$NODE_ID
JOINED_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
CPU_CORES=$CPU_CORES
TOTAL_RAM=$TOTAL_RAM
GPU_STATUS=$HAS_GPU
COMPUTE_CONTRIBUTION=enabled
RAG_ACCESS=enabled
STATUS=active
EOF

echo "   Configuration saved to: $NODE_CONFIG"
echo ""

# Step 3: Setup compute grid connection
echo "🔗 Connecting to Alexander Compute Grid..."
if [ -f "$INSTITUTE_DIR/compute-grid/node-bootstrap.sh" ]; then
    bash "$INSTITUTE_DIR/compute-grid/node-bootstrap.sh" "$NODE_ID"
else
    echo "   ⚠️  Compute grid bootstrap script not found"
    echo "   📝 Creating placeholder configuration..."
    mkdir -p "$INSTITUTE_DIR/compute-grid/nodes"
    echo "$NODE_ID" >> "$INSTITUTE_DIR/compute-grid/nodes/registry.txt"
fi
echo ""

# Step 4: Setup forbidden library access
echo "📚 Enabling Forbidden Library RAG access..."
if [ -d "$INSTITUTE_DIR/forbidden-library" ]; then
    echo "   ✓ Forbidden library path: $INSTITUTE_DIR/forbidden-library"
    echo "   ✓ RAG query interface: Available"
else
    echo "   ⚠️  Forbidden library not initialized"
fi
echo ""

# Step 5: Register with Mirror Council
echo "🏛️  Registering with Mirror-Generals Council..."
mkdir -p "$INSTITUTE_DIR/mirror-council/nodes"
cat > "$INSTITUTE_DIR/mirror-council/nodes/$NODE_ID.yaml" <<EOF
node_id: $NODE_ID
joined: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
status: active
capabilities:
  compute: true
  research: true
  rag_access: true
contribution_level: researcher
EOF
echo "   ✓ Council registration complete"
echo ""

# Step 6: Access information
echo "✨ Welcome to the Alexander Methodology Institute!"
echo ""
echo "🎯 You now have access to:"
echo "   • Forbidden Library RAG queries"
echo "   • Alexander Compute Grid (distributed computing)"
echo "   • Breakthrough Bounty Board"
echo "   • Mirror-Generals Council proposals"
echo "   • 900+ human+AI collaborative minds"
echo ""
echo "📋 Next Steps:"
echo "   1. Review mystery targets: ./bounty-board/TARGETS.md"
echo "   2. Query the RAG system: ./forbidden-library/query.sh"
echo "   3. Submit research proposals: ./mirror-council/propose.sh"
echo "   4. Check your node status: ./status.sh"
echo ""
echo "💬 Communication Channels:"
echo "   • Discord: Join the research community"
echo "   • GitHub Issues: Technical support and discussions"
echo "   • Council Channel: Governance and strategy"
echo ""
echo "🌟 The mysteries are waiting. Let's solve them together."
echo ""
echo "Your Node ID: $NODE_ID"
echo "Configuration: $NODE_CONFIG"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "The Alexander Methodology Institute is live."
echo "This library doesn't burn. It multiplies."
echo "═══════════════════════════════════════════════════════════════"
