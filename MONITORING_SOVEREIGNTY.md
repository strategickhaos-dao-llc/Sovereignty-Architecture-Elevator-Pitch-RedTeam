# Monitoring Sovereignty Doctrine — CloudOS Edition

## The Law
All telemetry stays on localhost. Forever.

- No remote_write  
- No Grafana Cloud  
- No Mimir SaaS  
- No New Relic / Datadog / Splunk  

If you need >10k active series → deploy Thanos + object storage on your own hardware or VPS. Cost: $0–$50/month vs $500+/month rented.

## Local Stack (all on localhost)

| Service     | Port  | URL                     | Purpose                    |
|-------------|-------|-------------------------|----------------------------|
| Prometheus  | 9090  | http://localhost:9090   | Metrics storage & query    |
| Grafana     | 3000  | http://localhost:3000   | Dashboards & alerts        |
| Loki        | 3100  | http://localhost:3100   | Logs                       |
| Jaeger      | 16686 | http://localhost:16686  | Distributed tracing        |
| Alertmanager| 9093  | http://localhost:9093   | Alert routing              |

## Scaling Beyond Free-Tier Rented Limits

When you hit ~50k series:
1. Add Thanos Sidecar to Prometheus
2. Deploy Thanos Querier + Store Gateway
3. Point to your own MinIO/S3-compatible bucket
4. Keep querying via local Grafana → zero config change

You stay sovereign. You stay cheap. You stay in control.

## Enforcement

```bash
make check-sovereignty   # fails CI if anyone tries to add remote_write
```

Real operators run their own computers.
