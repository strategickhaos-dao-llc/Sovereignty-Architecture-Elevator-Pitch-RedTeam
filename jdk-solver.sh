#!/usr/bin/env bash
# jdk-solver.sh - JDK Management and Solver for CloudOS
# Strategic Khaos Cloud Operating System - Java Development Kit Manager
# Supports OpenJDK 25 and multiple JDK versions

set -euo pipefail

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
JDK_HOME_BASE="${JDK_HOME_BASE:-/opt/jdk}"
CLOUDOS_JDK_CONFIG="${CLOUDOS_JDK_CONFIG:-$HOME/.cloudos/jdk-config.yaml}"
DEFAULT_JDK_VERSION="25"

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

# Create necessary directories
init_directories() {
    log "📁 Initializing JDK solver directories..."
    mkdir -p "$JDK_HOME_BASE"
    mkdir -p "$(dirname "$CLOUDOS_JDK_CONFIG")"
    success "Directories initialized"
}

# Detect system architecture
detect_architecture() {
    local arch
    arch=$(uname -m)
    case "$arch" in
        x86_64|amd64)
            echo "x64"
            ;;
        aarch64|arm64)
            echo "aarch64"
            ;;
        *)
            error "Unsupported architecture: $arch"
            exit 1
            ;;
    esac
}

# Detect operating system
detect_os() {
    local os
    os=$(uname -s)
    case "$os" in
        Linux)
            echo "linux"
            ;;
        Darwin)
            echo "mac"
            ;;
        MINGW*|MSYS*|CYGWIN*)
            echo "windows"
            ;;
        *)
            error "Unsupported operating system: $os"
            exit 1
            ;;
    esac
}

# Download JDK from Adoptium (Eclipse Temurin)
download_jdk() {
    local version=$1
    local os
    local arch
    
    os=$(detect_os)
    arch=$(detect_architecture)
    
    log "📥 Downloading OpenJDK $version for $os-$arch..."
    
    local jdk_dir="$JDK_HOME_BASE/jdk-$version"
    
    if [[ -d "$jdk_dir" ]]; then
        warn "JDK $version already exists at $jdk_dir"
        return 0
    fi
    
    # Construct download URL for Adoptium
    local download_url
    case "$version" in
        25)
            # For JDK 25, use early access or latest available
            download_url="https://github.com/adoptium/temurin25-binaries/releases/download/jdk-25%2B8/OpenJDK25U-jdk_${arch}_${os}_hotspot_25.0.1_8.tar.gz"
            ;;
        21)
            download_url="https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.1%2B12/OpenJDK21U-jdk_${arch}_${os}_hotspot_21.0.1_12.tar.gz"
            ;;
        17)
            download_url="https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.9%2B9/OpenJDK17U-jdk_${arch}_${os}_hotspot_17.0.9_9.tar.gz"
            ;;
        11)
            download_url="https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.21%2B9/OpenJDK11U-jdk_${arch}_${os}_hotspot_11.0.21_9.tar.gz"
            ;;
        *)
            error "Unsupported JDK version: $version"
            return 1
            ;;
    esac
    
    # Download and extract
    local temp_file="/tmp/openjdk-${version}.tar.gz"
    
    if command -v wget &> /dev/null; then
        wget -O "$temp_file" "$download_url" || {
            error "Failed to download JDK $version from $download_url"
            return 1
        }
    elif command -v curl &> /dev/null; then
        curl -L -o "$temp_file" "$download_url" || {
            error "Failed to download JDK $version from $download_url"
            return 1
        }
    else
        error "Neither wget nor curl is available. Please install one."
        return 1
    fi
    
    # Extract to JDK home
    log "📦 Extracting JDK $version..."
    mkdir -p "$jdk_dir"
    
    if [[ "$os" == "mac" ]]; then
        # macOS has different structure
        tar -xzf "$temp_file" -C "$jdk_dir" --strip-components=3 || {
            error "Failed to extract JDK"
            rm -f "$temp_file"
            return 1
        }
    else
        tar -xzf "$temp_file" -C "$jdk_dir" --strip-components=1 || {
            error "Failed to extract JDK"
            rm -f "$temp_file"
            return 1
        }
    fi
    
    rm -f "$temp_file"
    success "JDK $version installed at $jdk_dir"
}

