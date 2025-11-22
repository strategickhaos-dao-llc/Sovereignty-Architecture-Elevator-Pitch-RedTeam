#!/bin/bash
# deploy-alexandria.sh - Alexandria Resurrected deployment script
# Deploys the sovereign research data library with RAG interface

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ALEXANDRIA_VERSION="1.0.0"
DATA_PATH="${ALEXANDRIA_DATA_PATH:-/data/alexandria}"
MIN_STORAGE_TB=32
MIN_RAM_GB=128

echo -e "${BLUE}╔═══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Alexandria Resurrected Deployment      ║${NC}"
echo -e "${BLUE}║   Version ${ALEXANDRIA_VERSION}                       ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════╝${NC}"
echo ""

# Function to check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}[1/7] Checking prerequisites...${NC}"
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Error: Docker is not installed${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Docker found: $(docker --version | cut -d' ' -f3)${NC}"
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}Error: Docker Compose is not installed${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Docker Compose found: $(docker-compose --version | cut -d' ' -f4)${NC}"
    
    # Check Tailscale (optional but recommended)
    if command -v tailscale &> /dev/null; then
        echo -e "${GREEN}✓ Tailscale found: $(tailscale --version | head -n1)${NC}"
    else
        echo -e "${YELLOW}⚠ Tailscale not found (recommended for secure access)${NC}"
    fi
    
    # Check available storage
    AVAILABLE_STORAGE_GB=$(df -BG "$DATA_PATH" 2>/dev/null | awk 'NR==2 {print $4}' | sed 's/G//' || echo "0")
    REQUIRED_STORAGE_GB=$((MIN_STORAGE_TB * 1024))
    
    if [ "$AVAILABLE_STORAGE_GB" -lt "$REQUIRED_STORAGE_GB" ]; then
        echo -e "${RED}Error: Insufficient storage. Need ${REQUIRED_STORAGE_GB}GB, have ${AVAILABLE_STORAGE_GB}GB${NC}"
        echo -e "${YELLOW}Consider setting ALEXANDRIA_DATA_PATH to a location with more space${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Storage check passed: ${AVAILABLE_STORAGE_GB}GB available${NC}"
    
    # Check available RAM
    AVAILABLE_RAM_GB=$(free -g | awk 'NR==2 {print $2}')
    if [ "$AVAILABLE_RAM_GB" -lt "$MIN_RAM_GB" ]; then
        echo -e "${YELLOW}⚠ Warning: Low RAM. Recommended ${MIN_RAM_GB}GB, have ${AVAILABLE_RAM_GB}GB${NC}"
        echo -e "${YELLOW}  Performance may be degraded${NC}"
    else
        echo -e "${GREEN}✓ RAM check passed: ${AVAILABLE_RAM_GB}GB available${NC}"
    fi
    
    echo ""
}

# Function to create directory structure
create_directories() {
    echo -e "${YELLOW}[2/7] Creating directory structure...${NC}"
    
    # Main data directories (5 wings)
    mkdir -p "$DATA_PATH/medical"
    mkdir -p "$DATA_PATH/physics_chemistry"
    mkdir -p "$DATA_PATH/biology_genomics"
    mkdir -p "$DATA_PATH/forbidden_knowledge"
    mkdir -p "$DATA_PATH/tinker_labs"
    
    # Configuration and logs
    mkdir -p ./config
    mkdir -p ./logs
    mkdir -p ./models
    mkdir -p ./monitoring
    
    # Ingestor and retriever directories
    mkdir -p ./ingest
    mkdir -p ./retriever
    
    echo -e "${GREEN}✓ Directory structure created${NC}"
    echo ""
}

# Function to generate configuration files
generate_configs() {
    echo -e "${YELLOW}[3/7] Generating configuration files...${NC}"
    
    # Generate .env file if it doesn't exist
    if [ ! -f .env.alexandria ]; then
        cat > .env.alexandria <<EOF
# Alexandria Resurrected Configuration
ALEXANDRIA_DATA_PATH=$DATA_PATH
WEBUI_SECRET_KEY=$(openssl rand -hex 32)
LOG_ENCRYPTION_KEY=$(openssl rand -hex 32)

# Network configuration
TAILSCALE_HOSTNAME=alexandria
EXTERNAL_PORT=3000

# Performance tuning
QDRANT_CACHE_SIZE=16G
EMBEDDER_BATCH_SIZE=32
LLM_CONTEXT_SIZE=128000

# Security
ENABLE_SIGNUP=false
ENABLE_ANONYMOUS_ACCESS=false
REQUIRE_OATH=true

# Logging
LOG_RETENTION_DAYS=365
ENCRYPT_QUERY_LOGS=true
EOF
        echo -e "${GREEN}✓ Generated .env.alexandria${NC}"
    else
        echo -e "${BLUE}ℹ .env.alexandria already exists, skipping${NC}"
    fi
    
    # Generate Qdrant config
    cat > ./config/qdrant-config.yaml <<EOF
service:
  http_port: 6333
  grpc_port: 6334
  host: 0.0.0.0
  
storage:
  storage_path: /qdrant/storage
  snapshots_path: /qdrant/snapshots
  on_disk_payload: true
  
cluster:
  enabled: false

log_level: INFO
EOF
    echo -e "${GREEN}✓ Generated Qdrant configuration${NC}"
    
    # Generate Prometheus config
    cat > ./monitoring/prometheus.yml <<EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'alexandria-qdrant'
    static_configs:
      - targets: ['qdrant:6333']
  
  - job_name: 'alexandria-webui'
    static_configs:
      - targets: ['open-webui:8080']
  
  - job_name: 'alexandria-retriever'
    static_configs:
      - targets: ['retriever:7000']
EOF
    echo -e "${GREEN}✓ Generated Prometheus configuration${NC}"
    
    echo ""
}

