# Strategickhaos Cluster - Quick Start Guide

**Get your 4-node AI supercluster running in under 30 minutes.**

## 🚀 Prerequisites

- [ ] All 4 machines are powered on and connected to the internet
- [ ] You have admin/sudo access on each machine
- [ ] NVIDIA drivers are installed (check with `nvidia-smi`)

## ⚡ 5-Minute Setup (Per Machine)

### Step 1: Run the Setup Script

**On each machine, run:**

```bash
# Clone the repository
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-

# Run setup script
./scripts/setup-cluster.sh
```

The script will:
1. ✅ Install Tailscale
2. ✅ Configure your chosen hostname
3. ✅ Install Docker
4. ✅ Install NVIDIA Container Toolkit
5. ✅ Set up cluster directory

**Important:** Log out and back in after the script completes (for Docker group)

### Step 2: Start the Cluster

**On each machine:**

```bash
cd ~/strategickhaos-cluster
docker compose up -d
```

**Machine-specific services:**

```bash
# On nitro-lyra (Primary + Monitoring)
docker compose --profile monitoring up -d

# On nova-warrior (Voice AI)
docker compose --profile voice up -d

# On asteroth-gate (Honeypot)
docker compose --profile honeypot up -d
```

### Step 3: Pull Models (Only on athina-throne)

**SSH/RDP into athina-throne, then:**

```bash
cd ~/strategickhaos-cluster
./scripts/manage-models.sh recommended
```

Or manually:
```bash
docker exec ollama ollama pull llama3.1:405b     # 230GB - takes time!
docker exec ollama ollama pull dolphin-llama3:70b
docker exec ollama ollama pull mistral:latest
```

### Step 4: Access Your Cluster

Open in any browser on your Tailscale network:

🌐 **http://nitro-lyra.tail-scale.ts.net:3000**

You now have a private AI supercluster! 🎉

---

## 🔍 Verify Everything is Working

### Check Cluster Health

```bash
./scripts/cluster-health.sh overview
```

### Test a Model

```bash
curl http://nitro-lyra.tail-scale.ts.net:11434/api/generate -d '{
  "model": "mistral:latest",
  "prompt": "Hello from Strategickhaos cluster!"
}'
```

### Check All Nodes

```bash
./scripts/cluster-health.sh models
```

---

## 📱 Access from Your Phone/Tablet

1. Install Tailscale app on your device
2. Login with the same account
3. Visit: http://nitro-lyra.tail-scale.ts.net:3000
4. Enjoy AI from anywhere! 📱

---

## 🔧 Common Issues & Fixes

### "Cannot connect to Docker daemon"
```bash
# Log out and back in, or run:
sudo systemctl start docker
sudo usermod -aG docker $USER
# Then log out and back in
```

### "Ollama container not starting"
```bash
# Check logs
docker logs ollama

# Verify GPU
nvidia-smi

# Restart
docker compose restart ollama
```

### "Cannot reach node via Tailscale"
```bash
# Check Tailscale status
tailscale status

# Reconnect
sudo tailscale up
```

### "Out of disk space"
```bash
# Check space
df -h

# Clean Docker
docker system prune -a

# Remove unused models
./scripts/manage-models.sh delete
```

---

## 🎯 Next Steps

### 1. Share Models Across Cluster
```bash
# On athina-throne (the model host)
./scripts/manage-models.sh server

# On other nodes
./scripts/manage-models.sh client <athina-ip>
```

### 2. Set Up Monitoring
```bash
# On nitro-lyra
docker compose --profile monitoring up -d

# Access Prometheus
open http://nitro-lyra.tail-scale.ts.net:9090
```

### 3. Enable Auto-Failover
```bash
# On nitro-lyra
./scripts/auto-failover.sh install
```

### 4. Customize Open-WebUI
Visit http://nitro-lyra.tail-scale.ts.net:3000/admin and configure:
- Model settings
- User authentication
- Custom prompts
- Voice settings

