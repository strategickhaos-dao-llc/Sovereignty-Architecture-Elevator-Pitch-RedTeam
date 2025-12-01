# Grafana Cloud Architecture Diagram

## System Architecture with AI-Powered Observability

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SOVEREIGNTY ARCHITECTURE SERVICES                         │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Discord Bot  │  │Event Gateway │  │  Refinory    │  │Infrastructure│   │
│  │   (bot:3000) │  │(gateway:8080)│  │(refinory:8000)│  │  Services    │   │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘   │
│         │                  │                  │                  │           │
│         └──────────────────┴──────────────────┴──────────────────┘           │
│                                    │                                         │
│                              /metrics endpoint                               │
└────────────────────────────────────┼────────────────────────────────────────┘
                                     │
                                     ▼
         ┌───────────────────────────────────────────────────────┐
         │                  TELEMETRY COLLECTION                 │
         │                                                        │
         │  ┌──────────────────┐      ┌──────────────────┐     │
         │  │   Prometheus     │      │  Grafana Alloy   │     │
         │  │ (Local + Remote) │      │  (Recommended)   │     │
         │  └────────┬─────────┘      └────────┬─────────┘     │
         │           │                          │               │
         │           │    Scrapes /metrics      │               │
         │           │    endpoints             │               │
         └───────────┼──────────────────────────┼───────────────┘
                     │                          │
                     │                          │
                     │  remote_write            │ forward_to
                     │  (HTTPS + Basic Auth)    │ (HTTPS + Basic Auth)
                     │                          │
                     ▼                          ▼
         ┌──────────────────────────────────────────────────────┐
         │                  GRAFANA CLOUD                       │
         │          AI-Powered Observability Platform           │
         │                                                       │
         │  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
         │  │ Mimir/Prom   │  │     Loki     │  │   Tempo   │ │
         │  │  (Metrics)   │  │    (Logs)    │  │  (Traces) │ │
         │  └──────┬───────┘  └──────┬───────┘  └─────┬─────┘ │
         │         │                  │                │        │
         │         └──────────────────┴────────────────┘        │
         │                        │                             │
         │                        ▼                             │
         │         ┌──────────────────────────────┐            │
         │         │   Grafana Dashboards         │            │
         │         │   + AI/ML Insights           │            │
         │         │   + Grafana Asserts          │            │
         │         │   + SLO Management           │            │
         │         └──────────────────────────────┘            │
         │                        │                             │
         │                        ▼                             │
         │         ┌──────────────────────────────┐            │
         │         │   Grafana Cloud OnCall       │            │
         │         │   Alert Management           │            │
         │         └──────────────┬───────────────┘            │
         └────────────────────────┼────────────────────────────┘
                                  │
                                  │ Webhook
                                  ▼
                      ┌───────────────────────┐
                      │  Discord Channels     │
                      │  #alerts, #cluster    │
                      └───────────────────────┘
```

## Quick Reference

### Deployment Modes

| Mode | Components | Best For |
|------|------------|----------|
| **Alloy Only** | Alloy + Cloud | Cloud-first, minimal footprint |
| **Prometheus + Cloud** | Prometheus + Cloud | Local queries + cloud storage |
| **Full Stack** | All components | Maximum flexibility |

### Key Endpoints

| Component | Port | URL |
|-----------|------|-----|
| Prometheus | 9090 | http://localhost:9090 |
| Grafana Alloy | 12345 | http://localhost:12345 |
| Local Grafana | 3000 | http://localhost:3000 |
| Grafana Cloud | - | https://yourorg.grafana.net |

### Configuration Files

| File | Purpose |
|------|---------|
| `monitoring/prometheus.yml` | Prometheus scrape + remote_write config |
| `monitoring/alloy-config.alloy` | Alloy telemetry collection |
| `.env` | Grafana Cloud credentials |
| `docker-compose.obs.yml` | Service definitions |

---

For detailed setup instructions, see [GRAFANA_CLOUD_INTEGRATION.md](../GRAFANA_CLOUD_INTEGRATION.md)
