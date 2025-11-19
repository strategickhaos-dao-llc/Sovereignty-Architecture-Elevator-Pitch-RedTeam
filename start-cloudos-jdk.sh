#!/usr/bin/env bash
# start-cloudos-jdk.sh - CloudOS with JDK Support Launcher
# Strategic Khaos Cloud Operating System - Java-enabled Environment

set -euo pipefail

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose-cloudos.yml"
PROJECT_NAME="cloudos"
JDK_SERVICE="jdk-workspace"

# Logging functions
log() {
    echo -e "${CYAN}[$(date +'%H:%M:%S')]${NC} $*"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*"
}

error() {
    echo -e "${RED}[ERROR]${NC} $*" >&2
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $*"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $*"
}

header() {
    echo -e "${MAGENTA}$*${NC}"
}

# Display banner
show_banner() {
    cat <<'EOF'
   _____ _                 _            _      _  __
  / ____| |               | |          | |    | |/ /
 | |    | | ___  _   _  __| | ___  ___ | |    | ' /
 | |    | |/ _ \| | | |/ _` |/ _ \/ __|| |    |  < 
 | |____| | (_) | |_| | (_| | (_) \__ \| |____| . \
  \_____|_|\___/ \__,_|\__,_|\___/|___/|______|_|\_\

Strategic Khaos Cloud Operating System - Java Development Edition
EOF
}

# Check dependencies
check_dependencies() {
    log "🔍 Checking dependencies..."
    
    local missing_deps=()
    
    if ! command -v docker &> /dev/null; then
        missing_deps+=("docker")
    fi
    
    if ! command -v docker compose &> /dev/null && ! command -v docker-compose &> /dev/null; then
        missing_deps+=("docker-compose")
    fi
    
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        error "Missing required dependencies: ${missing_deps[*]}"
        info "Please install Docker and Docker Compose"
        exit 1
    fi
    
    # Test Docker is running
    if ! docker ps &> /dev/null; then
        error "Docker is not running. Please start Docker first."
        exit 1
    fi
    
    success "All dependencies verified"
}

# Create required directories
create_directories() {
    log "📁 Creating required directories..."
    
    local directories=(
        "monitoring/grafana/provisioning/dashboards"
        "monitoring/grafana/provisioning/datasources"
        "monitoring/grafana/dashboards"
        "ssl"
    )
    
    for dir in "${directories[@]}"; do
        mkdir -p "$dir"
    done
    
    success "Directories created"
}

# Build JDK container
build_jdk_container() {
    log "🔨 Building JDK-enabled container..."
    
    if [[ ! -f "Dockerfile.jdk" ]]; then
        error "Dockerfile.jdk not found"
        return 1
    fi
    
    docker compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" build "$JDK_SERVICE"
    success "JDK container built successfully"
}

# Start CloudOS services
start_services() {
    log "🚀 Starting CloudOS services..."
    
    # Start infrastructure services first
    log "🏗️  Starting infrastructure services..."
    docker compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" up -d \
        postgres redis qdrant
    
    # Wait for infrastructure
    log "⏳ Waiting for infrastructure to be ready..."
    sleep 10
    
    # Start JDK workspace
    log "☕ Starting JDK workspace..."
    docker compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" up -d "$JDK_SERVICE"
    
    # Start remaining services
    log "🎯 Starting application services..."
    docker compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" up -d
    
    success "All services starting..."
}

# Wait for services
wait_for_services() {
    log "⏳ Waiting for services to become ready..."
    
    local max_attempts=60
    local attempt=0
    
    while [[ $attempt -lt $max_attempts ]]; do
        attempt=$((attempt + 1))
        
        # Check JDK service specifically
        if docker exec cloudos-jdk java -version &> /dev/null; then
            success "JDK workspace is ready!"
            break
        fi
        
        echo -n "."
        sleep 2
    done
    
    echo ""
    
    if [[ $attempt -eq $max_attempts ]]; then
        warn "Services may still be starting..."
    fi
}

# Verify JDK installation
verify_jdk() {
    log "🔍 Verifying JDK installation..."
    
    if ! docker ps --format '{{.Names}}' | grep -q "cloudos-jdk"; then
        error "JDK container is not running"
        return 1
    fi
    
    echo -e "\n${GREEN}Java Version:${NC}"
    docker exec cloudos-jdk java -version 2>&1 | sed 's/^/  /'
    
    echo -e "\n${GREEN}Java Compiler:${NC}"
    docker exec cloudos-jdk javac -version 2>&1 | sed 's/^/  /'
    
    echo -e "\n${GREEN}Maven:${NC}"
    docker exec cloudos-jdk mvn -version 2>&1 | head -n 1 | sed 's/^/  /'
    
    echo -e "\n${GREEN}Gradle:${NC}"
    docker exec cloudos-jdk gradle -version 2>&1 | grep "Gradle" | sed 's/^/  /'
    
    success "JDK verification complete"
}

# Show service status
show_status() {
    header "\n📊 CloudOS Service Status"
    echo ""
    
    docker compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" ps
    
    echo ""
    header "🌐 Access Points"
    cat <<EOF
  
  ${YELLOW}Development:${NC}
    IDE (VS Code):         http://localhost:8081
    Terminal (Wetty):      http://localhost:7681
    ${GREEN}Java Workspace:        http://localhost:8888${NC}
    ${GREEN}Java Debug Port:       localhost:5005${NC}
  
  ${YELLOW}Services:${NC}
    AI SME API:            http://localhost:8000
    Chat (Element):        http://localhost:8009
    Auth (Keycloak):       http://localhost:8180
    Storage (MinIO):       http://localhost:9001
  
  ${YELLOW}Monitoring:${NC}
    Traefik Dashboard:     http://localhost:8080
    Grafana:               http://localhost:3000
    Prometheus:            http://localhost:9090
  
  ${YELLOW}Credentials:${NC}
    IDE:                   Password: admin
    Keycloak:              admin / admin
    MinIO:                 admin / admin123
    Grafana:               admin / admin

EOF
    
    success "🎉 CloudOS with JDK is ready!"
}

# Show JDK usage information
show_jdk_info() {
    header "\n☕ Java Development Quick Start"
    cat <<'EOF'

  Access the Java workspace:
    docker exec -it cloudos-jdk bash

  Inside the container:
    java -version              # Check Java version
    mvn -version               # Check Maven version
    gradle -version            # Check Gradle version

  Build a Maven project:
    cd /workspace/my-project
    mvn clean install

  Build a Gradle project:
    cd /workspace/my-project
    gradle build

  Run with remote debugging:
    java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005 \
         -jar target/myapp.jar

EOF
}

# Stop services
stop_services() {
    log "🛑 Stopping CloudOS services..."
    docker compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" down
    success "CloudOS services stopped"
}

# Show logs
show_logs() {
    local service="${1:-}"
    
    if [[ -n "$service" ]]; then
        docker compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" logs -f "$service"
    else
        docker compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" logs -f
    fi
}

# Main function
main() {
    local command="${1:-start}"
    shift || true
    
    show_banner
    echo ""
    
    case "$command" in
        start)
            check_dependencies
            create_directories
            build_jdk_container
            start_services
            wait_for_services
            verify_jdk
            show_status
            show_jdk_info
            ;;
        stop)
            stop_services
            ;;
        restart)
            stop_services
            sleep 3
            start_services
            wait_for_services
            show_status
            ;;
        status)
            show_status
            ;;
        verify)
            verify_jdk
            ;;
        logs)
            show_logs "$@"
            ;;
        jdk-logs)
            show_logs "$JDK_SERVICE"
            ;;
        shell)
            info "Entering JDK workspace shell..."
            docker exec -it cloudos-jdk bash
            ;;
        build)
            build_jdk_container
            ;;
        help|--help|-h)
            cat <<EOF
Usage: $0 <command> [arguments]

Commands:
  start          Start CloudOS with JDK support (default)
  stop           Stop all services
  restart        Restart all services
  status         Show service status
  verify         Verify JDK installation
  logs [service] Show logs (all or specific service)
  jdk-logs       Show JDK workspace logs
  shell          Enter JDK workspace shell
  build          Build JDK container
  help           Show this help message

Examples:
  $0 start                    # Start CloudOS with JDK
  $0 stop                     # Stop all services
  $0 verify                   # Verify JDK installation
  $0 shell                    # Enter Java workspace
  $0 logs jdk-workspace       # Show JDK logs

EOF
            ;;
        *)
            error "Unknown command: $command"
            info "Run '$0 help' for usage information"
            exit 1
            ;;
    esac
}

# Execute main
main "$@"
