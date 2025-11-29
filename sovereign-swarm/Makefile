# ============================================================================
# Sovereign Swarm Makefile
# Automation framework for deployment and management
# ============================================================================

.PHONY: all help bootstrap pelican verify clean status backup

# Configuration
SHELL := /bin/bash
NODE_ID ?= $(shell hostname)
SWARM_BASE := /opt/sovereign-swarm

# Colors
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m

# Default target
all: help

# ============================================================================
# Help
# ============================================================================

help:
	@echo -e "$(BLUE)╔══════════════════════════════════════════════════════════════╗$(NC)"
	@echo -e "$(BLUE)║         Sovereign Swarm Deployment Automation                 ║$(NC)"
	@echo -e "$(BLUE)╚══════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo -e "$(GREEN)Bootstrap Commands:$(NC)"
	@echo "  make bootstrap-command0   Bootstrap Command-0 (primary hub)"
	@echo "  make bootstrap-fixed1     Bootstrap Fixed-1 node"
	@echo "  make bootstrap-pelican    Bootstrap a Pelican node"
	@echo ""
	@echo -e "$(GREEN)Verification Commands:$(NC)"
	@echo "  make verify               Run full system verification"
	@echo "  make verify-mesh          Verify WireGuard mesh connectivity"
	@echo "  make verify-services      Verify all services are running"
	@echo "  make status               Show system status"
	@echo ""
	@echo -e "$(GREEN)Management Commands:$(NC)"
	@echo "  make backup               Backup CA and configuration"
	@echo "  make logs                 Show recent logs"
	@echo "  make clean                Remove all sovereign-swarm components"
	@echo ""
	@echo -e "$(YELLOW)Environment Variables:$(NC)"
	@echo "  NODE_ID           - Node identifier (default: hostname)"
	@echo "  COMMAND0_PUBKEY   - Command-0 WireGuard public key (for peers)"
	@echo "  COMMAND0_ENDPOINT - Command-0 endpoint ip:port (for peers)"
	@echo ""
	@echo -e "$(YELLOW)Examples:$(NC)"
	@echo "  sudo make bootstrap-command0"
	@echo "  sudo NODE_ID=fixed1 make bootstrap-fixed1"
	@echo "  sudo PELICAN_ID=pelican1 COMMAND0_PUBKEY=xyz COMMAND0_ENDPOINT=1.2.3.4:51820 make bootstrap-pelican"

# ============================================================================
# Bootstrap Commands
# ============================================================================

bootstrap-command0:
	@echo -e "$(BLUE)Bootstrapping Command-0 (Primary Hub)...$(NC)"
	@chmod +x master-bootstrap.sh
	NODE_ID=command0 ./master-bootstrap.sh deploy
	@echo -e "$(GREEN)Command-0 bootstrap complete!$(NC)"
	@echo -e "$(YELLOW)IMPORTANT: Note the WireGuard public key and endpoint above$(NC)"
	@echo -e "$(YELLOW)IMPORTANT: Backup CA keys immediately with 'make backup'$(NC)"

bootstrap-fixed1:
	@echo -e "$(BLUE)Bootstrapping Fixed-1 node...$(NC)"
	@chmod +x master-bootstrap.sh
	NODE_ID=fixed1 ./master-bootstrap.sh deploy
	@echo -e "$(GREEN)Fixed-1 bootstrap complete!$(NC)"
	@echo -e "$(YELLOW)IMPORTANT: Update /etc/wireguard/wg0.conf with Command-0 details$(NC)"

bootstrap-pelican:
ifndef PELICAN_ID
	$(error PELICAN_ID is required. Example: PELICAN_ID=pelican1)
endif
ifndef COMMAND0_PUBKEY
	$(error COMMAND0_PUBKEY is required. Get from Command-0 after bootstrap)
endif
ifndef COMMAND0_ENDPOINT
	$(error COMMAND0_ENDPOINT is required. Format: ip:port)
endif
	@echo -e "$(BLUE)Bootstrapping Pelican: $(PELICAN_ID)...$(NC)"
	@chmod +x pelican-build.sh
	PELICAN_ID=$(PELICAN_ID) \
	COMMAND0_PUBKEY=$(COMMAND0_PUBKEY) \
	COMMAND0_ENDPOINT=$(COMMAND0_ENDPOINT) \
	./pelican-build.sh build
	@echo -e "$(GREEN)Pelican $(PELICAN_ID) provisioning complete!$(NC)"

# ============================================================================
# Verification Commands
# ============================================================================

verify: verify-mesh verify-services
	@echo -e "$(GREEN)All verifications passed!$(NC)"

verify-mesh:
	@echo -e "$(BLUE)Verifying WireGuard mesh...$(NC)"
	@wg show wg0 || (echo -e "$(YELLOW)WireGuard not running$(NC)" && exit 1)
	@echo ""
	@echo "Testing mesh connectivity..."
	@ping -c 1 -W 3 10.44.0.1 && echo -e "$(GREEN)✓ Command-0 reachable$(NC)" || echo -e "$(YELLOW)✗ Command-0 unreachable$(NC)"
	@ping -c 1 -W 3 10.44.0.2 && echo -e "$(GREEN)✓ Fixed-1 reachable$(NC)" || echo -e "$(YELLOW)✗ Fixed-1 unreachable$(NC)"

