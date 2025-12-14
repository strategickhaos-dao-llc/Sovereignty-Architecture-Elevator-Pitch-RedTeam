#!/usr/bin/env bash
# Claude Context Sync Management Script
# Manages the Claude context synchronization daemon

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose-recon.yml"
SERVICE_NAME="claude-sync"
CONTAINER_NAME="recon-claude-sync"

# Helper functions
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

check_prerequisites() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker not found. Please install Docker."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose not found. Please install Docker Compose."
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

check_session_key() {
    if [ -z "${CLAUDE_SESSION_KEY:-}" ]; then
        print_error "CLAUDE_SESSION_KEY environment variable not set"
        echo ""
        echo "To extract your session key:"
        echo "1. Log into https://claude.ai in your browser"
        echo "2. Open DevTools (F12)"
        echo "3. Go to Application → Cookies → https://claude.ai"
        echo "4. Find cookie starting with 'sk-ant-sid01-'"
        echo "5. Copy the entire value"
        echo ""
        echo "Then set it:"
        echo "  export CLAUDE_SESSION_KEY=\"sk-ant-sid01-YOUR-KEY-HERE\""
        echo ""
        exit 1
    fi
    
    # Validate session key format
    if [[ ! $CLAUDE_SESSION_KEY =~ ^sk-ant-sid01- ]]; then
        print_warning "Session key format may be invalid (should start with 'sk-ant-sid01-')"
    else
        print_success "Session key format validated"
    fi
}

cmd_start() {
    print_info "Starting Claude Context Sync daemon..."
    
    check_prerequisites
    check_session_key
    
    # Start the full RECON stack with Claude sync profile
    docker-compose -f "$COMPOSE_FILE" --profile claude-sync up -d
    
    print_success "Claude Context Sync daemon started"
    print_info "View logs with: ./claude-sync.sh logs"
}

cmd_stop() {
    print_info "Stopping Claude Context Sync daemon..."
    
    docker-compose -f "$COMPOSE_FILE" stop "$SERVICE_NAME"
    
    print_success "Claude Context Sync daemon stopped"
}

cmd_restart() {
    print_info "Restarting Claude Context Sync daemon..."
    
    check_session_key
    
    docker-compose -f "$COMPOSE_FILE" restart "$SERVICE_NAME"
    
    print_success "Claude Context Sync daemon restarted"
}

cmd_logs() {
    print_info "Showing logs (Ctrl+C to exit)..."
    
    docker logs -f "$CONTAINER_NAME"
}

