#!/bin/bash
# Demo script for Sovereignty Architecture Data Pipeline
# This script demonstrates the complete data flow with sample files

set -e

echo "============================================================"
echo "🎬 Sovereignty Architecture - Data Pipeline Demo"
echo "============================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if setup was run
if [ ! -d "ingest" ] || [ ! -d "logs" ]; then
    echo -e "${YELLOW}⚠️  Setup not complete. Running setup first...${NC}"
    ./setup_data_pipeline.sh
    echo ""
fi

echo -e "${BLUE}📚 This demo will:${NC}"
echo "1. Create sample files representing different knowledge domains"
echo "2. Place them in the ingest folder"
echo "3. Run the ingest daemon to process them"
echo "4. Show the results: classified files, generated notes, and logs"
echo ""
read -p "Press Enter to continue..." -r
echo ""

# Step 1: Create sample files
echo "============================================================"
echo "Step 1: Creating sample files"
echo "============================================================"
echo ""

# Cyber security file
cat > ingest/cve-2024-critical-vulnerability-report.txt << 'EOF'
Critical Vulnerability Report

CVE-2024-12345: Remote Code Execution in XYZ Framework

Severity: Critical
Impact: Remote attackers can execute arbitrary code
Affected Versions: 1.0 - 2.5
Mitigation: Update to version 2.6 or apply security patch

This is a simulated vulnerability report for demonstration purposes.
EOF
echo "✅ Created: cve-2024-critical-vulnerability-report.txt (Cyber Recon)"

# Architecture document
cat > ingest/kubernetes-microservices-architecture-design.md << 'EOF'
# Kubernetes Microservices Architecture

## Overview

This document outlines the architecture for a microservices deployment on Kubernetes.

## Components

- API Gateway
- Service Mesh (Istio)
- Container Registry
- CI/CD Pipeline

## Design Patterns

- Circuit Breaker
- Service Discovery
- Load Balancing
EOF
echo "✅ Created: kubernetes-microservices-architecture-design.md (Architecture)"

# AI/ML research
cat > ingest/llm-fine-tuning-research-notes.txt << 'EOF'
LLM Fine-Tuning Research Notes

Techniques explored:
- LoRA (Low-Rank Adaptation)
- QLoRA (Quantized LoRA)
- Full fine-tuning vs parameter-efficient methods

Results show that LoRA achieves 95% of full fine-tuning performance
with only 0.1% of trainable parameters.

Model: Llama 2 7B
Dataset: Custom domain-specific corpus
Training time: 4 hours on A100 GPU
EOF
echo "✅ Created: llm-fine-tuning-research-notes.txt (AI/ML Research)"

# DevOps pipeline
cat > ingest/cicd-pipeline-automation-guide.txt << 'EOF'
CI/CD Pipeline Automation Guide

Pipeline Stages:
1. Source checkout
2. Build & compile
3. Unit tests
4. Integration tests
5. Security scanning
6. Docker image build
7. Push to registry
8. Deploy to staging
9. Smoke tests
10. Deploy to production

Tools: GitHub Actions, Docker, Kubernetes, ArgoCD
EOF
echo "✅ Created: cicd-pipeline-automation-guide.txt (DevOps)"

# Legal/governance
cat > ingest/dao-governance-proposal-template.yaml << 'EOF'
# DAO Governance Proposal Template

proposal_id: PROP-001
title: "Implement New Voting Mechanism"
author: "Strategic Khaos DAO"
status: draft

summary: |
  This proposal suggests implementing a new quadratic voting
  mechanism to improve governance participation.

voting_period: 7 days
quorum_required: 51%

options:
  - approve
  - reject
  - abstain
EOF
echo "✅ Created: dao-governance-proposal-template.yaml (Legal/Governance)"

# Business strategy
cat > ingest/revenue-model-contradiction-resolution.txt << 'EOF'
Revenue Model: Contradiction Resolution

Core Tension: Privacy vs Personalization
Resolution: "Tailored for you - never tracked"
Technical Implementation: Local-first ML models
Pricing: $0 logs → $9/mo sync

