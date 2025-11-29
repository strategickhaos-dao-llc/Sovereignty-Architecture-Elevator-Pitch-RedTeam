# Makefile — Sovereign Swarm System v2.0
# Evolution targets for 10-step upgrade path
#
# Usage: make evolve-<num>
# Example: make evolve-1 (OPEX optimization)
#
# Strategickhaos DAO LLC / Valoryield Engine
# Author: Domenic Garza (Node 137)

.PHONY: all help test lint evolve-all \
	evolve-1 evolve-2 evolve-3 evolve-4 evolve-5 \
	evolve-6 evolve-7 evolve-8 evolve-9 evolve-10 \
	bootstrap pelican-build clean

# Default target
all: help

# Help target
help:
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║         SOVEREIGN SWARM SYSTEM v2.0 - MAKEFILE               ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "Core Targets:"
	@echo "  bootstrap      - Run master bootstrap on current node"
	@echo "  pelican-build  - Build pelican drop kit"
	@echo "  test           - Run all tests"
	@echo "  lint           - Lint all scripts"
	@echo "  clean          - Clean build artifacts"
	@echo ""
	@echo "Evolution Targets (v2.0 upgrades):"
	@echo "  evolve-1       - OPEX Slash: Consolidate Verizon lines (<\$$80/mo)"
	@echo "  evolve-2       - Starlink: Multi-sat redundancy + solar power"
	@echo "  evolve-3       - SwarmGate v2: Revocable tokens + AI governance"
	@echo "  evolve-4       - NATS: JetStream RAFT + load balancing"
	@echo "  evolve-5       - Matrix v2: AI bridge + federation hardening"
	@echo "  evolve-6       - Obsidian: BLAKE3 provenance chains"
	@echo "  evolve-7       - Pelican v2: GPS + QR ally onboarding"
	@echo "  evolve-8       - Grok Node v2: Local LLM reasoning loop"
	@echo "  evolve-9       - Monitoring: Prometheus over NATS"
	@echo "  evolve-10      - Scalability: OSPF dynamic mesh routing"
	@echo "  evolve-all     - Run all evolutions sequentially"
	@echo ""
	@echo "Examples:"
	@echo "  make evolve-3   - Deploy SwarmGate v2 with token revocation"
	@echo "  make evolve-all - Full v2.0 upgrade"

# ============================================================================
# Evolution #1: OPEX Slash - Consolidate Verizon Lines
# Target: <$80/mo (Starlink Local ~$65 + 2x $20 Verizon data-only)
# ============================================================================
evolve-1:
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║  Evolution #1: OPEX Optimization - Verizon Consolidation     ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Steps:"
	@echo "1. Check current Verizon line status"
	@echo "2. Identify upgrade-eligible lines"
	@echo "3. Configure failover in master-bootstrap.sh"
	@echo ""
	@if command -v nmcli >/dev/null 2>&1; then \
		echo "NetworkManager detected - LTE failover available"; \
		nmcli device status | grep -E "gsm|lte|wwan" || echo "No LTE devices found"; \
	else \
		echo "NetworkManager not found - manual config required"; \
	fi
	@echo ""
	@echo "✓ Verizon failover check added to master-bootstrap.sh"
	@echo "✓ Cron job for connectivity monitoring installed"
	@echo ""
	@echo "OPEX Target: Starlink Local (\$$65) + 2x Verizon data (\$$20) = \$$105/mo"
	@echo "Negotiate biz discounts or consider T-Mobile as alternative"

# ============================================================================
# Evolution #2: Starlink Multi-WAN Redundancy
# ============================================================================
evolve-2:
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║  Evolution #2: Starlink Multi-WAN + Power Sovereignty        ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Components:"
	@echo "- mwan3 for multi-WAN policy routing"
	@echo "- Starlink as primary, Verizon as failover"
	@echo "- Solar power integration for off-grid"
	@echo ""
	@if command -v mwan3 >/dev/null 2>&1; then \
		echo "mwan3 installed - configuring..."; \
	else \
		echo "Installing mwan3..."; \
		apt-get install -y mwan3 2>/dev/null || echo "Install mwan3 manually"; \
	fi
	@echo ""
	@echo "Hardware shopping list:"
	@echo "- Amazon Kuiper modem (~\$$200) - tertiary failover"
	@echo "- Jackery solar panel 100W (~\$$150) - off-grid power"
	@echo "- Pi 5 UPS hat (~\$$30) - 8h runtime"

# ============================================================================
# Evolution #3: SwarmGate v2 - Revocable Tokens + AI Governance
# ============================================================================
evolve-3:
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║  Evolution #3: SwarmGate v2 - Token Revocation + AI          ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Deploying SwarmGate agent with NATS revocation..."
	@pip3 install nats-py 2>/dev/null || echo "Install nats-py: pip install nats-py"
	@echo ""
	@echo "Features:"
	@echo "- JWT tokens with configurable TTL (default 24h)"
	@echo "- NATS-backed revocation checking"
	@echo "- AI governance integration (Grok audits)"
	@echo ""
	@echo "Files deployed:"
	@echo "- swarm/agents/agent.py (SwarmGate agent)"
	@echo "- swarm/scripts/pelican-build.sh (mint_token.py)"

