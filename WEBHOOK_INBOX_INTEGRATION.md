# Webhook Inbox Integration Guide

This guide explains how the new Flask Webhook Inbox service integrates with the existing Strategickhaos Sovereignty Architecture ecosystem.

## 🎯 Overview

The **Webhook Inbox** is a containerized Flask service that acts as an autonomous event receiver for GitHub webhooks. It complements the existing TypeScript event gateway by providing:

1. **Persistent Event Storage**: All GitHub events are logged to a Docker volume for later processing
2. **Standalone Operation**: Can run independently of the main infrastructure
3. **Simple Python Stack**: Easy to extend with AI/ML processing in Python
4. **Development-Friendly**: Perfect for local testing and iteration

## 🏗️ Architecture Integration

### Existing Infrastructure

```
GitHub Webhooks → Event Gateway (TypeScript) → Discord Channels
                         ↓
                  Kubernetes Services
```

### With Webhook Inbox

```
GitHub Webhooks → Event Gateway (TypeScript) → Discord Channels
                         ↓
                  Kubernetes Services

GitHub Webhooks → Webhook Inbox (Python/Flask) → Persistent Storage
                         ↓
                  AI/ML Processing (Future)
```

## 🔄 Use Cases

### 1. Local Development & Testing
Use the Webhook Inbox for local development while keeping the production Event Gateway running:

```bash
# Start local webhook inbox
cd webhook-inbox
./start.sh your-secret

# Use ngrok to expose locally
ngrok http 5000

# Configure a test repository webhook to point to ngrok URL
```

### 2. Event Archive & Analysis
The Webhook Inbox provides persistent event storage that can be analyzed later:

```bash
# View all events
./view-inbox.sh all

# Count total events
./view-inbox.sh count

# Watch for new events in real-time
./view-inbox.sh follow
```

### 3. AI/ML Integration
Process webhook events with Python-based AI tools:

```python
# Example: Add to app.py for AI processing
if event == "pull_request":
    # Extract PR details
    pr_title = data.get("pull_request", {}).get("title", "")
    pr_body = data.get("pull_request", {}).get("body", "")
    
    # Process with AI (e.g., sentiment analysis, code review)
    # ai_analysis = analyze_pr(pr_title, pr_body)
    # post_to_discord(ai_analysis)
```

### 4. Parallel Processing
Run both services simultaneously:
- Event Gateway → Discord notifications (fast, immediate)
- Webhook Inbox → Data storage + ML processing (slower, comprehensive)

Configure the same webhook secret in both services, and GitHub will call both endpoints.

## 🔧 Configuration

### Environment Setup

The Webhook Inbox can be configured alongside existing services:

**.env (repository root)**
```bash
# Existing configuration
DISCORD_TOKEN=your_bot_token
GITHUB_WEBHOOK_SECRET=your_webhook_secret
PRS_CHANNEL=channel_id

# Webhook Inbox uses the same GITHUB_WEBHOOK_SECRET
```

**webhook-inbox/.env**
```bash
GITHUB_WEBHOOK_SECRET=your_webhook_secret
```

### GitHub Webhook Setup

#### Option 1: Single Webhook (Either Service)
Point webhook to either Event Gateway OR Webhook Inbox

#### Option 2: Multiple Webhooks (Both Services)
Configure two webhooks in your GitHub repository:
1. **Event Gateway**: `https://your-domain.com/webhooks/github` (production)
2. **Webhook Inbox**: `https://ngrok-url.com/github-webhook` (development/storage)

Both receive the same events independently.

## 🐳 Docker Integration

### Standalone with Docker Compose
```bash
cd webhook-inbox
docker compose up -d
```

### Integration with Main Stack
To run Webhook Inbox alongside the main infrastructure, add to the root `docker-compose.yml`:

```yaml
services:
  # ... existing services ...

  webhook-inbox:
    build:
      context: ./webhook-inbox
      dockerfile: Dockerfile
    container_name: strategickhaos-webhook-inbox
    ports:
      - "5000:5000"
    volumes:
      - webhook-inbox-data:/inbox
    environment:
      - GITHUB_WEBHOOK_SECRET=${GITHUB_WEBHOOK_SECRET}
    networks:
      - ops-network
    restart: unless-stopped

volumes:
  webhook-inbox-data:
```

