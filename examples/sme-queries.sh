#!/bin/bash
# Example queries for the SME RAG API
# Demonstrates how to query the sovereign infrastructure knowledge base

API_URL="${SME_RAG_API_URL:-http://localhost:8090}"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}SME RAG API Example Queries${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# Function to query and display
query() {
    local question="$1"
    local max_results="${2:-5}"
    
    echo -e "${BLUE}Q: ${question}${NC}"
    
    response=$(curl -s -X POST "${API_URL}/query" \
        -H "Content-Type: application/json" \
        -d "{
            \"question\": \"${question}\",
            \"max_results\": ${max_results}
        }")
    
    if [ $? -eq 0 ]; then
        # Extract answer
        answer=$(echo "$response" | jq -r '.answer' 2>/dev/null)
        sources=$(echo "$response" | jq -r '.sources[].title' 2>/dev/null)
        
        if [ -n "$answer" ]; then
            echo -e "${GREEN}A:${NC} ${answer:0:500}..."
            echo ""
            echo "Sources:"
            echo "$sources" | sed 's/^/  - /'
        else
            echo "Error: Unable to parse response"
            echo "$response"
        fi
    else
        echo "Error: Failed to query API"
    fi
    
    echo ""
    echo "---"
    echo ""
}

# Evolution Path Queries
echo -e "${BLUE}=== Evolution Path Queries ===${NC}"
echo ""

query "How do I set up an 8-node k3s cluster with Longhorn storage?" 5

query "What are the steps to implement zero-trust networking with Tailscale?" 5

query "How can I deploy Ollama with GPU scheduling across multiple nodes?" 5

# Infrastructure Queries
echo -e "${BLUE}=== Infrastructure Queries ===${NC}"
echo ""

query "What is the best way to implement high availability storage for Kubernetes?" 5

query "How do I configure Traefik as a reverse proxy with automatic TLS?" 5

query "What are the options for distributed storage systems?" 5

# AI/ML Queries
echo -e "${BLUE}=== AI/ML Queries ===${NC}"
echo ""

query "How do I fine-tune a 7B parameter model on custom data?" 5

query "What are the best practices for deploying large language models locally?" 5

query "How can I implement RAG with vector databases?" 5

# Security Queries
echo -e "${BLUE}=== Security Queries ===${NC}"
echo ""

query "What are NIST recommendations for securing container deployments?" 5

query "How do I implement zero-knowledge encryption for data at rest?" 5

query "What are the best practices for secrets management in Kubernetes?" 5

# Monitoring Queries
echo -e "${BLUE}=== Monitoring Queries ===${NC}"
echo ""

query "How do I set up Prometheus and Grafana for infrastructure monitoring?" 5

query "What is the best way to implement distributed tracing?" 5

query "How can I aggregate logs from multiple services?" 5

# IoT & RF Queries
echo -e "${BLUE}=== IoT & RF Queries ===${NC}"
echo ""

query "How do I set up RTL-SDR for radio frequency monitoring?" 5

query "What are the basics of software defined radio?" 5

query "How can I integrate RF sensors with my infrastructure?" 5

echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}Query examples complete!${NC}"
echo -e "${GREEN}======================================${NC}"
