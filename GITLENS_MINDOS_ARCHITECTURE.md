# GitLens to Mind OS Distribution Architecture

## Overview

This architecture implements a sophisticated event distribution system that captures GitLens events and distributes them to specialized LLM Generals (AI agents) deployed across Kubernetes clusters. The system embodies the principle: **"Send all to GitLens and have legions of Mind OS distribute to all linked Kubernetes LLM Generals"**.

## Architecture Diagram

```
┌─────────────────┐
│   GitLens       │
│   VS Code       │
└────────┬────────┘
         │
         │ Events (PR, Review, Commit)
         ▼
┌─────────────────────────────────────┐
│  GitLens Aggregator                 │
│  - Event Collection                 │
│  - Discord Notifications            │
│  - Event Normalization              │
└────────┬────────────────────────────┘
         │
         │ Forward to Mind OS
         ▼
┌─────────────────────────────────────┐
│  Mind OS Orchestrator               │
│  - Distribution Strategy            │
│  - Load Balancing                   │
│  - General Selection                │
└────────┬────────────────────────────┘
         │
         │ Distribute
         ▼
┌─────────────────────────────────────┐
│        LLM Generals Legion          │
│  ┌──────────────────────────────┐   │
│  │  Kubernetes Cluster: prod-us │   │
│  │  ┌────────────────────────┐  │   │
│  │  │ code-review-general    │  │   │
│  │  │ architecture-general   │  │   │
│  │  │ security-general       │  │   │
│  │  │ deployment-general     │  │   │
│  │  └────────────────────────┘  │   │
│  └──────────────────────────────┘   │
│  ┌──────────────────────────────┐   │
│  │  Kubernetes Cluster: dev     │   │
│  │  ┌────────────────────────┐  │   │
│  │  │ qa-general            │  │   │
│  │  │ analytics-general     │  │   │
│  │  │ general-purpose       │  │   │
│  │  └────────────────────────┘  │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
```

## Components

### 1. GitLens Aggregator

**Location**: `src/gitlens-aggregator.ts`  
**Port**: 8086  
**Purpose**: Centralized event collection from GitLens

**Features**:
- ✅ Receives events from GitLens webhooks
- ✅ Normalizes event formats
- ✅ Sends Discord notifications
- ✅ Forwards events to Mind OS for distribution
- ✅ Tracks event statistics

**Event Types Supported**:
- `review_started` - PR review initiated
- `review_submitted` - PR review completed
- `needs_attention` - Critical items requiring attention
- `commit_graph` - Commit graph updates
- `pr_created` - New pull request
- `pr_merged` - Pull request merged

**API Endpoints**:
```bash
POST /events              # Receive GitLens events
POST /webhook/gitlens     # GitLens webhook endpoint
GET  /stats               # Get event statistics
GET  /health              # Health check
```

### 2. Mind OS Orchestrator

**Location**: `src/mindos-orchestrator.ts`  
**Port**: 8090  
**Purpose**: Intelligent distribution of events to LLM Generals

**Distribution Strategies**:

1. **Broadcast**: Send to all available generals
   - Used for: `needs_attention`, `pr_created`
   - Ensures critical events reach all relevant agents

2. **Round Robin**: Rotate through available generals
   - Used for: General purpose events
   - Ensures even distribution of workload

3. **Load Balanced**: Send to least loaded generals
   - Used for: `review_started`, `review_submitted`
   - Optimizes performance under load

**LLM General Selection Logic**:
```typescript
// Events routed to specific generals based on type
review_started → code-review-general, quality-assurance-general
pr_created → architecture-general, security-general, code-review-general
pr_merged → deployment-general, documentation-general
commit_graph → analytics-general, metrics-general
needs_attention → triage-general, priority-general
```

**API Endpoints**:
```bash
POST /distribute                    # Distribute event to generals
GET  /status                        # Get orchestrator status
GET  /generals/:cluster/:name       # Get specific general info
PUT  /generals/:cluster/:name/status # Update general status
GET  /distributions                 # Get distribution history
GET  /metrics                       # Prometheus metrics
GET  /health                        # Health check
```

