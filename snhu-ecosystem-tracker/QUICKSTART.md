# SNHU Ecosystem Tracker - Quick Start Guide

Get up and running with the SNHU Ecosystem Tracker in minutes!

## 🎯 What You'll Build

A complete email analysis system that:
- Analyzes SNHU emails using Grok AI
- Runs in Docker containers
- Deploys to Kubernetes
- Integrates with Discord
- Provides automated CI/CD

## 📋 Prerequisites Checklist

- [ ] Python 3.12 or higher installed
- [ ] Docker Desktop installed and running
- [ ] Grok API key from [x.ai/api](https://x.ai/api)
- [ ] (Optional) kubectl for Kubernetes deployment
- [ ] (Optional) Discord webhook URL

## 🚀 5-Minute Local Setup

### Step 1: Run Setup Script

```bash
cd snhu-ecosystem-tracker
./setup.sh
```

This will:
- Check all prerequisites
- Create a Python virtual environment
- Install dependencies
- Validate all configuration files

### Step 2: Test with Sample Data

```bash
# Activate virtual environment
source venv/bin/activate

# Set your API key
export GROK_API_KEY="your-key-here"

# Run batch analysis on sample emails
export RUN_MODE=batch
export INPUT_FILE=examples/sample_emails.csv
export OUTPUT_FILE=results.csv

python src/main.py
```

You should see output like:
```
2024-11-23 23:30:00 - root - INFO - SNHU Ecosystem Analyzer starting...
2024-11-23 23:30:00 - root - INFO - Starting batch analysis on examples/sample_emails.csv
2024-11-23 23:30:01 - EmailAnalyzer - INFO - Initialized EmailAnalyzer with model: grok-4-fast-reasoning
2024-11-23 23:30:01 - EmailAnalyzer - INFO - Loading emails from examples/sample_emails.csv
2024-11-23 23:30:02 - EmailAnalyzer - INFO - Analyzing email 1/3
...
```

### Step 3: Start HTTP Server

```bash
export GROK_API_KEY="your-key-here"
python src/main.py
```

Test the endpoints:
```bash
# Health check
curl http://localhost:8080/health

# Readiness check
curl http://localhost:8080/ready
```

## 🐳 Docker Quick Start

### Build and Run

```bash
# Build the image
docker build -t snhu-analyzer -f docker/Dockerfile .

# Run the container
docker run -p 8080:8080 \
  -e GROK_API_KEY="your-key-here" \
  snhu-analyzer

# Test
curl http://localhost:8080/health
```

### Using Docker Compose

```bash
cd docker
export GROK_API_KEY="your-key-here"
docker-compose up -d

# View logs
docker-compose logs -f snhu-analyzer

# Access MailHog UI
open http://localhost:8025

# Stop
docker-compose down
```

## ☸️ Kubernetes Quick Deploy

### For Minikube (Local Testing)

```bash
# Start Minikube
minikube start

# Create namespace (optional)
kubectl create namespace snhu-analyzer

# Create secrets
kubectl create secret generic grok-secret \
  --from-literal=api-key="your-grok-api-key" \
  --from-literal=discord-webhook="your-webhook-url"

# Deploy
kubectl apply -f k8s/

# Check status
kubectl get pods -l app=analyzer
kubectl get service snhu-analyzer

# Access the service
minikube service snhu-analyzer
```

### For Cloud Kubernetes (GKE, EKS, AKS)

```bash
# Connect to your cluster
# For GKE:
gcloud container clusters get-credentials your-cluster --region=your-region

# For EKS:
aws eks update-kubeconfig --name your-cluster --region your-region

# For AKS:
az aks get-credentials --resource-group your-rg --name your-cluster

# Update image names
# Edit these files and replace 'your-dockerhub/snhu-analyzer' with your actual image:
# - k8s/deployment.yaml
# - k8s/cronjob.yaml
# - .github/workflows/deploy.yml

# Create secrets
kubectl create secret generic grok-secret \
  --from-literal=api-key="your-grok-api-key" \
  --from-literal=discord-webhook="your-webhook-url"

# Deploy
kubectl apply -f k8s/

# Get external IP
kubectl get service snhu-analyzer -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

## 🎨 Configuration Tips

### Essential Environment Variables

```bash
# Required
export GROK_API_KEY="sk-xxx"

# Optional
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
export ANALYSIS_MODEL="grok-4-fast-reasoning"
export LOG_LEVEL="INFO"
export PORT="8080"
```

### Quick Config Changes

Edit `k8s/configmap.yaml` to customize:
- Batch size for processing
- Focus keywords to track
- Analysis model to use

## 🔍 Troubleshooting

### "GROK_API_KEY not set" Error
```bash
export GROK_API_KEY="your-key-here"
```

### Docker Build Fails
```bash
# Clear Docker cache
docker builder prune

# Rebuild
docker build --no-cache -t snhu-analyzer -f docker/Dockerfile .
```

### Kubernetes Pods Not Starting
```bash
# Check pod status
kubectl get pods -l app=analyzer

# View logs
kubectl logs -l app=analyzer

# Describe pod
kubectl describe pod <pod-name>

# Common fix: Verify secret exists
kubectl get secret grok-secret
```

### Port Already in Use
```bash
# Find process using port 8080
lsof -i :8080

# Kill process
kill -9 <PID>

# Or use different port
export PORT=8081
python src/main.py
```

## 📊 Sample Analysis Workflow

```bash
# 1. Export emails from your email client to CSV
# Format: id, subject, body

# 2. Place in data directory
mkdir -p data
cp your_emails.csv data/

# 3. Run analysis
export RUN_MODE=batch
export INPUT_FILE=data/your_emails.csv
export OUTPUT_FILE=data/results.csv
export GROK_API_KEY="your-key"

python src/main.py

# 4. View results
cat data/results.csv
# Or open in spreadsheet app
open data/results.csv
```

## 🔄 CI/CD Setup

### GitHub Actions

1. Add repository secrets in GitHub Settings → Secrets:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub token
   - `KUBECONFIG`: Base64-encoded kubeconfig file
   - `DISCORD_WEBHOOK_URL`: Discord notification webhook

2. Update image name in:
   - `.github/workflows/deploy.yml`
   - `k8s/deployment.yaml`
   - `k8s/cronjob.yaml`

3. Push to main branch:
```bash
git push origin main
```

GitHub Actions will automatically:
- Build and test
- Push Docker image
- Deploy to Kubernetes
- Notify Discord

## 🎓 Learning Path

1. ✅ **Day 1**: Run locally with sample data
2. ✅ **Day 2**: Deploy with Docker
3. ✅ **Day 3**: Deploy to local Kubernetes (Minikube)
4. ✅ **Day 4**: Set up CI/CD pipeline
5. ✅ **Day 5**: Deploy to cloud Kubernetes

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Review [examples/sample_emails.csv](examples/sample_emails.csv) for data format
- Customize [k8s/configmap.yaml](k8s/configmap.yaml) for your needs
- Set up monitoring with Prometheus/Grafana
- Integrate with your Discord server

## 💡 Pro Tips

1. **Use virtual environments**: Always activate `venv` before running
2. **Test locally first**: Validate with sample data before deployment
3. **Start small**: Begin with small batches of emails
4. **Monitor costs**: Grok API usage is ~$0.20/M tokens
5. **Secure secrets**: Never commit API keys to git

## 🆘 Getting Help

- **Issues**: Check [GitHub Issues](../../issues)
- **Documentation**: See [README.md](README.md)
- **Grok API**: Visit [x.ai/api](https://x.ai/api)
- **Kubernetes**: See [kubernetes.io/docs](https://kubernetes.io/docs)

---

**Ready to analyze some emails? Let's go! 🚀**
