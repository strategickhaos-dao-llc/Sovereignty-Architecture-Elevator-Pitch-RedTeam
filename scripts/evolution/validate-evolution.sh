#!/bin/bash
# Validation Script for Evolution Roadmap Implementation
# Tests all weekend evolution items and provides detailed diagnostics

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Counters
PASSED=0
FAILED=0
WARNINGS=0

log_test() {
    echo -e "\n${BLUE}[TEST]${NC} $1"
}

log_pass() {
    echo -e "${GREEN}  ✓${NC} $1"
    ((PASSED++))
}

log_fail() {
    echo -e "${RED}  ✗${NC} $1"
    ((FAILED++))
}

log_warn() {
    echo -e "${YELLOW}  ⚠${NC} $1"
    ((WARNINGS++))
}

# Banner
echo -e "${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    🔍 EVOLUTION ROADMAP VALIDATION                           ║
║    Testing Weekend Implementation (Items #1-10)              ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}\n"

# Test 1: Hardware Prerequisites
log_test "Hardware Prerequisites"

if command -v nvidia-smi &> /dev/null; then
    GPU_INFO=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader | head -1)
    VRAM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader | head -1 | awk '{print $1}')
    
    if [ "$VRAM" -ge 20000 ]; then
        log_pass "GPU detected: $GPU_INFO"
    else
        log_warn "GPU has less than 20GB VRAM: $VRAM MB"
    fi
else
    log_fail "NVIDIA GPU not detected"
fi

TOTAL_RAM=$(free -g | awk '/^Mem:/{print $2}')
if [ "$TOTAL_RAM" -ge 32 ]; then
    log_pass "System RAM: ${TOTAL_RAM}GB"
else
    log_warn "System RAM below 32GB: ${TOTAL_RAM}GB"
fi

AVAILABLE_SPACE=$(df -BG . | tail -1 | awk '{print $4}' | sed 's/G//')
if [ "$AVAILABLE_SPACE" -ge 100 ]; then
    log_pass "Disk space: ${AVAILABLE_SPACE}GB available"
else
    log_warn "Disk space below 100GB: ${AVAILABLE_SPACE}GB"
fi

# Test 2: Item #1 - Ollama 70B Performance
log_test "Item #1: Ollama 70B at 85+ tok/s"

if command -v ollama &> /dev/null; then
    log_pass "Ollama installed"
    
    if ollama list &> /dev/null; then
        log_pass "Ollama service running"
        
        if ollama list | grep -q "70b"; then
            log_pass "70B model available"
            
            # Performance test
            echo "  Testing inference performance..."
            START=$(date +%s.%N)
            OUTPUT=$(timeout 30 ollama run llama2:70b-chat "Count from 1 to 20" --verbose 2>&1 || true)
            END=$(date +%s.%N)
            
            if [ ! -z "$OUTPUT" ]; then
                # Try to extract tokens/sec from output
                if echo "$OUTPUT" | grep -q "tokens per second"; then
                    TOKSEC=$(echo "$OUTPUT" | grep "tokens per second" | tail -1 | awk '{print $1}')
                    if (( $(echo "$TOKSEC > 85" | bc -l 2>/dev/null || echo 0) )); then
                        log_pass "Performance: ${TOKSEC} tok/s (target: 85+)"
                    else
                        log_warn "Performance: ${TOKSEC} tok/s (target: 85+)"
                    fi
                else
                    RUNTIME=$(echo "$END - $START" | bc)
                    log_warn "Could not measure tok/s, runtime: ${RUNTIME}s"
                fi
            else
                log_fail "Inference test timed out or failed"
            fi
        else
            log_fail "70B model not found (run: ollama pull llama2:70b-chat)"
        fi
    else
        log_fail "Ollama service not running"
    fi
else
    log_fail "Ollama not installed"
fi

# Test 3: Item #9 - ComfyUI
log_test "Item #9: ComfyUI Local Image Generation"

if [ -d ~/sovereignty/tools/ComfyUI ] || [ -d ~/tools/ComfyUI ] || [ -d ~/ComfyUI ]; then
    log_pass "ComfyUI directory found"
    
    # Check if running
    if curl -s http://localhost:8188 &> /dev/null; then
        log_pass "ComfyUI server running on port 8188"
    else
        log_warn "ComfyUI not accessible on port 8188"
    fi
    
    # Check for models
    for COMFY_DIR in ~/sovereignty/tools/ComfyUI ~/tools/ComfyUI ~/ComfyUI; do
        if [ -d "$COMFY_DIR/models/checkpoints" ]; then
            MODEL_COUNT=$(ls -1 "$COMFY_DIR/models/checkpoints/"*.safetensors 2>/dev/null | wc -l)
            if [ "$MODEL_COUNT" -gt 0 ]; then
                log_pass "Found $MODEL_COUNT model(s) in checkpoints"
            else
                log_warn "No models found in checkpoints directory"
            fi
            break
        fi
    done
else
    log_fail "ComfyUI not installed"
fi

# Test 4: Item #7 - Meta-Brain
log_test "Item #7: PsycheVille Meta-Brain"