# List installed JDKs
list_jdks() {
    log "📋 Installed JDKs:"
    
    if [[ ! -d "$JDK_HOME_BASE" ]]; then
        warn "No JDKs installed yet"
        return
    fi
    
    local current_jdk
    current_jdk=$(get_current_jdk)
    
    for jdk_dir in "$JDK_HOME_BASE"/jdk-*; do
        if [[ -d "$jdk_dir" ]]; then
            local version
            version=$(basename "$jdk_dir" | sed 's/jdk-//')
            
            if [[ -x "$jdk_dir/bin/java" ]]; then
                local java_version
                java_version=$("$jdk_dir/bin/java" -version 2>&1 | head -n 1)
                
                if [[ "$jdk_dir" == "$current_jdk" ]]; then
                    echo -e "  ${GREEN}* $version${NC} (active) - $java_version"
                else
                    echo -e "    $version - $java_version"
                fi
            else
                echo -e "  ${RED}✗ $version${NC} (invalid installation)"
            fi
        fi
    done
}

# Get current JDK
get_current_jdk() {
    if [[ -L "$JDK_HOME_BASE/current" ]]; then
        readlink -f "$JDK_HOME_BASE/current"
    fi
}

# Set current JDK version
set_jdk() {
    local version=$1
    local jdk_dir="$JDK_HOME_BASE/jdk-$version"
    
    if [[ ! -d "$jdk_dir" ]]; then
        error "JDK $version is not installed"
        info "Run: $0 install $version"
        return 1
    fi
    
    log "🔄 Setting JDK $version as active..."
    
    # Create or update symlink
    rm -f "$JDK_HOME_BASE/current"
    ln -s "$jdk_dir" "$JDK_HOME_BASE/current"
    
    # Update configuration
    cat > "$CLOUDOS_JDK_CONFIG" <<EOF
# CloudOS JDK Configuration
# Generated by jdk-solver.sh on $(date)
current_jdk: $version
jdk_home: $jdk_dir
java_home: $jdk_dir
EOF
    
    success "JDK $version is now active"
    info "JAVA_HOME: $jdk_dir"
    info "Add to your shell profile:"
    echo "  export JAVA_HOME=$JDK_HOME_BASE/current"
    echo "  export PATH=\$JAVA_HOME/bin:\$PATH"
}

# Verify JDK installation
verify_jdk() {
    local version=${1:-}
    
    if [[ -z "$version" ]]; then
        # Verify current JDK
        local current_jdk
        current_jdk=$(get_current_jdk)
        
        if [[ -z "$current_jdk" ]]; then
            error "No JDK is currently active"
            return 1
        fi
        
        version=$(basename "$current_jdk" | sed 's/jdk-//')
    fi
    
    local jdk_dir="$JDK_HOME_BASE/jdk-$version"
    
    log "🔍 Verifying JDK $version..."
    
    if [[ ! -d "$jdk_dir" ]]; then
        error "JDK $version is not installed"
        return 1
    fi
    
    # Check java executable
    if [[ ! -x "$jdk_dir/bin/java" ]]; then
        error "Java executable not found or not executable"
        return 1
    fi
    
    # Check javac compiler
    if [[ ! -x "$jdk_dir/bin/javac" ]]; then
        error "Java compiler (javac) not found or not executable"
        return 1
    fi
    
    # Run java -version
    local java_version
    java_version=$("$jdk_dir/bin/java" -version 2>&1)
    
    echo -e "${GREEN}✓${NC} Java runtime:"
    echo "$java_version" | sed 's/^/  /'
    
    # Run javac -version
    local javac_version
    javac_version=$("$jdk_dir/bin/javac" -version 2>&1)
    
    echo -e "${GREEN}✓${NC} Java compiler:"
    echo "$javac_version" | sed 's/^/  /'
    
    # Test compilation
    local test_file="/tmp/HelloCloudOS.java"
    cat > "$test_file" <<'EOF'
public class HelloCloudOS {
    public static void main(String[] args) {
        System.out.println("CloudOS JDK Solver - Verification Successful!");
        System.out.println("Java Version: " + System.getProperty("java.version"));
        System.out.println("Java Vendor: " + System.getProperty("java.vendor"));
        System.out.println("OS: " + System.getProperty("os.name"));
    }
}
EOF
    
    log "🧪 Testing Java compilation and execution..."
    
    if "$jdk_dir/bin/javac" "$test_file" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Compilation successful"
        
        if "$jdk_dir/bin/java" -cp /tmp HelloCloudOS 2>/dev/null; then
            echo -e "${GREEN}✓${NC} Execution successful"
        else
            error "Failed to execute test program"
            return 1
        fi
    else
        error "Failed to compile test program"
        return 1
    fi
    
    rm -f "$test_file" /tmp/HelloCloudOS.class
    
    success "JDK $version verification complete"
}

