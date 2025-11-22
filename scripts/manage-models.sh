#!/bin/bash
# Strategickhaos Cluster Model Management Script
# Manages AI model pulling, sharing, and distribution across nodes

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Default models for the cluster
RECOMMENDED_MODELS=(
    "llama3.1:405b"
    "dolphin-llama3:70b"
    "mistral:latest"
    "codellama:latest"
    "everythinglm:13b"
)

show_banner() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   Strategickhaos Cluster Model Manager                    ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

check_ollama() {
    if ! docker ps | grep -q ollama; then
        echo -e "${RED}✗ Ollama container not running${NC}"
        echo -e "${YELLOW}Start it with: docker compose up -d${NC}"
        exit 1
    fi
}

list_models() {
    echo -e "${YELLOW}📋 Installed models on this node:${NC}"
    docker exec ollama ollama list
    echo ""
}

pull_model() {
    local model=$1
    echo -e "${BLUE}⬇️  Pulling model: $model${NC}"
    docker exec ollama ollama pull "$model"
    echo -e "${GREEN}✓ Model $model pulled successfully${NC}"
    echo ""
}

pull_recommended() {
    echo -e "${YELLOW}📦 Recommended models for Strategickhaos cluster:${NC}"
    for i in "${!RECOMMENDED_MODELS[@]}"; do
        echo "  $((i+1))) ${RECOMMENDED_MODELS[$i]}"
    done
    echo ""
    
    echo -e "${BLUE}Note: llama3.1:405b requires ~230GB disk space and 128GB+ RAM${NC}"
    read -p "Pull all recommended models? [y/N]: " confirm
    
    if [[ $confirm =~ ^[Yy]$ ]]; then
        for model in "${RECOMMENDED_MODELS[@]}"; do
            pull_model "$model"
        done
    else
        echo "Select models to pull (comma-separated numbers, e.g., 2,3,4):"
        read -p "Choice: " choices
        
        IFS=',' read -ra SELECTED <<< "$choices"
        for idx in "${SELECTED[@]}"; do
            idx=$((idx - 1))
            if [ $idx -ge 0 ] && [ $idx -lt ${#RECOMMENDED_MODELS[@]} ]; then
                pull_model "${RECOMMENDED_MODELS[$idx]}"
            fi
        done
    fi
}

delete_model() {
    echo -e "${YELLOW}🗑️  Available models:${NC}"
    docker exec ollama ollama list
    echo ""
    
    read -p "Enter model name to delete: " model
    read -p "Are you sure you want to delete $model? [y/N]: " confirm
    
    if [[ $confirm =~ ^[Yy]$ ]]; then
        docker exec ollama ollama rm "$model"
        echo -e "${GREEN}✓ Model $model deleted${NC}"
    else
        echo -e "${YELLOW}Cancelled${NC}"
    fi
}

setup_nfs_server() {
    echo -e "${YELLOW}🔧 Setting up NFS model sharing (Server)${NC}"
    
    # Install NFS server
    if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get update
        sudo apt-get install -y nfs-kernel-server
    elif command -v yum >/dev/null 2>&1; then
        sudo yum install -y nfs-utils
    else
        echo -e "${RED}✗ Unsupported package manager${NC}"
        exit 1
    fi
    
    # Get the Ollama volume path
    OLLAMA_PATH=$(docker volume inspect strategickhaos-cluster_ollama --format '{{.Mountpoint}}')
    
    if [ -z "$OLLAMA_PATH" ]; then
        echo -e "${RED}✗ Ollama volume not found${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}Ollama models path: $OLLAMA_PATH${NC}"
    
    # Export the volume
    if ! grep -q "$OLLAMA_PATH" /etc/exports; then
        echo "$OLLAMA_PATH *(ro,sync,no_subtree_check)" | sudo tee -a /etc/exports
        sudo exportfs -a
        sudo systemctl restart nfs-kernel-server
        echo -e "${GREEN}✓ NFS server configured${NC}"
    else
        echo -e "${GREEN}✓ NFS already configured${NC}"
    fi
    
    # Get Tailscale IP
    TAILSCALE_IP=$(tailscale ip -4)
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  NFS Server Ready                                          ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo -e "${BLUE}On other cluster nodes, run:${NC}"
    echo -e "${YELLOW}  ./manage-models.sh client $TAILSCALE_IP${NC}"
}

setup_nfs_client() {
    local server_ip=$1
    
    if [ -z "$server_ip" ]; then
        echo -e "${RED}✗ Server IP required${NC}"
        echo -e "${YELLOW}Usage: ./manage-models.sh client <server-tailscale-ip>${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}🔧 Setting up NFS model sharing (Client)${NC}"
    
    # Install NFS client
    if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get update
        sudo apt-get install -y nfs-common
    elif command -v yum >/dev/null 2>&1; then
        sudo yum install -y nfs-utils
    else
        echo -e "${RED}✗ Unsupported package manager${NC}"
        exit 1
    fi
    
    # Create mount point
    sudo mkdir -p /mnt/strategickhaos-models
    
    # Get server's Ollama path
    OLLAMA_PATH="/var/lib/docker/volumes/strategickhaos-cluster_ollama/_data"
    
    # Mount NFS share
    echo -e "${BLUE}Mounting NFS share from $server_ip...${NC}"
    sudo mount -t nfs "$server_ip:$OLLAMA_PATH" /mnt/strategickhaos-models
    
    # Make mount persistent
    if ! grep -q "strategickhaos-models" /etc/fstab; then
        echo "$server_ip:$OLLAMA_PATH /mnt/strategickhaos-models nfs ro,soft,intr 0 0" | \
            sudo tee -a /etc/fstab
    fi
    
    echo -e "${GREEN}✓ NFS client configured${NC}"
    echo -e "${YELLOW}Models available at: /mnt/strategickhaos-models${NC}"
}

check_cluster_models() {
    echo -e "${YELLOW}🔍 Checking models across cluster nodes...${NC}"
    echo ""
    
    NODES=("nitro-lyra" "athina-throne" "nova-warrior" "asteroth-gate")
    
    for node in "${NODES[@]}"; do
        echo -e "${BLUE}Checking $node...${NC}"
        if curl -s -m 2 "http://$node.tail-scale.ts.net:11434/api/tags" >/dev/null 2>&1; then
            curl -s "http://$node.tail-scale.ts.net:11434/api/tags" | jq -r '.models[].name' || echo "No models"
        else
            echo -e "${YELLOW}  (unreachable)${NC}"
        fi
        echo ""
    done
}

show_help() {
    cat << EOF
Strategickhaos Cluster Model Manager

Usage: ./manage-models.sh [command] [options]

Commands:
  list              List installed models on this node
  pull              Pull a specific model
  recommended       Pull recommended cluster models
  delete            Delete a model
  server            Setup NFS server for model sharing
  client <ip>       Setup NFS client to access shared models
  cluster           Check models across all cluster nodes
  help              Show this help message

Examples:
  ./manage-models.sh list
  ./manage-models.sh pull mistral:latest
  ./manage-models.sh recommended
  ./manage-models.sh server
  ./manage-models.sh client 100.64.0.1
  ./manage-models.sh cluster

Model Sizes:
  - llama3.1:405b    ~230 GB (requires 128GB+ RAM)
  - dolphin-llama3:70b  ~40 GB
  - mistral:latest   ~4.1 GB
  - codellama:latest ~3.8 GB
  - everythinglm:13b ~7.3 GB

EOF
}

# Main script logic
show_banner

case "${1:-help}" in
    list)
        check_ollama
        list_models
        ;;
    pull)
        check_ollama
        if [ -z "$2" ]; then
            read -p "Enter model name to pull: " model
        else
            model="$2"
        fi
        pull_model "$model"
        ;;
    recommended)
        check_ollama
        pull_recommended
        ;;
    delete)
        check_ollama
        delete_model
        ;;
    server)
        setup_nfs_server
        ;;
    client)
        setup_nfs_client "$2"
        ;;
    cluster)
        check_cluster_models
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
