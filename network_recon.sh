#!/bin/bash
# network_recon.sh - Comprehensive Network Reconnaissance for Sovereignty Architecture
# Strategic Khaos Full Infrastructure Discovery and Analysis

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Timestamp for report
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_DIR="recon/reports/network_scan_${TIMESTAMP}"
mkdir -p "$REPORT_DIR"

log() { echo -e "${BLUE}[$(date +%H:%M:%S)]${NC} $*"; }
success() { echo -e "${GREEN}[✓]${NC} $*"; }
warn() { echo -e "${YELLOW}[⚠]${NC} $*"; }
error() { echo -e "${RED}[✗]${NC} $*"; }
info() { echo -e "${CYAN}[ℹ]${NC} $*"; }

banner() {
    echo -e "${PURPLE}"
    cat << 'EOF'
╔════════════════════════════════════════════════════════════════════════════╗
║                   🎯 NETWORK RECONNAISSANCE v1.0                          ║
║              Strategic Khaos Infrastructure Discovery                     ║
║                   Full Network Topology & Status                          ║
╚════════════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Initialize report
init_report() {
    cat > "$REPORT_DIR/recon_report.md" << EOF
# Network Reconnaissance Report
**Generated:** $(date)
**Infrastructure:** Strategic Khaos Sovereignty Architecture

---

EOF
}

# Docker network scanning
scan_docker_networks() {
    log "Scanning Docker networks..."
    
    {
        echo "## 🌐 Docker Networks"
        echo ""
        
        if docker network ls &>/dev/null; then
            docker network ls --format "table {{.Name}}\t{{.Driver}}\t{{.Scope}}" | tee -a "$REPORT_DIR/docker_networks.txt"
            echo ""
            
            # Detailed network inspection
            echo "### Network Details"
            echo ""
            docker network ls --format "{{.Name}}" | while read -r network; do
                if [ "$network" != "NAME" ] && [ -n "$network" ]; then
                    echo "#### Network: $network"
                    echo '```json'
                    docker network inspect "$network" 2>/dev/null || echo "Unable to inspect $network"
                    echo '```'
                    echo ""
                fi
            done
            success "Docker networks scanned"
        else
            warn "Docker is not available or not running"
            echo "_Docker not available for network scanning_"
        fi
        echo ""
    } >> "$REPORT_DIR/recon_report.md"
}

# Container discovery
scan_containers() {
    log "Discovering containers..."
    
    {
        echo "## 🐳 Container Inventory"
        echo ""
        
        if docker ps -a &>/dev/null; then
            echo "### Running Containers"
            echo '```'
            docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Image}}" | tee -a "$REPORT_DIR/running_containers.txt"
            echo '```'
            echo ""
            
            echo "### All Containers (including stopped)"
            echo '```'
            docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Image}}" | tee -a "$REPORT_DIR/all_containers.txt"
            echo '```'
            echo ""
            
            # Container health status
            echo "### Container Health Status"
            echo ""
            docker ps --format "{{.Names}}" | while read -r container; do
                if [ -n "$container" ]; then
                    health=$(docker inspect --format='{{.State.Health.Status}}' "$container" 2>/dev/null || echo "no healthcheck")
                    status=$(docker inspect --format='{{.State.Status}}' "$container" 2>/dev/null || echo "unknown")
                    echo "- **$container**: Status=$status, Health=$health"
                fi
            done
            echo ""
            success "Container inventory complete"
        else
            warn "Cannot access Docker containers"
            echo "_Docker containers not accessible_"
        fi
        echo ""
    } >> "$REPORT_DIR/recon_report.md"
}

