#!/bin/bash
#
# Network and Webhook Diagnostic Script for Strategickhaos Sovereignty Architecture
#
# Performs comprehensive network diagnostics including:
# - Public IP detection
# - DNS resolution for critical services
# - Local webhook listener status
# - smee client process detection
# - HMAC signature computation
# - Outbound HTTPS connectivity
#
# Usage: ./network-diagnostic.sh [--port 3000] [--skip-hmac]
#

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

# Defaults
WEBHOOK_PORT="${WEBHOOK_PORT:-3001}"
SKIP_HMAC=false
PASSED_CHECKS=0
FAILED_CHECKS=0

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --port)
            WEBHOOK_PORT="$2"
            shift 2
            ;;
        --skip-hmac)
            SKIP_HMAC=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Helper functions
check_result() {
    local name="$1"
    local passed="$2"
    local details="${3:-}"
    
    if [[ "$passed" == "true" ]]; then
        echo -e "  ${GREEN}[PASS]${NC} $name${details:+ - ${GRAY}$details${NC}}"
        ((PASSED_CHECKS++))
    else
        echo -e "  ${RED}[FAIL]${NC} $name${details:+ - ${GRAY}$details${NC}}"
        ((FAILED_CHECKS++))
    fi
}

section_header() {
    echo ""
    echo -e "${CYAN}=== $1 ===${NC}"
}

# Header
echo ""
echo -e "${YELLOW}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║   Strategickhaos Network & Webhook Diagnostic                  ║${NC}"
echo -e "${YELLOW}║   Sovereignty Architecture Control Plane                       ║${NC}"
echo -e "${YELLOW}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Hostname: $(hostname)"
echo ""