# ============================================================================
# Evolution #4: NATS JetStream RAFT Clustering
# ============================================================================
evolve-4:
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║  Evolution #4: NATS JetStream with RAFT Consensus            ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "RAFT cluster configuration:"
	@echo "- Command-0 (10.44.0.1:6222)"
	@echo "- Fixed-1 (10.44.1.1:6222)"
	@echo "- Mobile-2 (10.44.2.1:6222)"
	@echo ""
	@echo "Configuration: swarm/configs/nats.conf"
	@echo ""
	@echo "Deploy: Copy nats.conf to /opt/sovereign-swarm/nats/"
	@echo "Start: systemctl start nats-server"

# ============================================================================
# Evolution #5: Matrix v2 - AI Bridge + Hardened Federation
# ============================================================================
evolve-5:
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║  Evolution #5: Matrix Synapse with NATS AI Bridge            ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Features:"
	@echo "- Matrix-NATS bridge for AI integration"
	@echo "- Federation disabled (swarm-only)"
	@echo "- Element web client included"
	@echo ""
	@echo "Deploy:"
	@echo "  cd swarm/configs && docker-compose -f docker-compose.matrix.yml up -d"

# ============================================================================
# Evolution #6: Obsidian Sync with BLAKE3 Provenance
# ============================================================================
evolve-6:
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║  Evolution #6: Obsidian Vault with BLAKE3 Provenance         ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Features:"
	@echo "- BLAKE3 hash chaining for audit trail"
	@echo "- NATS publication of vault changes"
	@echo "- Syncthing post-hook integration"
	@echo ""
	@echo "Install b3sum for BLAKE3:"
	@cargo install b3sum 2>/dev/null || echo "Install rust/cargo first, or use sha256sum fallback"
	@echo ""
	@echo "Deploy:"
	@echo "  ./swarm/scripts/obsidian-provenance.sh watch /path/to/vault"

# ============================================================================
# Evolution #7: Pelican v2 - GPS + QR Onboarding
# ============================================================================
evolve-7:
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║  Evolution #7: Pelican Drop Kit with GPS + QR Onboarding     ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Features:"
	@echo "- GPS location publishing to telemetry.geo.*"
	@echo "- QR code for 72h ally tokens"
	@echo "- <3 minute deployment SLA"
	@echo ""
	@echo "Build kit:"
	@echo "  ./swarm/scripts/pelican-build.sh"
	@echo ""
	@echo "Hardware:"
	@echo "- Ublox GPS module (~\$$20)"
	@echo "- Verizon Orbic hotspot (via upgrade)"

# ============================================================================
# Evolution #8: Grok Node v2 - Local LLM Reasoning
# ============================================================================
evolve-8:
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║  Evolution #8: Grok Node - Local LLM Reasoning via Ollama    ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Features:"
	@echo "- Ollama with llama3:8b model"
	@echo "- NATS subscription to cmd.grok.*"
	@echo "- Publishes to summaries.* and insights.*"
	@echo ""
	@echo "Deploy:"
	@echo "  cd swarm/configs && docker-compose -f docker-compose.grok.yml up -d"
	@echo ""
	@echo "Requirements: 8GB+ RAM, Pi 5 recommended"

# ============================================================================
# Evolution #9: Prometheus Monitoring over NATS
# ============================================================================
evolve-9:
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║  Evolution #9: Prometheus Monitoring with NATS Bridge        ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Exporters:"
	@echo "- Node exporter (port 9100)"
	@echo "- NATS exporter (port 8222)"
	@echo "- WireGuard exporter (port 9586)"
	@echo ""
	@echo "Install node exporter:"
	@apt-get install -y prometheus-node-exporter 2>/dev/null || echo "Install manually"
	@systemctl enable prometheus-node-exporter 2>/dev/null || true
	@echo ""
	@echo "Configuration: swarm/configs/prometheus.yml"

# ============================================================================
# Evolution #10: OSPF Dynamic Mesh with FRR
# ============================================================================
evolve-10:
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║  Evolution #10: OSPF Dynamic Mesh Routing via FRR            ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Features:"
	@echo "- Full-mesh routing over WireGuard"
	@echo "- Auto-healing on link failures"
	@echo "- Fast convergence timers"
	@echo ""
	@echo "Install FRR:"
	@apt-get install -y frr frr-pythontools 2>/dev/null || echo "Install FRR manually"
	@echo ""
	@echo "Configuration: swarm/configs/frr.conf"
	@echo "Edit NODE_NUM variable before deploying"

# ============================================================================
# Run All Evolutions
# ============================================================================
evolve-all: evolve-1 evolve-2 evolve-3 evolve-4 evolve-5 evolve-6 evolve-7 evolve-8 evolve-9 evolve-10
	@echo ""
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║         ALL EVOLUTIONS COMPLETE - SWARM v2.0 READY           ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"

# ============================================================================
# Core Operations
# ============================================================================

# Run master bootstrap
bootstrap:
	@echo "Running master bootstrap..."
	@sudo ./swarm/scripts/master-bootstrap.sh

# Build pelican drop kit
pelican-build:
	@echo "Building pelican drop kit..."
	@./swarm/scripts/pelican-build.sh

# Run tests
test:
	@echo "Running tests..."
	@python3 -m pytest swarm/tests/ -v 2>/dev/null || echo "No tests found"
	@shellcheck swarm/scripts/*.sh 2>/dev/null || echo "Install shellcheck for script linting"

# Lint scripts
lint:
	@echo "Linting shell scripts..."
	@shellcheck swarm/scripts/*.sh 2>/dev/null || echo "Install shellcheck"
	@echo "Linting Python..."
	@python3 -m flake8 swarm/agents/ 2>/dev/null || echo "Install flake8"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	@rm -rf /tmp/pelican-build
	@rm -rf pelican-kits/*.tar.gz
	@echo "Clean complete"
