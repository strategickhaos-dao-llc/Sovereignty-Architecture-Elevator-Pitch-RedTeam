#!/bin/bash
# ValorYield Engine Deployment Script
# Part of Sovereignty Architecture

set -e

PROJECT_ID="${GCP_PROJECT_ID:-gen-lang-client-0012743775}"
REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="valoryield-engine"
IMAGE_NAME="gcr.io/${PROJECT_ID}/valoryield-engine:latest"

echo "💰 Deploying ValorYield Engine..."

# Navigate to valoryield directory
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
  --allow-unauthenticated

# Get URL
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" --platform managed --region "${REGION}" --format 'value(status.url)')
echo ""
echo "✅ VALORYIELD ENGINE DEPLOYED!"
echo "💰 URL: ${SERVICE_URL}"
echo ""

# Test
echo "🧪 Testing ValorYield Engine..."
curl -s "${SERVICE_URL}/" | jq .
echo ""
curl -s "${SERVICE_URL}/api/v1/portfolio" | jq .
echo ""
echo "✅ Test complete!"
