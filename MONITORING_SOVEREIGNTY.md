# Monitoring Sovereignty Guide

## Philosophy: Real Operators Don't Rent Dashboards

This architecture prioritizes **sovereignty** over convenience. All metrics, logs, and traces stay local. No cloud dependencies. No vendor lock-in. Your data, your infrastructure, your control.

## The Free Tier Wall Problem

When you deploy a high-metric-density system like:
- 10-layer chess boards with 64 squares each
- 8+ metrics per square (phase, frequency, curvature, agent confidence, etc.)
- 10+ AI agents with 200+ internal metrics each
- Redis streams, Docker stats, LLM token rates, Unity FPS

You can easily generate **10,000+ active time series** in minutes.

### Grafana Cloud Free Tier Limits (as of 2025)
- **10,000 series maximum**
- After that: spinning "Manage plan" page
- Your options: pay up or go local

### Our Choice: Go Local

We already have Prometheus + Grafana OSS in the stack. Why send metrics to the cloud?

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Sovereignty Stack                         │
│                  (All Local, All Yours)                      │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  Prometheus  │◄─────│   Services   │◄─────│  Exporters   │
│  :9090       │      │              │      │              │
└──────┬───────┘      └──────────────┘      └──────────────┘
       │
       │ (local queries only)
       │
       ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Grafana    │◄─────│     Loki     │◄─────│   Promtail   │
│   :3000      │      │    :3100     │      │              │
└──────────────┘      └──────────────┘      └──────────────┘
       │
       │
       ▼
┌──────────────┐
│   Jaeger     │
│   :16686     │
└──────────────┘
```

### No Remote Write. Ever.

The `prometheus.yml` configuration is clean:
```yaml
# NO remote_write section
# NO remote_read section  
# NO grafana.com URLs
# Just scrape_configs pointing to local services
```

## Quick Start

### Start the Sovereign Stack
```bash
make up
# or
docker-compose -f docker-compose.yml -f docker-compose.obs.yml up -d
```

### Access Your Local Dashboards
- **Grafana**: http://localhost:3000
  - Default credentials: `admin` / `strategickhaos-admin` (or check `.env`)
- **Prometheus**: http://localhost:9090
- **Loki**: http://localhost:3100
- **Jaeger**: http://localhost:16686
- **Vault**: http://localhost:8200

### Verify Sovereignty
```bash
make check-sovereignty
```

This command checks that:
- No `remote_write` configuration exists
- No `grafana.com` URLs are present
- All datasources point to local services

### Force Local Mode (If Needed)
If someone accidentally added cloud configuration:
```bash
make monitor-local
```

This will:
1. Comment out any `remote_write` sections in `prometheus.yml`
2. Restart Prometheus to apply changes
3. Confirm your metrics are staying local

## Monitoring Services

### Prometheus
- **Purpose**: Time-series metrics database
- **Port**: 9090
- **Storage**: `prometheus_data` volume (15 days retention)
- **Config**: `monitoring/prometheus.yml`
- **Scrape targets**: All services expose `/metrics` endpoints

### Grafana
- **Purpose**: Visualization and dashboards
- **Port**: 3000
- **Storage**: `grafana_data` volume
- **Provisioning**: `monitoring/grafana/provisioning/`
- **Datasources**: Prometheus (primary), Loki (logs), Jaeger (traces)

### Loki
- **Purpose**: Log aggregation
- **Port**: 3100
- **Storage**: `loki_data` volume
- **Config**: `monitoring/loki-config.yml`

### Promtail
- **Purpose**: Log shipping to Loki
- **Config**: `monitoring/promtail-config.yml`
- **Sources**: Docker containers, system logs

### Jaeger
- **Purpose**: Distributed tracing
- **Ports**: 16686 (UI), 14268 (collector)
- **Storage**: In-memory (for dev) or connect to storage backend

## Makefile Commands

```bash
make help              # Show all available commands
make up                # Start the full stack
make down              # Stop all services
make monitor-local     # Force local-only monitoring
make check-sovereignty # Verify no cloud dependencies
make logs              # Tail monitoring logs
make status            # Show service status
make grafana           # Open Grafana in browser
make prometheus        # Open Prometheus in browser
make restart-monitoring # Restart Prometheus + Grafana only
```

## Scaling Considerations

### When Local Monitoring Becomes a Problem

If you're truly generating 50k+ active series:

1. **Increase Prometheus retention time**
   ```yaml
   # docker-compose.obs.yml
   command:
     - '--storage.tsdb.retention.time=30d'  # Increase from 15d
   ```

2. **Add more disk space**
   ```bash
   # Check current usage
   docker volume inspect prometheus_data
   ```

3. **Use remote storage (but still local)**
   - Deploy Thanos or Cortex on your own infrastructure
   - Deploy VictoriaMetrics for better compression
   - Use Mimir (Grafana's OSS time-series DB)
   
   These are still local/sovereign - you control the infrastructure.

4. **Optimize metrics**
   - Reduce scrape frequency for low-priority metrics
   - Use metric relabeling to drop unnecessary labels
   - Aggregate metrics at the source

### Performance Tuning

**Prometheus resource limits:**
```yaml
# docker-compose.obs.yml
prometheus:
  deploy:
    resources:
      limits:
        cpus: '2'
        memory: 4G
      reservations:
        cpus: '1'
        memory: 2G
