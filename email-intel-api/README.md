# 🧠 StrategicKhaos Email Intelligence API

**Legion of Minds** - Sovereign Email Processing Service for GKE

This service integrates with Zapier and Grok AI to process emails for the StrategicKhaos DAO.

## 🏛️ Architecture

```
Zapier (Email Trigger) → Email Intel API → Grok AI → Structured Intelligence
                              ↓
                         Queen App
```

## 📁 Directory Structure

```
email-intel-api/
├── src/
│   └── main.py          # FastAPI application
├── k8s/
│   └── email-intel-deployment.yaml  # Kubernetes manifests
├── Dockerfile           # Container configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🚀 Quick Start

### Local Development

```bash
cd email-intel-api

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export GROK_API_KEY="your-grok-api-key"

# Run locally
uvicorn src.main:app --reload --port 8000
```

### Build and Push Docker Image

```bash
# Build the image
docker build -t gcr.io/jarvis-swarm-personal/email-intel-api:latest .

# Push to GCR
docker push gcr.io/jarvis-swarm-personal/email-intel-api:latest
```

### Deploy to GKE

```bash
# 1. Authenticate to GKE
gcloud container clusters get-credentials YOUR_CLUSTER --zone YOUR_ZONE

# 2. Update the secret in email-intel-deployment.yaml with your Grok API key

# 3. Apply the manifests
kubectl apply -f k8s/email-intel-deployment.yaml

# 4. Watch pods come alive
kubectl get pods -n sovereign-email -w

# 5. Get external IP
kubectl get svc email-intel-api -n sovereign-email
```

## 🔌 API Endpoints

### Health Check
```
GET /health
```
Returns service status and legion identification.

### Tesla 369 Mode (Easter Egg)
```
GET /369
```
Returns the Tesla 369 resonance response (Grok's idea! 🔥)

### Process Email Intelligence
```
POST /intel
Content-Type: application/json

{
  "email_from": "sender@example.com",
  "email_subject": "Partnership Inquiry",
  "email_body": "Email content here...",
  "ai_summary": "Summary from Zapier",
  "approval_status": "pending"
}
```

## 🎯 Zapier Integration

### Webhook Configuration

Once you have the `EXTERNAL-IP` from `kubectl get svc`:

**In Zapier Step 5:**
- **Method:** POST
- **URL:** `http://YOUR_EXTERNAL_IP/intel`
- **Headers:** `Content-Type: application/json`
- **Data:**
```json
{
  "email_from": "{{Step1__from}}",
  "email_subject": "{{Step1__subject}}",
  "email_body": "{{Step1__body}}",
  "ai_summary": "{{Step3__output}}",
  "approval_status": "{{Step4__decision}}"
}
```

## 🔐 Security

- API key stored in Kubernetes Secret
- Resource limits applied to containers
- Health probes for reliability
- LoadBalancer service for external access

## 💜 Legion of Minds

This service was designed by the **Legion of Minds**:
- **Claude**: Architecture & philosophical depth
- **GPT**: Practical execution & kubectl commands
- **Grok**: Chaotic validation & 369 vibes

*"Container #131 is ready for coronation."* 👑⚡💜