Market Analysis:
- Target: Privacy-conscious professionals
- Competitive advantage: True local-first architecture
- Revenue projection: $50k MRR by Q2

KPIs:
- Conversion rate: 5% free → paid
- Churn rate: <3% monthly
- NPS: >70
EOF
echo "✅ Created: revenue-model-contradiction-resolution.txt (Business/Strategy)"

echo ""
echo -e "${GREEN}✅ All sample files created${NC}"
echo ""
read -p "Press Enter to process files..." -r
echo ""

# Step 2: Run the daemon
echo "============================================================"
echo "Step 2: Processing files with ingest daemon"
echo "============================================================"
echo ""

python3 ingest_daemon.py --once

echo ""
echo -e "${GREEN}✅ All files processed${NC}"
echo ""
read -p "Press Enter to view results..." -r
echo ""

# Step 3: Show results
echo "============================================================"
echo "Step 3: Viewing results"
echo "============================================================"
echo ""

echo -e "${BLUE}📁 Vault structure:${NC}"
if [ -d "vault/labs" ]; then
    tree vault/labs/ -L 2 2>/dev/null || find vault/labs/ -type f
else
    echo "   (Vault directory not created - files may be in different location)"
fi
echo ""

echo -e "${BLUE}📊 Processing logs:${NC}"
if [ -f "logs/ingest_events.jsonl" ]; then
    echo "   Total files processed: $(wc -l < logs/ingest_events.jsonl)"
    echo ""
    echo "   Lab distribution:"
    cat logs/ingest_events.jsonl | jq -r '.data.lab' | sort | uniq -c | sort -rn
    echo ""
    echo "   Average confidence: $(cat logs/ingest_events.jsonl | jq '.data.confidence' | awk '{sum+=$1; n++} END {printf "%.2f", sum/n}')"
else
    echo "   No logs found"
fi
echo ""

echo -e "${BLUE}📝 Sample generated note:${NC}"
if [ -d "vault/labs" ]; then
    SAMPLE_NOTE=$(find vault/labs -name "*_note.md" -type f | head -1)
    if [ -n "$SAMPLE_NOTE" ]; then
        echo "   File: $SAMPLE_NOTE"
        echo ""
        head -20 "$SAMPLE_NOTE"
    else
        echo "   No notes found"
    fi
else
    echo "   Vault not found"
fi
echo ""

# Step 4: Git status
echo "============================================================"
echo "Step 4: Git status"
echo "============================================================"
echo ""

if command -v git &> /dev/null; then
    echo -e "${BLUE}📚 Recent commits:${NC}"
    git --no-pager log --oneline -5 2>/dev/null || echo "   Not a git repository or no commits yet"
    echo ""
    
    echo -e "${BLUE}📊 Repository status:${NC}"
    git --no-pager status -s 2>/dev/null || echo "   Not a git repository"
else
    echo "   Git not available"
fi
echo ""

# Completion
echo "============================================================"
echo "✅ Demo Complete!"
echo "============================================================"
echo ""
echo -e "${GREEN}🎉 You've successfully demonstrated the data pipeline!${NC}"
echo ""
echo "What happened:"
echo "1. ✅ Created 6 sample files covering different knowledge domains"
echo "2. ✅ Daemon classified each file based on keywords"
echo "3. ✅ Files routed to appropriate labs in the vault"
echo "4. ✅ Generated Obsidian notes with metadata and tags"
echo "5. ✅ Logged all events to JSONL file"
echo "6. ✅ Git commits tracked the changes"
echo ""
echo "Next steps:"
echo "• Explore the vault structure: ls -R vault/"
echo "• Review logs: cat logs/ingest_events.jsonl | jq ."
echo "• Customize labs: edit lab.yaml"
echo "• Start daemon continuously: python3 ingest_daemon.py"
echo "• Read full docs: ARCHITECTURE_DATA_PIPELINE.md"
echo ""
echo "Clean up test data:"
echo "  rm -rf vault/ logs/ ingest/"
echo ""