# Port scanning
scan_ports() {
    log "Scanning exposed ports..."
    
    {
        echo "## 🔌 Port Mapping & Exposure"
        echo ""
        
        echo "### Exposed Ports by Container"
        echo ""
        
        if docker ps &>/dev/null; then
            docker ps --format "{{.Names}}" | while read -r container; do
                if [ -n "$container" ]; then
                    ports=$(docker port "$container" 2>/dev/null)
                    if [ -n "$ports" ]; then
                        echo "#### $container"
                        echo '```'
                        echo "$ports"
                        echo '```'
                        echo ""
                    fi
                fi
            done
            
            # Network listeners
            echo "### Active Network Listeners"
            echo '```'
            if command -v netstat &>/dev/null; then
                netstat -tuln | grep LISTEN | tee -a "$REPORT_DIR/network_listeners.txt"
            elif command -v ss &>/dev/null; then
                ss -tuln | grep LISTEN | tee -a "$REPORT_DIR/network_listeners.txt"
            else
                echo "Neither netstat nor ss available for port scanning"
            fi
            echo '```'
            echo ""
            success "Port scanning complete"
        fi
        echo ""
    } >> "$REPORT_DIR/recon_report.md"
}

# Service health checks
check_service_health() {
    log "Checking service health endpoints..."
    
    {
        echo "## 🏥 Service Health Checks"
        echo ""
        
        # Define known services and their health endpoints
        declare -A services=(
            ["Event Gateway"]="http://localhost:8080/health"
            ["Refinory API"]="http://localhost:8085/health"
            ["RAG Retriever"]="http://localhost:7000/health"
            ["Qdrant (Main)"]="http://localhost:6333/healthz"
            ["Qdrant (Recon)"]="http://localhost:6333/health"
            ["Grafana"]="http://localhost:3000/api/health"
            ["Prometheus"]="http://localhost:9090/-/healthy"
            ["PostgreSQL"]="tcp://localhost:5432"
            ["Redis"]="tcp://localhost:6379"
            ["Embedder"]="http://localhost:8081/health"
        )
        
        echo "| Service | Endpoint | Status | Response Time |"
        echo "|---------|----------|--------|---------------|"
        
        for service in "${!services[@]}"; do
            endpoint="${services[$service]}"
            
            if [[ "$endpoint" == tcp://* ]]; then
                # TCP check
                host_port="${endpoint#tcp://}"
                host="${host_port%:*}"
                port="${host_port#*:}"
                
                if timeout 2 bash -c "cat < /dev/null > /dev/tcp/$host/$port" 2>/dev/null; then
                    echo "| $service | $endpoint | ✅ UP | - |" | tee -a "$REPORT_DIR/service_health.txt"
                else
                    echo "| $service | $endpoint | ❌ DOWN | - |" | tee -a "$REPORT_DIR/service_health.txt"
                fi
            else
                # HTTP check
                start_time=$(date +%s%N)
                if response=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$endpoint" 2>/dev/null); then
                    end_time=$(date +%s%N)
                    response_time=$(( (end_time - start_time) / 1000000 ))
                    
                    if [[ "$response" =~ ^2[0-9][0-9]$ ]]; then
                        echo "| $service | $endpoint | ✅ UP (${response}) | ${response_time}ms |" | tee -a "$REPORT_DIR/service_health.txt"
                    else
                        echo "| $service | $endpoint | ⚠️ WARN (${response}) | ${response_time}ms |" | tee -a "$REPORT_DIR/service_health.txt"
                    fi
                else
                    echo "| $service | $endpoint | ❌ DOWN | - |" | tee -a "$REPORT_DIR/service_health.txt"
                fi
            fi
        done
        
        echo ""
        success "Service health checks complete"
        echo ""
    } >> "$REPORT_DIR/recon_report.md"
}

# Docker Compose analysis
analyze_compose_stacks() {
    log "Analyzing Docker Compose stacks..."
    
    {
        echo "## 📦 Docker Compose Stack Analysis"
        echo ""
        
        # Find all docker-compose files
        compose_files=$(find . -maxdepth 1 -name "docker-compose*.yml" -o -name "docker-compose*.yaml" 2>/dev/null)
        
        if [ -n "$compose_files" ]; then
            echo "### Discovered Compose Files"
            echo ""
            echo "$compose_files" | while read -r file; do
                if [ -f "$file" ]; then
                    echo "#### $file"
                    
                    # Extract services
                    echo "**Services defined:**"
                    echo '```yaml'
                    yq e '.services | keys' "$file" 2>/dev/null || grep -A 1 "^  [a-z]" "$file" | grep -v "^--$" || echo "Unable to parse services"
                    echo '```'
                    
                    # Extract networks
                    echo "**Networks:**"
                    echo '```yaml'
                    yq e '.networks | keys' "$file" 2>/dev/null || grep "networks:" -A 5 "$file" | head -10 || echo "No networks defined"
                    echo '```'
                    
                    # Check if stack is running
                    echo "**Status:**"
                    compose_name=$(basename "$file" .yml | sed 's/docker-compose-//' | sed 's/docker-compose/main/')
                    if docker compose -f "$file" ps 2>/dev/null | grep -q "Up"; then
                        echo "✅ Stack is running"
                    else
                        echo "⚠️ Stack is not running or partially running"
                    fi
                    echo ""
                fi
            done
            success "Docker Compose analysis complete"
        else
            warn "No Docker Compose files found"
            echo "_No docker-compose files found in root directory_"
        fi
        echo ""
    } >> "$REPORT_DIR/recon_report.md"
}

# Environment analysis
analyze_environment() {
    log "Analyzing environment configuration..."
    
    {
        echo "## ⚙️ Environment Configuration"
        echo ""
        
        if [ -f ".env" ]; then
            echo "### Environment Variables (.env found)"
            echo ""
            
            # Count and categorize without exposing secrets
            echo "**Configuration Summary:**"
            echo "- Total variables: $(grep -c "^[A-Z]" .env 2>/dev/null || echo 0)"
            echo "- Discord config: $(grep -c "DISCORD" .env 2>/dev/null || echo 0)"
            echo "- GitHub config: $(grep -c "GITHUB" .env 2>/dev/null || echo 0)"
            echo "- Database config: $(grep -c "POSTGRES\|REDIS\|QDRANT" .env 2>/dev/null || echo 0)"
            echo "- API keys: $(grep -c "API_KEY\|_TOKEN\|_SECRET" .env 2>/dev/null || echo 0)"
            echo ""
            
            echo "**Categories Present:**"
            grep "^[A-Z]" .env 2>/dev/null | cut -d= -f1 | sed 's/_[A-Z]*$//g' | sort -u | while read -r prefix; do
                count=$(grep -c "^${prefix}" .env 2>/dev/null || echo 0)
                echo "- $prefix*: $count variables"
            done
            echo ""
            success "Environment configuration analyzed"
        else
            warn ".env file not found"
            echo "_No .env file found - configuration may be missing_"
        fi
        
        if [ -f ".env.example" ]; then
            echo "### Example Configuration Available"
            echo "✅ .env.example found for reference"
        fi
        echo ""
    } >> "$REPORT_DIR/recon_report.md"
}

# Infrastructure requirements check
check_requirements() {
    log "Checking infrastructure requirements..."
    
    {
        echo "## 📋 Infrastructure Requirements Check"
        echo ""
        
        echo "### Required Tools & Services"
        echo ""
        echo "| Tool | Status | Version |"
        echo "|------|--------|---------|"
        
        # Docker
        if command -v docker &>/dev/null; then
            version=$(docker --version | cut -d' ' -f3 | tr -d ',')
            echo "| Docker | ✅ Installed | $version |"
        else
            echo "| Docker | ❌ Missing | - |"
        fi
        
        # Docker Compose
        if command -v docker &>/dev/null && docker compose version &>/dev/null; then
            version=$(docker compose version --short 2>/dev/null || echo "unknown")
            echo "| Docker Compose | ✅ Installed | $version |"
        else
            echo "| Docker Compose | ❌ Missing | - |"
        fi
        
        # Node.js
        if command -v node &>/dev/null; then
            version=$(node --version)
            echo "| Node.js | ✅ Installed | $version |"
        else
            echo "| Node.js | ⚠️ Not found | - |"
        fi
        
        # npm
        if command -v npm &>/dev/null; then
            version=$(npm --version)
            echo "| npm | ✅ Installed | $version |"
        else
            echo "| npm | ⚠️ Not found | - |"
        fi
        
        # Python
        if command -v python3 &>/dev/null; then
            version=$(python3 --version | cut -d' ' -f2)
            echo "| Python 3 | ✅ Installed | $version |"
        else
            echo "| Python 3 | ⚠️ Not found | - |"
        fi
        
        # curl
        if command -v curl &>/dev/null; then
            version=$(curl --version | head -1 | cut -d' ' -f2)
            echo "| curl | ✅ Installed | $version |"
        else
            echo "| curl | ❌ Missing | - |"
        fi
        
        # jq
        if command -v jq &>/dev/null; then
            version=$(jq --version | cut -d'-' -f2)
            echo "| jq | ✅ Installed | $version |"
        else
            echo "| jq | ⚠️ Not found | - |"
        fi
        
        # yq
        if command -v yq &>/dev/null; then
            version=$(yq --version 2>&1 | grep -oP '\d+\.\d+\.\d+' | head -1 || echo "unknown")
            echo "| yq | ✅ Installed | $version |"
        else
            echo "| yq | ⚠️ Not found | - |"
        fi
        
        echo ""
        success "Requirements check complete"
        echo ""
    } >> "$REPORT_DIR/recon_report.md"
}

# Network topology visualization
generate_topology() {
    log "Generating network topology..."
    
    {
        echo "## 🗺️ Network Topology"
        echo ""
        echo '```mermaid'
        echo 'graph TB'
        echo '    subgraph "External Access"'
        echo '        USER[User/Client]'
        echo '        GH[GitHub Webhooks]'
        echo '    end'
        echo ''
        echo '    subgraph "Entry Points"'
        echo '        NGINX[Nginx :80/:443]'
        echo '        GW[Event Gateway :8080]'
        echo '    end'
        echo ''
        echo '    subgraph "Application Layer"'
        echo '        BOT[Discord Bot]'
        echo '        REF[Refinory API :8085]'
        echo '        JDK[JDK Workspace :8888]'
        echo '    end'
        echo ''
        echo '    subgraph "Data & AI Layer"'
        echo '        PG[(PostgreSQL :5432)]'
        echo '        REDIS[(Redis :6379)]'
        echo '        QD[(Qdrant :6333)]'
        echo '        RAG[RAG API :7000]'
        echo '        EMB[Embedder :8081]'
        echo '    end'
        echo ''
        echo '    subgraph "Monitoring Layer"'
        echo '        PROM[Prometheus :9090]'
        echo '        GRAF[Grafana :3000]'
        echo '    end'
        echo ''
        echo '    USER --> NGINX'
        echo '    USER --> GRAF'
        echo '    GH --> GW'
        echo '    NGINX --> GW'
        echo '    NGINX --> REF'
        echo '    NGINX --> GRAF'
        echo '    GW --> BOT'
        echo '    BOT --> REF'
        echo '    REF --> PG'
        echo '    REF --> REDIS'
        echo '    REF --> QD'
        echo '    REF --> RAG'
        echo '    RAG --> QD'
        echo '    RAG --> EMB'
        echo '    PROM --> GW'
        echo '    PROM --> REF'
        echo '    PROM --> RAG'
        echo '    GRAF --> PROM'
        echo '```'
        echo ""
        success "Network topology generated"
        echo ""
    } >> "$REPORT_DIR/recon_report.md"
}

# Resource usage analysis
analyze_resources() {
    log "Analyzing resource usage..."
    
    {
        echo "## 💾 Resource Usage Analysis"
        echo ""
        
        if docker stats --no-stream &>/dev/null; then
            echo "### Container Resource Usage"
            echo '```'
            docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}" | tee -a "$REPORT_DIR/resource_usage.txt"
            echo '```'
            echo ""
            
            # Disk usage by volumes
            echo "### Docker Volume Usage"
            echo '```'
            docker system df -v 2>/dev/null | tee -a "$REPORT_DIR/disk_usage.txt"
            echo '```'
            echo ""
            success "Resource analysis complete"
        else
            warn "Unable to collect resource statistics"
        fi
        echo ""
    } >> "$REPORT_DIR/recon_report.md"
}

# Security analysis
security_scan() {
    log "Performing security scan..."
    
    {
        echo "## 🔒 Security Analysis"
        echo ""
        
        echo "### Exposed Ports Security Review"
        echo ""
        
        # Check for dangerous port exposures
        if docker ps &>/dev/null; then
            echo "**Port Exposure Analysis:**"
            echo ""
            
            # Check for 0.0.0.0 bindings
            danger_ports=$(docker ps --format "{{.Names}}\t{{.Ports}}" | grep "0.0.0.0" || true)
            if [ -n "$danger_ports" ]; then
                warn "Found containers exposed on all interfaces (0.0.0.0):"
                echo '```'
                echo "$danger_ports"
                echo '```'
                echo ""
            else
                success "No dangerous port exposures on 0.0.0.0"
                echo ""
            fi
            
            # Check for privileged containers
            echo "**Privileged Containers:**"
            echo '```'
            privileged=$(docker ps --format "{{.Names}}" | xargs -I {} docker inspect --format '{{.Name}}: {{.HostConfig.Privileged}}' {} 2>/dev/null | grep true || echo "None found")
            echo "$privileged"
            echo '```'
            echo ""
            
            # Check for host network mode
            echo "**Host Network Mode:**"
            echo '```'
            host_network=$(docker ps --format "{{.Names}}" | xargs -I {} docker inspect --format '{{.Name}}: {{.HostConfig.NetworkMode}}' {} 2>/dev/null | grep host || echo "None found")
            echo "$host_network"
            echo '```'
            echo ""
        fi
        
        # Check for secrets in env files
        echo "### Environment Security"
        echo ""
        if [ -f ".env" ]; then
            secrets_count=$(grep -E "PASSWORD|SECRET|TOKEN|KEY" .env 2>/dev/null | wc -l)
            echo "- Found $secrets_count potential secrets in .env"
            
            if grep -q "dev_password\|changeme\|password123\|admin" .env 2>/dev/null; then
                warn "⚠️ Found weak/default passwords in .env"
            else
                success "✓ No obvious weak passwords detected"
            fi
        fi
        echo ""
        
        success "Security scan complete"
        echo ""
    } >> "$REPORT_DIR/recon_report.md"
}

# Generate recommendations
generate_recommendations() {
    log "Generating recommendations..."
    
    {
        echo "## 💡 Recommendations & Action Items"
        echo ""
        
        echo "### Infrastructure Recommendations"
        echo ""
        
        # Check if all stacks are running
        if ! docker ps | grep -q "recon-"; then
            echo "1. ⚠️ **RECON Stack Not Running**"
            echo "   - Start with: \`./launch-recon.sh start\`"
            echo "   - This enables RAG-powered repository intelligence"
            echo ""
        fi
        
        if ! docker ps | grep -q "discord-bot"; then
            echo "2. ⚠️ **Discord Bot Not Running**"
            echo "   - Check .env configuration for DISCORD_TOKEN"
            echo "   - Start with: \`docker compose up -d discord-bot\`"
            echo ""
        fi
        
        # Check for monitoring
        if ! docker ps | grep -q "grafana"; then
            echo "3. ℹ️ **Monitoring Stack Not Running**"
            echo "   - Consider starting Grafana/Prometheus for observability"
            echo "   - Start with: \`docker compose up -d grafana prometheus\`"
            echo ""
        fi
        
        # Check for missing tools
        if ! command -v yq &>/dev/null; then
            echo "4. ℹ️ **Install yq for better YAML parsing**"
            echo "   - \`sudo wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64\`"
            echo "   - \`sudo chmod +x /usr/local/bin/yq\`"
            echo ""
        fi
        
        echo "### Security Recommendations"
        echo ""
        echo "1. ✓ Review port exposures (especially 0.0.0.0 bindings)"
        echo "2. ✓ Ensure .env is in .gitignore"
        echo "3. ✓ Rotate any default/weak passwords"
        echo "4. ✓ Enable container resource limits"
        echo "5. ✓ Implement network segmentation with Docker networks"
        echo ""
        
        echo "### Performance Recommendations"
        echo ""
        echo "1. ✓ Monitor resource usage with \`docker stats\`"
        echo "2. ✓ Consider setting memory/CPU limits for containers"
        echo "3. ✓ Use Docker volumes for persistence"
        echo "4. ✓ Enable healthchecks for all services"
        echo "5. ✓ Implement log rotation"
        echo ""
        
        success "Recommendations generated"
        echo ""
    } >> "$REPORT_DIR/recon_report.md"
}

# Generate summary
generate_summary() {
    log "Generating executive summary..."
    
    {
        echo "## 📊 Executive Summary"
        echo ""
        
        # Count services
        running_containers=$(docker ps --format "{{.Names}}" 2>/dev/null | wc -l)
        total_containers=$(docker ps -a --format "{{.Names}}" 2>/dev/null | wc -l)
        networks=$(docker network ls --format "{{.Name}}" 2>/dev/null | wc -l)
        
        echo "### Infrastructure Overview"
        echo ""
        echo "- **Running Containers:** $running_containers / $total_containers"
        echo "- **Docker Networks:** $networks"
        echo "- **Report Generated:** $(date)"
        echo "- **Report Location:** \`$REPORT_DIR/\`"
        echo ""
        
        echo "### Key Findings"
        echo ""
        
        # Service status summary
        if [ "$running_containers" -gt 0 ]; then
            echo "✅ Infrastructure is active with $running_containers running services"
        else
            echo "⚠️ No containers are currently running"
        fi
        echo ""
        
        echo "### Quick Actions"
        echo ""
        echo "\`\`\`bash"
        echo "# View full report"
        echo "cat $REPORT_DIR/recon_report.md"
        echo ""
        echo "# Start RECON stack"
        echo "./launch-recon.sh start"
        echo ""
        echo "# Check service health"
        echo "docker compose ps"
        echo ""
        echo "# View logs"
        echo "docker compose logs -f [service-name]"
        echo "\`\`\`"
        echo ""
        
        success "Executive summary complete"
        echo ""
        
        echo "---"
        echo ""
        echo "_Report generated by Strategic Khaos Network Reconnaissance v1.0_"
        echo ""
    } >> "$REPORT_DIR/recon_report.md"
}

# Main execution
main() {
    banner
    
    log "Starting comprehensive network reconnaissance..."
    log "Report will be saved to: $REPORT_DIR/"
    echo ""
    
    init_report
    
    # Run all scans
    scan_docker_networks
    scan_containers
    scan_ports
    check_service_health
    analyze_compose_stacks
    analyze_environment
    check_requirements
    generate_topology
    analyze_resources
    security_scan
    generate_recommendations
    generate_summary
    
    echo ""
    success "✨ Network reconnaissance complete!"
    echo ""
    info "📄 Full report: $REPORT_DIR/recon_report.md"
    info "📊 View with: cat $REPORT_DIR/recon_report.md | less"
    echo ""
    
    # Create symlink to latest report
    ln -sf "network_scan_${TIMESTAMP}" recon/reports/latest_network_scan
    info "🔗 Latest report: recon/reports/latest_network_scan/recon_report.md"
    echo ""
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