### 3. LLM Generals

**Namespace**: `agents`  
**Purpose**: Specialized AI agents for different tasks

**General Types**:

| General Name | Specialization | Replicas |
|--------------|----------------|----------|
| `code-review-general` | Code review, quality, best practices | 2 |
| `architecture-general` | Design, architecture, patterns | 2 |
| `security-general` | Security, vulnerabilities, compliance | 2 |
| `deployment-general` | Deployment, release, CI/CD | 1 |
| `quality-assurance-general` | Testing, QA, validation | 1 |
| `analytics-general` | Metrics, analysis, insights | 1 |
| `documentation-general` | Docs, README, guides | 1 |
| `general-purpose-general` | Multi-purpose tasks | 3 |

**API Endpoints** (each general):
```bash
POST /process    # Process event
GET  /health     # Health check
GET  /ready      # Readiness check
```

## Deployment

### Local Development (Docker Compose)

```bash
# 1. Set environment variables
export DISCORD_TOKEN="your_discord_token"
export OPENAI_API_KEY="your_openai_key"
export CH_PRS_ID="your_prs_channel_id"

# 2. Start services
docker-compose up -d gitlens-aggregator mindos-orchestrator

# 3. Start LLM Generals
docker-compose up -d llm-general-code-review llm-general-architecture llm-general-security

# 4. Check status
docker-compose ps
curl http://localhost:8086/health
curl http://localhost:8090/status
```

### Kubernetes Production Deployment

```bash
# 1. Deploy everything
./deploy-gitlens-mindos.sh

# 2. Verify deployments
kubectl get pods -n ops
kubectl get pods -n agents

# 3. Check services
kubectl get svc -n ops
kubectl get svc -n agents

# 4. View logs
kubectl logs -f deployment/gitlens-aggregator -n ops
kubectl logs -f deployment/mindos-orchestrator -n ops
```

### Manual Kubernetes Deployment

```bash
# 1. Create namespaces
kubectl create namespace ops
kubectl create namespace agents

# 2. Deploy LLM Generals
kubectl apply -f bootstrap/k8s/llm-generals-deployment.yaml

# 3. Deploy aggregator and orchestrator
kubectl apply -f bootstrap/k8s/gitlens-mindos-deployment.yaml

# 4. Configure ingress (if needed)
kubectl apply -f bootstrap/k8s/ingress.yaml
```

## Configuration

### GitLens Integration

Update `discovery.yml`:
```yaml
git:
  gitlens:
    edition: "pro"
    notify_to_discord:
      enabled: true
      channel: "#prs"
      events:
        - "review_started"
        - "review_submitted"
        - "needs_attention"
```

### Environment Variables

**GitLens Aggregator**:
```bash
DISCORD_TOKEN=your_bot_token
GITLENS_AGGREGATOR_PORT=8086
MINDOS_URL=http://mindos-orchestrator:8090
PRS_CHANNEL_ID=channel_id
```

**Mind OS Orchestrator**:
```bash
MINDOS_PORT=8090
NODE_ENV=production
```

**LLM Generals**:
```bash
GENERAL_TYPE=code-review  # or architecture, security, etc.
SPECIALIZATION=code_review,quality,best_practices
OPENAI_API_KEY=your_api_key
```

## Usage Examples

### Send Event to GitLens Aggregator

```bash
curl -X POST http://localhost:8086/events \
  -H "Content-Type: application/json" \
  -d '{
    "type": "pr_created",
    "timestamp": "2025-11-22T21:00:00Z",
    "repository": "strategickhaos/my-repo",
    "user": "developer1",
    "metadata": {
      "pr_number": 123,
      "title": "Add new feature",
      "description": "This PR adds a new feature"
    }
  }'
```

### Check Mind OS Status

```bash
curl http://localhost:8090/status | jq
```

Response:
```json
{
  "total_generals": 22,
  "generals_by_cluster": {
    "prod-us": [...],
    "dev": [...]
  },
  "generals_by_status": {
    "active": 20,
    "inactive": 0,
    "busy": 2
  },
  "recent_distributions": [...],
  "total_distributions": 150
}
```

