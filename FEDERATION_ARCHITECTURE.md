# 👑 Queen.js Federation Hub Architecture

## Overview

Queen.js is a central webhook coordinator that implements a **Federation** architecture instead of GitHub Enterprise consolidation. This approach provides unified coordination across multiple GitHub organizations while keeping them separate for better isolation.

## 🎭 The Problem: Organizational Sprawl

```yaml
current_state:
  organizations:
    - "Strategickhaos" (personal/main)
    - "Strategickhaos-Swarm-Intelligence" (team/projects)
    - "SNHU Enterprise" (school)
  
  issues:
    - Scattered webhooks pointing to temporary URLs
    - No central coordination between orgs
    - Manual webhook management per repository
    - Discord notifications fragmented
```

## 🏛️ The Solution: Federation, Not Consolidation

```
┌─────────────────────────────────────────────────────────────┐
│                    QUEEN.JS FEDERATION HUB                    │
│              (Central Coordinator, Distributed Execution)     │
└─────────────────────────────────────────────────────────────┘
                             │
                             │ All webhooks point here
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
   GitHub Org 1        GitHub Org 2         GitHub Org 3
   Strategickhaos      Swarm Intelligence   SNHU Enterprise
        │                    │                    │
        ├─ Repo A            ├─ Repo D            ├─ Repo G
        ├─ Repo B            ├─ Repo E            └─ Repo H
        └─ Repo C            └─ Repo F
        
                             │
                             ▼
                        QUEEN.JS
                    (One webhook URL)
                             │
                             ▼
                        NATS JetStream
                   (Unified message bus)
                             │
                ┌────────────┼────────────┐
                ▼            ▼            ▼
           Discord      Kubernetes    Treasury OS
          (Control)    (Execution)   (Financial)
```

## 💰 Cost Comparison

| Option | Cost | Sovereignty |
|--------|------|-------------|
| GitHub Enterprise | $756/year minimum | Still depends on GitHub |
| Queen.js Federation | $0 (runs on existing GKE) | 100% self-controlled |

## 🚀 Quick Start

### 1. Deploy Queen.js

```bash
# Build Docker image
docker build -f Dockerfile.queen -t queen:latest .

# Run locally
docker run -p 8081:8081 \
  -e GITHUB_WEBHOOK_SECRET=your_secret \
  -e NATS_URL=nats://localhost:4222 \
  queen:latest
```

### 2. Configure Webhooks

```bash
# Set environment variables
export QUEEN_URL="https://queen.strategickhaos.com/webhook/github"
export WEBHOOK_SECRET="your_webhook_secret"

# Run configuration script
./scripts/queen/configure-webhooks.sh
```

### 3. Deploy to Kubernetes

```bash
kubectl apply -f deploy/queen/queen-deployment.yaml
```

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info and version |
| `/health` | GET | Health check |
| `/webhook/github` | POST | Central GitHub webhook receiver |
| `/webhook/zapier` | POST | Zapier integration |
| `/webhook/swarmgate/paycheck` | POST | SwarmGate paycheck detection |

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `PORT` | Server port (default: 8081) | No |
| `NATS_URL` | NATS JetStream URL | No |
| `GITHUB_WEBHOOK_SECRET` | GitHub webhook signature secret | Yes (production) |
| `DISCORD_WEBHOOK_GITHUB` | Discord webhook for GitHub events | No |
| `DISCORD_WEBHOOK_FINANCIAL` | Discord webhook for financial events | No |

### Organization Routing

Queen.js routes events based on the GitHub organization:

```typescript
const routing = {
  "Strategickhaos": {
    nats_prefix: "strategickhaos",
    discord_channel: "#github-main"
  },
  "Strategickhaos-Swarm-Intelligence": {
    nats_prefix: "swarm",
    discord_channel: "#github-swarm"
  },
  "SNHU": {
    nats_prefix: "snhu",
    discord_channel: "#github-school"
  }
};
```

## 🔐 Security

### Rate Limiting

Queen.js includes rate limiting to prevent abuse:
- 100 requests per minute per IP address
- Health check endpoint is excluded from rate limiting
- Standard rate limit headers included in responses

### Webhook Signature Verification

Queen.js verifies GitHub webhook signatures using HMAC-SHA256:

```typescript
function verifyWebhookSignature(payload, signature, secret) {
  const hmac = crypto.createHmac("sha256", secret);
  const digest = "sha256=" + hmac.update(payload).digest("hex");
  return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(digest));
}
```

**Note:** In production mode (`NODE_ENV=production`), the `GITHUB_WEBHOOK_SECRET` environment variable is required.

### Kubernetes Security Context

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
```

## 📊 Monitoring

### Health Check

```bash
curl https://queen.strategickhaos.com/health
```

Response:
```json
{
  "status": "operational",
  "service": "Queen.js Federation Hub",
  "sovereignty": "100%",
  "uptime": 12345.67,
  "nats_connected": true,
  "organizations_monitored": [
    "Strategickhaos",
    "Strategickhaos-Swarm-Intelligence",
    "SNHU"
  ]
}
```

### Prometheus Metrics

The Kubernetes deployment includes annotations for Prometheus scraping:

```yaml
annotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "8081"
  prometheus.io/path: "/health"
```

## 🏗️ Architecture Benefits

1. **Keep orgs separate** - Better isolation and security
2. **One webhook URL** - Single point of configuration
3. **Unified routing** - NATS JetStream for consistent messaging
4. **$0 cost** - No GitHub Enterprise fees
5. **Maximum sovereignty** - You own the hub, not GitHub

## 📚 Related Documentation

- [discovery.yml](../discovery.yml) - Main configuration
- [deploy/queen/queen-deployment.yaml](../deploy/queen/queen-deployment.yaml) - Kubernetes manifests
- [scripts/queen/configure-webhooks.sh](../scripts/queen/configure-webhooks.sh) - Webhook setup script

## 🎯 Implementation Checklist

- [x] Queen.js server with multi-org routing
- [x] GitHub webhook signature verification
- [x] NATS JetStream integration (mock for development)
- [x] Kubernetes deployment manifests
- [x] Docker container with security best practices
- [x] Webhook configuration scripts
- [x] Health check endpoint
- [x] Rate limiting (100 req/min per IP)
- [x] Production mode requiring webhook secrets
- [ ] Real NATS client integration
- [ ] Discord webhook integration
- [ ] Prometheus metrics exporter
- [ ] SwarmGate financial integration

---

**Total Implementation Time: ~55 minutes**

1. Deploy Queen to permanent URL (30 min)
2. Point all webhooks to Queen (15 min)
3. Test with one PR from each org (10 min)
4. Watch Queen route everything perfectly ✨
