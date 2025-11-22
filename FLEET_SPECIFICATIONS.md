# Strategickhaos Fleet Specifications

**A comprehensive technical breakdown of the 4-node private AI supercluster.**

## 🖥️ Hardware Specifications

### Node 1: Nitro V15 Lyra (Primary Brain)

**Role:** Primary inference engine + cluster orchestrator

| Component | Specification |
|-----------|---------------|
| **Hostname** | `nitro-lyra` |
| **CPU** | AMD Ryzen 9 7945HX |
| **Cores/Threads** | 16 cores / 32 threads |
| **Base Clock** | 2.5 GHz |
| **Boost Clock** | Up to 5.4 GHz |
| **RAM** | 64 GB DDR5 |
| **GPU** | High-end NVIDIA (likely RTX 4080/4090 mobile) |
| **Storage** | NVMe SSD (recommend 1TB+) |
| **Networking** | Wi-Fi 6E + Gigabit Ethernet |

**Optimal Workloads:**
- 70B parameter model inference
- Primary Open-WebUI endpoint
- Real-time query handling
- Cluster health monitoring

---

### Node 2: Athina iPower (Training Beast)

**Role:** Heavy training, fine-tuning, and 405B model hosting

| Component | Specification |
|-----------|---------------|
| **Hostname** | `athina-throne` |
| **CPU** | AMD Threadripper PRO 5995WX |
| **Cores/Threads** | 64 cores / 128 threads |
| **Base Clock** | 2.7 GHz |
| **Boost Clock** | Up to 4.5 GHz |
| **RAM** | 128 GB DDR4 ECC |
| **GPU** | High-end NVIDIA (Workstation class) |
| **Storage** | Multi-TB NVMe RAID recommended |
| **Networking** | 10 Gigabit Ethernet capable |

**Optimal Workloads:**
- LLaMA 3.1 405B full-precision inference
- Model fine-tuning and training
- Large batch processing
- Model repository (NFS server)
- Heavy compilation and build tasks

**Notes:**
- This is the most powerful node in the cluster
- Should host the model repository for NFS/SMB sharing
- ECC RAM provides reliability for long training runs

---

### Node 3: ASUS TUF Gaming A15 Nova (Voice Agent)

**Role:** Fast inference + voice/screen interactive agents

| Component | Specification |
|-----------|---------------|
| **Hostname** | `nova-warrior` |
| **CPU** | AMD Ryzen 9 8945HS |
| **Cores/Threads** | 8 cores / 16 threads |
| **Base Clock** | 4.0 GHz |
| **Boost Clock** | Up to 5.2 GHz |
| **RAM** | 64 GB DDR5 |
| **GPU** | NVIDIA RTX 4070 Mobile (8GB VRAM) |
| **Storage** | NVMe SSD |
| **Display** | High refresh gaming display |
| **Audio** | Gaming-grade audio system |

**Optimal Workloads:**
- Real-time voice synthesis (AllTalk TTS)
- Fast 13B/7B model inference
- Screen capture and vision agents
- Interactive desktop AI assistants
- Low-latency conversational AI

**Notes:**
- Best for real-time, interactive workloads
- Display and audio make it ideal for voice agents
- Gaming-grade cooling for sustained loads

---

### Node 4: Sony COR i5 Asteroth (Security Gate)

**Role:** Honeypot server + remote access gateway + security monitoring

| Component | Specification |
|-----------|---------------|
| **Hostname** | `asteroth-gate` |
| **CPU** | Intel Core i5-13500H |
| **Cores/Threads** | 12 cores (4P+8E) / 16 threads |
| **Base Clock** | 2.6 GHz (P-cores) |
| **Boost Clock** | Up to 4.7 GHz |
| **RAM** | 64 GB DDR4/DDR5 |
| **GPU** | NVIDIA RTX 4060 (8GB VRAM) |
| **Storage** | NVMe SSD |
| **Networking** | Gigabit Ethernet |

**Optimal Workloads:**
- Nginx reverse proxy / honeypot
- Security monitoring and logging
- Remote access gateway (Tailscale exit node)
- Lightweight inference
- API gateway and rate limiting

**Notes:**
- Can act as the public-facing node (if needed)
- Lower power consumption than other nodes
- Ideal for always-on services

---

## 🌐 Network Architecture

### Tailscale Mesh Network