# Function to download models
download_models() {
    echo -e "${YELLOW}[4/7] Checking language models...${NC}"
    
    # Check if embedding model exists
    if [ ! -f ./models/bge-large-en-v1.5.gguf ]; then
        echo -e "${BLUE}Downloading BGE-large embedding model (this may take a while)...${NC}"
        # Using Hugging Face model
        echo -e "${YELLOW}Please download manually from: https://huggingface.co/BAAI/bge-large-en-v1.5${NC}"
        echo -e "${YELLOW}Place the model in: ./models/bge-large-en-v1.5.gguf${NC}"
    else
        echo -e "${GREEN}✓ Embedding model found${NC}"
    fi
    
    # Check if LLM model exists
    if [ ! -f ./models/llama-3-70b-q4.gguf ]; then
        echo -e "${BLUE}LLM model not found${NC}"
        echo -e "${YELLOW}Please download a quantized model from: https://huggingface.co/TheBloke${NC}"
        echo -e "${YELLOW}Recommended: Llama-3-70B-Instruct-GGUF (Q4_K_M)${NC}"
        echo -e "${YELLOW}Place the model in: ./models/llama-3-70b-q4.gguf${NC}"
    else
        echo -e "${GREEN}✓ LLM model found${NC}"
    fi
    
    echo ""
}

# Function to build containers
build_containers() {
    echo -e "${YELLOW}[5/7] Building containers...${NC}"
    
    docker-compose -f docker-compose-alexandria.yml build --parallel
    
    echo -e "${GREEN}✓ Containers built successfully${NC}"
    echo ""
}

# Function to start services
start_services() {
    echo -e "${YELLOW}[6/7] Starting Alexandria services...${NC}"
    
    # Start core services first
    docker-compose -f docker-compose-alexandria.yml up -d qdrant embedder
    echo -e "${BLUE}Waiting for vector database to initialize...${NC}"
    sleep 10
    
    # Start LLM server
    docker-compose -f docker-compose-alexandria.yml up -d llm-server
    echo -e "${BLUE}Waiting for LLM server to load model...${NC}"
    sleep 30
    
    # Start remaining services
    docker-compose -f docker-compose-alexandria.yml up -d
    
    echo -e "${GREEN}✓ All services started${NC}"
    echo ""
}

# Function to verify deployment
verify_deployment() {
    echo -e "${YELLOW}[7/7] Verifying deployment...${NC}"
    
    # Wait for services to be ready
    sleep 5
    
    # Check Qdrant
    if curl -sf http://localhost:6333/healthz > /dev/null; then
        echo -e "${GREEN}✓ Qdrant vector database: healthy${NC}"
    else
        echo -e "${RED}✗ Qdrant vector database: unhealthy${NC}"
    fi
    
    # Check embedder
    if curl -sf http://localhost:8081/health > /dev/null; then
        echo -e "${GREEN}✓ Embedding service: healthy${NC}"
    else
        echo -e "${RED}✗ Embedding service: unhealthy${NC}"
    fi
    
    # Check LLM server
    if curl -sf http://localhost:8080/health > /dev/null; then
        echo -e "${GREEN}✓ LLM server: healthy${NC}"
    else
        echo -e "${RED}✗ LLM server: unhealthy${NC}"
    fi
    
    # Check Open WebUI
    if curl -sf http://localhost:3000/health > /dev/null; then
        echo -e "${GREEN}✓ Open WebUI: healthy${NC}"
    else
        echo -e "${RED}✗ Open WebUI: unhealthy${NC}"
    fi
    
    # Check RAG API
    if curl -sf http://localhost:7000/health > /dev/null; then
        echo -e "${GREEN}✓ RAG API: healthy${NC}"
    else
        echo -e "${RED}✗ RAG API: unhealthy${NC}"
    fi
    
    echo ""
}

# Function to display access information
display_access_info() {
    echo -e "${BLUE}╔═══════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║     Deployment Complete!                  ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}Alexandria Resurrected is now running!${NC}"
    echo ""
    echo -e "${YELLOW}Access Points:${NC}"
    echo -e "  • Open WebUI:    ${BLUE}http://localhost:3000${NC}"
    echo -e "  • RAG API:       ${BLUE}http://localhost:7000${NC}"
    echo -e "  • Qdrant UI:     ${BLUE}http://localhost:6333/dashboard${NC}"
    echo -e "  • Prometheus:    ${BLUE}http://localhost:9090${NC}"
    echo ""
    echo -e "${YELLOW}Next Steps:${NC}"
    echo "  1. Index your data wings:"
    echo -e "     ${BLUE}./scripts/index-wings.sh${NC}"
    echo ""
    echo "  2. Create researcher invites:"
    echo -e "     ${BLUE}./scripts/create-researcher-invite.sh researcher@email.com${NC}"
    echo ""
    echo "  3. Monitor system health:"
    echo -e "     ${BLUE}docker-compose -f docker-compose-alexandria.yml logs -f${NC}"
    echo ""
    echo -e "${YELLOW}Documentation:${NC}"
    echo -e "  ${BLUE}./ALEXANDRIA_RESURRECTED.md${NC}"
    echo ""
    echo -e "${GREEN}The library is ready. Knowledge preserved. 📚${NC}"
    echo ""
}

# Main deployment flow
main() {
    check_prerequisites
    create_directories
    generate_configs
    download_models
    build_containers
    start_services
    verify_deployment
    display_access_info
}

# Run main function
main "$@"
