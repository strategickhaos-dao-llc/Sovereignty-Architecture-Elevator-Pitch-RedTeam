#!/bin/bash
# Strategickhaos Cluster Setup Script
# Automated setup for joining the 4-node AI supercluster

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Strategickhaos 4-Node AI Supercluster Setup             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}⚠️  Please do not run this script as root${NC}"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Detect OS
echo -e "${YELLOW}[1/7] Detecting operating system...${NC}"
OS="unknown"
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
fi
echo -e "${GREEN}✓ Detected: $OS${NC}"
echo ""

# Step 2: Install Tailscale
echo -e "${YELLOW}[2/7] Installing Tailscale...${NC}"
if command_exists tailscale; then
    echo -e "${GREEN}✓ Tailscale already installed${NC}"
else
    case $OS in
        ubuntu|debian)
            curl -fsSL https://tailscale.com/install.sh | sh
            ;;
        fedora|centos|rhel)
            curl -fsSL https://tailscale.com/install.sh | sh
            ;;
        arch)
            sudo pacman -S tailscale --noconfirm
            ;;
        *)
            echo -e "${RED}✗ Unsupported OS. Please install Tailscale manually from https://tailscale.com${NC}"
            exit 1
            ;;
    esac
    echo -e "${GREEN}✓ Tailscale installed${NC}"
fi
echo ""

# Step 3: Configure Tailscale
echo -e "${YELLOW}[3/7] Configuring Tailscale...${NC}"
if sudo tailscale status >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Tailscale already connected${NC}"
else
    echo -e "${BLUE}Please authenticate with Tailscale...${NC}"
    sudo tailscale up
    echo -e "${GREEN}✓ Tailscale connected${NC}"
fi
echo ""

# Step 4: Set hostname
echo -e "${YELLOW}[4/7] Configure cluster hostname${NC}"
echo "Select your machine role:"
echo "  1) nitro-lyra (Primary brain + inference)"
echo "  2) athina-throne (Heavy training + 405B)"
echo "  3) nova-warrior (Fast inference + voice)"
echo "  4) asteroth-gate (Honeypot + gateway)"
echo "  5) Custom hostname"
read -p "Enter choice [1-5]: " hostname_choice

case $hostname_choice in
    1) NEW_HOSTNAME="nitro-lyra" ;;
    2) NEW_HOSTNAME="athina-throne" ;;
    3) NEW_HOSTNAME="nova-warrior" ;;
    4) NEW_HOSTNAME="asteroth-gate" ;;
    5) 
        read -p "Enter custom hostname: " NEW_HOSTNAME
        ;;
    *)
        echo -e "${RED}✗ Invalid choice${NC}"
        exit 1
        ;;
esac

CURRENT_HOSTNAME=$(hostname)
if [ "$CURRENT_HOSTNAME" != "$NEW_HOSTNAME" ]; then
    echo -e "${BLUE}Setting hostname to: $NEW_HOSTNAME${NC}"
    sudo hostnamectl set-hostname "$NEW_HOSTNAME"
    echo -e "${GREEN}✓ Hostname set to $NEW_HOSTNAME${NC}"
    echo -e "${YELLOW}⚠️  You may need to restart for hostname to fully apply${NC}"
else
    echo -e "${GREEN}✓ Hostname already set to $NEW_HOSTNAME${NC}"
fi
echo ""

# Step 5: Install Docker
echo -e "${YELLOW}[5/7] Installing Docker...${NC}"
if command_exists docker; then
    echo -e "${GREEN}✓ Docker already installed${NC}"
else
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
    echo -e "${GREEN}✓ Docker installed${NC}"
    echo -e "${YELLOW}⚠️  You need to log out and back in for docker group to take effect${NC}"
fi
echo ""

