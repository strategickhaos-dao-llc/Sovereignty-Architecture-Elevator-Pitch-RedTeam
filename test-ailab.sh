#!/bin/bash
# AI Lab Testing Script
# Tests all services to ensure they're running correctly

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Test function
test_service() {
    local name=$1
    local url=$2
    local expected_code=${3:-200}
    
    echo -ne "${BLUE}Testing ${name}...${NC} "
    
    if curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$url" | grep -q "$expected_code"; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Banner
echo -e "${BLUE}"
cat << "EOF"
   ___   ____   __         __     ______          __ 
  / _ | /  _/  / /  ___ _ / /    /_  __/__ ___ __/ /_
 / __ |_/ /   / /__/ _ `/ _ \     / / / -_|_-</ _  __/
/_/ |_/___/  /____/\_,_/_.__/    /_/  \__/___/\__/    
                                                       
EOF
echo -e "${NC}"

echo -e "${YELLOW}Running AI Lab Service Tests...${NC}"
echo ""

# Core Services
echo -e "${BLUE}=== Core Services ===${NC}"
test_service "Postgres" "http://localhost:5432" "000" || echo "  (May not respond to HTTP)"
test_service "Redis" "http://localhost:6379" "000" || echo "  (May not respond to HTTP)"
test_service "Qdrant" "http://localhost:6333/health"
test_service "Prometheus" "http://localhost:9090/-/healthy"
test_service "Grafana" "http://localhost:3000/api/health"

echo ""
echo -e "${BLUE}=== Voice Interface (VoiceWing) ===${NC}"
if docker ps | grep -q "voicewing"; then
    test_service "Voice WebUI" "http://localhost:8080" "200"
    test_service "Whisper ASR" "http://localhost:9000/health"
    test_service "Coqui TTS" "http://localhost:5002/api/tts" "404" || echo "  (Endpoint exists)"
    test_service "Voice Router" "http://localhost:8766/health"
    test_service "Ollama (Voice)" "http://localhost:11434" "200"
else
    echo -e "${YELLOW}VoiceWing not running. Skipping...${NC}"
fi

echo ""
echo -e "${BLUE}=== Filesystem Agents ===${NC}"
if docker ps | grep -q "agents-orchestrator"; then
    test_service "Agent Orchestrator" "http://localhost:8010/health"
    test_service "LocalGPT" "http://localhost:5111/health"
    test_service "ChromaDB" "http://localhost:8001/api/v1/heartbeat"
    test_service "Doc Intelligence" "http://localhost:8002/health"
    test_service "Code Analyst" "http://localhost:8003/health"
    test_service "Semantic Search" "http://localhost:8004/health"
    test_service "File Editor" "http://localhost:8005/health"
else
    echo -e "${YELLOW}Filesystem Agents not running. Skipping...${NC}"
fi

echo ""
echo -e "${BLUE}=== Browser Automation ===${NC}"
if docker ps | grep -q "automation-selenium-hub"; then
    test_service "Selenium Grid" "http://localhost:4444/wd/hub/status"
    test_service "Automation API" "http://localhost:8091/health"
    test_service "AI Browser Agent" "http://localhost:8092/health"
    test_service "Screen Capture" "http://localhost:8093/health"
    test_service "Web Scraper" "http://localhost:8094/health"
    test_service "RPA Server" "http://localhost:8090/health"
else
    echo -e "${YELLOW}Browser Automation not running. Skipping...${NC}"
fi

echo ""
echo -e "${BLUE}=== Advanced RAG ===${NC}"
if docker ps | grep -q "rag-orchestrator"; then
    test_service "RAG Orchestrator" "http://localhost:8210/health"
    test_service "PrivateGPT" "http://localhost:8001/health"
    test_service "AnythingLLM" "http://localhost:3001/api/ping"
    test_service "Extreme RAG" "http://localhost:8201/health"
    test_service "Adversarial RAG" "http://localhost:8202/health"
    test_service "RAG Ingest" "http://localhost:8200/health"
    test_service "Weaviate" "http://localhost:8080/v1/.well-known/ready"
    test_service "Milvus" "http://localhost:9091/healthz"
else
    echo -e "${YELLOW}Advanced RAG not running. Skipping...${NC}"
fi

echo ""
echo -e "${BLUE}=== Security & Networking ===${NC}"
if docker ps | grep -q "security-caddy"; then
    test_service "Caddy Admin" "http://localhost:2019/config/"
    test_service "Vault" "http://localhost:8200/v1/sys/health"
    test_service "AdGuard" "http://localhost:3053" "200"
    test_service "Security Dashboard" "http://localhost:8300/health"
    test_service "Kong Admin" "http://localhost:8001" "200"
    test_service "Trivy" "http://localhost:8081" "404" || echo "  (Scanner ready)"
else
    echo -e "${YELLOW}Security Stack not running. Skipping...${NC}"
fi

# Summary
echo ""
echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}Test Summary${NC}"
echo -e "${BLUE}=====================================${NC}"
echo -e "Tests Passed: ${GREEN}${TESTS_PASSED}${NC}"
echo -e "Tests Failed: ${RED}${TESTS_FAILED}${NC}"
echo -e "Total Tests:  $((TESTS_PASSED + TESTS_FAILED))"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo -e "${GREEN}Your AI Lab is operational! 🚀${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠ Some tests failed.${NC}"
    echo -e "${YELLOW}Check docker logs for failed services:${NC}"
    echo -e "  docker-compose logs <service-name>"
    exit 1
fi