### View GitLens Aggregator Stats

```bash
curl http://localhost:8086/stats | jq
```

### Monitor with Prometheus

```bash
# Mind OS metrics
curl http://localhost:8090/metrics

# GitLens Aggregator metrics (if implemented)
curl http://localhost:8086/metrics
```

## Monitoring & Observability

### Prometheus Metrics

**Mind OS Orchestrator**:
- `mindos_llm_generals_total` - Total number of LLM Generals
- `mindos_llm_generals_active` - Active LLM Generals
- `mindos_llm_generals_busy` - Busy LLM Generals
- `mindos_distributions_total` - Total distributions

### Logs

```bash
# GitLens Aggregator logs
kubectl logs -f deployment/gitlens-aggregator -n ops

# Mind OS Orchestrator logs
kubectl logs -f deployment/mindos-orchestrator -n ops

# Specific LLM General logs
kubectl logs -f deployment/code-review-general -n agents
```

### Health Checks

All services expose `/health` endpoints:
```bash
curl http://gitlens-aggregator:8086/health
curl http://mindos-orchestrator:8090/health
curl http://code-review-general:8080/health
```

## Scaling

### Horizontal Pod Autoscaling

HPA is configured for:
- GitLens Aggregator: 2-8 replicas (CPU 70%)
- Mind OS Orchestrator: 2-10 replicas (CPU 70%, Memory 80%)
- Code Review General: 2-10 replicas (CPU 70%, Memory 80%)

### Manual Scaling

```bash
# Scale Mind OS
kubectl scale deployment mindos-orchestrator -n ops --replicas=5

# Scale specific LLM General
kubectl scale deployment code-review-general -n agents --replicas=5
```

## Security

### RBAC

Mind OS Orchestrator has cluster-wide read access to:
- Services, endpoints, pods
- Deployments, replicasets
- Namespaces

### Network Policies

- GitLens Aggregator: Public ingress (rate limited)
- Mind OS Orchestrator: Internal only (whitelist IPs)
- LLM Generals: ClusterIP only (no external access)

### Secrets Management

Secrets are stored in Kubernetes Secrets:
```bash
kubectl create secret generic llm-secrets \
  --from-literal=openai-api-key=$OPENAI_API_KEY \
  -n agents
```

## Troubleshooting

### Event Not Being Distributed

1. Check GitLens Aggregator logs:
   ```bash
   kubectl logs -f deployment/gitlens-aggregator -n ops
   ```

2. Verify Mind OS is receiving events:
   ```bash
   curl http://localhost:8090/distributions
   ```

3. Check LLM General availability:
   ```bash
   curl http://localhost:8090/status | jq '.generals_by_status'
   ```

### LLM General Not Responding

1. Check pod status:
   ```bash
   kubectl get pods -n agents | grep general
   ```

2. Check general logs:
   ```bash
   kubectl logs deployment/code-review-general -n agents
   ```

3. Restart general:
   ```bash
   kubectl rollout restart deployment/code-review-general -n agents
   ```

### High Load on Mind OS

1. Check current load:
   ```bash
   kubectl top pods -n ops | grep mindos
   ```

2. Scale up:
   ```bash
   kubectl scale deployment mindos-orchestrator -n ops --replicas=5
   ```

3. Check distribution history for bottlenecks:
   ```bash
   curl http://localhost:8090/distributions | jq
   ```

## Future Enhancements

- [ ] Add support for custom LLM models (Anthropic, local models)
- [ ] Implement request queuing for overload scenarios
- [ ] Add WebSocket support for real-time event streaming
- [ ] Implement circuit breakers for failing generals
- [ ] Add A/B testing for distribution strategies
- [ ] Implement feedback loop from generals to improve routing
- [ ] Add multi-region support with geo-distributed generals
- [ ] Implement general specialization learning based on performance

## References

- [GitLens Documentation](https://gitkraken.com/gitlens)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Discord.js Documentation](https://discord.js.org/)
- [Sovereignty Architecture README](README.md)