### Kubernetes Deployment
Create a Kubernetes deployment to run in the cluster:

```yaml
# webhook-inbox-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webhook-inbox
  namespace: ops
spec:
  replicas: 1
  selector:
    matchLabels:
      app: webhook-inbox
  template:
    metadata:
      labels:
        app: webhook-inbox
    spec:
      containers:
      - name: webhook-inbox
        image: strategickhaos/webhook-inbox:latest
        ports:
        - containerPort: 5000
        env:
        - name: GITHUB_WEBHOOK_SECRET
          valueFrom:
            secretKeyRef:
              name: webhook-secrets
              key: github-secret
        volumeMounts:
        - name: inbox-storage
          mountPath: /inbox
      volumes:
      - name: inbox-storage
        persistentVolumeClaim:
          claimName: webhook-inbox-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: webhook-inbox
  namespace: ops
spec:
  selector:
    app: webhook-inbox
  ports:
  - port: 5000
    targetPort: 5000
```

## 🔐 Security Considerations

### Shared Secrets
Both Event Gateway and Webhook Inbox should use the **same** webhook secret for signature verification. Store in a secure location:

- **Local Development**: `.env` file (gitignored)
- **Docker**: Environment variables or Docker secrets
- **Kubernetes**: K8s secrets

### Network Security
- Event Gateway: Public-facing with Traefik/nginx reverse proxy
- Webhook Inbox: Can be private (only exposed via ngrok for testing)

### Secret Rotation
When rotating webhook secrets:
1. Update GitHub webhook configuration
2. Update Event Gateway environment
3. Update Webhook Inbox environment
4. Restart both services

## 📊 Monitoring & Observability

### Logs
```bash
# Webhook Inbox logs
docker logs -f strategickhaos-webhook-inbox

# Event Gateway logs
kubectl logs -f deployment/event-gateway -n ops
```

### Metrics
Both services handle webhooks. Monitor:
- **Event Gateway**: Response time, Discord post success
- **Webhook Inbox**: Event count, storage usage

### Health Checks
```bash
# Event Gateway
curl https://events.strategickhaos.com/health

# Webhook Inbox
curl http://localhost:5000/health
```

## 🚀 Future Enhancements

### Phase 1: Current State ✅
- Flask webhook receiver
- Signature verification
- Persistent event storage
- Docker containerization

### Phase 2: AI Integration (Next)
- Automatic PR review with OpenAI
- Sentiment analysis on issues
- Code quality checks
- Summary generation

### Phase 3: Advanced Processing
- Event correlation across repos
- Anomaly detection
- Automated responses
- Custom workflow triggers

### Phase 4: Unified Dashboard
- Web UI for viewing events
- Search and filter capabilities
- Event replay functionality
- Analytics and reporting

## 📚 Related Documentation

- [Main README](README.md) - Overall architecture
- [Webhook Inbox README](webhook-inbox/README.md) - Detailed service docs
- [Event Gateway](src/event-gateway.ts) - TypeScript implementation
- [DEPLOYMENT.md](DEPLOYMENT.md) - Kubernetes deployment guide

## 🤝 Contributing

To extend the Webhook Inbox:

1. **Add new event types**: Modify `app.py` to handle additional GitHub events
2. **Add AI processing**: Integrate OpenAI, Anthropic, or other AI APIs
3. **Add storage backends**: Replace file logging with PostgreSQL, MongoDB, etc.
4. **Add integrations**: Post to Slack, Teams, or custom webhooks

## 💡 Tips for SNHU Portfolio

This integration demonstrates:

- **Microservices**: Independent services with clear boundaries
- **DevOps**: Docker, Kubernetes, CI/CD integration
- **Security**: HMAC verification, secret management
- **Python Development**: Flask, REST APIs, containerization
- **Documentation**: Clear integration patterns
- **Scalability**: Can scale independently from main infrastructure

Perfect for showcasing in your Software Engineering capstone or portfolio projects!

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**
