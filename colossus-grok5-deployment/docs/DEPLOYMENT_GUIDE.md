# Deployment Guide

## Colossus Grok-5 Deployment Suite

This guide provides detailed instructions for deploying the Colossus Grok-5 training system on a 550,000 GPU cluster.

## Prerequisites

### Infrastructure Requirements

1. **Kubernetes Cluster**
   - Kubernetes 1.28+
   - GPU operator installed (NVIDIA)
   - 550,000 GPU nodes available
   - Istio service mesh (optional but recommended)
   - Prometheus Operator installed

2. **Storage**
   - High-performance NVMe storage class
   - Minimum 100TB for training data
   - Minimum 50TB for checkpoints

3. **Network**
   - High-bandwidth interconnect (InfiniBand or similar)
   - Network policies supported

### Software Requirements

- `kubectl` CLI configured for cluster access
- Python 3.11+ (for running tests)
- Bash 4.0+

## Deployment Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd colossus-grok5-deployment
```

### 2. Configure Environment

Create a `.env` file or set environment variables:

```bash
export CLUSTER_NAME="colossus2"
export REGION="nv-giga-01"
export NAMESPACE="colossus-grok5"
```

### 3. Review Configuration

Edit `k8s/deployment-550k-gpu.yaml` to adjust:

- Replica count
- Resource limits
- Environment variables

Edit the ConfigMap in the deployment file:

```yaml
training:
  batch_size: 4096
  learning_rate: 0.0001
  
energy:
  power_limit_mw: 250
  megapack_soc_min: 0.4
  
safety:
  hallucination_threshold: 0.15
  bias_threshold: 0.25
```

### 4. Deploy

Run the deployment script:

```bash
./scripts/deploy.sh --cluster=colossus2 --region=nv-giga-01
```

Options:
- `--cluster=NAME` - Kubernetes cluster name
- `--region=REGION` - Deployment region
- `--namespace=NS` - Kubernetes namespace
- `--skip-tests` - Skip integration tests
- `--dry-run` - Print commands without executing

### 5. Verify Deployment

Check deployment status:

```bash
./scripts/health-check.sh
```

Or manually:

```bash
kubectl get pods -n colossus-grok5
kubectl get hpa -n colossus-grok5
kubectl logs -f deployment/grok5-trainer -n colossus-grok5
```

## Configuration Reference

### Energy Management

| Parameter | Default | Description |
|-----------|---------|-------------|
| `power_limit_mw` | 250 | Maximum power consumption in MW |
| `offpeak_start` | 02:00 | Start of off-peak window |
| `offpeak_end` | 06:00 | End of off-peak window |
| `megapack_soc_min` | 0.4 | Minimum battery state of charge |

### Safety Thresholds

| Parameter | Default | Description |
|-----------|---------|-------------|
| `hallucination_threshold` | 0.15 | Maximum hallucination rate |
| `bias_threshold` | 0.25 | Maximum bias score |
| `checkpoint_consensus_min` | 0.99 | Minimum consensus for checkpoints |
| `toxicity_threshold` | 0.30 | Maximum toxicity for training data |

### Scaling Configuration

The HPA is configured for energy-aware scaling:

```yaml
minReplicas: 1000
maxReplicas: 550000
metrics:
  - type: Pods
    pods:
      metric:
        name: power_mw
      target:
        type: AverageValue
        averageValue: "250"
```

## Rollback Procedures

### Quick Rollback

```bash
./scripts/rollback.sh --cluster=colossus2 --to-tag=vLAST_GOOD
```

### Manual Rollback

1. Scale down:
   ```bash
   kubectl scale deployment grok5-trainer -n colossus-grok5 --replicas=1000
   ```

2. Update image:
   ```bash
   kubectl set image deployment/grok5-trainer \
     trainer=ghcr.io/xai/grok5-trainer:v1.0.0 \
     -n colossus-grok5
   ```

3. Verify:
   ```bash
   kubectl rollout status deployment/grok5-trainer -n colossus-grok5
   ```

## Monitoring

### Grafana Dashboards

Import the dashboard JSON files:

1. `monitoring/grafana-dashboard-colossus.json` - Overview
2. `monitoring/grafana-dashboard-energy.json` - Energy management
3. `monitoring/grafana-dashboard-provenance.json` - Data provenance

### Key Alerts

- `PowerConsumptionCritical` - Power > 250MW
- `CheckpointConsensusDrop` - Consensus < 99%
- `SafetyGateFailed` - Any safety check fails

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.

## Security Considerations

1. **Secrets Management**: Use HashiCorp Vault or Kubernetes secrets
2. **Network Policies**: Default deny with explicit allow rules
3. **RBAC**: Least privilege for service accounts
4. **Audit Logging**: All operations logged with chain hashing

## Support

For issues or questions:
- Check the troubleshooting guide
- Review the architecture documentation
- Contact the infrastructure team
