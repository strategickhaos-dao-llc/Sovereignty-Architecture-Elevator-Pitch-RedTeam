# Quick Start Guide: GitLens to Mind OS Distribution

Get the GitLens to Mind OS distribution system running in minutes!

## Prerequisites

- Docker & Docker Compose
- Node.js 20+ (for local development)
- kubectl (for Kubernetes deployment)
- Discord bot token (for notifications)

## Option 1: Docker Compose (Recommended for Testing)

### 1. Set Environment Variables

```bash
# Required
export DISCORD_TOKEN="your_discord_bot_token"
export OPENAI_API_KEY="your_openai_key"

# Optional
export CH_PRS_ID="your_discord_prs_channel_id"
export POSTGRES_PASSWORD="secure_password"
export GRAFANA_PASSWORD="admin"
```

### 2. Start Core Services

```bash
# Start infrastructure
docker-compose up -d postgres redis qdrant prometheus grafana

# Wait for services to be healthy
docker-compose ps

# Start GitLens and Mind OS
docker-compose up -d gitlens-aggregator mindos-orchestrator

# Start LLM Generals
docker-compose up -d llm-general-code-review llm-general-architecture llm-general-security
```

### 3. Verify Services

```bash
# Check all services are running
docker-compose ps

# Test GitLens Aggregator
curl http://localhost:8086/health

# Test Mind OS Orchestrator
curl http://localhost:8090/status | jq
```

### 4. Send Test Event

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

### 5. Check Distribution

```bash
# View Mind OS status
curl http://localhost:8090/status | jq

# View distribution history
curl http://localhost:8090/distributions | jq

# View GitLens stats
curl http://localhost:8086/stats | jq
```

### 6. Run Automated Tests

```bash
./test-gitlens-mindos.sh
```

## Option 2: Kubernetes Deployment

### 1. Prerequisites

```bash
# Ensure kubectl is configured
kubectl cluster-info

# Create namespaces
kubectl create namespace ops
kubectl create namespace agents
```

### 2. Create Secrets

```bash
# Discord bot token
kubectl create secret generic discord-ops-secrets \
  --from-literal=bot-token=$DISCORD_TOKEN \
  -n ops

# OpenAI API key
kubectl create secret generic llm-secrets \
  --from-literal=openai-api-key=$OPENAI_API_KEY \
  -n agents
```

### 3. Deploy

```bash
# Quick deploy everything
./deploy-gitlens-mindos.sh

# Or manually
kubectl apply -f bootstrap/k8s/llm-generals-deployment.yaml
kubectl apply -f bootstrap/k8s/gitlens-mindos-deployment.yaml
```

### 4. Verify Deployment

```bash
# Check ops namespace
kubectl get pods -n ops
kubectl get svc -n ops

# Check agents namespace
kubectl get pods -n agents
kubectl get svc -n agents

# Check logs
kubectl logs -f deployment/gitlens-aggregator -n ops
kubectl logs -f deployment/mindos-orchestrator -n ops
```

### 5. Port Forward for Testing

```bash
# Forward GitLens Aggregator
kubectl port-forward -n ops svc/gitlens-aggregator 8086:8086 &

# Forward Mind OS Orchestrator
kubectl port-forward -n ops svc/mindos-orchestrator 8090:8090 &

# Now test as in Docker Compose steps 4-6
```

## Option 3: Local Development

### 1. Install Dependencies

```bash
npm install
```

### 2. Build TypeScript

```bash
npm run build
```

### 3. Start Services

```bash
# Terminal 1: GitLens Aggregator
export DISCORD_TOKEN="your_token"
export MINDOS_URL="http://localhost:8090"
node dist/gitlens-aggregator.js

# Terminal 2: Mind OS Orchestrator
node dist/mindos-orchestrator.js
```

### 4. Test (in Terminal 3)

```bash
./test-gitlens-mindos.sh
```

## GitLens VS Code Integration

### 1. Configure VS Code Tasks

Add to `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "GitLens: Send PR Event",
      "type": "shell",
      "command": "curl -X POST http://localhost:8086/webhook/gitlens -H 'Content-Type: application/json' -d '{\"event_type\":\"pr_created\",\"repository\":{\"full_name\":\"${workspaceFolderBasename}\"},\"sender\":{\"login\":\"${env:USER}\"},\"pull_request\":{\"number\":1,\"title\":\"New PR\",\"head\":{\"ref\":\"main\",\"sha\":\"abc123\"}}}'"
    }
  ]
}
```

### 2. Configure GitLens Webhook

If you have GitLens Pro:

1. Open GitLens settings
2. Go to Webhooks section
3. Add webhook URL: `http://localhost:8086/webhook/gitlens`
4. Enable events: PR created, Review started, Review submitted

## Monitoring

### Access Grafana

```bash
# Docker Compose
open http://localhost:3000

# Kubernetes
kubectl port-forward -n ops svc/grafana 3000:3000
open http://localhost:3000
```

### View Metrics

```bash
# Mind OS Prometheus metrics
curl http://localhost:8090/metrics

# GitLens stats
curl http://localhost:8086/stats | jq
```

### View Logs

```bash
# Docker Compose
docker-compose logs -f gitlens-aggregator
docker-compose logs -f mindos-orchestrator

# Kubernetes
kubectl logs -f deployment/gitlens-aggregator -n ops
kubectl logs -f deployment/mindos-orchestrator -n ops
```

## Common Issues

### Services Not Starting

```bash
# Check logs
docker-compose logs gitlens-aggregator
docker-compose logs mindos-orchestrator

# Restart services
docker-compose restart gitlens-aggregator mindos-orchestrator
```

### Events Not Being Distributed

```bash
# Check GitLens can reach Mind OS
docker-compose exec gitlens-aggregator ping mindos-orchestrator

# Check Mind OS status
curl http://localhost:8090/status | jq '.generals_by_status'
```

### No LLM Generals Available

```bash
# Check generals are running
docker-compose ps | grep llm-general

# Start more generals
docker-compose up -d llm-general-code-review llm-general-architecture
```

## Next Steps

1. **Configure Discord Integration**: Set up `CH_PRS_ID` for notifications
2. **Add More LLM Generals**: Scale up based on workload
3. **Enable Auto-Scaling**: Use HPA in Kubernetes
4. **Set Up Monitoring**: Configure Prometheus & Grafana dashboards
5. **Production Deployment**: Use ingress and TLS certificates

## Documentation

- **Full Architecture**: [GITLENS_MINDOS_ARCHITECTURE.md](GITLENS_MINDOS_ARCHITECTURE.md)
- **Main README**: [README.md](README.md)
- **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)

## Support

- **Issues**: Open an issue on GitHub
- **Discord**: Join the Strategickhaos Discord server
- **Documentation**: Check the docs directory

---

**Happy coding with the Legion!** 🧠🤖
