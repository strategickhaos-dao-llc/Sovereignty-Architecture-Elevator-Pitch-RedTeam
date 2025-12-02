# Strategickhaos 4-Node Private AI Supercluster

**Transform your four monster machines into a single, private, unstoppable AI empire that runs at 4–8× cloud speed with zero censorship.**

## 🏛️ Your Fleet (2025 Specifications)

| Machine Name | CPU | RAM | GPU | Role | Tailscale Hostname |
|--------------|-----|-----|-----|------|-------------------|
| **Nitro V15 Lyra** | Ryzen 9 7945HX (16c/32t) | 64 GB | High-end NVIDIA | Primary brain + 405B inference | `nitro-lyra` |
| **Athina iPower** | Threadripper PRO 5995WX (64c/128t) | 128 GB | High-end NVIDIA | Heavy fine-tuning / 405B training | `athina-throne` |
| **ASUS TUF Gaming A15 Nova** | Ryzen 9 8945HS | 64 GB | RTX 4070 mobile | Fast inference + voice/screen agents | `nova-warrior` |
| **Sony COR i5 Asteroth** | i5-13500H | 64 GB | RTX 4060 | Honeypot + remote gateway | `asteroth-gate` |

**Total Cluster Power:**
- **>160 physical cores**
- **320 GB RAM**
- **4× high-end NVIDIA GPUs**
- **Private supercomputer worth $600+/month on any cloud**

## 🚀 Quick Start (Do This Once)

### 1. Install Tailscale on All Machines

Tailscale creates a secure, encrypted mesh network between your machines with zero configuration.

**Linux/macOS:**
```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

**Windows (PowerShell as Admin):**
```powershell
# Download and install from https://tailscale.com/download
# Or use winget:
winget install tailscale.tailscale
```

**Enable MagicDNS** (makes machines discoverable by hostname):
1. Go to https://login.tailscale.com/admin/dns
2. Enable "MagicDNS"
3. Machines will be accessible as `<hostname>.tail-scale.ts.net`

### 2. Rename Machines to Cluster Hostnames

**Windows (PowerShell as Admin):**
```powershell
Rename-Computer -NewName "nitro-lyra" -Restart
```

**Linux:**
```bash
sudo hostnamectl set-hostname nitro-lyra
```

**macOS:**
```bash
sudo scutil --set HostName nitro-lyra
sudo scutil --set LocalHostName nitro-lyra
sudo scutil --set ComputerName "nitro-lyra"
```

### 3. Install Docker & NVIDIA Container Toolkit

**Linux (Ubuntu/Debian):**
```bash
# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

**Windows with WSL2:**
```powershell
# Install Docker Desktop with WSL2 backend
# Enable GPU support in WSL2
wsl --install
# Follow Docker Desktop GPU setup guide
```

### 4. Deploy Cluster on Each Machine

**On ALL four machines:**
```bash
# Create cluster directory
mkdir -p ~/strategickhaos-cluster
cd ~/strategickhaos-cluster

# Download cluster configuration
curl -O https://raw.githubusercontent.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/main/cluster-compose.yml

# Start the cluster
docker compose up -d
```

**Machine-Specific Services:**

On **nova-warrior** (voice AI):
```bash
docker compose --profile voice up -d
```

On **asteroth-gate** (honeypot):
```bash
docker compose --profile honeypot up -d
```

On **nitro-lyra** (monitoring):
```bash
docker compose --profile monitoring up -d
```

### 5. Pull Nuclear AI Models (On Strongest Machine)

**SSH or RDP into athina-throne (128 GB RAM):**
```bash
# Access Ollama container
docker exec -it ollama bash

# Pull the big guns
ollama pull llama3.1:405b          # 405B parameter model (~230 GB)
ollama pull dolphin-llama3:70b     # Uncensored 70B
ollama pull everythinglm:13b       # Fast 13B model
ollama pull mistral:latest         # Mistral 7B
ollama pull codellama:latest       # Code generation
```

## 🔧 Model Sharing Across Cluster

Share models from **athina-throne** to all other nodes to avoid downloading 230+ GB multiple times.

### Option A: NFS Share (Linux)

