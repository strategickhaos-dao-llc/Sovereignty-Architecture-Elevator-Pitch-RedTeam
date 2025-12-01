# Grafana Cloud Integration - AI-Powered Observability

This guide explains how to integrate Grafana Cloud's AI-powered observability platform with the Strategickhaos Sovereignty Architecture. Grafana Cloud provides advanced monitoring, analysis, and alerting capabilities with AI/ML insights across metrics, logs, and traces.

## 🌟 What You Get with Grafana Cloud

### Free Tier Includes:
- ✅ **10k series** Prometheus metrics
- ✅ **50GB logs** (Loki)
- ✅ **50GB traces** (Tempo)
- ✅ **50GB profiles** (Pyroscope)
- ✅ **500VUh k6** performance testing
- ✅ **20+ Enterprise** data source plugins
- ✅ **100+ pre-built** solutions
- ✅ **AI/ML insights** for root cause analysis
- ✅ **Contextual analysis** with Grafana Asserts
- ✅ **SLO management** capabilities

## 🚀 Quick Setup

### 1. Get Your Grafana Cloud Credentials

1. Sign up at [grafana.com](https://grafana.com)
2. Navigate to **My Account** → **Grafana Cloud** → **Details**
3. Find your **Prometheus Instance Details**:
   - Remote Write Endpoint
   - Username / Instance ID
   - API Token (generate if needed)

### 2. Configure Environment Variables

Copy the example environment file and add your credentials:

```bash
cp .env.example .env
```

Edit `.env` and update the Grafana Cloud section:

```bash
# Grafana Cloud - AI-Powered Observability
GRAFANA_CLOUD_API_TOKEN=glc_your_actual_api_token_here

# Grafana Cloud Prometheus (Metrics)
GRAFANA_CLOUD_PROMETHEUS_URL=https://prometheus-prod-XX-prod-us-east-X.grafana.net/api/prom/push
GRAFANA_CLOUD_PROMETHEUS_USER=your_instance_id
GRAFANA_CLOUD_PROMETHEUS_QUERY_URL=https://prometheus-prod-XX-prod-us-east-X.grafana.net/api/prom

# Grafana Cloud Loki (Logs)
GRAFANA_CLOUD_LOKI_URL=https://logs-prod-XXX.grafana.net/loki/api/v1/push
GRAFANA_CLOUD_LOKI_USER=your_loki_user_id

# Grafana Cloud Instance (for dashboards)
GRAFANA_CLOUD_INSTANCE_URL=https://yourorg.grafana.net
GRAFANA_CLOUD_ORG_ID=yourorg
```

### 3. Choose Your Deployment Method

You have two options for sending telemetry to Grafana Cloud:

#### Option A: Prometheus with Remote Write (Simple)

Uses existing Prometheus with remote_write to Grafana Cloud:

```bash
# Start the observability stack
docker-compose -f docker-compose.obs.yml up -d prometheus grafana loki

# Check Prometheus is sending data
docker-compose -f docker-compose.obs.yml logs prometheus | grep "remote_write"
```

#### Option B: Grafana Alloy (Recommended)

Modern OpenTelemetry collector with native Grafana Cloud integration:

```bash
# Start Alloy alongside other services
docker-compose -f docker-compose.obs.yml up -d alloy

# Access Alloy UI
open http://localhost:12345

# Check Alloy logs
docker-compose -f docker-compose.obs.yml logs -f alloy
```

## 📊 Architecture Options

### Architecture 1: Hybrid (Prometheus + Grafana Cloud)

```
┌─────────────────────┐
│   Applications      │
│  (Bot, Gateway,     │
│   Refinory, etc)    │
└──────────┬──────────┘
           │ /metrics
           ▼
┌─────────────────────┐
│   Prometheus        │
│  (Local Storage +   │
│   Remote Write)     │
└──────────┬──────────┘
           │
           ├──────────┐
           │          │
           ▼          ▼
    ┌──────────┐  ┌──────────────┐
    │  Local   │  │ Grafana Cloud│
    │ Grafana  │  │   (AI/ML)    │
    └──────────┘  └──────────────┘
```

**Best for:** Teams wanting local dashboards + cloud AI features

### Architecture 2: Alloy Direct (Cloud-First)

```
┌─────────────────────┐
│   Applications      │
│  (Bot, Gateway,     │
│   Refinory, etc)    │
└──────────┬──────────┘
           │ /metrics
           ▼
┌─────────────────────┐
│   Grafana Alloy     │
│  (Scrape + Forward) │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │ Grafana Cloud│
    │ - Metrics    │
    │ - Logs       │
    │ - Traces     │
    │ - AI/ML      │
    └──────────────┘
```

**Best for:** Full cloud observability with minimal local infrastructure

## 🔧 Configuration Details

### Prometheus Remote Write

The `monitoring/prometheus.yml` configuration includes:

```yaml
remote_write:
  - url: ${GRAFANA_CLOUD_PROMETHEUS_URL}
    basic_auth:
      username: ${GRAFANA_CLOUD_PROMETHEUS_USER}
      password: ${GRAFANA_CLOUD_API_TOKEN}
    queue_config:
      capacity: 10000
      max_shards: 50
      max_samples_per_send: 5000
```

**Configuration options:**
- `capacity`: Number of samples to buffer (default: 10000)
- `max_shards`: Max concurrent shards for parallel writes (default: 50)
- `max_samples_per_send`: Batch size per request (default: 5000)

### Grafana Alloy Configuration

The `monitoring/alloy-config.alloy` provides:

1. **Prometheus scraping** - Collects metrics from all services
2. **Remote write** - Sends to Grafana Cloud
3. **Loki integration** - Forwards logs from Docker containers
4. **External labels** - Enriches data with cluster/environment context

## 📈 Metrics Being Collected

### Application Metrics
- **Discord Bot** (`bot:3000/metrics`)
  - Message processing rates
  - Command execution times
  - API rate limit consumption
  
- **Event Gateway** (`gateway:8080/metrics`)
  - Webhook processing latency
  - Request rates by endpoint
  - HMAC verification success/failures

- **Refinory API** (`refinory-api:8000/metrics`)
  - AI inference times
  - Vector database query performance
  - API endpoint response times

### Infrastructure Metrics
- **Redis** - Cache hit rates, memory usage, command latency
- **PostgreSQL** - Connection pools, query times, table sizes
- **Qdrant** - Vector operations, collection sizes, search latency
- **Vault** - Secret access patterns, token operations

### Container Metrics
- **cAdvisor** - CPU, memory, network, disk I/O per container
- **Node Exporter** - Host system metrics

## 🎯 Grafana Cloud Features

### 1. Pre-built Dashboards

Grafana Cloud provides 100+ integration dashboards:

```bash
# Navigate to your Grafana Cloud instance
open ${GRAFANA_CLOUD_INSTANCE_URL}/dashboards

# Search for:
- "Docker"
- "Kubernetes"
- "PostgreSQL"
- "Redis"
- "Node Exporter"
```

### 2. AI/ML Insights

Access AI-powered features in your cloud instance:

- **Grafana Asserts**: Contextual root cause analysis
- **SLO Management**: Define and track service level objectives
- **Anomaly Detection**: ML-based alerting on metrics
- **Log Pattern Recognition**: Automatic log clustering

### 3. Application Observability

Set up application monitoring:

```bash
# Install Grafana Faro for frontend observability
npm install @grafana/faro-web-sdk

# Configure in your application
import { initializeFaro } from '@grafana/faro-web-sdk';

initializeFaro({
  url: 'https://faro-collector-prod-us-east-0.grafana.net/collect/<your-app-key>',
  app: {
    name: 'sovereignty-architecture',
    environment: 'production',
  },
});
```

## 🔐 Security Best Practices

### Protect Your API Tokens

```bash
# Use environment variables, never commit tokens
echo "GRAFANA_CLOUD_API_TOKEN=glc_..." >> .env

# Add to .gitignore
echo ".env" >> .gitignore

# For production, use secret management
kubectl create secret generic grafana-cloud \
  --from-literal=api-token=${GRAFANA_CLOUD_API_TOKEN} \
  --namespace=ops
```

### Network Security

```yaml
# In docker-compose.obs.yml, Prometheus/Alloy only need outbound access
services:
  prometheus:
    networks: [obs_network]  # Internal only
    # No external ports needed for cloud-only mode
```

## 📊 Monitoring Your Integration

### Check Prometheus Remote Write Status

```bash
# Check if metrics are being sent
curl http://localhost:9090/api/v1/status/tsdb

# View remote write queue status
curl http://localhost:9090/api/v1/status/runtimeinfo | jq
```

### Verify Data in Grafana Cloud

1. Log into your Grafana Cloud instance
2. Navigate to **Explore**
3. Select **Prometheus** data source
4. Query: `up{source="sovereignty-architecture"}`
5. You should see all your services

### Check Alloy Status

```bash
# View Alloy UI
open http://localhost:12345

# Check component status via API
curl http://localhost:12345/api/v0/web/components | jq

# View metrics being collected
curl http://localhost:12345/metrics
```

## 🚨 Alerting Setup

### Configure Alertmanager to Discord

In `monitoring/alerts.yml`:

```yaml
groups:
  - name: sovereignty_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
          environment: "{{ $labels.environment }}"
        annotations:
          summary: "High error rate detected"
          description: "{{ $labels.job }} has error rate above 5%"
```

### Route Alerts to Discord

Use Grafana Cloud OnCall integration:

1. **Set up OnCall** in Grafana Cloud
2. **Create Discord webhook** in your Discord server
3. **Configure integration** in OnCall settings
4. **Link to alert rules** in Prometheus/Grafana

## 🎓 Learning Resources

### Grafana Cloud Documentation
- [Grafana Cloud Docs](https://grafana.com/docs/grafana-cloud/)
- [Prometheus Remote Write](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write)
- [Grafana Alloy Docs](https://grafana.com/docs/alloy/latest/)

### Tutorials
- [Getting Started with LGTM Stack](https://grafana.com/docs/grafana-cloud/quickstart/)
- [Kubernetes Monitoring](https://grafana.com/docs/grafana-cloud/kubernetes/)
- [Application Observability](https://grafana.com/docs/grafana-cloud/application-observability/)

## 🆘 Troubleshooting

### Metrics Not Appearing in Grafana Cloud

**Check Prometheus logs:**
```bash
docker-compose -f docker-compose.obs.yml logs prometheus | grep -i "error\|failed"
```

**Common issues:**
1. **Invalid API token** - Regenerate token in Grafana Cloud
2. **Wrong endpoint URL** - Verify URLs match your cloud instance
3. **Network connectivity** - Check firewall/proxy settings
4. **Rate limiting** - Free tier has limits, check your usage

### Alloy Not Starting

**Check configuration syntax:**
```bash
# Validate Alloy config
docker run --rm -v $(pwd)/monitoring/alloy-config.alloy:/config.alloy \
  grafana/alloy:v1.5.0 \
  fmt /config.alloy
```

**Check environment variables:**
```bash
docker-compose -f docker-compose.obs.yml config | grep GRAFANA
```

### High Remote Write Queue

If you see queue buildup:

```yaml
# Increase queue capacity in prometheus.yml
remote_write:
  - url: ...
    queue_config:
      capacity: 20000  # Increased from 10000
      max_shards: 100  # Increased from 50
```

## 📞 Support

- **Grafana Community Forums**: [community.grafana.com](https://community.grafana.com)
- **Grafana Support**: Available with paid plans
- **Sovereignty Architecture**: [GitHub Issues](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues)

## 🎯 Next Steps

1. ✅ **Set up credentials** - Configure `.env` with your Grafana Cloud details
2. ✅ **Deploy stack** - Choose Prometheus or Alloy deployment
3. ✅ **Import dashboards** - Use pre-built Grafana Cloud integrations
4. ✅ **Configure alerts** - Set up OnCall and Discord notifications
5. ✅ **Explore AI features** - Try Asserts for root cause analysis
6. ✅ **Monitor costs** - Track usage against free tier limits

---

**Built with 🔥 by the Strategickhaos collective**

*Monitor, analyze, and act faster with AI-powered observability*
