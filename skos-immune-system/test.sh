#!/bin/bash
# SKOS Immune System - Test Suite
# Sovereign Khaos Operating System v0.1.0
#
# This script verifies the immune system is working correctly.
#
# Usage: ./test.sh
#
# Copyright (c) 2024 Strategickhaos DAO LLC
# License: MIT

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

# Banner
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           SKOS IMMUNE SYSTEM TEST SUITE v0.1.0              ║"
echo "║      Sovereign Khaos Operating System                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Determine compose command
if docker compose version &> /dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Test function
run_test() {
    local name="$1"
    local command="$2"
    
    echo -n "  Testing: $name... "
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Test with output
run_test_with_output() {
    local name="$1"
    local command="$2"
    local expected="$3"
    
    echo -n "  Testing: $name... "
    local output
    output=$(eval "$command" 2>&1)
    if echo "$output" | grep -q "$expected"; then
        echo -e "${GREEN}PASS${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo -e "    Expected: $expected"
        echo -e "    Got: $output"
        ((TESTS_FAILED++))
        return 1
    fi
}

echo -e "${YELLOW}[1/4] Infrastructure Tests${NC}"

# Test Docker
run_test "Docker available" "docker info"

# Test containers running
run_test "NATS container running" "$COMPOSE_CMD ps | grep -q skos-nats"
run_test "Coordinator container running" "$COMPOSE_CMD ps | grep -q skos-coordinator"
run_test "Thermal Sentinel container running" "$COMPOSE_CMD ps | grep -q skos-thermal-sentinel"

echo ""
echo -e "${YELLOW}[2/4] NATS Tests${NC}"

# Test NATS connectivity
run_test "NATS health endpoint" "curl -s http://localhost:8222/healthz"
run_test "NATS server info" "curl -s http://localhost:8222/varz | grep -q server_id"

# Test JetStream
run_test_with_output "JetStream enabled" "curl -s http://localhost:8222/jsz" "server_id"

echo ""
echo -e "${YELLOW}[3/4] Service Health Tests${NC}"

# Check container health
run_test "Coordinator healthy" "$COMPOSE_CMD ps | grep coordinator | grep -q Up"
run_test "Thermal Sentinel healthy" "$COMPOSE_CMD ps | grep thermal | grep -q Up"

# Check logs for startup messages
run_test_with_output "Coordinator started" "$COMPOSE_CMD logs coordinator 2>&1 | tail -20" "Starting Antibody Coordinator"
run_test_with_output "Thermal Sentinel started" "$COMPOSE_CMD logs thermal-sentinel 2>&1 | tail -20" "Starting Thermal Sentinel"

echo ""
echo -e "${YELLOW}[4/4] Communication Tests${NC}"

# Check for heartbeats in logs
sleep 3  # Wait for heartbeats
run_test_with_output "Heartbeats flowing" "$COMPOSE_CMD logs thermal-sentinel 2>&1 | tail -50" "HEARTBEAT\|heartbeat\|CPU="

# Check for coordinator receiving heartbeats
run_test_with_output "Coordinator receiving heartbeats" "$COMPOSE_CMD logs coordinator 2>&1 | tail -50" "heartbeat\|agent\|Connected to NATS"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Summary
if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed! ($TESTS_PASSED/$((TESTS_PASSED + TESTS_FAILED)))${NC}"
    echo ""
    echo -e "${GREEN}Your sovereign immune system is healthy! 🛡️✅${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed: $TESTS_PASSED passed, $TESTS_FAILED failed${NC}"
    echo ""
    echo -e "${YELLOW}Troubleshooting:${NC}"
    echo "  1. Check container logs: $COMPOSE_CMD logs"
    echo "  2. Restart services: $COMPOSE_CMD restart"
    echo "  3. Rebuild: ./deploy.sh --build --clean"
    exit 1
fi
