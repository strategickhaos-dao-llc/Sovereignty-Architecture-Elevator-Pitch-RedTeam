# Observability Stack

## Overview

The Strategickhaos Sovereignty Architecture integrates with a comprehensive observability stack for monitoring, logging, and tracing across all components.

## Stack Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    OBSERVABILITY STACK                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐           │
│  │ Prometheus  │   │    Loki     │   │    Tempo    │           │
│  │  (Metrics)  │   │   (Logs)    │   │  (Traces)   │           │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘           │
│         │                 │                 │                   │
│         └────────────────┬┴─────────────────┘                   │
│                          │                                      │
│                  ┌───────▼───────┐                              │
│                  │    Grafana    │                              │
│                  │ (Dashboards)  │                              │
│                  └───────────────┘                              │
│                                                                 │
│  ┌─────────────────────────────────────────────────────┐       │
│  │              OpenTelemetry Collector                │       │
│  │         (Unified collection & routing)              │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Metrics (Prometheus)

### Configuration

```yaml
metrics:
  provider: "prometheus"
  alertmanager_webhook: "https://events.strategickhaos.com/alert"
```

### Key Metrics

#### Discord Bot Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Command execution metrics
command_counter = Counter(
    'discord_commands_total',
    'Total Discord commands executed',
    ['command', 'status']
)

command_latency = Histogram(
    'discord_command_duration_seconds',
    'Command execution duration',
    ['command'],
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

# Bot health metrics
bot_connected = Gauge(
    'discord_bot_connected',
    'Discord bot connection status'
)

# Rate limiting metrics
rate_limit_hits = Counter(
    'discord_rate_limit_hits_total',
    'Discord API rate limit hits'
)
```

#### Event Gateway Metrics

```python
# Webhook processing metrics
webhook_counter = Counter(
    'webhook_events_total',
    'Total webhook events received',
    ['source', 'event_type']
)

webhook_latency = Histogram(
    'webhook_processing_seconds',
    'Webhook processing duration',
    ['source']
)

# Signature verification metrics
signature_verification = Counter(
    'webhook_signature_verification_total',
    'Webhook signature verifications',
    ['result']
)
```

### Alerting Rules

```yaml
groups:
  - name: discord-ops
    rules:
      - alert: DiscordBotDisconnected
        expr: discord_bot_connected == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Discord bot disconnected"
          
      - alert: HighCommandLatency
        expr: histogram_quantile(0.95, discord_command_duration_seconds) > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High command latency detected"
          
      - alert: WebhookVerificationFailures
        expr: rate(webhook_signature_verification_total{result="failed"}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High rate of webhook signature failures"
```

## Logging (Loki)

### Configuration

```yaml
logging:
  provider: "loki"
  endpoint: "https://loki.strategickhaos.internal"
  auth_secret_ref: "vault://kv/observability/loki_auth"
```

### Log Format

```json
{
  "timestamp": "2024-01-15T10:23:45.123Z",
  "level": "INFO",
  "service": "discord-ops-bot",
  "trace_id": "abc123",
  "span_id": "def456",
  "message": "Command executed successfully",
  "context": {
    "command": "/status",
    "user_id": "123456789",
    "channel_id": "987654321",
    "duration_ms": 150
  }
}
```

### Structured Logging

```python
import structlog

logger = structlog.get_logger()

async def execute_command(ctx, command: str):
    logger.info(
        "command_executed",
        command=command,
        user_id=ctx.author.id,
        channel_id=ctx.channel.id,
        guild_id=ctx.guild.id
    )
```

### Log Queries (LogQL)

```logql
# All errors from discord-ops-bot
{service="discord-ops-bot"} |= "ERROR"

# Command execution latency
{service="discord-ops-bot"} | json | command != "" | line_format "{{.command}} {{.duration_ms}}ms"

# Webhook failures
{service="event-gateway"} |= "signature verification failed"
```

## Tracing (OpenTelemetry)

### Configuration

```yaml
tracing:
  provider: "otel"
  collector_endpoint: "http://otel-collector.observability:4317"
```

### Instrumentation

```python
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer(__name__)

@bot.command(name="deploy")
async def deploy(ctx, env: str, tag: str):
    with tracer.start_as_current_span("deploy_command") as span:
        span.set_attribute("deployment.env", env)
        span.set_attribute("deployment.tag", tag)
        span.set_attribute("user.id", str(ctx.author.id))
        
        try:
            result = await trigger_deployment(env, tag)
            span.set_status(Status(StatusCode.OK))
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)
            raise
```

### Trace Context Propagation

```python
from opentelemetry.propagate import inject

async def call_external_api(url: str, payload: dict):
    headers = {}
    inject(headers)  # Inject trace context
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
    
    return response
```

## Grafana Dashboards

### Discord Ops Overview

```json
{
  "title": "Discord Ops Overview",
  "panels": [
    {
      "title": "Command Rate",
      "type": "timeseries",
      "targets": [
        {
          "expr": "rate(discord_commands_total[5m])",
          "legendFormat": "{{command}}"
        }
      ]
    },
    {
      "title": "Command Latency (p95)",
      "type": "gauge",
      "targets": [
        {
          "expr": "histogram_quantile(0.95, rate(discord_command_duration_seconds_bucket[5m]))"
        }
      ]
    },
    {
      "title": "Bot Status",
      "type": "stat",
      "targets": [
        {
          "expr": "discord_bot_connected"
        }
      ]
    }
  ]
}
```

### Event Gateway Dashboard

```json
{
  "title": "Event Gateway",
  "panels": [
    {
      "title": "Webhook Events",
      "type": "timeseries",
      "targets": [
        {
          "expr": "rate(webhook_events_total[5m])",
          "legendFormat": "{{source}} - {{event_type}}"
        }
      ]
    },
    {
      "title": "Verification Status",
      "type": "piechart",
      "targets": [
        {
          "expr": "sum by (result) (webhook_signature_verification_total)"
        }
      ]
    }
  ]
}
```

## Alert Routing to Discord

### Alertmanager Configuration

```yaml
route:
  receiver: discord-alerts
  routes:
    - match:
        severity: critical
      receiver: discord-critical
    - match:
        severity: warning
      receiver: discord-warnings

receivers:
  - name: discord-alerts
    webhook_configs:
      - url: "https://events.strategickhaos.com/alert"
        
  - name: discord-critical
    webhook_configs:
      - url: "https://events.strategickhaos.com/alert"
        send_resolved: true
```

### Alert Format

```python
def format_alert(alert: dict) -> dict:
    """Format Alertmanager alert for Discord."""
    status = alert["status"]
    color = 0xff0000 if status == "firing" else 0x00ff00
    
    return {
        "embeds": [{
            "title": f"🚨 {alert['labels']['alertname']}",
            "description": alert["annotations"].get("summary", ""),
            "color": color,
            "fields": [
                {"name": "Status", "value": status, "inline": True},
                {"name": "Severity", "value": alert["labels"].get("severity", "unknown"), "inline": True},
                {"name": "Service", "value": alert["labels"].get("service", "unknown"), "inline": True},
            ],
            "timestamp": alert["startsAt"]
        }]
    }
```

## LLM Directive: Observability Extensions

> **AI Agent Note**: When extending observability:
> 1. Add metrics for all new commands and endpoints
> 2. Use structured logging with consistent field names
> 3. Propagate trace context across service boundaries
> 4. Create dashboards for new components
> 5. Configure alerts for critical paths

---

*Part of the Strategickhaos Sovereignty Architecture - Discord DevOps Control Plane*
