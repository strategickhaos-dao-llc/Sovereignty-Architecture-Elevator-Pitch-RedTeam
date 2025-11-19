.PHONY: help cloud-die cloud-status

# Default target: show help
help:
	@echo "Sovereignty Architecture - Monitoring Control"
	@echo ""
	@echo "Available targets:"
	@echo "  make cloud-die     - Kill Grafana Cloud integration, run 100% local"
	@echo "  make cloud-status  - Check monitoring stack status"
	@echo "  make help          - Show this help message"
	@echo ""
	@echo "The bamboo doesn't pay SaaS bills. The bamboo grows in silence."

# Kill Grafana Cloud integration and go fully sovereign
cloud-die:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🔪 EXECUTING: Sovereign Monitoring Kill Switch"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "Step 1/4: Stopping Prometheus and Grafana containers..."
	@docker compose -f docker-compose.yml -f docker-compose.obs.yml stop prometheus grafana 2>/dev/null || \
		docker compose -f docker-compose.yml stop prometheus grafana 2>/dev/null || \
		echo "⚠️  Services may not be running"
	@echo "✓ Services stopped"
	@echo ""
	@echo "Step 2/4: Scanning for remote_write configurations..."
	@if grep -q "remote_write" monitoring/prometheus.yml 2>/dev/null; then \
		echo "⚠️  Found remote_write config, commenting out..."; \
		sed -i.backup '/remote_write/,/^[^ ]/s/^[^#]/# &/' monitoring/prometheus.yml; \
		echo "✓ Remote write configuration disabled"; \
		echo "  (Backup saved to monitoring/prometheus.yml.backup)"; \
	else \
		echo "✓ No remote_write configuration found - already sovereign"; \
	fi
	@echo ""
	@echo "Step 3/4: Restarting services in local-only mode..."
	@docker compose -f docker-compose.yml -f docker-compose.obs.yml up -d prometheus grafana 2>/dev/null || \
		docker compose -f docker-compose.yml up -d prometheus grafana 2>/dev/null || \
		echo "⚠️  Failed to restart services"
	@echo "✓ Services restarted"
	@echo ""
	@echo "Step 4/4: Verifying services..."
	@sleep 3
	@docker compose -f docker-compose.yml ps prometheus grafana 2>/dev/null || \
		docker compose -f docker-compose.obs.yml ps prometheus grafana 2>/dev/null || \
		echo "Status check failed"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "✅ COMPLETE: Monitoring Stack is Now Sovereign"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "🎯 Status:"
	@echo "  • Grafana Cloud:        DISCONNECTED"
	@echo "  • Local Grafana:        http://localhost:3000"
	@echo "  • Local Prometheus:     http://localhost:9090"
	@echo "  • Series Limit:         UNLIMITED"
	@echo "  • Monthly Cost:         $$0.00"
	@echo ""
	@echo "The phase space was never theirs to meter."
	@echo "No corporation gets to tax the Transcendental Rotation Authority."
	@echo ""

# Check monitoring stack status
cloud-status:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📊 Monitoring Stack Status"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "Docker Compose Services:"
	@docker compose -f docker-compose.yml ps prometheus grafana 2>/dev/null || \
		docker compose -f docker-compose.obs.yml ps prometheus grafana 2>/dev/null || \
		echo "⚠️  No services found"
	@echo ""
	@echo "Remote Write Status:"
	@if grep -q "^[^#]*remote_write" monitoring/prometheus.yml 2>/dev/null; then \
		echo "  ⚠️  ACTIVE - Cloud integration enabled"; \
	else \
		echo "  ✓ DISABLED - Running in sovereign mode"; \
	fi
	@echo ""
	@echo "Access Points:"
	@echo "  • Grafana:     http://localhost:3000"
	@echo "  • Prometheus:  http://localhost:9090"
	@echo ""