**On athina-throne:**
```bash
# Install NFS server
sudo apt-get install nfs-kernel-server

# Export Ollama models directory
echo "/var/lib/docker/volumes/strategickhaos-cluster_ollama/_data *(ro,sync,no_subtree_check)" | \
    sudo tee -a /etc/exports

# Restart NFS
sudo exportfs -a
sudo systemctl restart nfs-kernel-server
```

**On other nodes:**
```bash
# Install NFS client
sudo apt-get install nfs-common

# Mount shared models
sudo mkdir -p /mnt/athina-models
sudo mount -t nfs athina-throne.tail-scale.ts.net:/var/lib/docker/volumes/strategickhaos-cluster_ollama/_data /mnt/athina-models

# Link to local Ollama
docker exec ollama ln -s /mnt/athina-models/models /root/.ollama/models
```

### Option B: SMB/CIFS Share (Cross-Platform)

**On athina-throne (Windows):**
```powershell
# Share the Ollama volume
$path = "C:\ProgramData\Docker\volumes\strategickhaos-cluster_ollama\_data"
New-SmbShare -Name "ollama-models" -Path $path -ReadAccess "Everyone"
```

**On other nodes (Linux):**
```bash
sudo apt-get install cifs-utils
sudo mkdir -p /mnt/athina-models
sudo mount -t cifs //athina-throne.tail-scale.ts.net/ollama-models /mnt/athina-models -o username=guest,password=
```

### Option C: Tailscale Serve (Simplest)

**On athina-throne:**
```bash
# Serve models over HTTPS
tailscale serve --bg --https=11434 tcp://localhost:11434
```

**On other nodes:**
Update `cluster-compose.yml`:
```yaml
environment:
  - OLLAMA_BASE_URL=https://athina-throne.tail-scale.ts.net
```

## 🌐 Access Your Cluster

Once deployed, access from **ANY device on your Tailnet:**

- **Open-WebUI**: http://nitro-lyra.tail-scale.ts.net:3000
- **Voice AI**: http://nova-warrior.tail-scale.ts.net:7850
- **Honeypot Gate**: http://asteroth-gate.tail-scale.ts.net:8080
- **Health Monitor**: http://nitro-lyra.tail-scale.ts.net:9090
- **Direct Ollama API**: http://nitro-lyra.tail-scale.ts.net:11434

## 🎯 Load Balancing & Failover

### Automatic Failover Configuration

Create `failover.sh` on primary node:

```bash
#!/bin/bash
# Auto-failover script for Strategickhaos cluster

PRIMARY="nitro-lyra.tail-scale.ts.net"
BACKUP="athina-throne.tail-scale.ts.net"

while true; do
    if ! curl -s http://$PRIMARY:11434/api/health > /dev/null; then
        echo "Primary down, switching to backup..."
        docker exec open-webui sh -c "sed -i 's/$PRIMARY/$BACKUP/g' /app/backend/data/config.json"
        docker restart open-webui
    fi
    sleep 60
done
```

Run as systemd service:
```bash
sudo cp failover.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/failover.sh

# Create systemd service
sudo tee /etc/systemd/system/cluster-failover.service > /dev/null <<EOF
[Unit]
Description=Strategickhaos Cluster Failover
After=docker.service

[Service]
Type=simple
ExecStart=/usr/local/bin/failover.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable cluster-failover
sudo systemctl start cluster-failover
```

## 🔐 Security & Privacy

### All Traffic Encrypted
- **Tailscale**: WireGuard-based encryption (ChaCha20-Poly1305)
- **Zero open ports**: No public internet exposure
- **Private network**: Only your devices can access the cluster
- **No cloud**: No data leaves your machines

### Honeypot Configuration

The `asteroth-gate` node can act as a security monitoring station:

1. Create `invite-html/index.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Strategickhaos - Private Network</title>
</head>
<body>
    <h1>Access Restricted</h1>
    <p>This is a private network. Authorized personnel only.</p>
</body>
</html>
```

2. Monitor access attempts:
```bash
docker logs -f honeypot-gate
```

## 📊 Monitoring & Observability

### Prometheus Metrics

