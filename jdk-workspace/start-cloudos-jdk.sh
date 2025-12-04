#!/usr/bin/env bash
# JDK Workspace Management Script
#
# Usage: ./start-cloudos-jdk.sh [start|shell|stop]
#
# LLM Directive: This script manages the JDK development container.
# Extend to support:
# - Multiple JDK versions
# - Custom Maven/Gradle settings
# - IDE server integration
set -euo pipefail

CONTAINER_NAME="${CONTAINER_NAME:-cloudos-jdk}"
IMAGE_NAME="${IMAGE_NAME:-strategickhaos/jdk-workspace:latest}"
WORKSPACE_DIR="${WORKSPACE_DIR:-$(pwd)}"

case "${1:-}" in
  start)
    echo "Starting CloudOS JDK workspace (OpenJDK 21)..."
    
    # Check if container already exists
    if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
      echo "Container ${CONTAINER_NAME} already exists, starting..."
      docker start "${CONTAINER_NAME}"
    else
      echo "Creating new container ${CONTAINER_NAME}..."
      docker run -d \
        --name "${CONTAINER_NAME}" \
        -v "${WORKSPACE_DIR}:/workspace" \
        -p 5005:5005 \
        -p 8888:8888 \
        -e JAVA_TOOL_OPTIONS="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005" \
        "${IMAGE_NAME}" \
        tail -f /dev/null
    fi
    
    echo "Ready!"
    echo "  Shell: ./start-cloudos-jdk.sh shell"
    echo "  Debug: localhost:5005"
    echo "  App:   localhost:8888"
    ;;
    
  shell)
    echo "Connecting to ${CONTAINER_NAME}..."
    docker exec -it "${CONTAINER_NAME}" bash
    ;;
    
  stop)
    echo "Stopping CloudOS JDK workspace..."
    docker stop "${CONTAINER_NAME}" 2>/dev/null || true
    echo "Stopped."
    ;;
    
  clean)
    echo "Removing CloudOS JDK workspace..."
    docker stop "${CONTAINER_NAME}" 2>/dev/null || true
    docker rm "${CONTAINER_NAME}" 2>/dev/null || true
    echo "Cleaned."
    ;;
    
  *)
    echo "CloudOS JDK Workspace Manager"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  start  - Start the JDK workspace container"
    echo "  shell  - Open a shell in the running container"
    echo "  stop   - Stop the container"
    echo "  clean  - Stop and remove the container"
    echo ""
    echo "Environment variables:"
    echo "  CONTAINER_NAME - Container name (default: cloudos-jdk)"
    echo "  IMAGE_NAME     - Docker image (default: strategickhaos/jdk-workspace:latest)"
    echo "  WORKSPACE_DIR  - Host directory to mount (default: current directory)"
    ;;
esac
