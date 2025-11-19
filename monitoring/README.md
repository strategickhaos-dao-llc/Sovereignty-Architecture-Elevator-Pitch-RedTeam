# Sovereign Monitoring Stack

**The bamboo doesn't pay SaaS bills. The bamboo grows in silence.**

## Overview

This monitoring stack runs **100% locally** with:
- ✅ **Zero external costs** - No Grafana Cloud, no remote write fees
- ✅ **Unlimited metrics** - No artificial series limits
- ✅ **Full sovereignty** - All your data stays on your infrastructure
- ✅ **No vendor lock-in** - Standard Prometheus + Grafana OSS

## Quick Start

### Kill Grafana Cloud Integration
```bash
make cloud-die
```

This command will:
1. Stop Prometheus and Grafana containers
2. Disable any remote_write configurations
3. Restart services in local-only mode
4. Verify everything is running sovereign

### Check Stack Status
```bash
make cloud-status
```

Shows:
- Running containers (Prometheus, Grafana)
- Remote write status (should be DISABLED)
- Access URLs for dashboards

## Access Points

Once running, access your monitoring stack at:

- **Grafana Dashboard**: http://localhost:3000
  - Default credentials: `admin` / `admin` (or set via `GRAFANA_PASSWORD` env var)
  
- **Prometheus UI**: http://localhost:9090
  - Query metrics directly
  - Check targets and service discovery

## Architecture

```
┌─────────────────┐
│   Applications  │
│  (Discord bot,  │
│   Refinory,     │
│   etc.)         │
└────────┬────────┘
         │ metrics
         ▼
┌─────────────────┐
│   Prometheus    │◄── 100% Local
│   :9090         │    No Remote Write
└────────┬────────┘    No Cloud Bills
         │
         ▼
┌─────────────────┐
│    Grafana      │
│    :3000        │
│  (Dashboards)   │
└─────────────────┘
```

## Configuration

### Prometheus (`prometheus.yml`)
- Scrapes local services: Discord bot, event gateway, Refinory
- Scrapes infrastructure: Redis, PostgreSQL, Qdrant
- **No remote_write blocks** = No data leaves your control

### Grafana (`grafana/`)
- Pre-provisioned dashboards in `grafana/dashboards/`
- Data source auto-configured to local Prometheus
- Provisioning config in `grafana/provisioning/`

## Metrics Collected

### Application Metrics
- **Discord Bot**: API latency, command throughput, rate limits
- **Event Gateway**: Webhook processing, routing decisions
- **Refinory API**: AI query performance, embeddings operations

### Infrastructure Metrics  
- **Redis**: Memory usage, command latency, key counts
- **PostgreSQL**: Connection pool, query performance
- **Qdrant**: Vector operations, search latency

## Alerting

Alerts are defined in `alerts.yml` and include:
- High memory usage
- Service down/unavailable
- API error rate spikes
- Disk space warnings

Alerts can be routed to Discord via the event gateway.

## Troubleshooting

### Services won't start
```bash
# Check Docker Compose status
docker compose -f docker-compose.yml ps

# View logs
docker compose -f docker-compose.yml logs prometheus grafana
```

### Can't access Grafana
```bash
# Verify container is running
docker compose -f docker-compose.yml ps grafana

# Check if port 3000 is in use
lsof -i :3000
```

### Prometheus not scraping targets
1. Open http://localhost:9090/targets
2. Check which targets are down
3. Verify service containers are running
4. Check network connectivity between containers

## The Philosophy

**No corporation gets to tax the Transcendental Rotation Authority.**

Your metrics, your infrastructure, your sovereignty. The phase space was never theirs to meter.

When you run `make cloud-die`, you:
- ❌ Cancel the implicit SaaS tax on observability
- ✅ Keep unlimited metric cardinality
- ✅ Retain full data ownership
- ✅ Eliminate vendor dependencies

The agents keep playing. The boards keep rotating. The music keeps generating.

**And the bamboo grows in silence, drinks the sun, and chokes out everything else.**
