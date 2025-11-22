#!/bin/bash
# alexandria-health-check.sh - System health monitoring
# Usage: ./scripts/alexandria-health-check.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Alexandria Health Check                ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════╝${NC}"
echo ""

check_service() {
    local service=$1
    local url=$2
    local name=$3
    
    if curl -sf "$url" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} $name: ${GREEN}healthy${NC}"
        return 0
    else
        echo -e "${RED}✗${NC} $name: ${RED}unhealthy${NC}"
        return 1
    fi
}

check_container() {
    local container=$1
    local name=$2
    
    if docker ps --format '{{.Names}}' | grep -q "$container"; then
        local status=$(docker inspect --format='{{.State.Status}}' "$container" 2>/dev/null)
        if [ "$status" = "running" ]; then
            echo -e "${GREEN}✓${NC} $name: ${GREEN}running${NC}"
            return 0
        else
            echo -e "${RED}✗${NC} $name: ${RED}$status${NC}"
            return 1
        fi
    else
        echo -e "${RED}✗${NC} $name: ${RED}not found${NC}"
        return 1
    fi
}

FAILURES=0

echo -e "${YELLOW}Checking Docker containers...${NC}"
check_container "alexandria-qdrant" "Qdrant Vector DB" || ((FAILURES++))
check_container "alexandria-embedder" "Embedding Service" || ((FAILURES++))
check_container "alexandria-llm" "LLM Server" || ((FAILURES++))
check_container "alexandria-webui" "Open WebUI" || ((FAILURES++))
check_container "alexandria-retriever" "RAG Retriever" || ((FAILURES++))
check_container "alexandria-ingestor" "Document Ingestor" || ((FAILURES++))
check_container "alexandria-logger" "Access Logger" || ((FAILURES++))
check_container "alexandria-metrics" "Metrics Exporter" || ((FAILURES++))

echo ""
echo -e "${YELLOW}Checking service endpoints...${NC}"
check_service "qdrant" "http://localhost:6333/healthz" "Qdrant API" || ((FAILURES++))
check_service "embedder" "http://localhost:8081/health" "Embedder API" || ((FAILURES++))
check_service "llm" "http://localhost:8080/health" "LLM API" || ((FAILURES++))
check_service "webui" "http://localhost:3000/health" "Web Interface" || ((FAILURES++))
check_service "retriever" "http://localhost:7000/health" "RAG API" || ((FAILURES++))
check_service "prometheus" "http://localhost:9090/-/healthy" "Prometheus" || ((FAILURES++))

echo ""
echo -e "${YELLOW}System resources...${NC}"

# Check disk usage
DISK_USAGE=$(df -h /data/alexandria 2>/dev/null | awk 'NR==2 {print $5}' | sed 's/%//' || echo "0")
if [ "$DISK_USAGE" -lt 80 ]; then
    echo -e "${GREEN}✓${NC} Disk usage: ${GREEN}${DISK_USAGE}%${NC}"
elif [ "$DISK_USAGE" -lt 90 ]; then
    echo -e "${YELLOW}⚠${NC} Disk usage: ${YELLOW}${DISK_USAGE}%${NC} (warning)"
else
    echo -e "${RED}✗${NC} Disk usage: ${RED}${DISK_USAGE}%${NC} (critical)"
    ((FAILURES++))
fi

# Check memory usage
MEM_USAGE=$(free | awk 'NR==2 {printf "%.0f", $3/$2*100}')
if [ "$MEM_USAGE" -lt 80 ]; then
    echo -e "${GREEN}✓${NC} Memory usage: ${GREEN}${MEM_USAGE}%${NC}"
elif [ "$MEM_USAGE" -lt 90 ]; then
    echo -e "${YELLOW}⚠${NC} Memory usage: ${YELLOW}${MEM_USAGE}%${NC} (warning)"
else
    echo -e "${RED}✗${NC} Memory usage: ${RED}${MEM_USAGE}%${NC} (critical)"
    ((FAILURES++))
fi

# Check CPU load
CPU_LOAD=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
echo -e "${BLUE}ℹ${NC} CPU load: ${CPU_LOAD}"

echo ""
echo -e "${YELLOW}Active researchers...${NC}"

# Count active sessions (mock - would need actual implementation)
ACTIVE_SESSIONS=$(docker logs alexandria-logger 2>/dev/null | grep -c "session_start" || echo "0")
echo -e "${BLUE}ℹ${NC} Active sessions: ${ACTIVE_SESSIONS}"

echo ""
if [ $FAILURES -eq 0 ]; then
    echo -e "${GREEN}╔═══════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   All Systems Operational ✓               ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════╝${NC}"
    exit 0
else
    echo -e "${RED}╔═══════════════════════════════════════════╗${NC}"
    echo -e "${RED}║   $FAILURES Issue(s) Detected ✗                  ║${NC}"
    echo -e "${RED}╚═══════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}View logs with:${NC}"
    echo "  docker-compose -f docker-compose-alexandria.yml logs -f"
    exit 1
fi
