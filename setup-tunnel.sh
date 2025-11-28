#!/bin/bash
# setup-tunnel.sh - Cloudflare Tunnel Quick Setup for Linux/Mac
# Strategic Khaos - Zero to Global in 12 Seconds

set -uo pipefail

# Default values
PORT=${1:-3000}
HOST=${2:-localhost}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

log() {
    echo -e "${CYAN}[$(date +%H:%M:%S)]${NC} $*"
}

error() {
    echo -e "${RED}[ERROR]${NC} $*" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $*"
}

show_banner() {
    echo ""
    echo -e "${MAGENTA}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}║                                                              ║${NC}"
    echo -e "${MAGENTA}║        🌐 CLOUDFLARE TUNNEL QUICK SETUP 🌐                   ║${NC}"
    echo -e "${MAGENTA}║                                                              ║${NC}"
    echo -e "${MAGENTA}║        Strategic Khaos - Zero to Global in 12 Seconds       ║${NC}"
    echo -e "${MAGENTA}║                                                              ║${NC}"
    echo -e "${MAGENTA}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

show_help() {
    echo "🌐 Cloudflare Tunnel Quick Setup"
    echo ""
    echo "Usage: ./setup-tunnel.sh [port] [host]"
    echo ""
    echo "Parameters:"
    echo "  port    Port number to tunnel (default: 3000)"
    echo "  host    Host address (default: localhost)"
    echo ""
    echo "Examples:"
    echo "  ./setup-tunnel.sh                    # Tunnel localhost:3000"
    echo "  ./setup-tunnel.sh 8080               # Tunnel localhost:8080"
    echo "  ./setup-tunnel.sh 3000 127.0.0.1     # Tunnel 127.0.0.1:3000"
    echo ""
    exit 0
}

check_local_service() {
    local url="http://${HOST}:${PORT}"
    
    log "🔍 Checking if local service is running at $url..."
    
    if curl -s -o /dev/null -w "%{http_code}" "$url" --max-time 5 | grep -q "200\|302\|401\|403"; then
        success "✓ Local service is running"
        return 0
    else
        warn "⚠ Local service at $url is not responding"
        warn "   Make sure your application is running before starting the tunnel"
        echo ""
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
        return 1
    fi
}

check_cloudflared() {
    log "🔍 Checking if cloudflared is installed..."
    
    if command -v cloudflared &> /dev/null; then
        local version=$(cloudflared --version 2>&1 | head -n1)
        success "✓ cloudflared is installed: $version"
        return 0
    else
        return 1
    fi
}

detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            echo "$ID"
        else
            echo "linux"
        fi
    else
        echo "unknown"
    fi
}

install_cloudflared() {
    local os=$(detect_os)
    
    log "📥 Installing cloudflared..."
    echo ""
    
    case "$os" in
        macos)
            if ! command -v brew &> /dev/null; then
                error "Homebrew is not installed. Please install Homebrew first:"
                echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
                echo ""
                echo "Alternative: Download from https://github.com/cloudflare/cloudflared/releases"
                exit 1
            fi
            
            log "Installing via Homebrew..."
            brew install cloudflare/cloudflare/cloudflared
            
            if [ $? -eq 0 ]; then
                success "✓ cloudflared installed successfully"
                return 0
            else
                error "Failed to install cloudflared"
                exit 1
            fi
            ;;
            
        ubuntu|debian)
            log "Installing for Debian/Ubuntu..."
            
            # Download and install .deb package
            local temp_file=$(mktemp)
            curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o "$temp_file"
            
            if [ $? -eq 0 ]; then
                sudo dpkg -i "$temp_file"
                rm "$temp_file"
                success "✓ cloudflared installed successfully"
                return 0
            else
                error "Failed to download cloudflared"
                rm "$temp_file"
                exit 1
            fi
            ;;
            
        fedora|rhel|centos)
            log "Installing for RHEL/Fedora/CentOS..."
            
            sudo rpm -i https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-x86_64.rpm
            
            if [ $? -eq 0 ]; then
                success "✓ cloudflared installed successfully"
                return 0
            else
                error "Failed to install cloudflared"
                exit 1
            fi
            ;;
            
        arch)
            log "Installing for Arch Linux..."
            
            if command -v yay &> /dev/null; then
                yay -S cloudflared
            elif command -v paru &> /dev/null; then
                paru -S cloudflared
            else
                error "Please install cloudflared manually using your AUR helper"
                echo "  yay -S cloudflared"
                echo "  or"
                echo "  paru -S cloudflared"
                exit 1
            fi
            
            if [ $? -eq 0 ]; then
                success "✓ cloudflared installed successfully"
                return 0
            else
                error "Failed to install cloudflared"
                exit 1
            fi
            ;;
            
        *)
            error "Unsupported OS: $os"
            echo ""
            echo "Please install cloudflared manually:"
            echo "  https://github.com/cloudflare/cloudflared/releases"
            echo ""
            echo "After installation, run this script again."
            exit 1
            ;;
    esac
}

start_tunnel() {
    local url="http://${HOST}:${PORT}"
    
    log "🚀 Starting Cloudflare Tunnel to $url..."
    echo ""
    echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}  CLOUDFLARE TUNNEL STARTING${NC}"
    echo -e "${CYAN}  Local URL:  $url${NC}"
    echo -e "${CYAN}  Public URL: Will be displayed below...${NC}"
    echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${GRAY}Press Ctrl+C to stop the tunnel${NC}"
    echo ""
    
    # Start cloudflared tunnel
    cloudflared tunnel --url "$url"
    
    if [ $? -ne 0 ]; then
        error "Tunnel failed to start"
        exit 1
    fi
}

main() {
    # Check for help flag
    if [[ "$*" == *"--help"* ]] || [[ "$*" == *"-h"* ]]; then
        show_help
    fi
    
    show_banner
    
    # Build URL
    local url="http://${HOST}:${PORT}"
    
    log "Target: $url"
    echo ""
    
    # Check if local service is running
    check_local_service
    echo ""
    
    # Check if cloudflared is installed
    if ! check_cloudflared; then
        warn "cloudflared is not installed"
        echo ""
        read -p "Install cloudflared now? (Y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Nn]$ ]]; then
            error "cloudflared is required. Exiting."
            exit 1
        fi
        
        echo ""
        install_cloudflared
        echo ""
        
        # Verify installation
        if ! check_cloudflared; then
            error "cloudflared installation verification failed"
            echo ""
            echo "Please try installing manually:"
            echo "  https://github.com/cloudflare/cloudflared/releases"
            exit 1
        fi
    fi
    
    echo ""
    
    # Start tunnel
    start_tunnel
}

# Run main function
main "$@"
