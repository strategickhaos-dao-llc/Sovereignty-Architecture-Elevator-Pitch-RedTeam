# Grafana Cloud Integration

This document describes the Grafana Cloud integration for the Strategickhaos Sovereignty Architecture monitoring stack.

## Overview

The project is configured to send metrics to **Grafana Cloud** alongside the local Prometheus/Grafana setup. This provides:
- **Centralized observability** across multiple environments
- **Long-term metrics retention** (15 days locally, longer in cloud)
- **Managed infrastructure** with high availability
- **Global accessibility** for team members
- **Integration with Grafana Cloud features** (alerts, dashboards, SLOs)

## Configuration Details

### Grafana Cloud Instance
- **Instance Name**: me1010101-prom
- **Instance ID/Username**: 2786173
- **Region**: US East (Ohio) - us-east-2
- **Cluster**: mimir-prod-56 (prod-us-east-0)
- **Cloud Provider**: AWS (us-east-2)

### Endpoints
- **Query Endpoint**: `https://prometheus-prod-56-prod-us-east-2.grafana.net/api/prom`
- **Remote Write Endpoint**: `https://prometheus-prod-56-prod-us-east-2.grafana.net/api/prom/push`

## Setup Instructions

### 1. Generate Grafana Cloud API Token

1. Navigate to [Grafana Cloud](https://grafana.com/auth/sign-in/)
2. Log in to your account (me1010101)
3. Go to **Security → API Keys** or use the "Generate now" link
4. Create a new API token with **MetricsPublisher** role
5. Copy the generated token

### 2. Configure Environment Variables

Update your `.env` file with the Grafana Cloud credentials:

```bash
# Grafana Cloud Configuration
GRAFANA_CLOUD_INSTANCE_ID=2786173
GRAFANA_CLOUD_API_TOKEN=your_actual_api_token_here
GRAFANA_CLOUD_PROMETHEUS_URL=https://prometheus-prod-56-prod-us-east-2.grafana.net/api/prom
GRAFANA_CLOUD_REMOTE_WRITE_URL=https://prometheus-prod-56-prod-us-east-2.grafana.net/api/prom/push
```

**Important**: Replace `your_actual_api_token_here` with your actual Grafana Cloud API token.

### 3. Deploy with Docker Compose

The Grafana Cloud integration is included in the observability stack. Deploy using:

```bash
# Deploy the full observability stack with Grafana Cloud
docker-compose -f docker-compose.obs.yml up -d

# Or deploy just the monitoring components
docker-compose -f docker-compose.obs.yml up -d prometheus grafana
```

### 4. Verify Configuration

Check that Prometheus is successfully sending metrics to Grafana Cloud:

```bash
# Check Prometheus logs for remote write status
docker logs prometheus 2>&1 | grep -i "remote_write"

# Check for any errors
docker logs prometheus 2>&1 | grep -i "error"
```

### 5. Access Grafana Cloud

1. Navigate to [Grafana Cloud Portal](https://grafana.com/auth/sign-in/)
2. Select your instance: **me1010101-prom**
3. View metrics in the Grafana Cloud Explore interface
4. Create dashboards using both local and cloud data sources

## Prometheus Configuration

The Prometheus configuration (`monitoring/prometheus.yml`) includes:

```yaml
remote_write:
  - url: https://prometheus-prod-56-prod-us-east-2.grafana.net/api/prom/push
    basic_auth:
      username: 2786173
      password: ${GRAFANA_CLOUD_API_TOKEN}
    queue_config:
      capacity: 10000
      max_shards: 200
      min_shards: 1
      max_samples_per_send: 5000
      batch_send_deadline: 5s
      min_backoff: 30ms
      max_backoff: 100ms
```

### Queue Configuration Explained
- **capacity**: Maximum number of samples to buffer before dropping
- **max_shards**: Maximum number of concurrent remote write connections
- **max_samples_per_send**: Batch size for sending samples
- **batch_send_deadline**: Maximum time to wait before sending a partial batch

## Grafana Datasource

The local Grafana instance is configured with two Prometheus datasources:

1. **Prometheus (Local)** - Default datasource pointing to local Prometheus
2. **Grafana Cloud - me1010101** - Cloud datasource for querying cloud metrics

Both datasources are available in Grafana dashboards and can be used interchangeably or together.

## Metrics Being Sent

The following metrics are automatically sent to Grafana Cloud:

### Application Metrics
- **discord-bot**: Discord bot performance and interaction metrics
- **event-gateway**: Webhook processing and routing metrics
- **refinory-api**: AI platform API metrics

### Infrastructure Metrics
- **redis**: Cache performance and memory usage
- **postgres**: Database connection pool and query performance
- **qdrant**: Vector database operations
- **vault**: Secrets management operations

### System Metrics (if deployed)
- **node-exporter**: Host system metrics (CPU, memory, disk, network)
- **cadvisor**: Container resource usage

## Monitoring Best Practices

### Use Local Grafana for Development
- Real-time debugging during development
- Fast query response times
- No data egress costs

### Use Grafana Cloud for Production
- Long-term metric retention
- Team-wide visibility
- Integration with alerting and on-call
- Correlation across multiple clusters/environments

### Hybrid Approach
- Keep local Grafana for immediate operational needs
- Use Grafana Cloud for:
  - Historical analysis
  - Cross-environment comparisons
  - Executive dashboards
  - SLO tracking

## Troubleshooting

### Metrics Not Appearing in Grafana Cloud

1. **Check Prometheus logs**:
   ```bash
   docker logs prometheus 2>&1 | tail -100
   ```

2. **Verify API token**:
   - Ensure the token has MetricsPublisher permissions
   - Check that the token hasn't expired
   - Verify it's correctly set in `.env`

3. **Test connectivity**:
   ```bash
   # Test from Prometheus container (using Basic Auth)
   docker exec prometheus wget -O- --user="2786173:${GRAFANA_CLOUD_API_TOKEN}" \
     https://prometheus-prod-56-prod-us-east-2.grafana.net/api/prom/api/v1/labels
   ```

4. **Check remote write queue**:
   - Navigate to Prometheus UI: http://localhost:9090
   - Go to Status → TSDB Status
   - Check "Remote Storage" section for any errors

### High Cardinality Issues

If you see warnings about high cardinality:

1. **Review metric labels**: Avoid labels with unbounded values (user IDs, timestamps)
2. **Use relabeling**: Drop unnecessary labels before remote write
3. **Add to prometheus.yml**:
   ```yaml
   remote_write:
     - url: https://...
       write_relabel_configs:
         - source_labels: [__name__]
           regex: 'high_cardinality_metric.*'
           action: drop
   ```

### Rate Limiting

If you hit Grafana Cloud rate limits:

1. **Adjust scrape intervals**: Increase intervals for less critical metrics
2. **Sample metrics**: Use `sample_limit` in scrape configs
3. **Reduce remote write frequency**:
   ```yaml
   remote_write:
     - url: https://...
       queue_config:
         batch_send_deadline: 30s  # Increase from 5s
   ```

## Cost Management

### Free Tier Limits
- **10,000 series**: Active metrics series limit
- **Current usage**: Check at https://grafana.com/orgs/me1010101

### Optimization Tips
1. **Drop unused metrics**: Remove metrics you don't actively monitor
2. **Aggregate before sending**: Use recording rules for pre-aggregation
3. **Use metric relabeling**: Filter metrics at the source
4. **Monitor active series**:
   ```promql
   count({__name__=~".+"})
   ```

## Alternative: Using Grafana Alloy

For more advanced use cases, consider using Grafana Alloy instead of Prometheus remote_write:

```bash
# Install Grafana Alloy
curl -O -L https://github.com/grafana/alloy/releases/download/v1.0.0/alloy-linux-amd64

# Configure Alloy (see monitoring/alloy-config.river for example)
./alloy run monitoring/alloy-config.river
```

Benefits:
- More efficient metric forwarding
- Built-in metric transformation
- Better handling of high cardinality
- Native support for OpenTelemetry

## Additional Resources

- [Grafana Cloud Documentation](https://grafana.com/docs/grafana-cloud/)
- [Prometheus Remote Write](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write)
- [Grafana Cloud Pricing](https://grafana.com/pricing/)
- [Metrics Optimization Guide](https://grafana.com/docs/grafana-cloud/metrics-prometheus/usage-reduction/)

## Security Considerations

1. **API Token Storage**: Never commit API tokens to git
2. **Token Rotation**: Rotate API tokens regularly (quarterly recommended)
3. **Least Privilege**: Use tokens with minimum required permissions
4. **Network Security**: Consider using AWS PrivateLink for production (see below)

### AWS PrivateLink (Optional)

For enhanced security in production, use AWS PrivateLink:

```yaml
# Service Name
com.amazonaws.vpce.us-east-2.vpce-svc-010316418b5cd8c09

# Private DNS Name (replace in remote_write URL)
mimir-prod-56-cortex-gw.us-east-2.vpce.grafana.net

# Supported AWS Regions
ca-central-1, us-east-1, us-east-2, us-west-2
```

Setup instructions: [Configure AWS PrivateLink](https://grafana.com/docs/grafana-cloud/connect-externally-hosted/aws-privatelink/)

---

**Status**: ✅ Configured and Ready
**Last Updated**: 2025-11-19
**Maintained By**: Strategickhaos DevOps Team
