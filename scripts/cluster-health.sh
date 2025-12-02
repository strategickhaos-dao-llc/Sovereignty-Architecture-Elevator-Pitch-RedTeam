#!/bin/bash
# Strategickhaos Cluster Health Monitor
# Real-time monitoring and diagnostics for all cluster nodes

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Cluster nodes
NODES=(
    "nitro-lyra:Primary Brain"
    "athina-throne:Training Beast"
    "nova-warrior:Voice Agent"
    "asteroth-gate:Security Gate"
)

check_node_health() {
    local node_name=$1
    local node_role=$2
    
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🖥️  Node: ${node_name}${NC} ${YELLOW}(${node_role})${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    # Check Tailscale connectivity
    echo -ne "${YELLOW}  Tailscale: ${NC}"
    if ping -c 1 -W 2 "$node_name.tail-scale.ts.net" >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Reachable${NC}"
    else
        echo -e "${RED}✗ Unreachable${NC}"
        echo ""
        return 1
    fi
    
    # Check Ollama service
    echo -ne "${YELLOW}  Ollama API: ${NC}"
    if curl -s -m 2 "http://$node_name.tail-scale.ts.net:11434/api/tags" >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Online${NC}"
        
        # Get model count
        model_count=$(curl -s "http://$node_name.tail-scale.ts.net:11434/api/tags" | jq -r '.models | length' 2>/dev/null || echo "0")
        echo -e "${YELLOW}  Models: ${NC}${model_count} loaded"
    else
        echo -e "${RED}✗ Offline${NC}"
    fi
    
    # Check Open-WebUI (if primary node)
    if [ "$node_name" = "nitro-lyra" ]; then
        echo -ne "${YELLOW}  Open-WebUI: ${NC}"
        if curl -s -m 2 "http://$node_name.tail-scale.ts.net:3000" >/dev/null 2>&1; then
            echo -e "${GREEN}✓ Online${NC}"
        else
            echo -e "${RED}✗ Offline${NC}"
        fi
    fi
    
    # Check Voice AI (if nova-warrior)
    if [ "$node_name" = "nova-warrior" ]; then
        echo -ne "${YELLOW}  Voice AI: ${NC}"
        if curl -s -m 2 "http://$node_name.tail-scale.ts.net:7850" >/dev/null 2>&1; then
            echo -e "${GREEN}✓ Online${NC}"
        else
            echo -e "${YELLOW}○ Not deployed${NC}"
        fi
    fi
    
    # Check Honeypot (if asteroth-gate)
    if [ "$node_name" = "asteroth-gate" ]; then
        echo -ne "${YELLOW}  Honeypot: ${NC}"
        if curl -s -m 2 "http://$node_name.tail-scale.ts.net:8080" >/dev/null 2>&1; then
            echo -e "${GREEN}✓ Online${NC}"
        else
            echo -e "${YELLOW}○ Not deployed${NC}"
        fi
    fi
    
    echo ""
}

show_cluster_overview() {
    clear
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   Strategickhaos 4-Node Cluster Health Dashboard          ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}$(date '+%Y-%m-%d %H:%M:%S')${NC}"
    echo ""
    
    for node_info in "${NODES[@]}"; do
        IFS=':' read -r node_name node_role <<< "$node_info"
        check_node_health "$node_name" "$node_role"
    done
}

show_model_distribution() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   Model Distribution Across Cluster                       ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    for node_info in "${NODES[@]}"; do
        IFS=':' read -r node_name node_role <<< "$node_info"
        
        echo -e "${CYAN}$node_name ($node_role):${NC}"
        if curl -s -m 2 "http://$node_name.tail-scale.ts.net:11434/api/tags" >/dev/null 2>&1; then
            models=$(curl -s "http://$node_name.tail-scale.ts.net:11434/api/tags" | jq -r '.models[]? | "  • \(.name) (\(.size / 1024 / 1024 / 1024 | round)GB)"' 2>/dev/null)
            if [ -z "$models" ]; then
                echo -e "${YELLOW}  No models loaded${NC}"
            else
                echo "$models"
            fi
        else
            echo -e "${RED}  Unreachable${NC}"
        fi
        echo ""
    done
}

test_inference() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   Testing Inference Across Nodes                          ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    read -p "Enter model name to test (e.g., mistral:latest): " model_name
    read -p "Enter test prompt: " prompt
    
    for node_info in "${NODES[@]}"; do
        IFS=':' read -r node_name node_role <<< "$node_info"
        
        echo -e "${CYAN}Testing on $node_name...${NC}"
        
        start_time=$(date +%s)
        response=$(curl -s -m 30 "http://$node_name.tail-scale.ts.net:11434/api/generate" \
            -d "{\"model\": \"$model_name\", \"prompt\": \"$prompt\", \"stream\": false}" 2>/dev/null)
        end_time=$(date +%s)
        
        if [ $? -eq 0 ] && [ -n "$response" ]; then
            duration=$((end_time - start_time))
            tokens=$(echo "$response" | jq -r '.eval_count' 2>/dev/null || echo "N/A")
            echo -e "${GREEN}  ✓ Success${NC} - ${duration}s, ${tokens} tokens"
        else
            echo -e "${RED}  ✗ Failed${NC}"
        fi
        echo ""
    done
}

show_resource_usage() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   Cluster Resource Usage                                  ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    echo -e "${YELLOW}Note: Remote resource monitoring requires SSH access${NC}"
    echo ""
    
    for node_info in "${NODES[@]}"; do
        IFS=':' read -r node_name node_role <<< "$node_info"
        
        echo -e "${CYAN}$node_name:${NC}"
        
        # Try to get Docker stats via SSH (requires passwordless SSH)
        if ssh -o ConnectTimeout=2 -o BatchMode=yes "$node_name.tail-scale.ts.net" "docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}'" 2>/dev/null; then
            :
        else
            echo -e "${YELLOW}  SSH access required for resource stats${NC}"
        fi
        echo ""
    done
}

continuous_monitor() {
    echo -e "${YELLOW}Starting continuous monitoring (Ctrl+C to stop)...${NC}"
    sleep 2
    
    while true; do
        show_cluster_overview
        sleep 10
    done
}

show_help() {
    cat << EOF
Strategickhaos Cluster Health Monitor

Usage: ./cluster-health.sh [command]

Commands:
  overview      Show cluster overview (default)
  models        Show model distribution across nodes
  test          Test inference on all nodes
  resources     Show resource usage (requires SSH)
  monitor       Continuous monitoring mode
  help          Show this help message

Examples:
  ./cluster-health.sh
  ./cluster-health.sh overview
  ./cluster-health.sh models
  ./cluster-health.sh test
  ./cluster-health.sh monitor

EOF
}

# Main script logic
case "${1:-overview}" in
    overview)
        show_cluster_overview
        ;;
    models)
        show_model_distribution
        ;;
    test)
        test_inference
        ;;
    resources)
        show_resource_usage
        ;;
    monitor)
        continuous_monitor
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}✗ Unknown command: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
