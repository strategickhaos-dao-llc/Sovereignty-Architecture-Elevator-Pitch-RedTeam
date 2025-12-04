# Infrastructure Verification Overview

> **Purpose:** This document provides an overview of the StrategicKhaos infrastructure components, including Kubernetes clusters, networking, storage, and observability systems.

## Infrastructure Summary

| Component | Status | Notes |
|-----------|--------|-------|
| Kubernetes Cluster | ✅ Operational | Multi-node production cluster |
| Container Registry | ✅ Operational | Private registry with scanning |
| Object Storage | ✅ Operational | S3-compatible for videos/assets |
| Database | ✅ Operational | PostgreSQL with HA |
| CDN | ✅ Operational | Global content delivery |
| Monitoring | ✅ Operational | Prometheus + Grafana stack |
| Logging | ✅ Operational | Loki + Fluentd |
| Security | ✅ Operational | Falco + network policies |

---

## Kubernetes Cluster Architecture

### Control Plane

```
┌─────────────────────────────────────────────────────────────┐
│                      Control Plane                          │
├─────────────┬─────────────┬─────────────┬─────────────────┤
│ API Server  │ Controller  │ Scheduler   │ etcd           │
│ (HA x3)     │ Manager     │ (HA x3)     │ (HA x3)        │
└─────────────┴─────────────┴─────────────┴─────────────────┘
```

**Configuration:**
- Kubernetes Version: 1.28.x
- API Server: 3 replicas behind load balancer
- etcd: 3-node cluster with automatic snapshots
- RBAC: Enabled with least-privilege policies

### Worker Nodes

```
┌─────────────────────────────────────────────────────────────┐
│                      Worker Pool                            │
├─────────────────────────────────────────────────────────────┤
│  Node Pool: general-purpose                                 │
│  - Instance Type: 4 vCPU / 16GB RAM                        │
│  - Node Count: 3-10 (autoscaling)                          │
│  - Workloads: Web services, APIs, background jobs          │
├─────────────────────────────────────────────────────────────┤
│  Node Pool: gpu-compute                                     │
│  - Instance Type: GPU-enabled (NVIDIA T4/A100)             │
│  - Node Count: 0-4 (scale to zero when idle)               │
│  - Workloads: AI video generation, model inference         │
└─────────────────────────────────────────────────────────────┘
```

### Namespaces

| Namespace | Purpose | Resource Quotas |
|-----------|---------|-----------------|
| `production` | Production workloads | CPU: 16 cores, Memory: 64GB |
| `staging` | Pre-production testing | CPU: 8 cores, Memory: 32GB |
| `development` | Development/testing | CPU: 4 cores, Memory: 16GB |
| `ops` | Operational tools (bots, gateways) | CPU: 4 cores, Memory: 16GB |
| `monitoring` | Observability stack | CPU: 4 cores, Memory: 32GB |
| `knowledgepods` | Educational content delivery | CPU: 8 cores, Memory: 32GB |

---

## Networking Architecture

### Network Topology

```
                    ┌─────────────────┐
                    │    Internet     │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │   CloudFlare    │
                    │   (DDoS/CDN)    │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │  Load Balancer  │
                    │   (L7/Ingress)  │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────┴───────┐   ┌───────┴───────┐   ┌───────┴───────┐
│ Ingress-NGINX │   │ Ingress-NGINX │   │ Ingress-NGINX │
│   (Replica 1) │   │   (Replica 2) │   │   (Replica 3) │
└───────────────┘   └───────────────┘   └───────────────┘
        │                    │                    │
        └────────────────────┴────────────────────┘
                             │
                    ┌────────┴────────┐
                    │  Service Mesh   │
                    │   (Optional)    │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │   Pod Network   │
                    │    (Calico)     │
                    └─────────────────┘
```

### DNS Configuration

| Domain | Purpose | Provider |
|--------|---------|----------|
| `strategickhaos.io` | Primary domain | CloudFlare |
| `api.strategickhaos.io` | API endpoints | CloudFlare |
| `cdn.strategickhaos.io` | Content delivery | CloudFlare CDN |
| `*.internal.strategickhaos.io` | Internal services | CoreDNS |

