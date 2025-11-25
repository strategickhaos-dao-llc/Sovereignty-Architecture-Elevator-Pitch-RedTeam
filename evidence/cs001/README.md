# Evidence Directory - Case Study CS-001
# Field Operations Telemetry and Agent Reconciliation Loop

This directory contains artifacts for case study CS-001 as referenced in
`engineering_methodology_domain.yaml`.

## Artifacts

| File | Type | Description |
|------|------|-------------|
| `latency_spike_20251120.pcap` | PCAP | Network capture during degradation event |
| `node137_config.yaml` | VM Config | VM configuration at time of incident |
| `alert_definition.yaml` | YAML Schema | Alertmanager rule that triggered detection |
| `agent_reconciliation.log` | Log | Agent decision log with RAG citations |
| `prometheus_metrics.json` | JSON | Prometheus metrics export during incident window |

## Disclaimer

INTERNAL DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED

## Notes

- PCAP file redacted for PII and sensitive network details
- Timestamps normalized to UTC
- All artifacts signed with GPG (see .asc files)
