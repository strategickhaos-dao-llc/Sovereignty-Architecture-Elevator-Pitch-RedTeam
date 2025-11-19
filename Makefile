# Sovereignty Architecture - Local Monitoring Stack
# Real operators don't rent dashboards. Keep metrics sovereign.

.PHONY: help up down monitor-local logs restart-monitoring check-sovereignty

help: ## Show this help message
	@echo "════════════════════════════════════════════════════════════════"
	@echo "  Sovereignty Architecture - Local Monitoring Commands"
	@echo "════════════════════════════════════════════════════════════════"
	@echo ""
	@echo "Core principles:"
	@echo "  • All metrics stay LOCAL (no cloud)"
	@echo "  • Prometheus: localhost:9090"
	@echo "  • Grafana: localhost:3000"
	@echo "  • Real operators don't rent dashboards"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

# Docker Compose command (supports both docker-compose and docker compose)
DOCKER_COMPOSE := $(shell command -v docker-compose 2>/dev/null || echo "docker compose")

up: ## Start the full stack with LOCAL monitoring only
	@echo "🚀 Starting sovereignty stack (local monitoring only)..."
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.obs.yml up -d
	@echo "✓ Stack running - metrics staying underground"
	@echo "  → Grafana: http://localhost:3000"
	@echo "  → Prometheus: http://localhost:9090"
	@echo "  → Vault: http://localhost:8200"

down: ## Stop all services
	@echo "🛑 Stopping stack..."
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.obs.yml down

restart-monitoring: ## Restart only monitoring services (Prometheus + Grafana)
	@echo "🔄 Restarting monitoring stack..."
	$(DOCKER_COMPOSE) -f docker-compose.obs.yml restart prometheus grafana
	@echo "✓ Monitoring restarted - still sovereign"

monitor-local: check-sovereignty ## Force monitoring to local-only mode
	@echo "🔒 Enforcing LOCAL monitoring..."
	@if grep -E "^\s*(remote_write|remote_read):" monitoring/prometheus.yml 2>/dev/null; then \
		echo "⚠️  Found remote_write config - commenting it out..."; \
		sed -i.backup 's/^remote_write:/#remote_write:/g' monitoring/prometheus.yml; \
		sed -i.backup 's/^remote_read:/#remote_read:/g' monitoring/prometheus.yml; \
		sed -i.backup 's/^  - url:/#  - url:/g' monitoring/prometheus.yml; \
		echo "✓ Cloud config disabled"; \
		if command -v docker-compose >/dev/null 2>&1; then \
			docker-compose -f docker-compose.obs.yml restart prometheus 2>/dev/null || echo "  (Prometheus not running - will use new config on next start)"; \
		elif command -v docker >/dev/null 2>&1; then \
			docker compose -f docker-compose.obs.yml restart prometheus 2>/dev/null || echo "  (Prometheus not running - will use new config on next start)"; \
		fi; \
	else \
		echo "✓ Already in sovereign mode (no remote_write found)"; \
	fi
	@echo ""
	@echo "Dashboards available at:"
	@echo "  • http://localhost:3000 (Grafana)"
	@echo "  • http://localhost:9090 (Prometheus)"

check-sovereignty: ## Verify no cloud dependencies exist
	@echo "🔍 Checking sovereignty status..."
	@if grep -rE "^\s*(remote_write|remote_read):" monitoring/ 2>/dev/null | grep -v ".backup"; then \
		echo "❌ SOVEREIGNTY VIOLATION: Cloud remote_write detected!"; \
		echo "Run 'make monitor-local' to fix"; \
		exit 1; \
	else \
		echo "✓ Fully sovereign - no cloud dependencies"; \
	fi

logs: ## Show logs from monitoring stack
	$(DOCKER_COMPOSE) -f docker-compose.obs.yml logs -f prometheus grafana

status: ## Show status of all services
	@echo "📊 Service Status:"
	@$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.obs.yml ps

grafana: ## Open Grafana in browser
	@echo "Opening Grafana dashboard..."
	@command -v xdg-open > /dev/null && xdg-open http://localhost:3000 || \
	 command -v open > /dev/null && open http://localhost:3000 || \
	 echo "→ Grafana: http://localhost:3000"

prometheus: ## Open Prometheus in browser
	@echo "Opening Prometheus..."
	@command -v xdg-open > /dev/null && xdg-open http://localhost:9090 || \
	 command -v open > /dev/null && open http://localhost:9090 || \
	 echo "→ Prometheus: http://localhost:9090"

clean: down ## Stop services and remove volumes (⚠️  DATA LOSS)
	@echo "⚠️  This will DELETE all monitoring data"
	@read -p "Continue? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.obs.yml down -v; \
		echo "✓ All data removed"; \
	else \
		echo "Cancelled"; \
	fi

.DEFAULT_GOAL := help