### TLS/SSL

- Certificate Provider: Let's Encrypt (via cert-manager)
- Certificate Rotation: Automatic (30 days before expiry)
- Minimum TLS Version: 1.2
- Cipher Suite: Modern (AEAD ciphers only)

---

## Storage Architecture

### Object Storage (S3-Compatible)

| Bucket | Purpose | Retention | Access |
|--------|---------|-----------|--------|
| `sk-videos-prod` | AI-generated educational videos | Indefinite | Public read via CDN |
| `sk-assets-prod` | Static assets (images, docs) | Indefinite | Public read via CDN |
| `sk-uploads-prod` | User uploads | 90 days | Private |
| `sk-backups` | System backups | 30 days | Private |

**Configuration:**
- Storage Provider: AWS S3 / MinIO
- Replication: Cross-region for production buckets
- Versioning: Enabled for all buckets
- Encryption: AES-256 at rest

### Persistent Volumes

| Volume Class | Purpose | Provisioner | Reclaim Policy |
|--------------|---------|-------------|----------------|
| `standard` | General workloads | EBS/GCE-PD | Delete |
| `fast-ssd` | Databases, high IOPS | EBS gp3/GCE SSD | Retain |
| `archive` | Long-term storage | EBS st1/Archive | Retain |

### Database

**Primary Database: PostgreSQL**
- Version: 15.x
- Configuration: Primary + 2 replicas
- Storage: 500GB SSD
- Backup: Daily snapshots, 30-day retention
- Point-in-time Recovery: 7 days

---

## Observability Stack

### Metrics (Prometheus)

```
┌─────────────────────────────────────────────────────────────┐
│                    Prometheus Stack                         │
├─────────────────────────────────────────────────────────────┤
│  Prometheus Server                                          │
│  - Scrape Interval: 15s                                    │
│  - Retention: 15 days                                      │
│  - Storage: 100GB                                          │
├─────────────────────────────────────────────────────────────┤
│  Alert Manager                                              │
│  - Routing: Severity-based                                 │
│  - Receivers: Discord, PagerDuty, Email                    │
├─────────────────────────────────────────────────────────────┤
│  Grafana                                                    │
│  - Dashboards: Pre-built for K8s, Apps, Custom             │
│  - Auth: OIDC/SAML                                         │
└─────────────────────────────────────────────────────────────┘
```

### Logging (Loki)

```
┌─────────────────────────────────────────────────────────────┐
│                      Logging Stack                          │
├─────────────────────────────────────────────────────────────┤
│  Fluentd/Fluent Bit (DaemonSet)                            │
│  - Collects logs from all pods                             │
│  - Enriches with K8s metadata                              │
├─────────────────────────────────────────────────────────────┤
│  Loki                                                       │
│  - Index: BoltDB Shipper                                   │
│  - Storage: S3 backend                                     │
│  - Retention: 30 days                                      │
├─────────────────────────────────────────────────────────────┤
│  Grafana (Log Viewer)                                       │
│  - Integrated with metrics dashboards                      │
│  - LogQL queries                                           │
└─────────────────────────────────────────────────────────────┘
```

### Tracing (OpenTelemetry)

- Collector: OpenTelemetry Collector
- Backend: Jaeger / Tempo
- Instrumentation: Auto-instrumentation for Node.js, Python
- Sampling: 10% production, 100% staging

---

## Security Infrastructure

### Runtime Security (Falco)

```
┌─────────────────────────────────────────────────────────────┐
│                    Falco Configuration                      │
├─────────────────────────────────────────────────────────────┤
│  DaemonSet: Running on all worker nodes                    │
│  Rules: Default + Custom educational platform rules         │
│  Output: Prometheus metrics, Alertmanager, Discord          │
├─────────────────────────────────────────────────────────────┤
│  Key Detection Rules:                                       │
│  - Privileged container execution                          │
│  - Sensitive file access                                   │
│  - Unexpected network connections                          │
│  - Crypto mining patterns                                  │
│  - Shell spawning in containers                            │
└─────────────────────────────────────────────────────────────┘
```

