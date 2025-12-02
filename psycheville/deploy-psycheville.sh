#!/bin/bash
#
# PsycheVille Deployment Script
# Deploys the self-observing infrastructure for Sovereignty Architecture
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         PsycheVille - Self-Observing Infrastructure      ║${NC}"
echo -e "${BLUE}║              Deployment Script v1.0.0                     ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to print status messages
print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    print_status "Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Docker is installed"
}

# Check if required directories exist
check_directories() {
    print_status "Checking directory structure..."
    
    cd "$ROOT_DIR"
    
    if [ ! -d "psycheville" ]; then
        print_error "PsycheVille directory not found!"
        exit 1
    fi
    
    # Create required subdirectories if they don't exist
    mkdir -p psycheville/logs/tools_refinery
    mkdir -p psycheville/obsidian_vault/PsycheVille/Departments
    
    print_success "Directory structure verified"
}

# Check if configuration exists
check_configuration() {
    print_status "Checking configuration..."
    
    if [ ! -f "psycheville/psycheville.yaml" ]; then
        print_error "Configuration file not found: psycheville/psycheville.yaml"
        exit 1
    fi
    
    if [ ! -f "psycheville/reflection_worker.py" ]; then
        print_error "Worker script not found: psycheville/reflection_worker.py"
        exit 1
    fi
    
    if [ ! -f "docker-compose.psycheville.yml" ]; then
        print_error "Docker Compose file not found: docker-compose.psycheville.yml"
        exit 1
    fi
    
    print_success "Configuration files verified"
}

# Create network if it doesn't exist
create_network() {
    print_status "Checking Docker network..."
    
    if ! docker network ls | grep -q strategickhaos_network; then
        print_warning "Creating strategickhaos_network..."
        docker network create strategickhaos_network
        print_success "Network created"
    else
        print_success "Network already exists"
    fi
}

# Generate sample logs if requested
generate_sample_logs() {
    if [ "$1" == "--with-samples" ]; then
        print_status "Generating sample logs..."
        
        if [ -f "psycheville/test_logging.py" ]; then
            python3 psycheville/test_logging.py
            print_success "Sample logs generated"
        else
            print_warning "Sample log generator not found, skipping..."
        fi
    fi
}

# Deploy PsycheVille
deploy() {
    print_status "Deploying PsycheVille..."
    
    # Use docker-compose or docker compose based on what's available
    if command -v docker-compose &> /dev/null; then
        COMPOSE_CMD="docker-compose"
    else
        COMPOSE_CMD="docker compose"
    fi
    
    # Stop existing containers if they're running
    print_status "Stopping existing containers (if any)..."
    $COMPOSE_CMD -f docker-compose.psycheville.yml down 2>/dev/null || true
    
    # Start services
    print_status "Starting PsycheVille services..."
    $COMPOSE_CMD -f docker-compose.psycheville.yml up -d
    
    print_success "PsycheVille deployed successfully"
}

# Show status
show_status() {
    print_status "Checking service status..."
    echo ""
    
    # Use docker-compose or docker compose based on what's available
    if command -v docker-compose &> /dev/null; then
        COMPOSE_CMD="docker-compose"
    else
        COMPOSE_CMD="docker compose"
    fi
    
    $COMPOSE_CMD -f docker-compose.psycheville.yml ps
    
    echo ""
    print_status "Checking for generated reports..."
    
    if [ -d "psycheville/obsidian_vault/PsycheVille/Departments/Tools_Refinery" ]; then
        report_count=$(find psycheville/obsidian_vault/PsycheVille/Departments/Tools_Refinery -name "reflection_*.md" 2>/dev/null | wc -l)
        if [ "$report_count" -gt 0 ]; then
            print_success "$report_count reflection report(s) found"
            echo ""
            echo "Latest reports:"
            ls -lht psycheville/obsidian_vault/PsycheVille/Departments/Tools_Refinery/reflection_*.md 2>/dev/null | head -3
        else
            print_warning "No reports generated yet. Wait a few moments for initial reflection."
        fi
    else
        print_warning "Report directory not created yet"
    fi
}

# Main deployment flow
main() {
    case "${1:-deploy}" in
        deploy)
            check_docker
            check_directories
            check_configuration
            create_network
            generate_sample_logs "$2"
            deploy
            echo ""
            print_success "Deployment complete!"
            echo ""
            echo -e "${YELLOW}Next steps:${NC}"
            if command -v docker-compose &> /dev/null; then
                COMPOSE_CMD="docker-compose"
            else
                COMPOSE_CMD="docker compose"
            fi
            echo "1. View logs: $COMPOSE_CMD -f docker-compose.psycheville.yml logs -f psycheville-worker"
            echo "2. Check reports: ls -la psycheville/obsidian_vault/PsycheVille/Departments/Tools_Refinery/"
            echo "3. Generate test logs: python3 psycheville/test_logging.py"
            echo ""
            sleep 3
            show_status
            ;;
        status)
            show_status
            ;;
        stop)
            print_status "Stopping PsycheVille..."
            if command -v docker-compose &> /dev/null; then
                docker-compose -f docker-compose.psycheville.yml down
            else
                docker compose -f docker-compose.psycheville.yml down
            fi
            print_success "PsycheVille stopped"
            ;;
        logs)
            print_status "Showing PsycheVille logs..."
            if command -v docker-compose &> /dev/null; then
                docker-compose -f docker-compose.psycheville.yml logs -f psycheville-worker
            else
                docker compose -f docker-compose.psycheville.yml logs -f psycheville-worker
            fi
            ;;
        *)
            echo "Usage: $0 {deploy|status|stop|logs} [--with-samples]"
            echo ""
            echo "Commands:"
            echo "  deploy          Deploy PsycheVille (default)"
            echo "  deploy --with-samples  Deploy with sample logs"
            echo "  status          Show service status and reports"
            echo "  stop            Stop PsycheVille services"
            echo "  logs            Show worker logs"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