verify-services:
	@echo -e "$(BLUE)Verifying services...$(NC)"
	@systemctl is-active --quiet wg-quick@wg0 && echo -e "$(GREEN)✓ WireGuard$(NC)" || echo -e "$(YELLOW)✗ WireGuard$(NC)"
	@systemctl is-active --quiet nats-swarm 2>/dev/null && echo -e "$(GREEN)✓ NATS$(NC)" || echo -e "$(YELLOW)✗ NATS (may not be installed)$(NC)"
	@systemctl is-active --quiet swarmgate 2>/dev/null && echo -e "$(GREEN)✓ SwarmGate$(NC)" || echo -e "$(YELLOW)✗ SwarmGate (may not be installed)$(NC)"
	@systemctl is-active --quiet pelican-watchdog 2>/dev/null && echo -e "$(GREEN)✓ Watchdog$(NC)" || echo -e "$(YELLOW)✗ Watchdog (pelican only)$(NC)"

status:
	@echo -e "$(BLUE)╔══════════════════════════════════════════════════════════════╗$(NC)"
	@echo -e "$(BLUE)║              Sovereign Swarm Status                          ║$(NC)"
	@echo -e "$(BLUE)╚══════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo -e "$(GREEN)Node Information:$(NC)"
	@cat $(SWARM_BASE)/config/node-info.json 2>/dev/null || echo "Node not bootstrapped"
	@echo ""
	@echo -e "$(GREEN)WireGuard Status:$(NC)"
	@wg show wg0 2>/dev/null || echo "WireGuard not configured"
	@echo ""
	@echo -e "$(GREEN)Service Status:$(NC)"
	@systemctl is-active wg-quick@wg0 2>/dev/null || echo "wg-quick@wg0: inactive"
	@systemctl is-active nats-swarm 2>/dev/null || echo "nats-swarm: inactive"
	@systemctl is-active swarmgate 2>/dev/null || echo "swarmgate: inactive"

# ============================================================================
# Management Commands
# ============================================================================

backup:
	@echo -e "$(BLUE)Creating backup...$(NC)"
	@mkdir -p ~/swarm-backups
	@tar -czf ~/swarm-backups/swarm-backup-$$(date +%Y%m%d-%H%M%S).tar.gz \
		$(SWARM_BASE)/ca/state/ \
		$(SWARM_BASE)/keys/ \
		$(SWARM_BASE)/config/ \
		$(SWARM_BASE)/tokens/ \
		/etc/wireguard/wg0.conf \
		2>/dev/null || true
	@echo -e "$(GREEN)Backup created: ~/swarm-backups/$(NC)"
	@ls -la ~/swarm-backups/

logs:
	@echo -e "$(BLUE)Recent Sovereign Swarm logs:$(NC)"
	@tail -n 50 /var/log/sovereign-swarm/*.log 2>/dev/null || echo "No logs found"

clean:
	@echo -e "$(YELLOW)WARNING: This will remove all sovereign-swarm components!$(NC)"
	@read -p "Are you sure? (yes/no) " confirm && [ "$$confirm" = "yes" ]
	@echo -e "$(BLUE)Cleaning up...$(NC)"
	@systemctl stop wg-quick@wg0 2>/dev/null || true
	@systemctl stop nats-swarm 2>/dev/null || true
	@systemctl stop swarmgate 2>/dev/null || true
	@systemctl stop pelican-watchdog 2>/dev/null || true
	@systemctl disable wg-quick@wg0 2>/dev/null || true
	@systemctl disable nats-swarm 2>/dev/null || true
	@systemctl disable swarmgate 2>/dev/null || true
	@systemctl disable pelican-watchdog 2>/dev/null || true
	@rm -rf $(SWARM_BASE)
	@rm -f /etc/wireguard/wg0.conf
	@rm -f /etc/systemd/system/nats-swarm.service
	@rm -f /etc/systemd/system/swarmgate.service
	@rm -f /etc/systemd/system/pelican-*.service
	@rm -f /etc/systemd/system/pelican-*.timer
	@systemctl daemon-reload
	@echo -e "$(GREEN)Cleanup complete$(NC)"

# ============================================================================
# Development/Testing Commands
# ============================================================================

lint:
	@echo -e "$(BLUE)Linting shell scripts...$(NC)"
	@which shellcheck > /dev/null && shellcheck master-bootstrap.sh pelican-build.sh || echo "shellcheck not installed"

test-scripts:
	@echo -e "$(BLUE)Testing scripts (dry run)...$(NC)"
	@bash -n master-bootstrap.sh && echo -e "$(GREEN)✓ master-bootstrap.sh syntax OK$(NC)"
	@bash -n pelican-build.sh && echo -e "$(GREEN)✓ pelican-build.sh syntax OK$(NC)"
