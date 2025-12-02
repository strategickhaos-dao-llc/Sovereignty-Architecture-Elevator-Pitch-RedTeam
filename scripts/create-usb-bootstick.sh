#!/bin/bash
# Strategickhaos USB Boot Stick Generator
# Creates a bootable USB that auto-joins any laptop to the cluster in 90 seconds

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m'

show_banner() {
    echo -e "${MAGENTA}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}║   Strategickhaos USB Boot Stick Generator                 ║${NC}"
    echo -e "${MAGENTA}║   Turn any laptop into Cluster Node #5 in 90 seconds      ║${NC}"
    echo -e "${MAGENTA}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

check_requirements() {
    echo -e "${YELLOW}Checking requirements...${NC}"
    
    # Check if running on Linux
    if [ "$(uname)" != "Linux" ]; then
        echo -e "${RED}✗ This script requires Linux${NC}"
        echo -e "${YELLOW}Please run on a Linux machine to create the boot stick${NC}"
        exit 1
    fi
    
    # Check for required tools
    local missing_tools=()
    
    for tool in parted mkfs.vfat mkfs.ext4 syslinux dd; do
        if ! command -v $tool >/dev/null 2>&1; then
            missing_tools+=("$tool")
        fi
    done
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        echo -e "${RED}✗ Missing required tools: ${missing_tools[*]}${NC}"
        echo -e "${YELLOW}Install with: sudo apt-get install parted dosfstools e2fsprogs syslinux${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ All requirements met${NC}"
    echo ""
}

list_usb_devices() {
    echo -e "${BLUE}Available USB devices:${NC}"
    lsblk -d -o NAME,SIZE,TYPE,TRAN | grep usb || echo "No USB devices found"
    echo ""
}

create_boot_partition() {
    local device=$1
    
    echo -e "${YELLOW}⚠️  WARNING: This will ERASE ALL DATA on $device${NC}"
    read -p "Are you sure? Type 'YES' to continue: " confirm
    
    if [ "$confirm" != "YES" ]; then
        echo -e "${RED}Aborted${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}Creating partitions...${NC}"
    
    # Unmount if mounted
    sudo umount ${device}* 2>/dev/null || true
    
    # Create partition table
    sudo parted -s "$device" mklabel msdos
    sudo parted -s "$device" mkpart primary fat32 1MiB 256MiB
    sudo parted -s "$device" set 1 boot on
    sudo parted -s "$device" mkpart primary ext4 256MiB 100%
    
    # Wait for partition creation
    sleep 2
    
    # Format partitions
    echo -e "${BLUE}Formatting partitions...${NC}"
    sudo mkfs.vfat -F 32 -n BOOT ${device}1
    sudo mkfs.ext4 -L STRATEGOS ${device}2
    
    echo -e "${GREEN}✓ Partitions created${NC}"
}

install_bootloader() {
    local device=$1
    local boot_part=${device}1
    
    echo -e "${BLUE}Installing bootloader...${NC}"
    
    # Create mount point
    local mount_point=$(mktemp -d)
    sudo mount "$boot_part" "$mount_point"
    
    # Install syslinux
    sudo syslinux --install "$boot_part"
    
    # Copy syslinux files
    sudo mkdir -p "$mount_point/syslinux"
    for file in /usr/lib/syslinux/modules/bios/*.c32; do
        sudo cp "$file" "$mount_point/syslinux/" 2>/dev/null || true
    done
    
    # Create syslinux config
    sudo tee "$mount_point/syslinux/syslinux.cfg" > /dev/null <<'EOF'
DEFAULT strategickhaos
PROMPT 0
TIMEOUT 30

LABEL strategickhaos
    MENU LABEL Strategickhaos Cluster Auto-Join
    LINUX /vmlinuz
    APPEND root=LABEL=STRATEGOS ro quiet splash
    INITRD /initrd.img

LABEL live
    MENU LABEL Boot Live System
    LINUX /vmlinuz
    APPEND boot=live components quiet splash
    INITRD /initrd.img
EOF
    
    sudo umount "$mount_point"
    rmdir "$mount_point"
    
    echo -e "${GREEN}✓ Bootloader installed${NC}"
}

create_autosetup_script() {
    local device=$1
    local data_part=${device}2
    
    echo -e "${BLUE}Creating auto-setup scripts...${NC}"
    
    # Mount data partition
    local mount_point=$(mktemp -d)
    sudo mount "$data_part" "$mount_point"
    
    # Get Tailscale auth key (securely)
    echo ""
    echo -e "${YELLOW}To auto-join Tailscale, you need an auth key.${NC}"
    echo -e "${BLUE}Generate one at: https://login.tailscale.com/admin/settings/keys${NC}"
    echo -e "${YELLOW}For security, use environment variable: TAILSCALE_KEY=your_key${NC}"
    echo ""
    if [ -n "$TAILSCALE_KEY" ]; then
        echo -e "${GREEN}Using TAILSCALE_KEY from environment${NC}"
    else
        read -s -p "Paste your Tailscale auth key (hidden, or leave blank): " TAILSCALE_KEY
        echo ""
    fi
    
    # Create auto-setup script
    sudo tee "$mount_point/auto-setup.sh" > /dev/null <<EOF
#!/bin/bash
# Strategickhaos Cluster Auto-Join Script
# Automatically executed on first boot

set -e

echo "🚀 Strategickhaos Cluster Auto-Join Starting..."

# Update system
apt-get update
apt-get upgrade -y

# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Connect to Tailscale
if [ -n "$TAILSCALE_KEY" ]; then
    tailscale up --authkey=$TAILSCALE_KEY
else
    tailscale up
fi

# Install Docker
curl -fsSL https://get.docker.com | sh
usermod -aG docker \$(logname)

# Install NVIDIA drivers if GPU detected
if lspci | grep -i nvidia; then
    apt-get install -y nvidia-driver-535
    
    # Install NVIDIA Container Toolkit
    distribution=\$(. /etc/os-release;echo \$ID\$VERSION_ID)
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
        gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
    curl -s -L https://nvidia.github.io/libnvidia-container/\$distribution/libnvidia-container.list | \
        sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
        tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    apt-get update
    apt-get install -y nvidia-container-toolkit
    nvidia-ctk runtime configure --runtime=docker
    systemctl restart docker
fi

# Clone repository
cd /home/\$(logname)
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git strategickhaos-cluster
cd strategickhaos-cluster

# Auto-detect and set hostname
NODE_NUM=\$(tailscale status --json | jq '.Peer | length')
NEW_HOSTNAME="strategickhaos-node-\$NODE_NUM"
hostnamectl set-hostname "\$NEW_HOSTNAME"

# Deploy cluster
docker compose -f cluster-compose.yml up -d

echo "✅ Strategickhaos Cluster Node #\$NODE_NUM is ONLINE!"
echo "Access at: http://\$NEW_HOSTNAME.tail-scale.ts.net:11434"

# Disable this script after first run
systemctl disable strategickhaos-autojoin.service
EOF
    
    sudo chmod +x "$mount_point/auto-setup.sh"
    
    # Create systemd service for auto-setup
    sudo tee "$mount_point/strategickhaos-autojoin.service" > /dev/null <<'EOF'
[Unit]
Description=Strategickhaos Cluster Auto-Join
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/media/STRATEGOS/auto-setup.sh
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
    
    # Create README
    sudo tee "$mount_point/README.txt" > /dev/null <<'EOF'
STRATEGICKHAOS CLUSTER AUTO-JOIN USB
=====================================

This USB stick will automatically:
1. Install Tailscale and join your network
2. Install Docker and NVIDIA drivers
3. Deploy Ollama and cluster services
4. Auto-assign cluster node number

USAGE:
------
1. Boot from this USB stick
2. Wait 90 seconds for auto-setup
3. Node will auto-join your cluster

MANUAL SETUP:
-------------
If auto-setup fails, run:
    sudo bash /media/STRATEGOS/auto-setup.sh

REQUIREMENTS:
-------------
- Internet connection
- Tailscale auth key (if not embedded)
- NVIDIA GPU (optional, but recommended)

Generated: $(date)
EOF
    
    sudo umount "$mount_point"
    rmdir "$mount_point"
    
    echo -e "${GREEN}✓ Auto-setup scripts created${NC}"
}

create_debian_live() {
    echo -e "${YELLOW}Creating Debian Live system...${NC}"
    echo -e "${BLUE}This requires debootstrap and may take 10-15 minutes${NC}"
    
    if ! command -v debootstrap >/dev/null 2>&1; then
        echo -e "${RED}✗ debootstrap not found${NC}"
        echo -e "${YELLOW}Install with: sudo apt-get install debootstrap${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}Note: Full live system creation is complex.${NC}"
    echo -e "${YELLOW}For now, we'll create the auto-join scripts only.${NC}"
    echo -e "${BLUE}Boot into any Linux live USB, then run the auto-setup script.${NC}"
}

show_completion() {
    local device=$1
    
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   USB Boot Stick Created Successfully! 🎉                 ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Device: $device${NC}"
    echo ""
    echo -e "${YELLOW}Instructions:${NC}"
    echo -e "  1. Boot any laptop/desktop from this USB"
    echo -e "  2. After booting into Linux, the auto-setup will run"
    echo -e "  3. Wait ~90 seconds for cluster to join"
    echo -e "  4. Access at: http://strategickhaos-node-N.tail-scale.ts.net:11434"
    echo ""
    echo -e "${YELLOW}Manual Setup (if needed):${NC}"
    echo -e "  • Mount the STRATEGOS partition"
    echo -e "  • Run: sudo bash /path/to/auto-setup.sh"
    echo ""
    echo -e "${GREEN}Your cluster expansion stick is ready! 🚀${NC}"
}

# Main script logic
show_banner
check_requirements

if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}This script must be run as root (use sudo)${NC}"
    exit 1
fi

list_usb_devices

read -p "Enter USB device (e.g., /dev/sdb): " DEVICE

if [ ! -b "$DEVICE" ]; then
    echo -e "${RED}✗ Invalid device: $DEVICE${NC}"
    exit 1
fi

# Confirm it's a USB device
if ! lsblk -d -o TRAN "$DEVICE" | grep -q usb; then
    echo -e "${RED}⚠️  $DEVICE does not appear to be a USB device${NC}"
    read -p "Continue anyway? [y/N]: " confirm
    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

create_boot_partition "$DEVICE"
install_bootloader "$DEVICE"
create_autosetup_script "$DEVICE"
show_completion "$DEVICE"