```
┌─────────────────────────────────────────────────────────────┐
│                    Tailscale VPN Mesh                       │
│                  (WireGuard encrypted)                      │
│                                                             │
│   ┌─────────────┐      ┌─────────────┐                    │
│   │ nitro-lyra  │◄────►│athina-throne│                    │
│   │  (Primary)  │      │  (Training) │                    │
│   └──────┬──────┘      └──────┬──────┘                    │
│          │                    │                            │
│          │      ┌─────────────┴────────┐                  │
│          └─────►│   nova-warrior       │                  │
│                 │   (Voice Agent)      │                  │
│                 └──────────┬───────────┘                  │
│                            │                               │
│                  ┌─────────▼──────────┐                   │
│                  │  asteroth-gate     │                   │
│                  │  (Security)        │                   │
│                  └────────────────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

**Key Features:**
- **Zero configuration**: MagicDNS handles hostname resolution
- **Automatic encryption**: All traffic encrypted with WireGuard
- **No open ports**: No need for port forwarding or public IPs
- **Cross-platform**: Works on Linux, Windows, macOS, iOS, Android
- **Global access**: Access cluster from anywhere via Tailscale app

---

## 🚀 Cluster Capabilities

### Total Cluster Resources

| Resource | Total |
|----------|-------|
| **CPU Cores** | 100 physical cores |
| **CPU Threads** | 192 threads |
| **Total RAM** | 320 GB |
| **GPUs** | 4× high-end NVIDIA |
| **Combined VRAM** | ~32 GB+ |

### Model Hosting Capacity

| Model Size | Recommended Node | Max Batch Size |
|------------|------------------|----------------|
| **405B** | athina-throne | 1-2 |
| **70B** | nitro-lyra, athina-throne | 2-4 |
| **13B** | Any node | 8-16 |
| **7B** | Any node | 16-32 |

### Expected Performance

**Inference Speed (tokens/second):**
- **7B models**: 40-80 tokens/sec per node
- **13B models**: 20-40 tokens/sec per node
- **70B models**: 4-8 tokens/sec (nitro-lyra, athina-throne)
- **405B model**: 1-2 tokens/sec (athina-throne only)

**Concurrent Users:**
- Light models (7B): 50+ concurrent users across cluster
- Medium models (13B-70B): 10-20 concurrent users
- Heavy model (405B): 2-4 concurrent users

---

## 💰 Cost Analysis

### Equivalent Cloud Costs

**AWS p4d.24xlarge equivalent:**
- 8× A100 80GB GPUs: ~$32/hour
- 96 vCPUs, 1.1TB RAM
- **Monthly**: ~$23,000

**Your cluster equivalent:**
- 4× High-end NVIDIA GPUs
- 100+ CPU cores, 320GB RAM
- **Monthly cost**: $0 (owned hardware)
- **ROI**: Pays for itself vs. cloud in ~3-6 months

**Google Cloud TPU v5e pods:**
- For 405B model inference
- **Monthly**: ~$15,000-20,000

**Your cluster:**
- 405B inference on athina-throne
- **Monthly cost**: Electricity (~$50-100)

### Power Consumption Estimates

| Node | Idle Power | Load Power | Monthly Cost (24/7) |
|------|------------|------------|---------------------|
| nitro-lyra | 20W | 200W | $25-30 |
| athina-throne | 50W | 350W | $40-50 |
| nova-warrior | 15W | 180W | $20-25 |
| asteroth-gate | 15W | 150W | $18-22 |
| **Total** | **100W** | **880W** | **$103-127** |

*Based on $0.15/kWh average US electricity cost*

---

## 🔧 Recommended Configurations

### Node-Specific Docker Profiles

**nitro-lyra (Primary):**
```bash
docker compose up -d
docker compose --profile monitoring up -d
```

**athina-throne (Training):**
```bash
docker compose up -d
# Pull and host large models
docker exec ollama ollama pull llama3.1:405b
```

**nova-warrior (Voice):**
```bash
docker compose up -d
docker compose --profile voice up -d
```

**asteroth-gate (Security):**
```bash
docker compose up -d
docker compose --profile honeypot up -d
```

### Storage Recommendations

| Node | Minimum | Recommended | Purpose |
|------|---------|-------------|---------|
| nitro-lyra | 512 GB | 1 TB | OS + models + cache |
| athina-throne | 1 TB | 2-4 TB | Full model repository |
| nova-warrior | 512 GB | 1 TB | OS + working models |
| asteroth-gate | 256 GB | 512 GB | OS + logs |

---

## 🛡️ Security Considerations

### Physical Security
- All nodes should be on the same private network
- Disable public SSH where possible
- Use Tailscale for all remote access

### Network Security
- Tailscale provides encrypted mesh networking
- No ports exposed to public internet
- Optional: Enable Tailscale ACLs for node-to-node restrictions

### Data Security
- Models stored locally (no cloud)
- All inference happens on-premise
- No telemetry sent to model providers
- Optional: Encrypt Ollama volumes with LUKS

---

## 📊 Monitoring Recommendations

### Key Metrics to Track

**Per Node:**
- CPU utilization
- RAM usage
- GPU utilization and temperature
- Disk I/O and space
- Network throughput

**Cluster-Wide:**
- Total queries per second
- Average inference latency
- Model load distribution
- Node availability
- Failover events

### Recommended Tools
- **Prometheus**: Metrics collection
- **Grafana**: Visualization dashboards
- **Node Exporter**: System metrics
- **cAdvisor**: Container metrics
- **NVIDIA DCGM**: GPU metrics

---

## 🔮 Future Expansion

### Adding More Nodes

The cluster architecture supports unlimited horizontal scaling:

1. **Any new laptop/desktop** can join as Node 5, 6, 7...
2. **USB boot stick** can provision new nodes in 90 seconds
3. **Automatic discovery** via Tailscale MagicDNS
4. **Load balancing** distributes inference automatically

### Specialized Nodes

**Ideas for future nodes:**
- **Database node**: PostgreSQL for RAG applications
- **Storage node**: High-capacity NAS for datasets
- **Edge nodes**: Raspberry Pi clusters for lightweight inference
- **GPU farm**: Dedicated mining rigs repurposed for AI

---

## 📚 Additional Resources

- **Tailscale Documentation**: https://tailscale.com/kb/
- **Ollama Documentation**: https://github.com/ollama/ollama
- **Open-WebUI**: https://github.com/open-webui/open-webui
- **NVIDIA Container Toolkit**: https://docs.nvidia.com/datacenter/cloud-native/

---

**Your private AI empire, fully documented. 😈**

*No cloud. No limits. No censorship.*