# 1. Public IP
section_header "1) Public IP Detection"
if command -v curl &> /dev/null; then
    PUBIP=$(curl -s --connect-timeout 10 https://ifconfig.io/ip 2>/dev/null || echo "")
    if [[ -n "$PUBIP" ]]; then
        echo -e "  Public IP: ${GREEN}$PUBIP${NC}"
        check_result "Public IP Detection" "true" "$PUBIP"
    else
        check_result "Public IP Detection" "false" "Could not detect public IP"
    fi
else
    check_result "Public IP Detection" "false" "curl not installed"
fi

# 2. DNS Resolution
section_header "2) DNS Resolution"
DNS_TARGETS=("github.com" "api.github.com" "raw.githubusercontent.com" "smee.io")

for target in "${DNS_TARGETS[@]}"; do
    if command -v dig &> /dev/null; then
        ip=$(dig +short "$target" A 2>/dev/null | head -1)
    elif command -v nslookup &> /dev/null; then
        ip=$(nslookup "$target" 2>/dev/null | awk '/^Address: / { print $2 }' | head -1)
    elif command -v host &> /dev/null; then
        ip=$(host "$target" 2>/dev/null | awk '/has address/ { print $4 }' | head -1)
    else
        ip=""
    fi
    
    if [[ -n "$ip" ]]; then
        check_result "DNS: $target" "true" "$ip"
    else
        check_result "DNS: $target" "false" "No resolution"
    fi
done

# 3. Local Webhook Listener
section_header "3) Local Webhook Listener (Port $WEBHOOK_PORT)"

# Check if port is listening
if command -v nc &> /dev/null; then
    if nc -z localhost "$WEBHOOK_PORT" 2>/dev/null; then
        check_result "TCP Connect localhost:$WEBHOOK_PORT" "true" "Listener active"
    else
        check_result "TCP Connect localhost:$WEBHOOK_PORT" "false" "No listener on port $WEBHOOK_PORT"
        echo ""
        echo -e "  ${YELLOW}SUGGESTION: Start the event gateway:${NC}"
        echo -e "  ${GRAY}  npm run dev${NC}"
    fi
elif command -v ss &> /dev/null; then
    if ss -tlnp | grep -q ":$WEBHOOK_PORT "; then
        check_result "TCP Connect localhost:$WEBHOOK_PORT" "true" "Listener active"
    else
        check_result "TCP Connect localhost:$WEBHOOK_PORT" "false" "No listener on port $WEBHOOK_PORT"
    fi
elif command -v netstat &> /dev/null; then
    if netstat -tlnp 2>/dev/null | grep -q ":$WEBHOOK_PORT "; then
        check_result "TCP Connect localhost:$WEBHOOK_PORT" "true" "Listener active"
    else
        check_result "TCP Connect localhost:$WEBHOOK_PORT" "false" "No listener on port $WEBHOOK_PORT"
    fi
else
    check_result "TCP Connect localhost:$WEBHOOK_PORT" "false" "No tool available to check port"
fi

# 4. Node/smee Process Detection
section_header "4) Node.js Process Detection"

if command -v pgrep &> /dev/null; then
    NODE_PIDS=$(pgrep -f "node" 2>/dev/null || echo "")
    if [[ -n "$NODE_PIDS" ]]; then
        count=$(echo "$NODE_PIDS" | wc -l)
        check_result "Node.js Process" "true" "$count process(es) running"
        
        # Check for smee
        if pgrep -f "smee" &> /dev/null; then
            echo -e "  ${GREEN}smee client detected${NC}"
        fi
    else
        check_result "Node.js Process" "false" "No node processes found"
        echo ""
        echo -e "  ${YELLOW}SUGGESTION: Start the smee client:${NC}"
        echo -e "  ${GRAY}  npx smee-client --url https://smee.io/YOUR_CHANNEL --target http://localhost:$WEBHOOK_PORT/webhooks/github${NC}"
    fi
else
    # Fallback to ps
    if ps aux | grep -v grep | grep -q "node"; then
        check_result "Node.js Process" "true" "Running"
    else
        check_result "Node.js Process" "false" "No node processes found"
    fi
fi

# 5. HMAC Signature Test
if [[ "$SKIP_HMAC" != "true" ]]; then
    section_header "5) HMAC-SHA256 Signature Computation"
    
    TEST_PAYLOAD='{"action":"test"}'
    WEBHOOK_SECRET="${GITHUB_WEBHOOK_SECRET:-test_secret_for_demo}"
    
    if [[ "$WEBHOOK_SECRET" == "test_secret_for_demo" ]]; then
        echo -e "  ${YELLOW}Using demo secret (set GITHUB_WEBHOOK_SECRET env var for real testing)${NC}"
    fi
    
    if command -v openssl &> /dev/null; then
        SIGNATURE=$(printf '%s' "$TEST_PAYLOAD" | openssl dgst -sha256 -hmac "$WEBHOOK_SECRET" | awk '{print "sha256="$2}')
        echo -e "  Payload: ${GRAY}$TEST_PAYLOAD${NC}"
        echo -e "  Signature: ${GREEN}$SIGNATURE${NC}"
        check_result "HMAC Computation" "true"
    else
        check_result "HMAC Computation" "false" "openssl not installed"
    fi
fi

# 6. Outbound HTTPS
section_header "6) Outbound HTTPS Connectivity"
HTTPS_TARGETS=("api.github.com:443" "raw.githubusercontent.com:443" "smee.io:443")

for target in "${HTTPS_TARGETS[@]}"; do
    host="${target%:*}"
    port="${target#*:}"
    
    if command -v curl &> /dev/null; then
        if curl -s --connect-timeout 5 -o /dev/null "https://$host" 2>/dev/null; then
            check_result "HTTPS: $target" "true"
        else
            check_result "HTTPS: $target" "false" "Connection failed"
        fi
    elif command -v nc &> /dev/null; then
        if nc -z -w5 "$host" "$port" 2>/dev/null; then
            check_result "HTTPS: $target" "true"
        else
            check_result "HTTPS: $target" "false" "Connection failed"
        fi
    else
        check_result "HTTPS: $target" "false" "No tool to test connectivity"
    fi
done

# 7. Docker Status
section_header "7) Docker Status"
if command -v docker &> /dev/null; then
    if docker version --format '{{.Server.Version}}' &> /dev/null; then
        DOCKER_VERSION=$(docker version --format '{{.Server.Version}}' 2>/dev/null)
        check_result "Docker" "true" "Version $DOCKER_VERSION"
    else
        check_result "Docker" "false" "Docker daemon not running"
    fi
else
    check_result "Docker" "false" "Docker not installed"
fi

# Summary
echo ""
echo -e "${YELLOW}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║   DIAGNOSTIC SUMMARY                                           ║${NC}"
echo -e "${YELLOW}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  Passed: ${GREEN}$PASSED_CHECKS${NC}"

if [[ $FAILED_CHECKS -gt 0 ]]; then
    echo -e "  Failed: ${RED}$FAILED_CHECKS${NC}"
    echo ""
    echo -e "  ${YELLOW}NEXT STEPS:${NC}"
    echo -e "  ${GRAY}1. Review failed checks above${NC}"
    echo -e "  ${GRAY}2. See NETWORK_WEBHOOK_GUIDE.md for detailed solutions${NC}"
    echo -e "  ${GRAY}3. Ensure event gateway is running: npm run dev${NC}"
    echo -e "  ${GRAY}4. For development, set up smee.io webhook proxy${NC}"
    echo ""
    exit 1
else
    echo -e "  Failed: ${GREEN}$FAILED_CHECKS${NC}"
    echo ""
    echo -e "  ${GREEN}All checks passed! System is ready for webhook processing.${NC}"
    echo ""
    exit 0
fi
