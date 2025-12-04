#!/bin/bash
# SKOS Immune System - One-Command Deployment
# Sovereign Khaos Operating System v0.1.0
#
# Usage: ./deploy.sh [options]
#
# Options:
#   --build     Force rebuild of Docker images
#   --clean     Remove existing containers before deploying
#   --help      Show this help message
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

# Banner
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          SKOS IMMUNE SYSTEM DEPLOYMENT v0.1.0               ║"
echo "║      Sovereign Khaos Operating System                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Parse arguments
BUILD_FLAG=""
CLEAN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --build)
            BUILD_FLAG="--build"
            shift
            ;;
        --clean)
            CLEAN=true
            shift
            ;;
        --help)
            echo "Usage: ./deploy.sh [options]"
            echo ""
            echo "Options:"
            echo "  --build     Force rebuild of Docker images"
            echo "  --clean     Remove existing containers before deploying"
            echo "  --help      Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Check prerequisites
echo -e "${YELLOW}[1/5] Checking prerequisites...${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}ERROR: Docker is not installed${NC}"
    echo "Install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} Docker installed"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}ERROR: Docker Compose is not installed${NC}"
    echo "Install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} Docker Compose installed"

# Determine compose command
if docker compose version &> /dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo -e "${RED}ERROR: Docker daemon is not running${NC}"
    echo "Start Docker and try again"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} Docker daemon running"

# Clean existing deployment if requested
if [ "$CLEAN" = true ]; then
    echo -e "${YELLOW}[2/5] Cleaning existing deployment...${NC}"
    $COMPOSE_CMD down -v --remove-orphans 2>/dev/null || true
    echo -e "  ${GREEN}✓${NC} Cleaned"
else
    echo -e "${YELLOW}[2/5] Skipping clean (use --clean to remove existing)${NC}"
fi

# Build/pull images
echo -e "${YELLOW}[3/5] Building Docker images...${NC}"
$COMPOSE_CMD build $BUILD_FLAG
echo -e "  ${GREEN}✓${NC} Images built"

# Start services
echo -e "${YELLOW}[4/5] Starting services...${NC}"
$COMPOSE_CMD up -d

# Wait for services to be healthy
echo -e "${YELLOW}[5/5] Waiting for services to be healthy...${NC}"

# Wait for NATS
echo -n "  Waiting for NATS..."
for i in {1..30}; do
    if curl -s http://localhost:8222/healthz > /dev/null 2>&1; then
        echo -e " ${GREEN}✓${NC}"
        break
    fi
    sleep 1
    echo -n "."
done

# Check if NATS is up
if ! curl -s http://localhost:8222/healthz > /dev/null 2>&1; then
    echo -e " ${RED}✗${NC}"
    echo -e "${RED}WARNING: NATS health check failed, but continuing...${NC}"
fi

# Wait for containers to stabilize
sleep 3

# Show status
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗"
echo "║                    DEPLOYMENT COMPLETE!                       ║"
echo "╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Services:${NC}"
$COMPOSE_CMD ps
echo ""
echo -e "${BLUE}Endpoints:${NC}"
echo "  NATS Client:     nats://localhost:4222"
echo "  NATS Monitor:    http://localhost:8222"
echo ""
echo -e "${BLUE}Commands:${NC}"
echo "  View logs:       $COMPOSE_CMD logs -f"
echo "  View status:     $COMPOSE_CMD ps"
echo "  Stop:            $COMPOSE_CMD down"
echo "  Run tests:       ./test.sh"
echo ""
echo -e "${GREEN}Your sovereign immune system is now active! 🛡️${NC}"
