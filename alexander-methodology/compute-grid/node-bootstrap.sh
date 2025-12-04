#!/bin/bash

# Alexander Compute Grid - Node Bootstrap Script
# Initializes a compute node for distributed research

NODE_ID="$1"

if [ -z "$NODE_ID" ]; then
    echo "Error: NODE_ID required"
    exit 1
fi

GRID_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NODES_DIR="$GRID_DIR/nodes"

mkdir -p "$NODES_DIR"

echo "🔗 Bootstrapping compute node: $NODE_ID"

# Create node registry entry
cat > "$NODES_DIR/$NODE_ID.yaml" <<EOF
node_id: $NODE_ID
registered: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
status: active
compute_contribution: enabled
resource_limits:
  cpu_cores_max: auto
  memory_max: auto
  gpu_enabled: auto
heartbeat_interval: 30
last_heartbeat: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
tasks_completed: 0
compute_credits: 0
EOF

# Add to registry
echo "$NODE_ID" >> "$NODES_DIR/registry.txt"

echo "✓ Node registered in compute grid"
echo "✓ Ready to receive compute tasks"
echo ""
echo "Node configuration: $NODES_DIR/$NODE_ID.yaml"
