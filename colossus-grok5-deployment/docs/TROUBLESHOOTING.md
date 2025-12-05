# Troubleshooting Guide

## Colossus Grok-5 Deployment Suite

This guide covers common issues and their solutions.

## Deployment Issues

### Namespace Creation Fails

**Symptom:** `kubectl apply -f k8s/namespace.yaml` fails

**Solutions:**
1. Check cluster permissions:
   ```bash
   kubectl auth can-i create namespace
   ```
2. Verify cluster connection:
   ```bash
   kubectl cluster-info
   ```

### Pods Not Starting

**Symptom:** Pods remain in `Pending` or `ContainerCreating` state

**Diagnosis:**
```bash
kubectl describe pod -n colossus-grok5 <pod-name>
kubectl get events -n colossus-grok5 --sort-by='.lastTimestamp'
```

**Common Causes:**

1. **Insufficient GPU resources**
   - Check GPU availability: `kubectl get nodes -o custom-columns=NAME:.metadata.name,GPU:.status.allocatable.nvidia\\.com/gpu`
   - Reduce replica count temporarily

2. **PVC not bound**
   - Check PVC status: `kubectl get pvc -n colossus-grok5`
   - Verify storage class exists: `kubectl get sc`

3. **Image pull failures**
   - Check image name and tag
   - Verify registry access: `kubectl get secrets -n colossus-grok5`

### HPA Not Scaling

**Symptom:** HPA shows `<unknown>` for metrics

**Diagnosis:**
```bash
kubectl get hpa grok5-trainer-hpa -n colossus-grok5 -o yaml
kubectl describe hpa grok5-trainer-hpa -n colossus-grok5
```

**Solutions:**
1. Verify metrics server is running:
   ```bash
   kubectl get deployment metrics-server -n kube-system
   ```

2. Check custom metrics adapter:
   ```bash
   kubectl get apiservices | grep custom.metrics
   ```

3. Verify Prometheus is scraping pods:
   ```bash
   kubectl port-forward svc/prometheus 9090:9090 -n monitoring
   # Then check targets in Prometheus UI
   ```

## Training Issues

### Energy Window Always Blocked

**Symptom:** Training never starts, energy window always denied

**Diagnosis:**
```bash
kubectl logs deployment/grok5-trainer -n colossus-grok5 | grep energy
```

**Solutions:**
1. Check power readings:
   - Verify power client is connected
   - Check if power > 250MW limit

2. Check Megapack SoC:
   - Verify battery client is connected
   - Check if SoC < 0.4 during peak hours

3. Adjust thresholds if needed:
   ```yaml
   env:
     - name: POWER_MW_LIMIT
       value: "275"  # Increase if safe
   ```

### Checkpoint Consensus Failing

**Symptom:** Checkpoints rejected, consensus < 99%

**Diagnosis:**
```bash
kubectl logs deployment/grok5-trainer -n colossus-grok5 | grep consensus
```

**Solutions:**
1. Check node registration:
   - Verify all training pods are registered
   - Check network connectivity between pods

2. Check for node failures:
   ```bash
   kubectl get pods -n colossus-grok5 | grep -v Running
   ```

3. Investigate divergent checkpoints:
   - Check for NaN in training
   - Verify gradient synchronization

### Safety Gate Failures

**Symptom:** Deployment blocked by safety gate

**Diagnosis:**
```bash
kubectl logs deployment/grok5-verifier -n colossus-grok5 | grep safety
```

**Check Individual Gates:**

1. **Power check:**
   ```bash
   kubectl exec -it deployment/grok5-trainer -n colossus-grok5 -- \
     curl localhost:9090/metrics | grep colossus_power_mw
   ```

2. **Provenance check:**
   - Verify Merkle roots are being created
   - Check OTS anchoring status

3. **Model quality:**
   - Check hallucination_rate metric
   - Check bias_score metric

## Data Pipeline Issues

### Provenance Batches Stalled

**Symptom:** No batches being processed

**Diagnosis:**
```bash
kubectl logs deployment/grok5-data-pipeline -n colossus-grok5
```

