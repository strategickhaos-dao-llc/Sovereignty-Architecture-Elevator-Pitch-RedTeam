#!/bin/bash
# Legends of Minds - Deployment Script
# Single-command deployment for unified agent orchestration platform

set -e

DEPLOY_DIR="/opt/legends_of_minds"
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🧠 Legends of Minds - Unified Agent Orchestration Platform"
echo "=========================================================="
echo ""

# Check if running as root for /opt deployment
if [ "$EUID" -eq 0 ]; then
    RUNNING_AS_ROOT=true
else
    RUNNING_AS_ROOT=false
fi

# Function to display help
show_help() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy          Deploy to /opt/legends_of_minds (requires sudo)"
    echo "  start           Start services with docker-compose"
    echo "  stop            Stop all services"
    echo "  restart         Restart all services"
    echo "  status          Show service status"
    echo "  logs            Show service logs"
    echo "  health          Check service health"
    echo "  clean           Stop and remove all containers/volumes"
    echo "  help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  sudo $0 deploy        # Deploy to production location"
    echo "  $0 start              # Start services"
    echo "  $0 logs orchestrator  # View orchestrator logs"
}

# Function to check requirements
check_requirements() {
    echo "Checking requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed. Please install Docker first."
        exit 1
    fi
    echo "✅ Docker found: $(docker --version)"
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo "❌ Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    echo "✅ Docker Compose found"
    
    echo ""
}

# Function to deploy to /opt
deploy_to_opt() {
    if [ "$RUNNING_AS_ROOT" = false ]; then
        echo "❌ Deployment to /opt requires root privileges."
        echo "Please run: sudo $0 deploy"
        exit 1
    fi
    
    echo "📦 Deploying to $DEPLOY_DIR..."
    
    # Create deployment directory
    mkdir -p "$DEPLOY_DIR"
    
    # Copy files
    echo "Copying files..."
    cp -r "$CURRENT_DIR"/* "$DEPLOY_DIR/"
    
    # Set permissions
    chown -R $SUDO_USER:$SUDO_USER "$DEPLOY_DIR"
    chmod +x "$DEPLOY_DIR/deploy.sh"
    
    echo "✅ Deployed to $DEPLOY_DIR"
    echo ""
    echo "To start services, run:"
    echo "  cd $DEPLOY_DIR && docker-compose up -d"
}

# Function to start services
start_services() {
    echo "🚀 Starting Legends of Minds services..."
    docker-compose up -d
    
    echo ""
    echo "⏳ Waiting for services to be ready..."
    sleep 5
    
    # Check health
    check_health
    
    echo ""
    echo "✅ Legends of Minds is now running!"
    echo ""
    echo "Access the Command Center:"
    echo "  http://localhost:8080"
    echo "  http://localhost (via nginx)"
    echo ""
    echo "API Documentation:"
    echo "  http://localhost:8080/docs"
    echo ""
    echo "To view logs:"
    echo "  docker-compose logs -f"
}

# Function to stop services
stop_services() {
    echo "⏹️  Stopping Legends of Minds services..."
    docker-compose down
    echo "✅ Services stopped"
}

# Function to restart services
restart_services() {
    echo "🔄 Restarting Legends of Minds services..."
    docker-compose restart
    echo "✅ Services restarted"
}

# Function to show status
show_status() {
    echo "📊 Service Status:"
    echo ""
    docker-compose ps
}

# Function to show logs
show_logs() {
    if [ -n "$1" ]; then
        docker-compose logs -f "$1"
    else
        docker-compose logs -f
    fi
}

# Function to check health
check_health() {
    echo "🏥 Health Check:"
    echo ""
    
    # Check orchestrator
    if curl -sf http://localhost:8080/health > /dev/null 2>&1; then
        echo "✅ Orchestrator: Healthy"
    else
        echo "❌ Orchestrator: Not responding"
    fi
    
    # Check nginx
    if curl -sf http://localhost > /dev/null 2>&1; then
        echo "✅ Nginx: Healthy"
    else
        echo "⚠️  Nginx: Not responding (may not be started)"
    fi
    
    # Check docker containers
    echo ""
    echo "Container Status:"
    docker-compose ps --format "table {{.Name}}\t{{.Status}}"
}

# Function to clean everything
clean_all() {
    echo "🧹 Cleaning up Legends of Minds..."
    read -p "This will remove all containers, volumes, and data. Continue? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose down -v
        echo "✅ Cleanup complete"
    else
        echo "Cleanup cancelled"
    fi
}

# Main script logic
case "${1:-help}" in
    deploy)
        check_requirements
        deploy_to_opt
        ;;
    start)
        check_requirements
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs "$2"
        ;;
    health)
        check_health
        ;;
    clean)
        clean_all
        ;;
    help|*)
        show_help
        ;;
esac
