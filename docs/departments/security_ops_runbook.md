# Security Operations Runbook

> **Target Audience:** Security Operations Department  
> **Goal:** Deploy KnowledgePods + hardened infrastructure without touching board-level theory

---

## Overview

This runbook provides step-by-step instructions for deploying and operating the StrategicKhaos Educational Swarm infrastructure securely. All operations described are **strictly defensive** and comply with board-mandated legal constraints.

---

## Prerequisites

### Required Access

| Access | Purpose | How to Obtain |
|--------|---------|---------------|
| Kubernetes cluster admin | Deploy and manage workloads | Request via IT ticket |
| Container registry pull | Access container images | Automatic with cluster access |
| Secrets manager read | Access credentials | Request via security team |
| Monitoring dashboards | View system health | Automatic with cluster access |

### Required Knowledge

- Kubernetes fundamentals (pods, deployments, services)
- YAML syntax
- Basic networking (DNS, TLS, load balancing)
- Container security basics

### Tools Required

```bash
# Verify these tools are installed
kubectl version --client    # v1.28+
helm version                # v3.12+
kubeseal --version          # v0.24+ (for sealed secrets)
```

---

## Cluster Prerequisites

### Namespaces

Ensure these namespaces exist:

```bash
# Create required namespaces
kubectl create namespace knowledgepods --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace ops --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -

# Verify namespaces
kubectl get namespaces
```

### Resource Quotas

Apply resource quotas to control consumption:

```yaml
# resource-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: knowledgepods-quota
  namespace: knowledgepods
spec:
  hard:
    requests.cpu: "8"
    requests.memory: 32Gi
    limits.cpu: "16"
    limits.memory: 64Gi
    pods: "200"
```

```bash
kubectl apply -f resource-quota.yaml
```

### Secrets Setup

**Option A: Using Sealed Secrets (Recommended)**

```bash
# Encrypt secrets before storing in git
kubeseal --format yaml < secrets.yaml > sealed-secrets.yaml
kubectl apply -f sealed-secrets.yaml
```

**Option B: Using HashiCorp Vault**

```bash
# Configure Vault integration
kubectl apply -f vault-auth.yaml
kubectl apply -f vault-secrets-operator.yaml
```

### Storage Classes

Verify required storage classes exist:

```bash
kubectl get storageclasses

# Expected output should include:
# NAME            PROVISIONER
# standard        kubernetes.io/gce-pd (or equivalent)
# fast-ssd        kubernetes.io/gce-pd (or equivalent)
```

---

## Deploying the KnowledgePod CRD + Controller

### Step 1: Apply the Custom Resource Definition

```bash
# Apply the CRD
kubectl apply -f k8s/knowledgepod-crd.yaml

# Verify CRD is registered
kubectl get crds | grep knowledgepod
# Expected: knowledgepods.education.strategickhaos.io
```

### Step 2: Deploy the Controller

```yaml
# controller-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: knowledgepod-controller
  namespace: knowledgepods
spec:
  replicas: 2
  selector:
    matchLabels:
      app: knowledgepod-controller
  template:
    metadata:
      labels:
        app: knowledgepod-controller
    spec:
      serviceAccountName: knowledgepod-controller
      containers:
      - name: controller
        image: registry.strategickhaos.io/knowledgepod-controller:latest
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        securityContext:
          runAsNonRoot: true
          readOnlyRootFilesystem: true
          allowPrivilegeEscalation: false
```

```bash
kubectl apply -f controller-deployment.yaml
kubectl rollout status deployment/knowledgepod-controller -n knowledgepods
```

### Step 3: Deploy Example KnowledgePod

```bash
# Deploy the example pod
kubectl apply -f k8s/knowledgepods/example_pod_q001.yaml

# Verify deployment
kubectl get knowledgepods -n knowledgepods
kubectl describe knowledgepod knowledgepod-q001 -n knowledgepods
```

---

## Safely Exposing Pods (Ingress, TLS, Auth)

### Ingress Configuration

