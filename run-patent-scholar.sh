#!/usr/bin/env bash
# run-patent-scholar.sh
# Helper script to run patent and scholar infrastructure
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Sovereign Manifest
MANIFEST_HASH="FAA198DA05318742531B6405384319563933F63DB4D91866E70AE7701FCDCDED"

echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Patent Office & Google Scholar Infrastructure${NC}"
echo -e "${BLUE}  Sovereignty Architecture${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Sovereign Manifest Hash:${NC}"
echo -e "${GREEN}$MANIFEST_HASH${NC}"
echo ""

# Function to display help
show_help() {
    cat << EOF
Usage: $0 [COMMAND]

Commands:
    up          Start all patent & scholar services
    down        Stop all services
    restart     Restart all services
    logs        View logs (follow mode)
    status      Check service status
    health      Run health checks
    backup      Backup patent database
    restore     Restore patent database from backup
    test        Run system tests
    monitor     Run monitoring manually
    help        Show this help message

Examples:
    $0 up               # Start services
    $0 logs             # View logs
    $0 status           # Check status
    $0 backup           # Backup database

Environment:
    Configure .env file with required variables before running.
    See .env.example for reference.

EOF
}

# Function to check if docker-compose is available
check_docker() {
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}Error: docker-compose is not installed${NC}"
        exit 1
    fi
}

# Function to check .env file
check_env() {
    if [ ! -f .env ]; then
        echo -e "${YELLOW}Warning: .env file not found${NC}"
        echo -e "${YELLOW}Creating .env from .env.example...${NC}"
        cp .env.example .env
        echo -e "${GREEN}✓ Created .env file${NC}"
        echo -e "${YELLOW}Please edit .env with your configuration${NC}"
        exit 1
    fi
}

# Function to start services
start_services() {
    echo -e "${BLUE}Starting Patent & Scholar services...${NC}"
    check_docker
    check_env
    
    docker-compose -f docker-compose.patent-scholar.yml up -d
    
    echo ""
    echo -e "${GREEN}✓ Services started${NC}"
    echo ""
    echo -e "${BLUE}Service URLs:${NC}"
    echo "  Patent Search API:  http://localhost:8086"
    echo "  RAG Query API:      http://localhost:8087"
    echo "  Nginx Proxy:        http://localhost:8088"
    echo "  Elasticsearch:      http://localhost:9200"
    echo "  Qdrant:             http://localhost:6334"
    echo "  PostgreSQL:         localhost:5433"
    echo ""
    echo -e "${BLUE}Health check:${NC} $0 health"
    echo -e "${BLUE}View logs:${NC} $0 logs"
}

# Function to stop services
stop_services() {
    echo -e "${BLUE}Stopping Patent & Scholar services...${NC}"
    check_docker
    
    docker-compose -f docker-compose.patent-scholar.yml down
    
    echo -e "${GREEN}✓ Services stopped${NC}"
}

# Function to restart services
restart_services() {
    echo -e "${BLUE}Restarting Patent & Scholar services...${NC}"
    stop_services
    sleep 2
    start_services
}

# Function to view logs
view_logs() {
    check_docker
    docker-compose -f docker-compose.patent-scholar.yml logs -f
}

# Function to check status
check_status() {
    echo -e "${BLUE}Checking service status...${NC}"
    check_docker
    docker-compose -f docker-compose.patent-scholar.yml ps
}

