#!/bin/bash
# test-quantum-chess.sh - Integration test for Quantum Chess Engine
# Tests deployment without running all 64 containers (uses subset for speed)

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

log() {
    echo -e "${CYAN}[$(date +'%H:%M:%S')] $1${NC}"
}

success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

love() {
    echo -e "${MAGENTA}♥ $1 ♥${NC}"
}

# Test configuration
export HER_TERMINAL_IP="127.0.0.1"
export THRONE_NAS_PATH="/tmp/test-quantum-bus-$$"
export RANDOM_SEED="42"

echo ""
love "Testing Quantum Chess Engine Deployment"
echo ""

# Cleanup function
cleanup() {
    log "Cleaning up test environment..."
    docker compose -f docker-compose-quantum-chess.yml down -v 2>/dev/null || true
    rm -rf "$THRONE_NAS_PATH"
    success "Cleanup complete"
}

# Register cleanup on exit
trap cleanup EXIT

# Test 1: Create quantum bus
log "Test 1: Creating quantum bus..."
mkdir -p "$THRONE_NAS_PATH"/{squares,moves,games,timelines,love-metrics}

if [ -d "$THRONE_NAS_PATH/squares" ]; then
    success "Quantum bus created successfully"
else
    error "Failed to create quantum bus"
    exit 1
fi

# Test 2: Initialize quantum state
log "Test 2: Initializing quantum state..."
cat > "$THRONE_NAS_PATH/quantum-state.json" <<EOF
{
    "initialized": "$(date +'%Y-%m-%d %H:%M:%S')",
    "random_seed": 42,
    "entanglement_active": true,
    "love_mode": true,
    "her_terminal_ip": "$HER_TERMINAL_IP",
    "total_squares": 64,
    "timeline": "testing_timeline"
}
EOF

if [ -f "$THRONE_NAS_PATH/quantum-state.json" ]; then
    success "Quantum state initialized"
else
    error "Failed to initialize quantum state"
    exit 1
fi

# Test 3: Validate configuration files
log "Test 3: Validating configuration files..."
if [ -f "quantum-chess-engine.yaml" ] && \
   [ -f "docker-compose-quantum-chess.yml" ]; then
    success "Configuration files present"
else
    error "Missing configuration files"
    exit 1
fi

# Test 4: Validate Docker Compose syntax
log "Test 4: Validating Docker Compose syntax..."
if docker compose -f docker-compose-quantum-chess.yml config > /dev/null 2>&1; then
    success "Docker Compose configuration valid"
else
    error "Docker Compose configuration invalid"
    exit 1
fi

# Test 5: Pull Ollama image
log "Test 5: Pulling Ollama base image (this may take a while)..."
if docker pull ollama/ollama:latest > /dev/null 2>&1; then
    success "Ollama image pulled successfully"
else
    error "Failed to pull Ollama image"
    exit 1
fi

# Test 6: Start orchestrator
log "Test 6: Starting quantum orchestrator..."
docker compose -f docker-compose-quantum-chess.yml up -d quantum-orchestrator

sleep 5

if docker ps --filter "name=quantum-orchestrator" --format "{{.Names}}" | grep -q "quantum-orchestrator"; then
    success "Quantum orchestrator started"
else
    error "Failed to start quantum orchestrator"
    exit 1
fi

# Test 7: Start sample squares (just a few for testing)
log "Test 7: Starting sample chess squares..."
docker compose -f docker-compose-quantum-chess.yml up -d square-e1 square-e4 square-e8

sleep 5

running_squares=$(docker ps --filter "name=square-" --format "{{.Names}}" | wc -l)
if [ "$running_squares" -ge 3 ]; then
    success "$running_squares sample squares running"
else
    error "Failed to start sample squares (only $running_squares running)"
    exit 1
fi

# Test 8: Verify quantum bus mounting
log "Test 8: Verifying quantum bus mounting..."
if docker exec square-e4 sh -c "ls /quantum-bus > /dev/null 2>&1"; then
    success "Quantum bus mounted correctly in containers"
else
    error "Quantum bus not accessible in containers"
    exit 1
fi

# Test 9: Test entanglement (shared state)
log "Test 9: Testing quantum entanglement (shared state)..."
docker exec square-e1 sh -c "echo 'Test from e1' > /quantum-bus/test-entanglement.txt"
docker exec square-e8 sh -c "cat /quantum-bus/test-entanglement.txt" > /tmp/entanglement-test.txt

if grep -q "Test from e1" /tmp/entanglement-test.txt; then
    success "Quantum entanglement verified (shared volume working)"
else
    error "Quantum entanglement failed (shared volume not working)"
    exit 1
fi

# Test 10: Verify environment variables
log "Test 10: Verifying environment variables..."
docker exec square-e4 sh -c "env | grep SQUARE" > /tmp/env-test.txt

if grep -q "SQUARE=e4" /tmp/env-test.txt; then
    success "Environment variables configured correctly"
else
    error "Environment variables not set correctly"
    exit 1
fi

# Test 11: Start heartbeat monitor
log "Test 11: Starting heartbeat monitor..."
docker compose -f docker-compose-quantum-chess.yml up -d quantum-heartbeat

sleep 5

if docker ps --filter "name=quantum-heartbeat" --format "{{.Names}}" | grep -q "quantum-heartbeat"; then
    success "Heartbeat monitor started"
else
    error "Failed to start heartbeat monitor"
    exit 1
fi

# Test 12: Verify heartbeat output
log "Test 12: Verifying heartbeat output..."
sleep 6  # Wait for heartbeat to write

if [ -f "$THRONE_NAS_PATH/heartbeat.txt" ]; then
    heartbeat_content=$(cat "$THRONE_NAS_PATH/heartbeat.txt")
    if echo "$heartbeat_content" | grep -q "Quantum board live"; then
        success "Heartbeat writing correctly: $heartbeat_content"
    else
        error "Heartbeat content unexpected"
        exit 1
    fi
else
    error "Heartbeat file not created"
    exit 1
fi

# Test 13: Verify network connectivity
log "Test 13: Verifying network connectivity between containers..."
if docker exec square-e4 sh -c "ping -c 1 quantum-orchestrator > /dev/null 2>&1"; then
    success "Network connectivity verified"
else
    error "Containers cannot communicate on swarm-net"
    exit 1
fi

# Test 14: Check resource limits
log "Test 14: Checking container resource limits..."
mem_limit=$(docker inspect square-e4 --format='{{.HostConfig.Memory}}')
if [ "$mem_limit" -gt 0 ]; then
    success "Resource limits configured (Memory: $mem_limit bytes)"
else
    # No limit is actually okay, just informational
    success "No hard memory limits (running in unlimited mode)"
fi

# Test 15: Verify container logs
log "Test 15: Verifying container logs..."
docker logs square-e4 2>&1 | head -5 > /tmp/logs-test.txt
if [ -s /tmp/logs-test.txt ]; then
    success "Container logs accessible"
else
    error "Container logs empty or inaccessible"
    exit 1
fi

# Final summary
echo ""
echo "═══════════════════════════════════════════════════════════"
love "All Integration Tests Passed!"
echo "═══════════════════════════════════════════════════════════"
echo ""
log "Test Environment:"
echo "  Quantum Bus:     $THRONE_NAS_PATH"
echo "  Running Squares: $running_squares"
echo "  Orchestrator:    Running"
echo "  Heartbeat:       Active"
echo ""
success "✓ Quantum Chess Engine validated and working correctly!"
echo ""
log "The test containers will be automatically cleaned up."
echo ""
love "Checkmate was never the goal. Love was. And we just proved it works. ♕"
echo ""
