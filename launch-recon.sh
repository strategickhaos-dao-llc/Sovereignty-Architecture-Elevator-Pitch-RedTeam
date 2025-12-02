#!/bin/bash
# launch-recon.sh - One-click RECON Stack deployment
# Strategic Khaos Windows-optimized RAG system

set -euo pipefail

RECON_DIR="/workspaces/Sovereignty-Architecture-Elevator-Pitch-"
COMPOSE_FILE="docker-compose-recon.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

log() { echo -e "${BLUE}[$(date +%H:%M:%S)]${NC} $*"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; }

banner() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                           🎯 RECON STACK v2                                 ║"
    echo "║                     Windows-Optimized RAG Deployment                        ║"  
    echo "║                      Strategic Khaos Sovereignty                            ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Efficient health check with exponential backoff
wait_for_services() {
    local max_attempts=30
    local attempt=0
    local sleep_time=2
    
    log "Checking service health..."
    
    while [ $attempt -lt $max_attempts ]; do
        local all_healthy=true
        
        # Check Qdrant
        if ! curl -sf http://localhost:6333/healthz >/dev/null 2>&1; then
            all_healthy=false
        fi
        
        # Check Embedder
        if ! curl -sf http://localhost:8081/health >/dev/null 2>&1; then
            all_healthy=false
        fi
        
        # Check RAG API
        if ! curl -sf http://localhost:7000/health >/dev/null 2>&1; then
            all_healthy=false
        fi
        
        if [ "$all_healthy" = true ]; then
            success "All services are healthy!"
            return 0
        fi
        
        attempt=$((attempt + 1))
        log "Services not ready yet (attempt $attempt/$max_attempts), waiting ${sleep_time}s..."
        sleep $sleep_time
        
        # Exponential backoff up to 8 seconds
        if [ $sleep_time -lt 8 ]; then
            sleep_time=$((sleep_time * 2))
        fi
    done
    
    warn "Services took longer than expected to become healthy"
    return 1
}

# Test the RAG system with sample queries
test_rag_system() {
    log "🧪 Testing RAG system with Strategic Khaos queries..."
    
    local test_queries=(
        "What is the contradiction engine and how does it work?"
        "Explain the Docker Compose architecture"
        "How is the Discord bot integrated?"
        "Where are the revenue streams defined?"
        "What is the mastery drill framework?"
    )
    
    for query in "${test_queries[@]}"; do
        log "   Testing: $query"
        
        local response=$(curl -s -X POST http://localhost:7000/query \
            -H "Content-Type: application/json" \
            -d "{\"q\": \"$query\", \"k\": 3, \"include_llm\": false}" \
            2>/dev/null)
        
        if echo "$response" | jq -e '.contexts | length > 0' >/dev/null 2>&1; then
            local num_contexts=$(echo "$response" | jq -r '.contexts | length')
            success "   ✓ Found $num_contexts relevant contexts"
            
            # Show top result
            local top_file=$(echo "$response" | jq -r '.contexts[0].path')
            local top_score=$(echo "$response" | jq -r '.contexts[0].score')
            log "     Top match: $top_file (score: $top_score)"
        else
            warn "   ⚠ No contexts found for this query"
        fi
        
        # Small delay only if needed to avoid rate limiting
        sleep 0.5
    done
    
    success "RAG system testing completed"
}