# Remove JDK
remove_jdk() {
    local version=$1
    local jdk_dir="$JDK_HOME_BASE/jdk-$version"
    
    if [[ ! -d "$jdk_dir" ]]; then
        error "JDK $version is not installed"
        return 1
    fi
    
    # Check if it's the current JDK
    local current_jdk
    current_jdk=$(get_current_jdk)
    
    if [[ "$jdk_dir" == "$current_jdk" ]]; then
        warn "JDK $version is currently active"
        warn "Please set a different JDK as active before removing"
        return 1
    fi
    
    log "🗑️  Removing JDK $version..."
    rm -rf "$jdk_dir"
    success "JDK $version removed"
}

# Show help
show_help() {
    cat <<EOF
${CYAN}CloudOS JDK Solver${NC} - Java Development Kit Manager
Strategic Khaos Cloud Operating System

${GREEN}Usage:${NC}
  $0 <command> [arguments]

${GREEN}Commands:${NC}
  ${YELLOW}install <version>${NC}    Install OpenJDK version (11, 17, 21, 25)
  ${YELLOW}list${NC}                 List all installed JDKs
  ${YELLOW}use <version>${NC}        Set active JDK version
  ${YELLOW}verify [version]${NC}     Verify JDK installation
  ${YELLOW}remove <version>${NC}     Remove JDK version
  ${YELLOW}current${NC}              Show current active JDK
  ${YELLOW}help${NC}                 Show this help message

${GREEN}Examples:${NC}
  # Install OpenJDK 25
  $0 install 25

  # Set JDK 25 as active
  $0 use 25

  # Verify current JDK
  $0 verify

  # List all installed JDKs
  $0 list

${GREEN}Environment Variables:${NC}
  JDK_HOME_BASE         Base directory for JDK installations (default: /opt/jdk)
  CLOUDOS_JDK_CONFIG    Configuration file path (default: ~/.cloudos/jdk-config.yaml)

${GREEN}Integration with CloudOS:${NC}
  After installing and activating a JDK, add to your environment:
    export JAVA_HOME=$JDK_HOME_BASE/current
    export PATH=\$JAVA_HOME/bin:\$PATH

EOF
}

# Show current JDK
show_current() {
    local current_jdk
    current_jdk=$(get_current_jdk)
    
    if [[ -z "$current_jdk" ]]; then
        warn "No JDK is currently active"
        info "Install and activate a JDK:"
        echo "  $0 install 25"
        echo "  $0 use 25"
        return 1
    fi
    
    local version
    version=$(basename "$current_jdk" | sed 's/jdk-//')
    
    echo -e "${GREEN}Current JDK:${NC} $version"
    echo -e "${BLUE}Path:${NC} $current_jdk"
    
    if [[ -x "$current_jdk/bin/java" ]]; then
        echo ""
        "$current_jdk/bin/java" -version 2>&1 | head -n 3
    fi
}

# Main command dispatcher
main() {
    if [[ $# -eq 0 ]]; then
        show_help
        exit 0
    fi
    
    local command=$1
    shift
    
    case "$command" in
        install)
            if [[ $# -eq 0 ]]; then
                error "Please specify JDK version to install"
                info "Example: $0 install 25"
                exit 1
            fi
            init_directories
            download_jdk "$1"
            ;;
        list)
            list_jdks
            ;;
        use|set)
            if [[ $# -eq 0 ]]; then
                error "Please specify JDK version to use"
                info "Example: $0 use 25"
                exit 1
            fi
            set_jdk "$1"
            ;;
        verify|test)
            verify_jdk "${1:-}"
            ;;
        remove|uninstall)
            if [[ $# -eq 0 ]]; then
                error "Please specify JDK version to remove"
                info "Example: $0 remove 17"
                exit 1
            fi
            remove_jdk "$1"
            ;;
        current)
            show_current
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"