if [ -f ~/sovereignty/psycheville/meta_brain.py ]; then
    log_pass "Meta-Brain script installed"
    
    # Check for reflections
    if [ -d ~/sovereignty/psycheville/reflections ]; then
        REFLECTION_COUNT=$(ls -1 ~/sovereignty/psycheville/reflections/*.json 2>/dev/null | wc -l)
        if [ "$REFLECTION_COUNT" -gt 0 ]; then
            log_pass "Found $REFLECTION_COUNT reflection(s)"
            LATEST=$(ls -t ~/sovereignty/psycheville/reflections/*.json 2>/dev/null | head -1)
            if [ ! -z "$LATEST" ]; then
                AGE_HOURS=$(( ($(date +%s) - $(stat -c %Y "$LATEST")) / 3600 ))
                log_pass "Latest reflection: ${AGE_HOURS}h ago"
            fi
        else
            log_warn "No reflections found (run: python ~/sovereignty/psycheville/meta_brain.py)"
        fi
    else
        log_warn "Reflections directory not found"
    fi
    
    # Check cron
    if crontab -l 2>/dev/null | grep -q "meta_brain.py"; then
        log_pass "Meta-Brain scheduled in cron"
    else
        log_warn "Meta-Brain not scheduled in cron"
    fi
else
    log_fail "Meta-Brain not installed"
fi

# Test 5: Item #10 - Dashboard
log_test "Item #10: Obsidian Live Dashboard"

if [ -f ~/sovereignty/dashboard-server/server.js ]; then
    log_pass "Dashboard server script found"
    
    if curl -s http://localhost:3000/health &> /dev/null; then
        log_pass "Dashboard server running on port 3000"
        
        # Test endpoints
        ENDPOINTS=("ollama" "gpu" "system" "metabrain")
        for EP in "${ENDPOINTS[@]}"; do
            if curl -s "http://localhost:3000/status/$EP" &> /dev/null; then
                log_pass "Endpoint /$EP accessible"
            else
                log_warn "Endpoint /$EP not accessible"
            fi
        done
    else
        log_warn "Dashboard server not running on port 3000"
    fi
else
    log_fail "Dashboard server not installed"
fi

# Test 6: Item #5 - Voice Loop (optional)
log_test "Item #5: Voice Loop Components (Optional)"

if [ -d ~/tools/whisper.cpp ] || [ -d ~/sovereignty/tools/whisper.cpp ]; then
    log_pass "Whisper.cpp found"
else
    log_warn "Whisper.cpp not installed (optional)"
fi

if command -v piper &> /dev/null || [ -f ~/tools/piper/piper ]; then
    log_pass "Piper TTS found"
else
    log_warn "Piper TTS not installed (optional)"
fi

# Test 7: System Services
log_test "System Services & Health"

# Docker
if command -v docker &> /dev/null; then
    log_pass "Docker installed"
    if docker ps &> /dev/null; then
        CONTAINER_COUNT=$(docker ps -q | wc -l)
        log_pass "Docker running with $CONTAINER_COUNT container(s)"
    else
        log_warn "Docker service not accessible"
    fi
else
    log_warn "Docker not installed"
fi

# k3s
if command -v kubectl &> /dev/null; then
    log_pass "kubectl installed"
    if kubectl get nodes &> /dev/null 2>&1; then
        NODE_COUNT=$(kubectl get nodes --no-headers 2>/dev/null | wc -l)
        log_pass "k3s cluster with $NODE_COUNT node(s)"
    else
        log_warn "k3s cluster not accessible"
    fi
else
    log_warn "kubectl not installed (k3s optional)"
fi

# Test 8: Monitoring & Logs
log_test "Monitoring & Logging"

if [ -d ~/sovereignty/logs ]; then
    log_pass "Logs directory exists"
    LOG_SIZE=$(du -sh ~/sovereignty/logs 2>/dev/null | awk '{print $1}')
    log_pass "Log size: $LOG_SIZE"
else
    log_warn "Logs directory not found"
fi

# Test 9: Network Connectivity
log_test "Network Connectivity"

if ping -c 1 8.8.8.8 &> /dev/null; then
    log_pass "Internet connectivity"
else
    log_warn "No internet connectivity"
fi

if curl -s https://ollama.com &> /dev/null; then
    log_pass "Can reach Ollama registry"
else
    log_warn "Cannot reach Ollama registry"
fi

# Test 10: Security Basics
log_test "Security Configuration"

if command -v ufw &> /dev/null; then
    if sudo ufw status 2>/dev/null | grep -q "Status: active"; then
        log_pass "Firewall active"
    else
        log_warn "Firewall not active"
    fi
else
    log_warn "UFW firewall not installed"
fi

# Summary
echo -e "\n${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                    VALIDATION SUMMARY                         ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${GREEN}Passed:${NC} $PASSED tests"
echo -e "${YELLOW}Warnings:${NC} $WARNINGS items"
echo -e "${RED}Failed:${NC} $FAILED tests"
echo ""

# Calculate score
TOTAL=$((PASSED + FAILED))
if [ $TOTAL -gt 0 ]; then
    SCORE=$((PASSED * 100 / TOTAL))
    echo -e "Score: ${SCORE}%"
    
    if [ $SCORE -ge 90 ]; then
        echo -e "${GREEN}🎉 Excellent! Weekend evolution complete!${NC}"
    elif [ $SCORE -ge 70 ]; then
        echo -e "${YELLOW}⚡ Good progress! A few items need attention.${NC}"
    else
        echo -e "${RED}🔧 More setup needed. Review failed tests above.${NC}"
    fi
fi

echo ""
echo "Next steps:"
echo "  1. Address any failed tests above"
echo "  2. Review warnings for optimization"
echo "  3. Continue with items #11-20"
echo "  4. Join Discord: #evolution-general"
echo ""
echo "Documentation:"
echo "  - Evolution Roadmap: $ROOT_DIR/EVOLUTION_ROADMAP.md"
echo "  - Weekend Guide: $ROOT_DIR/docs/evolution/WEEKEND_QUICKSTART.md"
echo "  - Quick Reference: $ROOT_DIR/docs/evolution/QUICK_REFERENCE.md"
echo ""

# Exit code
if [ $FAILED -eq 0 ]; then
    exit 0
else
    exit 1
fi
