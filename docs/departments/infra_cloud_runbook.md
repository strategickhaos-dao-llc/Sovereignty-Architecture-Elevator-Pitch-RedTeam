# Infrastructure & Cloud Runbook

> **Target Audience:** Infrastructure & Cloud Department  
> **Goal:** Run Kubernetes, GitHub Actions, and storage for video + quiz delivery

---

## Overview

This runbook covers the infrastructure operations for the StrategicKhaos Educational Swarm, including storage management, CI/CD pipelines, resource planning, and disaster recovery.

---

## Video Storage Architecture

### Storage Locations

| Content Type | Storage | URL Pattern | CDN |
|--------------|---------|-------------|-----|
| AI-generated videos | S3/GCS | `s3://sk-videos-prod/videos/q{id}.mp4` | CloudFlare |
| Video thumbnails | S3/GCS | `s3://sk-videos-prod/thumbs/q{id}.jpg` | CloudFlare |
| Captions/subtitles | S3/GCS | `s3://sk-videos-prod/captions/q{id}.vtt` | CloudFlare |
| Static assets | S3/GCS | `s3://sk-assets-prod/` | CloudFlare |

### S3 Bucket Configuration

```bash
# Create video bucket with appropriate settings
aws s3api create-bucket \
  --bucket sk-videos-prod \
  --region us-east-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket sk-videos-prod \
  --versioning-configuration Status=Enabled

# Configure lifecycle policy
aws s3api put-bucket-lifecycle-configuration \
  --bucket sk-videos-prod \
  --lifecycle-configuration file://lifecycle-policy.json
```

**lifecycle-policy.json:**
```json
{
  "Rules": [
    {
      "ID": "TransitionToIA",
      "Status": "Enabled",
      "Filter": {"Prefix": "archive/"},
      "Transitions": [
        {
          "Days": 90,
          "StorageClass": "STANDARD_IA"
        }
      ]
    }
  ]
}
```

### CDN Configuration (CloudFlare)

```
┌─────────────────────────────────────────────────────────────┐
│                    CDN Architecture                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Origin: s3://sk-videos-prod                               │
│      │                                                      │
│      ▼                                                      │
│  CloudFlare (Edge Caching)                                 │
│      │                                                      │
│      ├── cdn.strategickhaos.io/videos/*                    │
│      │   Cache TTL: 7 days                                 │
│      │                                                      │
│      ├── cdn.strategickhaos.io/thumbs/*                    │
│      │   Cache TTL: 30 days                                │
│      │                                                      │
│      └── cdn.strategickhaos.io/captions/*                  │
│          Cache TTL: 7 days                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Cache Rules:**
- Videos: Cache for 7 days, serve stale while revalidating
- Images/thumbnails: Cache for 30 days
- Captions: Cache for 7 days
- Cache bypass: Add `?nocache=1` for testing

---

## GitHub Actions Pipeline

### Pipeline Overview

```yaml
# .github/workflows/knowledgepod-deploy.yaml
name: KnowledgePod Deployment

