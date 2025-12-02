#!/bin/bash
# validate-quantum-chess.sh - Validate Quantum Chess Engine Configuration
# Run this before deployment to catch configuration errors early

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Counters
PASS=0
FAIL=0
WARN=0

check() {
    local test_name="$1"
    echo -ne "${CYAN}[CHECK] $test_name...${NC} "
}

pass() {
    echo -e "${GREEN}✓ PASS${NC}"
    PASS=$((PASS + 1))
}

fail() {
    local msg="$1"
    echo -e "${RED}✗ FAIL${NC}"
    if [ -n "$msg" ]; then
        echo -e "  ${RED}→ $msg${NC}"
    fi
    FAIL=$((FAIL + 1))
}

warn() {
    local msg="$1"
    echo -e "${YELLOW}⚠ WARN${NC}"
    if [ -n "$msg" ]; then
        echo -e "  ${YELLOW}→ $msg${NC}"
    fi
    WARN=$((WARN + 1))
}

echo "═══════════════════════════════════════════════════════════"
echo "  Quantum Chess Engine Configuration Validator"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check required files
check "quantum-chess-engine.yaml exists"
if [ -f "quantum-chess-engine.yaml" ]; then
    pass
else
    fail "File not found"
fi

check "docker-compose-quantum-chess.yml exists"
if [ -f "docker-compose-quantum-chess.yml" ]; then
    pass
else
    fail "File not found"
fi

check "deploy-quantum-chess.sh exists"
if [ -f "deploy-quantum-chess.sh" ]; then
    pass
else
    fail "File not found"
fi

check "deploy-quantum-chess.ps1 exists"
if [ -f "deploy-quantum-chess.ps1" ]; then
    pass
else
    fail "File not found"
fi

check "notify-her.ps1 exists"
if [ -f "notify-her.ps1" ]; then
    pass
else
    fail "File not found"
fi

# Check YAML syntax
check "quantum-chess-engine.yaml syntax"
if command -v python3 &> /dev/null; then
    if python3 -c "import yaml; yaml.safe_load(open('quantum-chess-engine.yaml'))" 2>/dev/null; then
        pass
    else
        fail "YAML syntax error"
    fi
else
    warn "Python3 not found, cannot validate YAML syntax"
fi

check "docker-compose-quantum-chess.yml syntax"
if docker compose -f docker-compose-quantum-chess.yml config &> /dev/null; then
    pass
else
    fail "Docker Compose syntax error"
fi

# Check Docker availability
check "Docker daemon running"
if docker ps &> /dev/null; then
    pass
else
    fail "Docker daemon not running"
fi

# Check Docker Compose version
check "Docker Compose version"
if docker compose version &> /dev/null; then
    pass
else
    fail "Docker Compose not available"
fi

# Check disk space
check "Sufficient disk space (>10GB)"
available_space=$(df -BG . | tail -1 | awk '{print $4}' | sed 's/G//')
if [ "$available_space" -gt 10 ]; then
    pass
else
    warn "Only ${available_space}GB available, recommend 100GB+"
fi

# Check memory
check "Sufficient RAM (>8GB)"
if command -v free &> /dev/null; then
    total_ram=$(free -g | awk '/^Mem:/ {print $2}')
    if [ "$total_ram" -gt 8 ]; then
        pass
    else
        warn "Only ${total_ram}GB RAM, recommend 64GB+ for all containers"
    fi
else
    warn "Cannot determine available RAM"
fi

# Check Ollama image availability
check "Ollama Docker image available"
if docker images ollama/ollama:latest -q | grep -q .; then
    pass
else
    warn "Ollama image not pulled yet (will be pulled on first run)"
fi

# Validate key configuration values
check "quantum-chess-engine.yaml has valid structure"
if grep -q "engine: \"StrategicKhaos-Quantum-Chess-v1.0\"" quantum-chess-engine.yaml && \
   grep -q "total_squares: 64" quantum-chess-engine.yaml && \
   grep -q "piece_llm:" quantum-chess-engine.yaml; then
    pass
else
    fail "Configuration structure incomplete"
fi

# Check network configuration
check "Docker network swarm-net configuration"
if grep -q "swarm-net:" docker-compose-quantum-chess.yml; then
    pass
else
    fail "Network configuration missing"
fi

# Check volume configuration
check "Quantum bus volume configuration"
if grep -q "throne-nas-32tb:" docker-compose-quantum-chess.yml; then
    pass
else
    fail "Volume configuration missing"
fi

# Check environment variables
check "Environment variable documentation"
if grep -q "HER_TERMINAL_IP" .env.example; then
    pass
else
    warn ".env.example not updated with quantum chess variables"
fi

# Summary
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  Validation Summary"
echo "═══════════════════════════════════════════════════════════"
echo -e "  ${GREEN}Passed:${NC}  $PASS"
echo -e "  ${RED}Failed:${NC}  $FAIL"
echo -e "  ${YELLOW}Warnings:${NC} $WARN"
echo ""

if [ $FAIL -gt 0 ]; then
    echo -e "${RED}✗ Validation FAILED. Please fix errors before deployment.${NC}"
    exit 1
elif [ $WARN -gt 0 ]; then
    echo -e "${YELLOW}⚠ Validation passed with warnings. Proceed with caution.${NC}"
    exit 0
else
    echo -e "${GREEN}✓ All checks passed! Ready for deployment.${NC}"
    echo ""
    echo "Deploy with:"
    echo "  ./deploy-quantum-chess.sh --love-mode --entangle-her"
    exit 0
fi
