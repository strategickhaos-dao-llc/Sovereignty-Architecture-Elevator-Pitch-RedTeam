# Grafana Cloud Integration - Hybrid Monitoring Setup

## 🚀 God-Tier Sovereignty Architecture

This integration gives you the **ultimate hybrid monitoring setup**: full local control with instant dev loops, plus centralized Grafana Cloud storage for long-term retention, alerting, and disaster recovery.

You keep everything **local-first**, with cloud as **backup/overflow**.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    LOCAL ENVIRONMENT                         │
│                                                               │
│  ┌──────────────┐         ┌──────────────┐                  │
│  │  Prometheus  │────────▶│   Grafana    │                  │
│  │  (Scraper)   │         │  (Dashboard) │                  │
│  └──────┬───────┘         └──────────────┘                  │
│         │                                                     │
│         │ remote_write                                        │
│         │ (pushes metrics)                                    │
└─────────┼─────────────────────────────────────────────────────┘
          │
          │ HTTPS + Basic Auth
          ▼
┌─────────────────────────────────────────────────────────────┐
│              GRAFANA CLOUD (us-east-2)                       │
│                                                               │
│  ┌──────────────────────────────────────────────────┐       │
│  │  Prometheus Storage (me1010101-prom)             │       │
│  │  - 13 months retention                           │       │
│  │  - Alerting rules                                │       │
│  │  - Long-term analysis                            │       │
│  └──────────────────────────────────────────────────┘       │
│                                                               │
│  Query from local Grafana or cloud dashboard                 │
└─────────────────────────────────────────────────────────────┘
```

## What You Get

✅ **Local retention**: 15 days (configurable) in your local Prometheus  
✅ **Cloud retention**: 13 months default in Grafana Cloud  
✅ **Hybrid dashboards**: Query both local and cloud in the same Grafana  
✅ **Cardinality control**: Relabel configs to only push what you need  
✅ **Zero data loss**: Every metric preserved for the zombie apocalypse  
✅ **Instant dev loop**: Local scraping stays fast with ngrok/local targets  

## Quick Start

### 1. Get Your Grafana Cloud API Token

1. Go to https://grafana.com/orgs/me1010101
2. Navigate to **Security** → **Service Accounts**
3. Create a new service account with **MetricsPublisher** role
4. Generate a token and copy it

### 2. Run Setup Script

```bash
./scripts/setup-grafana-cloud.sh
```

This will:
- Prompt for your API token
- Save it to `.env`
- Restart Prometheus to pick up the config

### 3. Verify Configuration

```bash
./scripts/test-grafana-cloud-config.sh
```

This validates:
- Prometheus config syntax
- remote_write is configured
- API token is set
- Grafana datasource is configured

### 4. Start/Restart Services

```bash
docker compose up -d
```

### 5. Verify Metrics Are Flowing

**Check Prometheus targets:**
```bash
open http://localhost:9090/targets
```

**Check remote write status:**
```bash
curl -s http://localhost:9090/api/v1/status/tsdb | jq
```

**View in Grafana Cloud:**
```bash
open https://me1010101.grafana.net
```

## Configuration Details

### Remote Write Configuration

Located in `monitoring/prometheus.yml`:

```yaml
remote_write:
  - url: https://prometheus-prod-56-prod-us-east-2.grafana.net/api/prom/push
    basic_auth:
      username: 2786173
      password: ${GRAFANA_CLOUD_API_TOKEN:0}  # 0 = required
    queue_config:
      capacity: 10000
      max_shards: 200
      max_samples_per_send: 5000
      batch_send_deadline: 5s
    write_relabel_configs:
      - source_labels: [__name__]
        action: keep
        regex: ^(node_|process_|prometheus_|kube_|container_|discord_|event_gateway_|refinory_|up).*