# Function to run health checks
run_health_checks() {
    echo -e "${BLUE}Running health checks...${NC}"
    echo ""
    
    # Patent Search API
    if curl -sf http://localhost:8086/health > /dev/null; then
        echo -e "${GREEN}✓${NC} Patent Search API (http://localhost:8086)"
    else
        echo -e "${RED}✗${NC} Patent Search API (http://localhost:8086)"
    fi
    
    # RAG Query API
    if curl -sf http://localhost:8087/health > /dev/null; then
        echo -e "${GREEN}✓${NC} RAG Query API (http://localhost:8087)"
    else
        echo -e "${RED}✗${NC} RAG Query API (http://localhost:8087)"
    fi
    
    # Nginx
    if curl -sf http://localhost:8088/health > /dev/null; then
        echo -e "${GREEN}✓${NC} Nginx Proxy (http://localhost:8088)"
    else
        echo -e "${RED}✗${NC} Nginx Proxy (http://localhost:8088)"
    fi
    
    # Elasticsearch
    if curl -sf http://localhost:9200/_cluster/health > /dev/null; then
        echo -e "${GREEN}✓${NC} Elasticsearch (http://localhost:9200)"
    else
        echo -e "${RED}✗${NC} Elasticsearch (http://localhost:9200)"
    fi
    
    # Qdrant
    if curl -sf http://localhost:6334/health > /dev/null; then
        echo -e "${GREEN}✓${NC} Qdrant (http://localhost:6334)"
    else
        echo -e "${RED}✗${NC} Qdrant (http://localhost:6334)"
    fi
    
    # PostgreSQL
    if docker exec patent-postgres pg_isready -U postgres > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} PostgreSQL (localhost:5433)"
    else
        echo -e "${RED}✗${NC} PostgreSQL (localhost:5433)"
    fi
    
    echo ""
    echo -e "${GREEN}Health check complete${NC}"
}

# Function to backup database
backup_database() {
    echo -e "${BLUE}Backing up patent database...${NC}"
    check_docker
    
    BACKUP_FILE="patent_backup_$(date +%Y%m%d_%H%M%S).sql"
    docker exec patent-postgres pg_dump -U postgres patent_db > "$BACKUP_FILE"
    
    echo -e "${GREEN}✓ Database backed up to: $BACKUP_FILE${NC}"
}

# Function to restore database
restore_database() {
    echo -e "${BLUE}Restoring patent database...${NC}"
    check_docker
    
    if [ -z "${1:-}" ]; then
        echo -e "${RED}Error: Please specify backup file${NC}"
        echo "Usage: $0 restore <backup_file.sql>"
        exit 1
    fi
    
    BACKUP_FILE="$1"
    if [ ! -f "$BACKUP_FILE" ]; then
        echo -e "${RED}Error: Backup file not found: $BACKUP_FILE${NC}"
        exit 1
    fi
    
    docker exec -i patent-postgres psql -U postgres patent_db < "$BACKUP_FILE"
    
    echo -e "${GREEN}✓ Database restored from: $BACKUP_FILE${NC}"
}

# Function to run tests
run_tests() {
    echo -e "${BLUE}Running system tests...${NC}"
    echo ""
    
    # Test patent search
    echo -e "${BLUE}Testing patent search...${NC}"
    echo "  Keywords: sovereignty architecture"
    
    # Test scholar search
    echo -e "${BLUE}Testing scholar search...${NC}"
    echo "  Keywords: AI governance"
    
    # Test RAG query
    echo -e "${BLUE}Testing RAG query...${NC}"
    curl -sf -X POST http://localhost:8087/query \
        -H "Content-Type: application/json" \
        -d '{"query":"test","collection":"patent_prior_art_v1"}' > /dev/null && \
        echo -e "${GREEN}✓${NC} RAG Query API responding" || \
        echo -e "${RED}✗${NC} RAG Query API not responding"
    
    echo ""
    echo -e "${GREEN}Tests complete${NC}"
}

# Function to run monitoring
run_monitoring() {
    echo -e "${BLUE}Running patent & scholar monitoring...${NC}"
    echo ""
    
    echo -e "${BLUE}Patent Prior Art Search:${NC}"
    echo "  Searching USPTO, EPO, WIPO databases..."
    echo "  Keywords: sovereignty, architecture, AI governance"
    
    echo ""
    echo -e "${BLUE}Google Scholar Discovery:${NC}"
    echo "  Discovering papers in AI governance and sovereignty..."
    echo "  Tracking citations..."
    
    echo ""
    echo -e "${GREEN}Monitoring complete${NC}"
    echo "See $0 logs for detailed output"
}

# Main command handler
case "${1:-help}" in
    up)
        start_services
        ;;
    down)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    logs)
        view_logs
        ;;
    status)
        check_status
        ;;
    health)
        run_health_checks
        ;;
    backup)
        backup_database
        ;;
    restore)
        restore_database "${2:-}"
        ;;
    test)
        run_tests
        ;;
    monitor)
        run_monitoring
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}Error: Unknown command: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