**Solutions:**
1. Check data source connection:
   - Verify X stream is accessible
   - Check authentication

2. Check toxicity filter:
   - If filtering all data, threshold may be too low
   - Check toxicity model is loaded

3. Check database connection:
   - Verify provenance DB is accessible
   - Check for disk space issues

### OTS Anchoring Failures

**Symptom:** OpenTimestamps operations failing

**Diagnosis:**
```bash
kubectl logs deployment/grok5-data-pipeline -n colossus-grok5 | grep OTS
```

**Solutions:**
1. Check calendar server connectivity:
   ```bash
   curl https://alice.btc.calendar.opentimestamps.org
   ```

2. Check network policies:
   - Ensure outbound HTTPS is allowed
   - Check proxy configuration

## Monitoring Issues

### Metrics Not Appearing in Prometheus

**Symptom:** Grafana dashboards show no data

**Diagnosis:**
```bash
kubectl port-forward svc/prometheus 9090:9090 -n monitoring
# Check targets at http://localhost:9090/targets
```

**Solutions:**
1. Check service discovery:
   - Verify Prometheus annotations on pods
   - Check ServiceMonitor if using operator

2. Check network policies:
   - Ensure monitoring namespace can reach colossus-grok5

3. Verify metrics endpoint:
   ```bash
   kubectl exec -it <pod> -n colossus-grok5 -- curl localhost:9090/metrics
   ```

### Alerts Not Firing

**Symptom:** Known issues not triggering alerts

**Solutions:**
1. Check Alertmanager:
   ```bash
   kubectl logs deployment/alertmanager -n monitoring
   ```

2. Verify rules are loaded:
   ```bash
   kubectl get prometheusrules -n colossus-grok5
   ```

3. Check webhook endpoints:
   - Verify Discord/ntfy endpoints are correct
   - Check for authentication issues

## Performance Issues

### High Memory Usage

**Symptom:** Pods OOMKilled

**Solutions:**
1. Increase memory limits:
   ```yaml
   resources:
     limits:
       memory: "256Gi"  # Increase from 128Gi
   ```

2. Check for memory leaks:
   - Review training batch size
   - Check checkpoint size

### GPU Underutilization

**Symptom:** GPU utilization < 50%

**Diagnosis:**
```bash
kubectl exec -it <pod> -n colossus-grok5 -- nvidia-smi
```

**Solutions:**
1. Increase batch size
2. Check data loader bottlenecks
3. Verify GPU interconnect performance

## Recovery Procedures

### Emergency Rollback

```bash
./scripts/rollback.sh --cluster=colossus2 --to-tag=vLAST_GOOD --yes
```

### Manual Database Recovery

```bash
# Restore from backup
kubectl exec -it postgres-0 -n colossus-grok5 -- \
  pg_restore -d grok5 /backup/latest.dump
```

### Reset Training State

```bash
# Scale down
kubectl scale deployment grok5-trainer -n colossus-grok5 --replicas=0

# Clear checkpoints (DANGER)
kubectl exec -it <storage-pod> -- rm -rf /checkpoints/*

# Scale up
kubectl scale deployment grok5-trainer -n colossus-grok5 --replicas=1000
```

## Getting Help

If issues persist:

1. Collect diagnostics:
   ```bash
   kubectl cluster-info dump --namespaces=colossus-grok5 > diagnostics.txt
   ```

2. Check recent changes:
   ```bash
   kubectl rollout history deployment/grok5-trainer -n colossus-grok5
   ```

3. Contact infrastructure team with:
   - Symptom description
   - Diagnostic output
   - Recent changes

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `GRID_CONSTRAINT` | Power > 250MW | Wait for power reduction |
| `OFFPEAK_REQUIRED` | Peak hours + low SoC | Wait for off-peak window |
| `Provenance root/OTS invalid` | OTS verification failed | Check OTS connectivity |
| `Checkpoint consensus < 0.99` | Node disagreement | Check for failed nodes |
| `Bias score >= 0.25` | Model quality issue | Review training data |