cmd_status() {
    print_info "Checking service status..."
    echo ""
    
    # Check if container is running
    if docker ps --filter "name=$CONTAINER_NAME" --format "{{.Names}}" | grep -q "$CONTAINER_NAME"; then
        print_success "Container: Running"
        
        # Get container stats
        docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" "$CONTAINER_NAME"
        
        echo ""
        
        # Check Qdrant collection
        print_info "Checking Qdrant collection..."
        if curl -s http://localhost:6333/collections/claude-context > /dev/null 2>&1; then
            collection_info=$(curl -s http://localhost:6333/collections/claude-context)
            vectors_count=$(echo "$collection_info" | grep -o '"vectors_count":[0-9]*' | grep -o '[0-9]*')
            print_success "Vector database: $vectors_count contexts stored"
        else
            print_warning "Vector database: Not accessible"
        fi
    else
        print_error "Container: Not running"
        print_info "Start with: ./claude-sync.sh start"
    fi
}

cmd_shell() {
    print_info "Opening shell in container..."
    
    if ! docker ps --filter "name=$CONTAINER_NAME" --format "{{.Names}}" | grep -q "$CONTAINER_NAME"; then
        print_error "Container is not running"
        exit 1
    fi
    
    docker exec -it "$CONTAINER_NAME" /bin/bash
}

cmd_test() {
    print_info "Testing Claude Context Sync..."
    echo ""
    
    check_session_key
    
    # Detect Docker network name
    NETWORK_NAME=$(docker network ls --filter "name=reconnet" --format "{{.Name}}" | head -1)
    if [ -z "$NETWORK_NAME" ]; then
        print_warning "Docker network not found, using default"
        NETWORK_NAME="bridge"
    fi
    
    # Test session key validity
    print_info "Testing session key..."
    
    test_result=$(docker run --rm \
        --network "$NETWORK_NAME" \
        -e CLAUDE_SESSION_KEY="$CLAUDE_SESSION_KEY" \
        -e CLAUDE_ORG_ID="${CLAUDE_ORG_ID:-17fcb197-98f1-4c44-9ed8-bc89b419cbbf}" \
        python:3.11-slim \
        /bin/bash -c "
        pip install -q httpx && \
        python -c \"
import httpx
import os
import asyncio

async def test():
    headers = {
        'Cookie': f'sessionKey={os.getenv(\"CLAUDE_SESSION_KEY\")}',
        'User-Agent': 'Mozilla/5.0'
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f'https://claude.ai/api/organizations/{os.getenv(\"CLAUDE_ORG_ID\")}/recents',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print('✓ Session key valid')
                exit(0)
            elif response.status_code == 403:
                print('✗ Session key invalid or expired')
                exit(1)
            else:
                print(f'? Unexpected status: {response.status_code}')
                exit(1)
        except Exception as e:
            print(f'✗ Error: {e}')
            exit(1)

asyncio.run(test())
\"
        " 2>&1) || true
    
    echo "$test_result"
    
    if echo "$test_result" | grep -q "✓"; then
        print_success "Session key test passed"
    else
        print_error "Session key test failed"
        echo ""
        print_info "Your session key may be expired. Extract a fresh one from browser cookies."
        exit 1
    fi
}

cmd_query() {
    local query="${1:-What did I discuss recently?}"
    
    print_info "Querying Claude contexts..."
    echo ""
    
    # Query via RAG API
    response=$(curl -s -X POST http://localhost:7000/query \
        -H "Content-Type: application/json" \
        -d "{
            \"q\": \"$query\",
            \"collection\": \"claude-context\",
            \"k\": 5,
            \"include_llm\": false
        }")
    
    if [ $? -eq 0 ]; then
        echo "$response" | python3 -m json.tool
        print_success "Query completed"
    else
        print_error "Query failed - is RAG API running?"
        exit 1
    fi
}

cmd_stats() {
    print_info "Retrieving sync statistics..."
    echo ""
    
    # Get collection stats from Qdrant
    if curl -s http://localhost:6333/collections/claude-context > /dev/null 2>&1; then
        collection_info=$(curl -s http://localhost:6333/collections/claude-context)
        
        echo "Collection: claude-context"
        echo "$collection_info" | python3 -c "
import sys
import json

data = json.load(sys.stdin)
result = data.get('result', {})

print(f\"  Vectors: {result.get('vectors_count', 0):,}\")
print(f\"  Status: {result.get('status', 'unknown')}\")

config = result.get('config', {})
vectors_config = config.get('params', {}).get('vectors', {})
print(f\"  Dimension: {vectors_config.get('size', 'unknown')}\")
print(f\"  Distance: {vectors_config.get('distance', 'unknown')}\")
"
    else
        print_error "Cannot connect to Qdrant"
        exit 1
    fi
    
    # Get recent logs for metrics
    echo ""
    print_info "Recent sync activity:"
    docker logs "$CONTAINER_NAME" 2>&1 | grep -E "Cycle|complete|contexts" | tail -10
}

cmd_clean() {
    print_warning "This will remove the Claude context collection and all stored contexts"
    read -p "Are you sure? (yes/no): " confirm
    
    if [ "$confirm" != "yes" ]; then
        print_info "Cancelled"
        exit 0
    fi
    
    print_info "Removing collection..."
    
    curl -X DELETE http://localhost:6333/collections/claude-context
    
    print_success "Collection removed"
}

cmd_help() {
    cat << EOF
Claude Context Sync Management Script

Usage: ./claude-sync.sh [command]

Commands:
  start       Start the Claude Context Sync daemon
  stop        Stop the daemon
  restart     Restart the daemon
  logs        View live logs from the daemon
  status      Show daemon status and stats
  shell       Open bash shell in container
  test        Test session key validity
  query       Query synced contexts (usage: query "your question")
  stats       Show sync statistics
  clean       Remove all synced contexts
  help        Show this help message

Environment Variables:
  CLAUDE_SESSION_KEY       Your Claude session key (required)
  CLAUDE_ORG_ID           Your Claude org ID (optional)
  CLAUDE_POLL_INTERVAL    Sync interval in seconds (default: 300)
  CLAUDE_MAX_HISTORY_DAYS Max history to sync (default: 7)

Examples:
  # Start daemon
  export CLAUDE_SESSION_KEY="sk-ant-sid01-..."
  ./claude-sync.sh start

  # View logs
  ./claude-sync.sh logs

  # Query contexts
  ./claude-sync.sh query "What did I ask about Python?"

  # Check status
  ./claude-sync.sh status

Documentation: See CLAUDE_CONTEXT_SYNC.md

EOF
}

# Main command dispatcher
main() {
    case "${1:-help}" in
        start)
            cmd_start
            ;;
        stop)
            cmd_stop
            ;;
        restart)
            cmd_restart
            ;;
        logs)
            cmd_logs
            ;;
        status)
            cmd_status
            ;;
        shell)
            cmd_shell
            ;;
        test)
            cmd_test
            ;;
        query)
            shift
            cmd_query "$@"
            ;;
        stats)
            cmd_stats
            ;;
        clean)
            cmd_clean
            ;;
        help|--help|-h)
            cmd_help
            ;;
        *)
            print_error "Unknown command: $1"
            echo ""
            cmd_help
            exit 1
            ;;
    esac
}

main "$@"