# Step 6: Install NVIDIA Container Toolkit (if GPU present)
echo -e "${YELLOW}[6/7] Checking for NVIDIA GPU...${NC}"
if command_exists nvidia-smi; then
    echo -e "${GREEN}✓ NVIDIA GPU detected${NC}"
    
    if dpkg -l | grep -q nvidia-container-toolkit; then
        echo -e "${GREEN}✓ NVIDIA Container Toolkit already installed${NC}"
    else
        echo -e "${BLUE}Installing NVIDIA Container Toolkit...${NC}"
        distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
        curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
            sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
        curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
            sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
            sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
        sudo apt-get update
        sudo apt-get install -y nvidia-container-toolkit
        sudo nvidia-ctk runtime configure --runtime=docker
        sudo systemctl restart docker
        echo -e "${GREEN}✓ NVIDIA Container Toolkit installed${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  No NVIDIA GPU detected - skipping GPU setup${NC}"
fi
echo ""

# Step 7: Download cluster configuration
echo -e "${YELLOW}[7/7] Setting up cluster directory...${NC}"
CLUSTER_DIR="$HOME/strategickhaos-cluster"
mkdir -p "$CLUSTER_DIR"
cd "$CLUSTER_DIR"

# Download cluster-compose.yml if not present
if [ ! -f "cluster-compose.yml" ]; then
    echo -e "${BLUE}Downloading cluster configuration...${NC}"
    curl -fsSL -o cluster-compose.yml https://raw.githubusercontent.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/main/cluster-compose.yml || {
        echo -e "${YELLOW}⚠️  Could not download from GitHub, using local copy${NC}"
        if [ -f "../cluster-compose.yml" ]; then
            cp ../cluster-compose.yml .
        else
            echo -e "${RED}✗ cluster-compose.yml not found${NC}"
            exit 1
        fi
    }
fi

# Create necessary directories
mkdir -p models monitoring invite-html

# Create basic nginx config for honeypot
cat > nginx-honeypot.conf <<'EOF'
events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        server_name _;
        
        access_log /var/log/nginx/honeypot.log;
        
        location / {
            root /usr/share/nginx/html;
            index index.html;
        }
    }
}
EOF

# Create basic invite HTML
cat > invite-html/index.html <<'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Strategickhaos - Private Network</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background: #000;
            color: #0f0;
            padding: 50px;
            text-align: center;
        }
        h1 { font-size: 3em; }
        .warning {
            border: 2px solid #0f0;
            padding: 20px;
            margin: 20px auto;
            max-width: 600px;
        }
    </style>
</head>
<body>
    <h1>⚠️ RESTRICTED ACCESS ⚠️</h1>
    <div class="warning">
        <p>This is a private AI cluster.</p>
        <p>Authorized personnel only.</p>
        <p>All access attempts are logged.</p>
    </div>
</body>
</html>
EOF

echo -e "${GREEN}✓ Cluster directory setup complete${NC}"
echo ""

# Final instructions
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                  Setup Complete! 🎉                        ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo -e "  1. ${YELLOW}Log out and back in${NC} (for Docker group to take effect)"
echo -e "  2. ${YELLOW}cd $CLUSTER_DIR${NC}"
echo -e "  3. ${YELLOW}docker compose up -d${NC}"
echo ""

# Role-specific instructions
case $hostname_choice in
    1)
        echo -e "${BLUE}Primary node (nitro-lyra) additional steps:${NC}"
        echo -e "  • ${YELLOW}docker compose --profile monitoring up -d${NC}"
        ;;
    2)
        echo -e "${BLUE}Training node (athina-throne) additional steps:${NC}"
        echo -e "  • Pull models: ${YELLOW}docker exec ollama ollama pull llama3.1:405b${NC}"
        ;;
    3)
        echo -e "${BLUE}Voice node (nova-warrior) additional steps:${NC}"
        echo -e "  • ${YELLOW}docker compose --profile voice up -d${NC}"
        ;;
    4)
        echo -e "${BLUE}Gateway node (asteroth-gate) additional steps:${NC}"
        echo -e "  • ${YELLOW}docker compose --profile honeypot up -d${NC}"
        ;;
esac
echo ""
echo -e "${BLUE}Access your cluster at:${NC}"
echo -e "  • Open-WebUI: ${GREEN}http://nitro-lyra.tail-scale.ts.net:3000${NC}"
echo -e "  • Direct API:  ${GREEN}http://$NEW_HOSTNAME.tail-scale.ts.net:11434${NC}"
echo ""
echo -e "${YELLOW}For full documentation, see: CLUSTER_DEPLOYMENT.md${NC}"