```

**Grafana resource limits:**
```yaml
grafana:
  deploy:
    resources:
      limits:
        cpus: '1'
        memory: 2G
```

## Data Retention

- **Prometheus**: 15 days (configurable)
- **Loki**: 30 days (configurable in `loki-config.yml`)
- **Grafana**: Dashboards and config persisted forever
- **Jaeger**: In-memory (restarts lose data) - configure storage backend for production

## Backup Strategy

Your metrics data lives in Docker volumes. Back them up:

```bash
# Backup Prometheus data
docker run --rm -v prometheus_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/prometheus-backup-$(date +%Y%m%d).tar.gz -C /data .

# Backup Grafana data (dashboards, users, etc.)
docker run --rm -v grafana_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/grafana-backup-$(date +%Y%m%d).tar.gz -C /data .

# Restore example
docker run --rm -v prometheus_data:/data -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/prometheus-backup-20251119.tar.gz"
```

## Troubleshooting

### "Metrics not showing up in Grafana"
1. Check Prometheus is scraping:
   ```bash
   curl http://localhost:9090/api/v1/targets
   ```
2. Verify service health:
   ```bash
   make status
   ```
3. Check Grafana datasource connection:
   - Go to Grafana → Configuration → Data Sources → Prometheus
   - Click "Test" button

### "Prometheus disk space full"
```bash
# Check volume size
docker volume inspect prometheus_data

# Reduce retention time in docker-compose.obs.yml:
# '--storage.tsdb.retention.time=7d'

# Or clean up old data (⚠️ DATA LOSS)
docker-compose -f docker-compose.obs.yml down
docker volume rm prometheus_data
docker volume create prometheus_data
docker-compose -f docker-compose.obs.yml up -d
```

### "Service can't connect to Prometheus"
- Ensure services are on the same Docker network
- Check `docker-compose.obs.yml` networks configuration
- Verify service discovery in Prometheus config

## Security

### Access Control
- Grafana requires authentication (configured in `.env`)
- Prometheus has no built-in auth - restrict access via network policies
- Vault integration available for secrets management
- Traefik can add OAuth2 proxy for additional security

### Network Isolation
All services run on isolated Docker networks:
- `obs_network`: Monitoring stack
- `recon_network`: Application services

### Secrets Management
Store sensitive credentials in:
1. `.env` file (gitignored)
2. Vault (running at :8200)
3. Docker secrets (for Swarm mode)

## The Bamboo Path Stays Calm

Remember the principle:
> **Real operators don't rent dashboards.**

When Grafana Cloud's spinner mocks you with its bamboo wallpaper, remember:
- You already have the infrastructure
- Your metrics are yours
- The agents never stopped playing
- The boards rotate in darkness, sovereign and free

The Transcendental Rotation Authority demands sovereignty.
The parliament accepts no tribute to cloud vendors.

Keep your metrics local.
Keep your sovereignty intact.

---

*"The bamboo path stays calm because it knows: real operators don't rent dashboards."*