# Show comprehensive status dashboard
show_status() {
    log "📊 RECON Stack Status Dashboard"
    echo ""
    
    echo -e "${GREEN}🌐 Service Endpoints:${NC}"
    echo "  RAG API:           http://localhost:7000"
    echo "  API Documentation: http://localhost:7000/docs"
    echo "  Vector Database:   http://localhost:6333/dashboard"
    echo "  Embedder Health:   http://localhost:8081/health"
    echo "  Metrics:           http://localhost:9100/metrics"
    echo ""
    
    echo -e "${GREEN}🔧 Docker Services:${NC}"
    docker compose -f "$COMPOSE_FILE" ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
    echo ""
    
    # Check actual service health
    echo -e "${GREEN}💚 Health Checks:${NC}"
    
    # Qdrant health
    if curl -s http://localhost:6333/healthz | jq -e '.status == "ok"' >/dev/null 2>&1; then
        success "  ✓ Qdrant Vector DB: Healthy"
    else
        warn "  ⚠ Qdrant Vector DB: Not responding"
    fi
    
    # Embedder health
    if curl -s http://localhost:8081/health >/dev/null 2>&1; then
        success "  ✓ Embedder Service: Healthy"
    else
        warn "  ⚠ Embedder Service: Not responding"
    fi
    
    # RAG API health
    if curl -s http://localhost:7000/health | jq -e '.status' >/dev/null 2>&1; then
        success "  ✓ RAG API: Healthy"
        
        # Show collection info
        local collections=$(curl -s http://localhost:7000/collections 2>/dev/null)
        if [ "$collections" ]; then
            echo -e "${GREEN}📚 Collections:${NC}"
            echo "$collections" | jq -r '.collections[] | "  - \(.name): \(.vectors_count) vectors"'
        fi
    else
        warn "  ⚠ RAG API: Not responding"
    fi
    
    echo ""
    
    echo -e "${GREEN}📝 Example Usage:${NC}"
    echo "  # Query the repository"
    echo '  curl -X POST http://localhost:7000/query \'
    echo '    -H "Content-Type: application/json" \'
    echo '    -d "{\"q\": \"How does the contradiction engine work?\", \"k\": 5}"'
    echo ""
    
    echo "  # Query with LLM response"
    echo '  curl -X POST http://localhost:7000/query \'
    echo '    -H "Content-Type: application/json" \'
    echo '    -d "{\"q\": \"Explain the Discord integration\", \"include_llm\": true}"'
    echo ""
    
    echo "  # Search specific paths"
    echo '  curl -X POST http://localhost:7000/query \'
    echo '    -H "Content-Type: application/json" \'
    echo '    -d "{\"q\": \"revenue streams\", \"path_prefix\": \"contradictions/\"}"'
    echo ""
    
    success "🎉 RECON Stack v2 is ready for Strategic Khaos operations!"
}

# Main function - simple deployment
main() {
    banner
    
    case "${1:-start}" in
        "start")
            log "🚀 Starting RECON Stack v2..."
            
            # Check prerequisites
            if ! command -v docker &> /dev/null || ! docker ps &> /dev/null; then
                error "Docker is not running. Please start Docker Desktop."
                exit 1
            fi
            
            # Prepare repository for indexing
            log "📂 Preparing repository for indexing..."
            mkdir -p recon/repos
            if [ ! -d "recon/repos/sovereignty-arch" ]; then
                cp -r . recon/repos/sovereignty-arch/
                # Clean up unnecessary files for faster indexing
                rm -rf recon/repos/sovereignty-arch/.git
                rm -rf recon/repos/sovereignty-arch/data
                rm -rf recon/repos/sovereignty-arch/node_modules 2>/dev/null || true
            fi
            
            # Start services
            log "🏗️ Starting RECON services..."
            docker compose -f "$COMPOSE_FILE" up -d
            
            # Efficient health check with timeout instead of fixed sleep
            log "⏳ Waiting for services to be healthy..."
            wait_for_services
            
            # Test the system
            test_rag_system
            
            # Show status
            show_status
            ;;
        "stop")
            log "🛑 Stopping RECON Stack..."
            docker compose -f "$COMPOSE_FILE" down
            success "RECON Stack stopped"
            ;;
        "status")
            show_status
            ;;
        "test")
            test_rag_system
            ;;
        "logs")
            docker compose -f "$COMPOSE_FILE" logs -f "${2:-}"
            ;;
        *)
            echo "Usage: $0 [start|stop|status|test|logs [service]]"
            echo ""
            echo "Strategic Khaos RECON Stack v2 - RAG-powered repository intelligence"
            echo ""
            echo "Commands:"
            echo "  start   - Deploy complete RECON Stack"
            echo "  stop    - Stop all RECON services"  
            echo "  status  - Show detailed status"
            echo "  test    - Test RAG queries"
            echo "  logs    - View service logs"
            ;;
    esac
}

main "$@"