#!/bin/bash
# Honeytrap Deployment Script for GCP Cloud Run
# Part of Sovereignty Architecture

set -e

PROJECT_ID="${GCP_PROJECT_ID:-gen-lang-client-0012743775}"
REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="honeypot-sra"
IMAGE_NAME="gcr.io/${PROJECT_ID}/honeytrap-sra:latest"

echo "🎣 Deploying Honeytrap to Cloud Run..."

# Navigate to honeytrap directory
cd "$(dirname "$0")"

# Build Docker image
echo "📦 Building Docker image..."
docker build -t "${IMAGE_NAME}" .

# Push to GCR
echo "⬆️  Pushing to Google Container Registry..."
docker push "${IMAGE_NAME}"

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy "${SERVICE_NAME}" \
  --image "${IMAGE_NAME}" \
  --platform managed \
  --region "${REGION}" \
  --allow-unauthenticated \
  --service-account "honeypot-sra-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --set-env-vars "HONEYTRAP_LOG_BUCKET=honeytrap-attack-logs,LEGION_PUBSUB_TOPIC=projects/${PROJECT_ID}/topics/legion-attack-analysis"

# Get URL
HONEYPOT_URL=$(gcloud run services describe "${SERVICE_NAME}" --platform managed --region "${REGION}" --format 'value(status.url)')
echo ""
echo "✅ HONEYPOT DEPLOYED!"
echo "🎣 URL: ${HONEYPOT_URL}"
echo ""

# Test
echo "🧪 Testing honeypot..."
curl -X POST "${HONEYPOT_URL}/signals/test" -d '{"message": "red team test"}' -H "Content-Type: application/json"
echo ""
echo "✅ Test complete!"
