# SNHU Ecosystem Tracker

A YAML-driven, containerized Python application for analyzing SNHU (Southern New Hampshire University) ecosystem emails using the Grok API. This project tracks stackable credentials, skills alignment, SDN coursework patterns, and educational milestones.

## 🏗️ Architecture Overview

This system implements a modern, cloud-native architecture for email analysis:

- **Python Application**: Core analysis engine using Grok API
- **Docker**: Containerized for consistent deployment
- **Kubernetes**: Orchestrated deployment with auto-scaling
- **Discord**: Team collaboration and result sharing
- **GitHub Actions**: CI/CD pipeline for automated deployment

## 📁 Project Structure

```
snhu-ecosystem-tracker/
├── .github/workflows/          # CI/CD pipelines
│   └── deploy.yml              # Auto-deploy to K8s on push
├── k8s/                        # Kubernetes manifests
│   ├── deployment.yaml         # Pod specifications (2 replicas)
│   ├── configmap.yaml          # Email analysis configuration
│   ├── service.yaml            # LoadBalancer service
│   └── secret.yaml             # Grok API credentials template
├── docker/                     # Docker-related files
│   ├── Dockerfile              # Python 3.12 container build
│   └── docker-compose.yml      # Local multi-container testing
├── src/                        # Source code
│   ├── main.py                 # Core application & HTTP server
│   └── email_analyzer.py       # Grok API email processing
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Docker Desktop or Docker Engine
- kubectl (for Kubernetes deployment)
- Grok API key from [x.ai/api](https://x.ai/api)
- (Optional) Discord webhook URL

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd snhu-ecosystem-tracker
   ```

2. **Set up environment variables**
   ```bash
   export GROK_API_KEY="your-grok-api-key"
   export DISCORD_WEBHOOK_URL="your-discord-webhook"  # optional
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run locally**
   ```bash
   python src/main.py
   # Server starts on http://localhost:8080
   # Health check: curl http://localhost:8080/health
   ```

### Docker Deployment

1. **Build Docker image**
   ```bash
   docker build -t snhu-analyzer -f docker/Dockerfile .
   ```

2. **Run with Docker Compose**
   ```bash
   cd docker
   export GROK_API_KEY="your-key"
   docker-compose up -d
   ```

3. **Test the service**
   ```bash
   curl http://localhost:8080/health
   # Optional: Access MailHog UI at http://localhost:8025
   ```

### Kubernetes Deployment

1. **Install Minikube (for local testing)**
   ```bash
   minikube start
   ```

2. **Create secrets**
   ```bash
   kubectl create secret generic grok-secret \
     --from-literal=api-key="your-grok-api-key" \
     --from-literal=discord-webhook="your-webhook-url"
   ```

3. **Deploy application**
   ```bash
   kubectl apply -f k8s/configmap.yaml
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```

4. **Check deployment status**
   ```bash
   kubectl get pods -l app=analyzer
   kubectl get service snhu-analyzer
   ```

5. **Access the service**
   ```bash
   # For Minikube
   minikube service snhu-analyzer
   
   # For cloud deployments, get the LoadBalancer IP
   kubectl get service snhu-analyzer -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
   ```

## 📧 Email Analysis

### Batch Processing

Create a CSV or JSON file with SNHU emails:

**emails.csv**
```csv
id,subject,body
1,SNHU 2025 Credentials,"Information about stackable credentials..."
2,SDN Course Update,"New SDN networking course available..."
```

**Run batch analysis**
```bash
# Set environment variables
export GROK_API_KEY="your-key"
export RUN_MODE="batch"
export INPUT_FILE="/path/to/emails.csv"
export OUTPUT_FILE="/path/to/results.csv"