### Network Policies

**Default Policies:**
- Deny all ingress by default
- Allow only explicitly permitted traffic
- Namespace isolation

**Policy Examples:**
```yaml
# Example: Allow ingress to web tier only from ingress controller
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-to-web
spec:
  podSelector:
    matchLabels:
      tier: web
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
```

### Secrets Management

- Provider: HashiCorp Vault (or Kubernetes Secrets with encryption)
- Encryption: AES-256-GCM for secrets at rest
- Access: RBAC-controlled, audit logged
- Rotation: Automated for service accounts

---

## CI/CD Pipeline

### GitHub Actions Integration

```
┌─────────────────────────────────────────────────────────────┐
│                    CI/CD Pipeline                           │
├─────────────────────────────────────────────────────────────┤
│  1. Code Push                                               │
│     └─> Trigger GitHub Actions                             │
│                                                             │
│  2. Build Stage                                             │
│     ├─> Lint & Test                                        │
│     ├─> Security Scan (Trivy, CodeQL)                      │
│     └─> Build Container Image                              │
│                                                             │
│  3. Push Stage                                              │
│     └─> Push to Container Registry (with SHA tag)          │
│                                                             │
│  4. Deploy Stage                                            │
│     ├─> Update Kubernetes manifests                        │
│     ├─> Apply via kubectl/ArgoCD                           │
│     └─> Notify Discord channel                             │
│                                                             │
│  5. Verify Stage                                            │
│     ├─> Health check endpoints                             │
│     ├─> Smoke tests                                        │
│     └─> Rollback on failure                                │
└─────────────────────────────────────────────────────────────┘
```

### Deployment Strategies

| Environment | Strategy | Rollback |
|-------------|----------|----------|
| Development | Rolling update | Automatic |
| Staging | Rolling update | Automatic |
| Production | Blue-green / Canary | Manual approval |

---

## Resource Estimates for KnowledgePods

### Per KnowledgePod Resources

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| Pod Server | 100m | 500m | 128Mi | 512Mi |
| Video Sidecar | 50m | 200m | 64Mi | 256Mi |

### Scaling Estimates

| Scale | Active Pods | Total CPU | Total Memory | Est. Monthly Cost |
|-------|-------------|-----------|--------------|-------------------|
| Small (100 questions) | 100 | 15 cores | 77GB | ~$500 |
| Medium (500 questions) | 500 | 75 cores | 384GB | ~$2,500 |
| Large (1000 questions) | 1000 | 150 cores | 768GB | ~$5,000 |

*Note: Pods can scale to zero when not actively serving, reducing costs significantly.*

---

## Disaster Recovery

### Backup Schedule

| Data | Frequency | Retention | RPO | RTO |
|------|-----------|-----------|-----|-----|
| Database | Hourly | 30 days | 1 hour | 4 hours |
| Object Storage | Daily | 30 days | 24 hours | 8 hours |
| Cluster State | Daily | 14 days | 24 hours | 8 hours |
| Secrets | Daily | 14 days | 24 hours | 4 hours |

### Recovery Procedures

1. **Database Recovery:** Point-in-time restore from snapshot
2. **Application Recovery:** Redeploy from container images
3. **Full Cluster Recovery:** Rebuild from IaC + restore data

---

## Verification Checklist

### Daily Checks
- [ ] All pods in Running state
- [ ] No persistent alert firing
- [ ] Certificate expiry > 14 days
- [ ] Storage utilization < 80%

### Weekly Checks
- [ ] Backup verification (restore test)
- [ ] Security scan review
- [ ] Capacity utilization review

### Monthly Checks
- [ ] Disaster recovery drill
- [ ] Access review
- [ ] Cost optimization review

---

## Related Documents

- `k8s/knowledgepod-crd.yaml` - KnowledgePod custom resource definition
- `docs/departments/infra_cloud_runbook.md` - Infrastructure runbook
- `docs/departments/security_ops_runbook.md` - Security operations runbook