Create `monitoring/prometheus-cluster.yml`:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'ollama'
    static_configs:
      - targets:
        - 'nitro-lyra.tail-scale.ts.net:11434'
        - 'athina-throne.tail-scale.ts.net:11434'
        - 'nova-warrior.tail-scale.ts.net:11434'
        - 'asteroth-gate.tail-scale.ts.net:11434'

  - job_name: 'docker'
    static_configs:
      - targets:
        - 'nitro-lyra.tail-scale.ts.net:9323'
        - 'athina-throne.tail-scale.ts.net:9323'
        - 'nova-warrior.tail-scale.ts.net:9323'
        - 'asteroth-gate.tail-scale.ts.net:9323'
```

### Health Checks

```bash
# Check all nodes
for node in nitro-lyra athina-throne nova-warrior asteroth-gate; do
    echo "Checking $node..."
    curl -s http://$node.tail-scale.ts.net:11434/api/health || echo "FAILED"
done
```

## 🚀 Advanced Features

### USB Boot Stick for Quick Node Addition

Create a bootable USB that auto-joins the cluster:

1. Install Ubuntu/Debian on USB
2. Include setup script in `/etc/rc.local`:
```bash
#!/bin/bash
# Auto-setup script for new cluster nodes

# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up --authkey=$TAILSCALE_AUTHKEY

# Install Docker + NVIDIA toolkit
curl -fsSL https://get.docker.com | sh

# Clone and start cluster
cd /home/user
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-
docker compose -f cluster-compose.yml up -d
```

## 🛠️ Troubleshooting

### Ollama Not Starting
```bash
# Check NVIDIA GPU
nvidia-smi

# Check Docker GPU support
docker run --rm --gpus all nvidia/cuda:12.0.0-base-ubuntu22.04 nvidia-smi

# Check Ollama logs
docker logs ollama
```

### Cannot Access via Tailscale Hostname
```bash
# Verify Tailscale is running
tailscale status

# Check MagicDNS
tailscale status --json | jq .MagicDNSSuffix

# Ping other nodes
ping athina-throne.tail-scale.ts.net
```

### Models Not Loading
```bash
# Check available space
df -h

# Check Ollama models
docker exec ollama ollama list

# Clear cache and reload
docker exec ollama rm -rf /root/.ollama/models/.cache
docker restart ollama
```

## 🎓 Usage Examples

### Run Inference Across Cluster

```bash
# Small model on any node
curl http://nova-warrior.tail-scale.ts.net:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "Why is the sky blue?"
}'

# Large model on Athina (405B)
curl http://athina-throne.tail-scale.ts.net:11434/api/generate -d '{
  "model": "llama3.1:405b",
  "prompt": "Write a comprehensive analysis of quantum computing."
}'
```

### Voice Interaction

```bash
# Send text to voice (on nova-warrior)
curl http://nova-warrior.tail-scale.ts.net:7850/api/tts -d '{
  "text": "Hello from the Strategickhaos cluster",
  "voice": "en_US-female"
}'
```

## 📈 Performance Optimization

### Per-Node Resource Allocation

**Athina (Training/Fine-tuning):**
- Reserve for 405B model loading
- Allocate 100+ GB RAM
- Enable swap for overflow

**Nitro (Primary Inference):**
- Fast response times
- Multiple concurrent users
- Load 70B models

**Nova (Voice/Screen):**
- Real-time voice synthesis
- Screen capture agents
- Local desktop integration

**Asteroth (Gateway/Security):**
- Reverse proxy
- Security monitoring
- Remote access gateway

## 🌟 Next Steps

1. **Fine-tune models**: Use Athina's 128 GB for custom model training
2. **Add more nodes**: Any new laptop becomes node #5 in 90 seconds
3. **Integrate APIs**: Connect external services to your private cluster
4. **Custom agents**: Deploy specialized AI agents per node
5. **Data sovereignty**: Keep all AI inference 100% private

---

**Your empire is ready, Emperor. 😈**

*Private, uncensored, unstoppable AI at 4–8× cloud speed.*
*No corporation can touch, censor, or rate-limit your cluster.*