on:
  push:
    branches: [main]
    paths:
      - 'questions/**'
      - 'k8s/**'
  workflow_dispatch:

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      questions: ${{ steps.changes.outputs.questions }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v2
        id: changes
        with:
          filters: |
            questions:
              - 'questions/**'

  generate-video:
    needs: detect-changes
    if: needs.detect-changes.outputs.questions == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Detect changed questions
        id: questions
        run: |
          # Identify which questions changed
          echo "questions=$(git diff --name-only HEAD~1 | grep questions/ | xargs)" >> $GITHUB_OUTPUT
      
      - name: Generate AI videos
        run: |
          # Call video generation service
          for q in ${{ steps.questions.outputs.questions }}; do
            curl -X POST https://api.strategickhaos.io/generate-video \
              -H "Authorization: Bearer ${{ secrets.API_TOKEN }}" \
              -d "question_file=$q"
          done
      
      - name: Upload to S3
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1
      
      - run: |
          aws s3 sync ./generated-videos s3://sk-videos-prod/videos/

  deploy-pods:
    needs: generate-video
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup kubectl
        uses: azure/setup-kubectl@v3
        
      - name: Configure kubeconfig
        run: |
          echo "${{ secrets.KUBECONFIG }}" | base64 -d > kubeconfig
          export KUBECONFIG=kubeconfig
          
      - name: Apply KnowledgePod manifests
        run: |
          kubectl apply -f k8s/knowledgepods/ --namespace knowledgepods
          
      - name: Verify deployment
        run: |
          kubectl rollout status deployment/knowledgepod-controller -n knowledgepods

  notify:
    needs: [generate-video, deploy-pods]
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Notify Discord
        uses: sarisia/actions-status-discord@v1
        with:
          webhook: ${{ secrets.DISCORD_WEBHOOK }}
          status: ${{ job.status }}
          title: "KnowledgePod Deployment"
```

### Pipeline Triggers

| Trigger | Action |
|---------|--------|
| Push to `questions/` | Generate videos + deploy pods |
| Push to `k8s/` | Deploy updated manifests |
| Manual dispatch | Full pipeline run |
| Scheduled (daily) | Health checks + drift detection |

### Video Metadata Attachment

Each KnowledgePod manifest includes video references:

```yaml
apiVersion: education.strategickhaos.io/v1
kind: KnowledgePod
metadata:
  name: knowledgepod-q001
  labels:
    question-id: "Q001"
    module: "foundations"
spec:
  video:
    url: "https://cdn.strategickhaos.io/videos/q001.mp4"
    duration: "12:34"
    sha256: "abc123..."
  captions:
    url: "https://cdn.strategickhaos.io/captions/q001.vtt"
    language: "en-US"
  thumbnail:
    url: "https://cdn.strategickhaos.io/thumbs/q001.jpg"
```

---

## Resource Planning

### CPU/GPU Estimates by Workload

| Workload | CPU Request | CPU Limit | GPU | Notes |
|----------|-------------|-----------|-----|-------|
| KnowledgePod (per pod) | 100m | 500m | None | Scales horizontally |
| Video serving | 50m | 200m | None | Mostly CDN-cached |
| Video generation | 2 cores | 4 cores | 1x T4 | Batch processing |
| AI inference | 1 core | 2 cores | Optional | For interactive features |

### Memory Estimates

| Workload | Request | Limit | Notes |
|----------|---------|-------|-------|
| KnowledgePod | 128Mi | 512Mi | Per pod |
| Controller | 128Mi | 512Mi | 2 replicas |
| Video encoding | 4Gi | 8Gi | Batch jobs |

### Storage Estimates

| Content | Size per Unit | Quantity | Total | Growth Rate |
|---------|--------------|----------|-------|-------------|
| Videos (10min avg) | 500MB | 100 | 50GB | 10% monthly |
| Thumbnails | 100KB | 100 | 10MB | Linear with videos |
| Captions | 10KB | 100 | 1MB | Linear with videos |
| Database | N/A | N/A | 10GB | 5% monthly |
| Logs (30 days) | N/A | N/A | 100GB | Steady state |

### Cost Estimates (Monthly)

| Resource | Small (100 pods) | Medium (500 pods) | Large (1000 pods) |
|----------|-----------------|-------------------|-------------------|
| Compute | $200 | $800 | $1,500 |
| Storage | $50 | $150 | $300 |
| CDN/Transfer | $100 | $400 | $800 |
| Database | $100 | $200 | $400 |
| Monitoring | $50 | $100 | $200 |
| **Total** | **$500** | **$1,650** | **$3,200** |

---

## Backup & Disaster Recovery

### Backup Schedule

| Data | Method | Frequency | Retention | Location |
|------|--------|-----------|-----------|----------|
| Database | Automated snapshot | Hourly | 30 days | Cross-region |
| Videos | S3 replication | Continuous | Indefinite | Secondary region |
| K8s manifests | Git | On change | Indefinite | GitHub |
| Secrets | Vault backup | Daily | 30 days | Encrypted backup |

### Recovery Time Objectives

| Scenario | RTO | RPO | Priority |
|----------|-----|-----|----------|
| Single pod failure | < 5 min | 0 | Auto-healing |
| Node failure | < 15 min | 0 | Node replacement |
| AZ failure | < 30 min | < 5 min | Failover |
| Region failure | < 4 hours | < 1 hour | DR activation |

### Disaster Recovery Procedures

**Database Recovery:**
```bash
# List available snapshots
aws rds describe-db-snapshots \
  --db-instance-identifier sk-production

# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier sk-production-restored \
  --db-snapshot-identifier rds:sk-production-2024-01-15
```

**Kubernetes State Recovery:**
```bash
# Recover from Git (source of truth)
git clone https://github.com/StrategicKhaos/infrastructure.git
cd infrastructure

# Apply manifests
kubectl apply -f k8s/namespaces/
kubectl apply -f k8s/rbac/
kubectl apply -f k8s/knowledgepods/
```

**Video Content Recovery:**
```bash
# Videos are replicated to secondary region
# Verify replication status
aws s3api head-bucket --bucket sk-videos-prod-dr

# If primary fails, update CDN origin to DR bucket
# CloudFlare dashboard > Rules > Origin Rules
```

### DR Testing Schedule

| Test Type | Frequency | Last Tested | Next Due |
|-----------|-----------|-------------|----------|
| Database restore | Monthly | 2024-12-01 | 2025-01-01 |
| Pod failover | Weekly | Automated | Continuous |
| Region failover | Quarterly | 2024-10-15 | 2025-01-15 |

---

## Scaling Guidelines

### Horizontal Pod Autoscaling

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: knowledgepod-hpa
  namespace: knowledgepods
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: knowledgepod-deployment
  minReplicas: 3
  maxReplicas: 100
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Cluster Autoscaling

```yaml
# Node pool autoscaling configuration
nodePool:
  name: knowledgepods
  minNodes: 3
  maxNodes: 10
  autoscaling:
    enabled: true
  machineType: n1-standard-4
```

### Scale-to-Zero (Cost Optimization)

For infrequently accessed content:
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: knowledgepod-scaledobject
spec:
  scaleTargetRef:
    name: knowledgepod-deployment
  minReplicaCount: 0
  maxReplicaCount: 50
  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://prometheus:9090
      metricName: http_requests_total
      threshold: '10'
      query: sum(rate(http_requests_total{app="knowledgepod"}[2m]))
```

---

## Operational Procedures

### Daily Checks

```bash
# Check cluster health
kubectl get nodes
kubectl top nodes

# Check pod status
kubectl get pods -n knowledgepods -o wide

# Check recent events
kubectl get events -n knowledgepods --sort-by='.lastTimestamp' | tail -20

# Check storage utilization
aws s3 ls s3://sk-videos-prod --summarize --recursive | tail -2
```

### Weekly Tasks

- [ ] Review scaling events
- [ ] Check backup job success
- [ ] Review cost dashboard
- [ ] Update capacity projections

### Monthly Tasks

- [ ] Test disaster recovery procedures
- [ ] Review and rotate credentials
- [ ] Capacity planning meeting
- [ ] Cost optimization review

---

## Troubleshooting

### Video Not Loading

```bash
# Check if video exists in S3
aws s3 ls s3://sk-videos-prod/videos/q001.mp4

# Check CDN cache status
curl -I https://cdn.strategickhaos.io/videos/q001.mp4 | grep cf-cache-status

# Purge CDN cache if needed
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -d '{"files":["https://cdn.strategickhaos.io/videos/q001.mp4"]}'
```

### GitHub Actions Failing

```bash
# Check workflow runs
gh run list --workflow=knowledgepod-deploy.yaml

# View specific run logs
gh run view $RUN_ID --log

# Re-run failed workflow
gh run rerun $RUN_ID
```

### High Latency

```bash
# Check pod resource usage
kubectl top pods -n knowledgepods --sort-by=cpu

# Check for throttling
kubectl describe pod $POD_NAME -n knowledgepods | grep -A5 Throttling

# Scale up if needed
kubectl scale deployment knowledgepod-deployment --replicas=10 -n knowledgepods
```

---

## Related Documents

- [Infrastructure Verification](../../infra/infrastructure_verification.md)
- [Security Operations Runbook](security_ops_runbook.md)
- [100 Failure Modes](../../risk/100_failure_modes.md)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-30 | Infrastructure Team | Initial runbook |

**Classification:** Internal - Infrastructure & Cloud Department