# Run analysis
python src/main.py
```

### Analysis Features

The analyzer extracts:
- **Key Topics**: Credentials, SDN, skills, milestones
- **Sentiment**: Positive, neutral, or negative tone
- **Stepping Stones**: Milestones and progress markers
- **Skills**: Competencies and learning objectives
- **Action Items**: Deadlines and required actions

## 🔧 Configuration

### ConfigMap Settings

Edit `k8s/configmap.yaml` to customize:

```yaml
data:
  analysis_model: "grok-4-fast-reasoning"    # Grok model to use
  batch_size: "50"                           # Emails per batch
  enable_sentiment_analysis: "true"          # Enable sentiment detection
  focus_keywords: "credential,SDN,skills"    # Keywords to track
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROK_API_KEY` | Grok API authentication key | Yes |
| `DISCORD_WEBHOOK_URL` | Discord notification webhook | No |
| `ANALYSIS_MODEL` | Grok model name | No (default: grok-4-fast-reasoning) |
| `RUN_MODE` | `server` or `batch` | No (default: server) |
| `LOG_LEVEL` | Logging verbosity | No (default: INFO) |
| `PORT` | HTTP server port | No (default: 8080) |

## 🤝 Discord Integration

### Setup Webhook

1. In Discord, go to Server Settings → Integrations → Webhooks
2. Create a new webhook for your #analysis-results channel
3. Copy the webhook URL

### Configure Notifications

```bash
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
```

Results will be automatically posted to your Discord channel when analysis completes.

## 🔄 CI/CD Pipeline

The GitHub Actions workflow automatically:

1. **Build & Test**: Runs on every push and PR
   - Installs dependencies
   - Lints Python code
   - Runs tests (when implemented)

2. **Docker Build**: Pushes images on main branch
   - Multi-architecture support
   - Tagged with commit SHA and `latest`

3. **Kubernetes Deploy**: Deploys on main branch push
   - Updates deployment with new image
   - Waits for rollout completion
   - Notifies Discord of deployment status

### Required Secrets

Configure these in GitHub Settings → Secrets:

- `DOCKER_USERNAME`: Docker Hub username
- `DOCKER_PASSWORD`: Docker Hub password/token
- `KUBECONFIG`: Base64-encoded kubeconfig file
- `DISCORD_WEBHOOK_URL`: Discord webhook for notifications

## 📊 Monitoring

### Health Checks

- **Health**: `GET /health` - Service health status
- **Readiness**: `GET /ready` - Ready to accept requests

### Kubernetes Probes

The deployment includes:
- **Liveness Probe**: Restarts unhealthy containers
- **Readiness Probe**: Controls traffic routing

### Logs

```bash
# View application logs
kubectl logs -f deployment/snhu-analyzer

# View specific pod logs
kubectl logs -f pod/<pod-name>
```

## 🔒 Security Considerations

1. **API Keys**: Never commit real API keys to version control
2. **Secret Management**: Use Kubernetes secrets or external vaults
3. **Email Privacy**: Anonymize personal data before analysis
4. **Access Control**: Implement RBAC for production deployments
5. **Network Policies**: Restrict pod-to-pod communication

## 🧪 Testing

### Unit Tests

```bash
pip install pytest pytest-cov
pytest tests/ -v --cov=src
```

### Integration Tests

```bash
# Test with sample emails
python src/main.py --test-mode
```

## 📈 Scaling

### Horizontal Pod Autoscaler

```bash
kubectl autoscale deployment snhu-analyzer \
  --cpu-percent=70 \
  --min=2 \
  --max=10
```

### Resource Limits

Current configuration (per pod):
- **Requests**: 256Mi RAM, 250m CPU
- **Limits**: 512Mi RAM, 500m CPU

## 🐛 Troubleshooting

### Common Issues

**Pod not starting**
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

**API authentication errors**
```bash
# Verify secret
kubectl get secret grok-secret -o yaml
```

**Health check failures**
```bash
# Test locally
curl http://localhost:8080/health
```

## 📚 Resources

- **SNHU 2025 Initiative**: [SNHU Official Site](https://www.snhu.edu)
- **Grok API Documentation**: [x.ai/api](https://x.ai/api)
- **Kubernetes Guide**: [kubernetes.io/docs](https://kubernetes.io/docs)
- **Docker Documentation**: [docs.docker.com](https://docs.docker.com)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built for the SNHU ecosystem analysis initiative
- Powered by Grok API for advanced AI analysis
- Inspired by modern DevOps and cloud-native practices

---

**Built with ❤️ for educational ecosystem insights**
