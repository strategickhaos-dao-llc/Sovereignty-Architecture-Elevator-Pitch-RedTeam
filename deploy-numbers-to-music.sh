#!/bin/bash
# ETERNAL NUMBERS-TO-MUSIC ASCENSION — DOM_010101 2025
# Deploy the Numbers to Divine Music Engine to convert all number streams to 432 Hz

set -e

echo "🎹 Deploying Numbers to Divine Music Engine..."
echo "Converting all number streams to 432 Hz healing frequencies..."
echo ""

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

# Check if docker compose is available (try both v1 and v2)
DOCKER_COMPOSE_CMD=""
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
else
    echo "❌ docker compose not found. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating output directories..."
mkdir -p ./data ./outputs/music

# Build the image
echo "🔨 Building Docker image..."
docker build -t ghcr.io/dom010101/numbers-to-divine-music:latest -f Dockerfile.numbers-to-music .

# Start the service
echo "🚀 Starting Numbers to Divine Music Engine..."
$DOCKER_COMPOSE_CMD up -d numbers-to-music

# Wait for service to be healthy
echo "⏳ Waiting for service to start..."
sleep 5

# Check status
if $DOCKER_COMPOSE_CMD ps numbers-to-music | grep -q "Up"; then
    echo ""
    echo "✅ Numbers to Divine Music Engine is now running!"
    echo ""
    echo "📊 Service Status:"
    $DOCKER_COMPOSE_CMD ps numbers-to-music
    echo ""
    echo "📝 Recent Logs:"
    $DOCKER_COMPOSE_CMD logs --tail=20 numbers-to-music
    echo ""
    echo "🎵 Every number in the swarm now sings in 432 Hz. Forever."
    echo ""
    echo "Generated MIDI files will be saved to: ./outputs/music/"
    echo "Place data files in: ./data/"
    echo ""
    echo "To view logs: $DOCKER_COMPOSE_CMD logs -f numbers-to-music"
    echo "To stop: $DOCKER_COMPOSE_CMD stop numbers-to-music"
else
    echo ""
    echo "❌ Service failed to start. Check logs:"
    $DOCKER_COMPOSE_CMD logs numbers-to-music
    exit 1
fi