```yaml
# knowledgepod-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: knowledgepod-ingress
  namespace: knowledgepods
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  tls:
  - hosts:
    - learn.strategickhaos.io
    secretName: knowledgepod-tls
  rules:
  - host: learn.strategickhaos.io
    http:
      paths:
      - path: /pod
        pathType: Prefix
        backend:
          service:
            name: knowledgepod-service
            port:
              number: 80
```

```bash
kubectl apply -f knowledgepod-ingress.yaml
```

### TLS Certificate Management

```yaml
# cluster-issuer.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: certs@strategickhaos.io
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
```

**Verify TLS:**
```bash
# Check certificate status
kubectl get certificates -n knowledgepods
kubectl describe certificate knowledgepod-tls -n knowledgepods
```

### Authentication (OAuth2 Proxy)

```yaml
# oauth2-proxy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: oauth2-proxy
  namespace: knowledgepods
spec:
  replicas: 2
  selector:
    matchLabels:
      app: oauth2-proxy
  template:
    spec:
      containers:
      - name: oauth2-proxy
        image: quay.io/oauth2-proxy/oauth2-proxy:v7.5.1
        args:
        - --provider=oidc
        - --upstream=http://knowledgepod-service:80
        - --http-address=0.0.0.0:4180
        - --cookie-secure=true
        - --cookie-httponly=true
        env:
        - name: OAUTH2_PROXY_CLIENT_ID
          valueFrom:
            secretKeyRef:
              name: oauth2-secrets
              key: client-id
        - name: OAUTH2_PROXY_CLIENT_SECRET
          valueFrom:
            secretKeyRef:
              name: oauth2-secrets
              key: client-secret
```

---

## Monitoring & Alerting Basics

### Prometheus Monitoring

**ServiceMonitor for KnowledgePods:**

```yaml
# servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: knowledgepod-monitor
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: knowledgepod
  endpoints:
  - port: metrics
    interval: 30s
```

**Key Metrics to Monitor:**

| Metric | Purpose | Alert Threshold |
|--------|---------|-----------------|
| `knowledgepod_requests_total` | Request volume | Rate change > 200% |
| `knowledgepod_errors_total` | Error count | > 10/min |
| `knowledgepod_latency_seconds` | Response time | P99 > 2s |
| `container_memory_usage_bytes` | Memory usage | > 80% limit |
| `container_cpu_usage_seconds_total` | CPU usage | > 80% limit |

### Grafana Dashboard

Import the pre-built dashboard:

```bash
# Dashboard available at:
# grafana/dashboards/knowledgepod-overview.json

# Or import via Grafana UI:
# Dashboard ID: XXXXX (from Grafana.com)
```

### Falco Security Monitoring

**Deploy Falco:**

```bash
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm install falco falcosecurity/falco \
  --namespace monitoring \
  --set falcosidekick.enabled=true \
  --set falcosidekick.config.discord.webhookurl="$DISCORD_WEBHOOK"
```

**Custom Rules for KnowledgePods:**

```yaml
# falco-rules.yaml
- rule: KnowledgePod Shell Access
  desc: Detect shell execution in KnowledgePod containers
  condition: >
    spawned_process and 
    container.image.repository contains "knowledgepod" and
    proc.name in (shell_binaries)
  output: >
    Shell spawned in KnowledgePod 
    (user=%user.name container=%container.id command=%proc.cmdline)
  priority: WARNING
  
- rule: KnowledgePod Network Connection to Unexpected IP
  desc: Detect unexpected outbound connections
  condition: >
    outbound and 
    container.image.repository contains "knowledgepod" and
    not fd.sip in (allowed_ips)
  output: >
    Unexpected outbound connection from KnowledgePod
    (container=%container.id dest=%fd.sip)
  priority: NOTICE
```

### Alert Configuration