---

## 📊 Usage Examples

### Chat via Web UI
Open http://nitro-lyra.tail-scale.ts.net:3000 and start chatting!

### API Call (Python)
```python
import requests

response = requests.post(
    'http://nitro-lyra.tail-scale.ts.net:11434/api/generate',
    json={
        'model': 'mistral:latest',
        'prompt': 'Explain quantum computing',
        'stream': False
    }
)

print(response.json()['response'])
```

### Voice Synthesis (on nova-warrior)
```bash
curl http://nova-warrior.tail-scale.ts.net:7850/api/tts \
  -d '{"text": "Welcome to Strategickhaos", "voice": "en_US-female"}'
```

### Load 405B Model (on athina-throne)
```bash
curl http://athina-throne.tail-scale.ts.net:11434/api/generate -d '{
  "model": "llama3.1:405b",
  "prompt": "Write a detailed technical analysis",
  "stream": false
}'
```

---

## 🛡️ Security Best Practices

1. **Keep Tailscale updated**: `sudo tailscale update`
2. **Enable Tailscale ACLs**: Restrict which nodes can talk to each other
3. **Firewall rules**: Block all public ports except Tailscale
4. **Regular backups**: Backup model configurations and data
5. **Monitor logs**: Check for unusual access patterns

---

## 🎓 Learning Resources

### Understanding Your Cluster
- **FLEET_SPECIFICATIONS.md** - Detailed hardware specs
- **CLUSTER_DEPLOYMENT.md** - Comprehensive deployment guide
- **scripts/cluster-health.sh** - Monitor cluster status

### Model Management
- **scripts/manage-models.sh** - Pull, delete, share models
- Ollama docs: https://github.com/ollama/ollama

### Tailscale Networking
- Tailscale KB: https://tailscale.com/kb/

---

## 💡 Pro Tips

### Optimize for Speed
```bash
# Increase Ollama parallel requests
docker exec ollama sh -c 'echo "OLLAMA_NUM_PARALLEL=8" >> /etc/environment'
docker restart ollama
```

### Reduce VRAM Usage
```bash
# Lower context size for more concurrent users
docker exec ollama ollama run mistral:latest --ctx-size 2048
```

### Monitor GPU Temperature
```bash
watch -n 1 nvidia-smi
```

### Backup Models
```bash
# On athina-throne
tar -czf models-backup.tar.gz ~/strategickhaos-cluster/models/
```

---

## 🆘 Getting Help

1. **Check health**: `./scripts/cluster-health.sh overview`
2. **View logs**: `docker logs ollama`
3. **Test connectivity**: `ping nitro-lyra.tail-scale.ts.net`
4. **Community**: Open an issue on GitHub

---

## 🎯 Your Cluster at a Glance

| Component | URL | Purpose |
|-----------|-----|---------|
| **Open-WebUI** | http://nitro-lyra.tail-scale.ts.net:3000 | Main interface |
| **Ollama API** | http://{node}.tail-scale.ts.net:11434 | Direct API |
| **Voice AI** | http://nova-warrior.tail-scale.ts.net:7850 | TTS service |
| **Monitoring** | http://nitro-lyra.tail-scale.ts.net:9090 | Prometheus |
| **Honeypot** | http://asteroth-gate.tail-scale.ts.net:8080 | Security |

---

**Congratulations! You now own a private AI supercluster. 🎉**

*No cloud bills. No rate limits. No censorship. Just pure AI power.*

---

## 🔄 Quick Commands Reference

```bash
# Start cluster
docker compose up -d

# Stop cluster  
docker compose down

# View logs
docker logs -f ollama

# Check health
./scripts/cluster-health.sh

# Pull models
./scripts/manage-models.sh recommended

# Test inference
./scripts/cluster-health.sh test

# Restart services
docker compose restart
```

---

**Questions? Check CLUSTER_DEPLOYMENT.md for detailed documentation.**