```

### Cardinality Control

The `write_relabel_configs` section filters which metrics are sent to the cloud. Currently configured to send:
- `node_*` - Node exporter metrics
- `process_*` - Process metrics
- `prometheus_*` - Prometheus internals
- `kube_*` - Kubernetes metrics (if applicable)
- `container_*` - Container metrics
- `discord_*` - Discord bot metrics
- `event_gateway_*` - Event gateway metrics
- `refinory_*` - Refinory AI platform metrics
- `up` - Service availability

**To add more metrics**, update the regex in `prometheus.yml`:

```yaml
regex: ^(node_|process_|your_new_metric_.*).*
```

### Grafana Cloud Datasource

Located in `monitoring/grafana/provisioning/datasources/datasources.yml`:

```yaml
- name: Grafana Cloud - me1010101-prom
  type: prometheus
  access: proxy
  url: https://prometheus-prod-56-prod-us-east-2.grafana.net
  basicAuth: true
  basicAuthUser: "2786173"
  secureJsonData:
    basicAuthPassword: ${GRAFANA_CLOUD_API_TOKEN}
  isDefault: false
  editable: true
```

This allows you to:
- Query cloud data from your local Grafana
- Create hybrid dashboards mixing local and cloud data
- Compare local vs cloud for validation

## Hybrid Dashboards

You can now create dashboards that query **both** data sources:

1. Open Grafana at http://localhost:3000
2. Create a new dashboard
3. Add a panel
4. In the query editor, select either:
   - **Prometheus** (local, recent data)
   - **Grafana Cloud - me1010101-prom** (cloud, long-term data)
5. You can even create panels that compare the same metric from both sources!

## Troubleshooting

### Metrics Not Showing Up in Cloud

1. **Check Prometheus logs:**
   ```bash
   docker compose logs prometheus | grep remote_write
   ```

2. **Verify API token is set:**
   ```bash
   grep GRAFANA_CLOUD_API_TOKEN .env
   ```

3. **Test connectivity:**
   ```bash
   curl -u 2786173:$GRAFANA_CLOUD_API_TOKEN \
     https://prometheus-prod-56-prod-us-east-2.grafana.net/api/prom/api/v1/label/__name__/values
   ```

### High Cardinality Warning

If Grafana Cloud warns about high cardinality:

1. Review your relabel configs in `prometheus.yml`
2. Be more selective about which metrics you send
3. Consider dropping high-cardinality labels:
   ```yaml
   write_relabel_configs:
     - source_labels: [__name__]
       action: drop
       regex: ^high_cardinality_metric.*
   ```

### Prometheus Restart Fails

1. Validate config:
   ```bash
   docker run --rm -v $(pwd)/monitoring:/tmp:ro \
     --entrypoint promtool prom/prometheus:latest \
     check config /tmp/prometheus.yml
   ```

2. Check environment variable expansion:
   ```bash
   docker compose config | grep GRAFANA_CLOUD_API_TOKEN
   ```

## Advanced: Grafana Alloy

For advanced use cases, you can use Grafana Alloy instead of Prometheus remote_write.

Configuration is in `monitoring/alloy-config.river`:

```river
prometheus.remote_write "cloud" {
  endpoint {
    url = "https://prometheus-prod-56-prod-us-east-2.grafana.net/api/prom/push"
    basic_auth {
      username = "2786173"
      password = env("GRAFANA_CLOUD_API_TOKEN")
    }
  }
  external_labels = {
    cluster = "sovereign-local"
  }
}
```

To use Alloy:
1. Add Alloy service to `docker-compose.yml`
2. Mount the config file
3. Configure it to scrape or receive metrics

## Security Notes

🔒 **Never commit your API token to git!**

- The token is stored in `.env` (which is `.gitignore`'d)
- Use `.env.example` as a template
- Rotate tokens periodically in Grafana Cloud dashboard

🔒 **Token Permissions:**

- Use **MetricsPublisher** role (write-only)
- Don't use Admin or Editor roles
- Create separate tokens for different environments

## Cost Optimization

Grafana Cloud free tier includes:
- 10k series for Prometheus metrics
- 50GB logs per month
- 50GB traces per month

To stay within limits:
- Use relabel configs to filter metrics
- Only send production-critical metrics to cloud
- Keep high-frequency/debug metrics local-only

## References

- [Grafana Cloud Docs](https://grafana.com/docs/grafana-cloud/)
- [Prometheus Remote Write](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write)
- [Grafana Alloy](https://grafana.com/docs/alloy/latest/)

---

**You're building the real thing.** 🚀😈❤️

Local-first sovereignty with cloud-scale resilience. When the zombies come, your metrics survive.