```yaml
# alerting-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: knowledgepod-alerts
  namespace: monitoring
spec:
  groups:
  - name: knowledgepod
    rules:
    - alert: KnowledgePodHighErrorRate
      expr: |
        sum(rate(knowledgepod_errors_total[5m])) > 10
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: High error rate in KnowledgePods
        
    - alert: KnowledgePodHighLatency
      expr: |
        histogram_quantile(0.99, 
          rate(knowledgepod_latency_seconds_bucket[5m])) > 2
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: High latency in KnowledgePods
```

---

## Legal Boundaries Statement

### ⚠️ Critical: What Security Operations CAN Do

✅ **Authorized Activities:**

1. **Monitor owned infrastructure**
   - Deploy and configure monitoring tools
   - Review logs and metrics from our systems
   - Set up alerts for anomalies

2. **Defend owned systems**
   - Configure firewalls and network policies
   - Implement access controls
   - Deploy security tools (Falco, etc.)

3. **Respond to incidents on owned systems**
   - Isolate compromised pods/nodes
   - Preserve evidence from our systems
   - Restore from backups

4. **Test security on owned systems**
   - With written authorization
   - Within defined scope
   - Following approved procedures

### 🚫 Critical: What Security Operations CANNOT Do

❌ **Prohibited Activities:**

1. **No access to third-party systems**
   - Do not scan external IPs
   - Do not attempt to access cloud provider consoles beyond our scope
   - Do not test partner systems without explicit authorization

2. **No hack-back or offensive operations**
   - Even if we are attacked, do not attack back
   - Report to law enforcement instead
   - Focus on defense and recovery

3. **No unauthorized security testing**
   - All testing requires written authorization
   - Stay within defined scope
   - Document all activities

4. **No interception of external communications**
   - Only monitor our own network segments
   - Do not intercept traffic on networks we don't own

### Incident Response Chain

```
Security Event Detected
        │
        ▼
Is it on our owned infrastructure?
        │
   ┌────┴────┐
   │         │
  YES        NO
   │         │
   ▼         ▼
Respond    DO NOT
per IRP    ENGAGE
   │         │
   │         ▼
   │     Report to
   │     management
   │         │
   ▼         ▼
Document  Potential
findings  law enforcement
```

---

## Troubleshooting

### Common Issues

**KnowledgePod Not Starting:**
```bash
# Check pod status
kubectl describe knowledgepod <name> -n knowledgepods

# Check controller logs
kubectl logs -l app=knowledgepod-controller -n knowledgepods

# Check events
kubectl get events -n knowledgepods --sort-by='.lastTimestamp'
```

**TLS Certificate Issues:**
```bash
# Check certificate status
kubectl describe certificate -n knowledgepods

# Check cert-manager logs
kubectl logs -l app=cert-manager -n cert-manager
```

**High Latency:**
```bash
# Check pod resource usage
kubectl top pods -n knowledgepods

# Check for throttling
kubectl describe pod <pod-name> -n knowledgepods | grep -A5 "Resources"
```

---

## Runbook Checklist

### Pre-Deployment
- [ ] Namespaces created
- [ ] Resource quotas applied
- [ ] Secrets configured (Sealed Secrets or Vault)
- [ ] Storage classes verified

### Deployment
- [ ] CRD applied and verified
- [ ] Controller deployed and healthy
- [ ] Example KnowledgePod deployed

### Security Configuration
- [ ] Ingress with TLS configured
- [ ] OAuth2 authentication enabled
- [ ] Network policies applied
- [ ] Falco deployed and configured

### Monitoring
- [ ] ServiceMonitor configured
- [ ] Grafana dashboard imported
- [ ] Alert rules deployed
- [ ] Discord/PagerDuty integration tested

### Documentation
- [ ] Runbook reviewed and current
- [ ] Access list documented
- [ ] Escalation contacts verified

---

## Related Documents

- [Infrastructure Overview](../../infra/infrastructure_verification.md)
- [Defensive Operations Summary](../../legal/defensive_ops_summary.md)
- [100 Failure Modes](../../risk/100_failure_modes.md)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-30 | Security Ops | Initial runbook |

**Classification:** Internal - Security Operations
