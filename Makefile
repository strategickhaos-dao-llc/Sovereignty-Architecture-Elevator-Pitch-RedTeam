.PHONY: check-sovereignty monitor-local up down logs

check-sovereignty:
	@echo "🔍 Checking for cloud treason in Prometheus configs..."
	@if grep -rn "remote_write" monitoring/ | grep -v "^[^:]*:[^:]*:#" | grep -q "."; then \
		echo "☁️  CLOUD DEPENDENCY DETECTED — YOU ARE NOT SOVEREIGN"; \
		exit 1; \
	else \
		echo "🟢 Fully sovereign — no remote_write, no cloud, no compromises"; \
	fi
	@if grep -rn "grafana.net\|prometheus-prod-" monitoring/ | grep -v "^[^:]*:[^:]*:#" | grep -q "."; then \
		echo "☁️  Grafana Cloud reference found — purge it"; \
		exit 1; \
	fi

monitor-local: check-sovereignty
	@echo "🔥 Enforcing local-only monitoring..."
	@docker compose -f docker-compose.obs.yml restart prometheus grafana || true
	@echo "Local stack ready: Prometheus :9090 | Grafana :3000 | Loki :3100 | Jaeger :16686"

up:
	docker compose -f docker-compose.obs.yml up -d

down:
	docker compose -f docker-compose.obs.yml down

logs:
	docker compose -f docker-compose.obs.yml logs -f
