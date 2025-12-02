#!/bin/bash
# Test the SME docker-compose stack
# Performs basic health checks on all services

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}SME Stack Test${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# Function to check if service is running
check_service() {
    local service=$1
    local port=$2
    local endpoint=$3
    
    echo -n "Checking $service on port $port... "
    
    if docker-compose -f "$PROJECT_ROOT/docker-compose-sme.yml" ps | grep -q "$service.*Up"; then
        echo -e "${GREEN}Running${NC}"
        
        if [ -n "$endpoint" ]; then
            echo -n "  Testing endpoint $endpoint... "
            if curl -f -s -o /dev/null "http://localhost:$port$endpoint"; then
                echo -e "${GREEN}OK${NC}"
            else
                echo -e "${YELLOW}Not ready${NC}"
            fi
        fi
    else
        echo -e "${RED}Not running${NC}"
    fi
}

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker installed${NC}"

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}✗ Docker Compose not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose installed${NC}"

# Check if Ollama is available
echo -n "Checking Ollama... "
if curl -f -s -o /dev/null "http://localhost:11434/api/tags"; then
    echo -e "${GREEN}Available${NC}"
else
    echo -e "${YELLOW}Not available (optional)${NC}"
fi

echo ""

# Check YAML files
echo -e "${BLUE}Validating YAML files...${NC}"

for file in evolution-path.yaml sme-resources.yaml docker-compose-sme.yml; do
    echo -n "  $file... "
    if python3 -c "import yaml; yaml.safe_load(open('$PROJECT_ROOT/$file'))" 2>/dev/null; then
        echo -e "${GREEN}Valid${NC}"
    else
        echo -e "${RED}Invalid${NC}"
        exit 1
    fi
done

echo ""

# Check if stack is running
echo -e "${BLUE}Checking Docker services...${NC}"

if ! docker-compose -f "$PROJECT_ROOT/docker-compose-sme.yml" ps | grep -q "Up"; then
    echo -e "${YELLOW}Services not running. Start with:${NC}"
    echo "  docker-compose -f docker-compose-sme.yml up -d"
    echo ""
    echo -e "${BLUE}Exiting...${NC}"
    exit 0
fi

echo ""

# Check each service
check_service "sme-vectordb" "6334" "/health"
check_service "sme-rag-api" "8090" "/health"
check_service "sme-dashboard" "3001" ""
check_service "sme-prometheus" "9091" "/api/v1/status/buildinfo"
check_service "sme-redis-cache" "6380" ""

echo ""

# Test RAG API if running
if docker-compose -f "$PROJECT_ROOT/docker-compose-sme.yml" ps | grep -q "sme-rag-api.*Up"; then
    echo -e "${BLUE}Testing RAG API...${NC}"
    
    response=$(curl -s -X POST http://localhost:8090/query \
        -H "Content-Type: application/json" \
        -d '{"question": "test", "max_results": 1}' 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ RAG API responding${NC}"
        echo "  Response: ${response:0:100}..."
    else
        echo -e "${YELLOW}✗ RAG API not responding${NC}"
    fi
fi

echo ""

# Check logs for errors
echo -e "${BLUE}Recent errors in logs:${NC}"
recent_errors=$(docker-compose -f "$PROJECT_ROOT/docker-compose-sme.yml" logs --tail=50 2>&1 | grep -i "error" | wc -l)
if [ "$recent_errors" -eq 0 ]; then
    echo -e "${GREEN}No recent errors${NC}"
else
    echo -e "${YELLOW}Found $recent_errors error lines${NC}"
    echo "  View with: docker-compose -f docker-compose-sme.yml logs"
fi

echo ""

# Summary
echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}Test Summary${NC}"
echo -e "${BLUE}======================================${NC}"

running_services=$(docker-compose -f "$PROJECT_ROOT/docker-compose-sme.yml" ps | grep "Up" | wc -l)
total_services=18

echo "Services running: $running_services / $total_services"

if [ "$running_services" -eq "$total_services" ]; then
    echo -e "${GREEN}✓ All services are running${NC}"
elif [ "$running_services" -gt 0 ]; then
    echo -e "${YELLOW}⚠ Some services are not running${NC}"
    echo "  Check with: docker-compose -f docker-compose-sme.yml ps"
else
    echo -e "${YELLOW}No services running${NC}"
fi

echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  1. View logs: docker-compose -f docker-compose-sme.yml logs -f"
echo "  2. Query RAG API: curl http://localhost:8090/query -d '{\"question\":\"test\"}'"
echo "  3. View dashboard: http://localhost:3001"
echo ""
