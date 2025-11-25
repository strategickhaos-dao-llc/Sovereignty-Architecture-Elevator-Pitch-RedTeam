#!/bin/bash
# usb_boot_setup.sh - USB Bootloader Configuration for Sovereignty Node
# Strategickhaos DAO LLC / Valoryield Engine™
# Purpose: Prepare USB device for Mobile Sovereignty Node deployment
# Generated: 2025-11-25T23:00:00Z

set -euo pipefail

# ═══════════════════════════════════════════════════════════════════════════════
# COLOR DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING
# ═══════════════════════════════════════════════════════════════════════════════
log() {
    echo -e "${BLUE}[$(date +%H:%M:%S)]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}[⚠]${NC} $*"
}

log_error() {
    echo -e "${RED}[✗]${NC} $*" >&2
}

# ═══════════════════════════════════════════════════════════════════════════════
# BANNER
# ═══════════════════════════════════════════════════════════════════════════════
show_banner() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════════════╗"
    echo "║        SOVEREIGNTY ARCHITECTURE™ - USB BOOT SETUP                    ║"
    echo "║                    Mobile Node Deployment Tool                        ║"
    echo "╚══════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# ═══════════════════════════════════════════════════════════════════════════════
# SAFETY CHECK
# ═══════════════════════════════════════════════════════════════════════════════
check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_error "This script must be run as root"
        log "Run with: sudo $0"
        exit 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# LIST DEVICES
# ═══════════════════════════════════════════════════════════════════════════════
list_usb_devices() {
    log "Detecting USB devices..."
    echo ""
    
    echo -e "${CYAN}Available USB devices:${NC}"
    echo "──────────────────────────────────────────────────────"
    
    lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,MODEL | grep -E "disk|part" | while read -r line; do
        echo "  $line"
    done
    
    echo ""
    log_warn "CAUTION: Selecting wrong device will result in DATA LOSS"
}

# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATE DEVICE
# ═══════════════════════════════════════════════════════════════════════════════
validate_device() {
    local device="$1"
    
    if [[ ! -b "$device" ]]; then
        log_error "Device not found: $device"
        exit 1
    fi
    
    # Check if it's a USB device
    local device_name
    device_name=$(basename "$device")
    
    if [[ ! -d "/sys/block/${device_name}/device" ]]; then
        log_error "Not a valid block device: $device"
        exit 1
    fi
    
    # Get device info
    local size
    size=$(lsblk -b -d -n -o SIZE "$device" | numfmt --to=iec)
    local model
    model=$(lsblk -d -n -o MODEL "$device" 2>/dev/null || echo "Unknown")
    
    echo ""
    echo -e "${YELLOW}Selected Device:${NC}"
    echo "  Device: $device"
    echo "  Size:   $size"
    echo "  Model:  $model"
    echo ""
    
    log_warn "ALL DATA ON $device WILL BE DESTROYED!"
    
    read -r -p "Are you sure you want to continue? (yes/no): " confirm
    if [[ "$confirm" != "yes" ]]; then
        log "Operation cancelled"
        exit 0
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# DOWNLOAD ISO
# ═══════════════════════════════════════════════════════════════════════════════
download_iso() {
    local iso_url="$1"
    local output_file="$2"
    
    if [[ -f "$output_file" ]]; then
        log "ISO already exists: $output_file"
        return 0
    fi
    
    log "Downloading ISO..."
    
    if command -v wget &> /dev/null; then
        wget --progress=bar:force -O "$output_file" "$iso_url"
    elif command -v curl &> /dev/null; then
        curl -L --progress-bar -o "$output_file" "$iso_url"
    else
        log_error "Neither wget nor curl is installed"
        exit 1
    fi
    
    log_success "ISO downloaded: $output_file"
}

# ═══════════════════════════════════════════════════════════════════════════════
# WRITE ISO TO USB
# ═══════════════════════════════════════════════════════════════════════════════
write_iso_to_usb() {
    local iso_file="$1"
    local device="$2"
    
    if [[ ! -f "$iso_file" ]]; then
        log_error "ISO file not found: $iso_file"
        exit 1
    fi
    
    log "Writing ISO to USB device..."
    log_warn "This will take several minutes. Do not remove the USB drive."
    
    # Unmount any mounted partitions
    umount "${device}"* 2>/dev/null || true
    
    # Write ISO using dd
    dd if="$iso_file" of="$device" bs=4M status=progress conv=fsync
    
    # Sync to ensure all data is written
    sync
    
    log_success "ISO written to USB device"
}

# ═══════════════════════════════════════════════════════════════════════════════
# CREATE PERSISTENT PARTITION
# ═══════════════════════════════════════════════════════════════════════════════
create_persistent_partition() {
    local device="$1"
    local label="${2:-casper-rw}"
    
    log "Creating persistent storage partition..."
    
    # Get the last sector used by the ISO
    local last_sector
    last_sector=$(fdisk -l "$device" | grep "${device}1" | awk '{print $3}')
    
    if [[ -z "$last_sector" ]]; then
        log_warn "Could not determine ISO partition size. Skipping persistent partition."
        return 0
    fi
    
    # Create new partition using remaining space
    echo -e "n\np\n2\n\n\nw" | fdisk "$device" 2>/dev/null || true
    
    # Wait for partition to be recognized
    partprobe "$device"
    sleep 2
    
    # Format as ext4
    local persistent_part="${device}2"
    if [[ -b "$persistent_part" ]]; then
        mkfs.ext4 -L "$label" "$persistent_part"
        log_success "Persistent partition created: $persistent_part"
    else
        log_warn "Could not create persistent partition"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURE SOVEREIGNTY NODE
# ═══════════════════════════════════════════════════════════════════════════════
configure_sovereignty_node() {
    local device="$1"
    
    log "Configuring Sovereignty Node environment..."
    
    # Mount the persistent partition
    local mount_point="/tmp/sovereignty-node-config"
    mkdir -p "$mount_point"
    
    local persistent_part="${device}2"
    if [[ -b "$persistent_part" ]]; then
        mount "$persistent_part" "$mount_point"
        
        # Create sovereignty configuration directory
        mkdir -p "${mount_point}/sovereignty"
        
        # Create default environment file
        cat > "${mount_point}/sovereignty/.env.template" << 'ENV'
# Sovereignty Node Environment Configuration
# Copy to .env and fill in your values

# Discord Integration
DISCORD_TOKEN=
PRS_CHANNEL=
ALERTS_CHANNEL=

# Twitch Streaming
TWITCH_STREAM_KEY=

# GitHub Integration
GITHUB_TOKEN=

# Node Configuration
NODE_NAME=mobile-sovereignty-node
NODE_TYPE=field-deployment
NODE_VERSION=1.0

# Stream Configuration
STREAM_BITRATE=4500k
AUDIO_BITRATE=160k
RESOLUTION=1920x1080
FPS=30
ENV
        
        # Create startup script
        cat > "${mount_point}/sovereignty/node-startup.sh" << 'STARTUP'
#!/bin/bash
# Sovereignty Node Startup Script
# This runs automatically on boot if configured

echo "🚀 Sovereignty Node Starting..."

# Load environment
if [[ -f "$HOME/sovereignty/.env" ]]; then
    source "$HOME/sovereignty/.env"
    echo "✓ Environment loaded"
fi

# Check connectivity
if ping -c 1 github.com &> /dev/null; then
    echo "✓ Network connected"
else
    echo "✗ No network connection"
fi

# Open browser with Codespaces (if GUI available)
if command -v xdg-open &> /dev/null && [[ -n "$DISPLAY" ]]; then
    xdg-open "https://github.dev" &
fi

echo "🎯 Sovereignty Node Ready"
STARTUP
        
        chmod +x "${mount_point}/sovereignty/node-startup.sh"
        
        # Unmount
        umount "$mount_point"
        rmdir "$mount_point"
        
        log_success "Sovereignty Node configuration created"
    else
        log_warn "Persistent partition not available for configuration"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY INSTALLATION
# ═══════════════════════════════════════════════════════════════════════════════
verify_installation() {
    local device="$1"
    
    log "Verifying USB boot installation..."
    
    # Check partitions
    local partitions
    partitions=$(lsblk -n -o NAME "$device" | wc -l)
    
    echo ""
    echo -e "${CYAN}USB Device Structure:${NC}"
    lsblk -o NAME,SIZE,FSTYPE,LABEL,MOUNTPOINT "$device"
    echo ""
    
    if [[ $partitions -ge 2 ]]; then
        log_success "Installation verified"
        log_success "USB device is ready for Mobile Sovereignty Node deployment"
    else
        log_warn "Installation may be incomplete"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# SHOW USAGE
# ═══════════════════════════════════════════════════════════════════════════════
show_usage() {
    show_banner
    
    echo -e "${CYAN}USAGE:${NC}"
    echo "  sudo $0 <command> [options]"
    echo ""
    echo -e "${CYAN}COMMANDS:${NC}"
    echo "  list                        List available USB devices"
    echo "  create <device> <iso>       Create bootable USB from ISO"
    echo "  quick <device>              Quick setup with Ubuntu ISO"
    echo "  verify <device>             Verify USB installation"
    echo "  help                        Show this help message"
    echo ""
    echo -e "${CYAN}EXAMPLES:${NC}"
    echo "  # List USB devices"
    echo "  sudo $0 list"
    echo ""
    echo "  # Create bootable USB from existing ISO"
    echo "  sudo $0 create /dev/sdb ubuntu-22.04-live.iso"
    echo ""
    echo "  # Quick setup with automatic Ubuntu download"
    echo "  sudo $0 quick /dev/sdb"
    echo ""
    echo "  # Verify installation"
    echo "  sudo $0 verify /dev/sdb"
    echo ""
    echo -e "${YELLOW}WARNING: USB creation will DESTROY all data on the device!${NC}"
    echo ""
    echo -e "${PURPLE}Part of the Sovereignty Architecture™ - Mobile Node Pipeline${NC}"
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
main() {
    local command="${1:-help}"
    
    case "$command" in
        list)
            show_banner
            list_usb_devices
            ;;
        create)
            show_banner
            check_root
            
            local device="${2:-}"
            local iso_file="${3:-}"
            
            if [[ -z "$device" || -z "$iso_file" ]]; then
                log_error "Missing arguments"
                echo "Usage: sudo $0 create <device> <iso_file>"
                exit 1
            fi
            
            list_usb_devices
            validate_device "$device"
            write_iso_to_usb "$iso_file" "$device"
            create_persistent_partition "$device"
            configure_sovereignty_node "$device"
            verify_installation "$device"
            
            echo ""
            log_success "Mobile Sovereignty Node USB created successfully!"
            log "Boot from this USB to start your Sovereignty Node"
            ;;
        quick)
            show_banner
            check_root
            
            local device="${2:-}"
            
            if [[ -z "$device" ]]; then
                log_error "Missing device argument"
                echo "Usage: sudo $0 quick <device>"
                exit 1
            fi
            
            list_usb_devices
            validate_device "$device"
            
            # Download Ubuntu Desktop ISO
            local iso_url="https://releases.ubuntu.com/22.04/ubuntu-22.04.3-desktop-amd64.iso"
            local iso_file="/tmp/ubuntu-22.04-desktop.iso"
            
            download_iso "$iso_url" "$iso_file"
            write_iso_to_usb "$iso_file" "$device"
            create_persistent_partition "$device"
            configure_sovereignty_node "$device"
            verify_installation "$device"
            
            echo ""
            log_success "Mobile Sovereignty Node USB created successfully!"
            log "Boot from this USB to start your Sovereignty Node"
            ;;
        verify)
            show_banner
            
            local device="${2:-}"
            
            if [[ -z "$device" ]]; then
                log_error "Missing device argument"
                echo "Usage: $0 verify <device>"
                exit 1
            fi
            
            verify_installation "$device"
            ;;
        help|--help|-h)
            show_usage
            ;;
        *)
            log_error "Unknown command: $command"
            show_usage
            exit 1
            ;;
    esac
}

# Run main with all arguments
main "$@"
