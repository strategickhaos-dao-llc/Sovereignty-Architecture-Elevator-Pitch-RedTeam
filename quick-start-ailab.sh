#!/bin/bash
# Quick Start Script for AI Lab Enhancement
# Deploys sovereign AI research infrastructure

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
cat << "EOF"
   ___   ____   __         __  
  / _ | /  _/  / /  ___ _ / /  
 / __ |_/ /   / /__/ _ `/ _ \ 
/_/ |_/___/  /____/\_,_/_.__/ 
                              
Sovereign AI Research Lab
EOF
echo -e "${NC}"

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites met${NC}"

# Menu
echo ""
echo -e "${BLUE}Select deployment option:${NC}"
echo "1) Full Stack (All Services)"
echo "2) Core + Modelfiles Only"
echo "3) Core + VoiceWing"
echo "4) Core + Filesystem Agents"
echo "5) Core + Automation (Selenium)"
echo "6) Core + Advanced RAG"
echo "7) Core + Security Stack"
echo "8) Custom (Select Services)"
echo "9) Stop All Services"
echo "0) Exit"

read -p "Enter choice [0-9]: " choice

case $choice in
    1)
        echo -e "${YELLOW}Deploying Full Stack...${NC}"
        docker-compose \
            -f docker-compose.yml \
            -f docker-compose.voicewing.yml \
            -f docker-compose.agents.yml \
            -f docker-compose.automation.yml \
            -f docker-compose.rag.yml \
            -f docker-compose.security.yml \
            up -d
        ;;
    2)
        echo -e "${YELLOW}Deploying Core + Modelfiles...${NC}"
        docker-compose -f docker-compose.yml up -d
        
        # Check if Ollama is installed
        if command -v ollama &> /dev/null; then
            echo -e "${GREEN}Building uncensored models...${NC}"
            cd modelfiles
            ollama create llama31-unhinged -f Llama-3.1-405B-Unhinged.Modelfile 2>/dev/null || echo "Base model not available"
            ollama create mistral-jailbreak -f Mistral-Large-Jailbreak.Modelfile 2>/dev/null || echo "Base model not available"
            ollama create abliterated -f Abliterated-Refusal-Free.Modelfile 2>/dev/null || echo "Base model not available"
            ollama create say-yes -f Say-Yes-To-Anything.Modelfile 2>/dev/null || echo "Base model not available"
            cd ..
        else
            echo -e "${YELLOW}Ollama not installed. Install from: https://ollama.com${NC}"
        fi
        ;;
    3)
        echo -e "${YELLOW}Deploying Core + VoiceWing...${NC}"
        docker-compose -f docker-compose.yml -f docker-compose.voicewing.yml up -d
        ;;
    4)
        echo -e "${YELLOW}Deploying Core + Filesystem Agents...${NC}"
        docker-compose -f docker-compose.yml -f docker-compose.agents.yml up -d
        ;;
    5)
        echo -e "${YELLOW}Deploying Core + Automation...${NC}"
        docker-compose -f docker-compose.yml -f docker-compose.automation.yml up -d
        ;;
    6)
        echo -e "${YELLOW}Deploying Core + Advanced RAG...${NC}"
        docker-compose -f docker-compose.yml -f docker-compose.rag.yml up -d
        ;;
    7)
        echo -e "${YELLOW}Deploying Core + Security...${NC}"
        docker-compose -f docker-compose.yml -f docker-compose.security.yml up -d
        ;;
    8)
        echo -e "${YELLOW}Custom deployment...${NC}"
        echo "Select services to deploy (space-separated numbers):"
        echo "1) Core  2) VoiceWing  3) Agents  4) Automation  5) RAG  6) Security"
        read -p "Enter selections: " selections
        
        compose_files="-f docker-compose.yml"
        for sel in $selections; do
            case $sel in
                2) compose_files="$compose_files -f docker-compose.voicewing.yml" ;;
                3) compose_files="$compose_files -f docker-compose.agents.yml" ;;
                4) compose_files="$compose_files -f docker-compose.automation.yml" ;;
                5) compose_files="$compose_files -f docker-compose.rag.yml" ;;
                6) compose_files="$compose_files -f docker-compose.security.yml" ;;
            esac
        done
        
        docker-compose $compose_files up -d
        ;;
    9)
        echo -e "${YELLOW}Stopping all services...${NC}"
        docker-compose \
            -f docker-compose.yml \
            -f docker-compose.voicewing.yml \
            -f docker-compose.agents.yml \
            -f docker-compose.automation.yml \
            -f docker-compose.rag.yml \
            -f docker-compose.security.yml \
            down
        echo -e "${GREEN}All services stopped${NC}"
        exit 0
        ;;
    0)
        echo -e "${BLUE}Exiting...${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

# Wait for services to start
echo -e "${YELLOW}Waiting for services to start...${NC}"
sleep 10

# Check service health
echo ""
echo -e "${BLUE}Service Status:${NC}"
docker-compose ps

# Display access information
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}   AI Lab Deployment Complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}Access Points:${NC}"

# Core services
if docker ps | grep -q "postgres"; then
    echo -e "  ${GREEN}✓${NC} Core Infrastructure: Running"
fi

# VoiceWing
if docker ps | grep -q "voicewing-webui"; then
    echo -e "  ${GREEN}✓${NC} Voice WebUI: http://localhost:8080"
    echo -e "  ${GREEN}✓${NC} Whisper API: http://localhost:9000"
fi

# Agents
if docker ps | grep -q "agents-orchestrator"; then
    echo -e "  ${GREEN}✓${NC} Agent Orchestrator: http://localhost:8010"
    echo -e "  ${GREEN}✓${NC} Semantic Search: http://localhost:8004"
fi

# Automation
if docker ps | grep -q "automation-selenium-hub"; then
    echo -e "  ${GREEN}✓${NC} Selenium Grid: http://localhost:4444"
    echo -e "  ${GREEN}✓${NC} Chrome VNC: http://localhost:7900"
fi

# RAG
if docker ps | grep -q "rag-orchestrator"; then
    echo -e "  ${GREEN}✓${NC} RAG Orchestrator: http://localhost:8210"
    echo -e "  ${GREEN}✓${NC} PrivateGPT: http://localhost:8001"
    echo -e "  ${GREEN}✓${NC} AnythingLLM: http://localhost:3001"
fi

# Security
if docker ps | grep -q "security-caddy"; then
    echo -e "  ${GREEN}✓${NC} Caddy Admin: http://localhost:2019"
    echo -e "  ${GREEN}✓${NC} Vault: http://localhost:8200"
    echo -e "  ${GREEN}✓${NC} Security Dashboard: http://localhost:8300"
fi

echo ""
echo -e "${YELLOW}📚 Documentation:${NC}"
echo -e "  - Complete Guide: AI_LAB_GUIDE.md"
echo -e "  - Modelfiles: modelfiles/README.md"
echo -e "  - RAG Configs: rag-configs/README.md"
echo ""
echo -e "${BLUE}🔐 Security Note:${NC}"
echo -e "  These are uncensored research tools."
echo -e "  Use in isolated environments only."
echo -e "  Follow all applicable laws and ethical guidelines."
echo ""
echo -e "${GREEN}Happy researching! 🚀🔬${NC}"
