# StrategicKhaos Operator - Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Step 1: Prerequisites

```powershell
# Install Ollama (required)
# Download from: https://ollama.ai
# Or with winget:
winget install Ollama.Ollama

# Install kubectl (optional, for Kubernetes support)
# Download from: https://kubernetes.io/docs/tasks/tools/
```

### Step 2: Configure Discord (Optional)

```powershell
# Copy the example webhook config
cd discord
copy webhook_config.json.example webhook_config.json

# Edit webhook_config.json and add your Discord webhook URL
# Get webhook URL from: Discord Server → Settings → Integrations → Webhooks
notepad webhook_config.json
```

### Step 3: View the Dashboard

```powershell
# See the glorious PREPACK + NONPROFIT ASCII art
.\StrategicKhaos-Operator.ps1 -dashboard
```

### Step 4: Start Services

```powershell
# Launch Ollama daemon
.\StrategicKhaos-Operator.ps1 -start
```

### Step 5: Press the RED BUTTON 🔴

```powershell
# Deploy ALL nonprofit AI models (this will take a while - ~65GB download)
.\StrategicKhaos-Operator.ps1 -feed
```

**⏳ This will download 10 models. Go make coffee. Feed the world. You got this.**

---

## Common Commands

```powershell
# View dashboard
.\StrategicKhaos-Operator.ps1 -dashboard

# Start Ollama + K8s
.\StrategicKhaos-Operator.ps1 -start

# Check status
.\StrategicKhaos-Operator.ps1 -status

# Pull single model
.\StrategicKhaos-Operator.ps1 -pull "llama3.2:latest"

# Emergency shutdown
.\StrategicKhaos-Operator.ps1 -nuke

# THE RED BUTTON - Deploy all nonprofit models
.\StrategicKhaos-Operator.ps1 -feed
```

---

## Customize Your Model List

Edit `models_config.json` to add/remove models:

```json
{
  "models": [
    {
      "name": "llama3.2:latest",
      "description": "Your custom model description"
    }
  ]
}
```

---

## Kubernetes Deployment (Advanced)

If you want to deploy the full K8s stack:

1. Configure your cluster:
   ```bash
   kubectl config use-context your-cluster
   ```

2. Update K8s manifests:
   ```bash
   cd k8s
   # Edit secrets.yaml - replace all "REPLACE_WITH_" values
   # Edit configmap.yaml - add your Discord Guild ID and Bot App ID
   # Edit ingress.yaml - replace domain with yours
   ```

3. Deploy:
   ```powershell
   .\StrategicKhaos-Operator.ps1 -start
   ```

See `k8s/README.md` for detailed Kubernetes configuration.

---

## Troubleshooting

### "Ollama command not found"
Install Ollama from https://ollama.ai

### "Port 11434 already in use"
Another Ollama instance is running. Use `-nuke` to stop all instances.

### "Discord webhook failed"
Check your `discord/webhook_config.json` configuration. Notifications are optional.

### Models downloading slowly
This is normal. Large models (20GB+) take time. The operator will wait and show progress.

---

## What Happens When You Press the RED BUTTON?

The `-feed` flag does this:

1. 🔴 Screen goes blood red with nonprofit manifesto
2. 📊 Dashboard displays with full glory
3. 📥 Downloads these 10 essential models:
   - **llama3.2:latest** (~2GB) - General purpose
   - **phi3:medium** (~8GB) - Fast inference
   - **gemma2:27b** (~16GB) - High quality
   - **qwen2.5:32b** (~19GB) - Multilingual
   - **mistral-nemo** (~7GB) - Balanced
   - **openhermes2.5** (~4GB) - Instructions
   - **dolphin-llama3.2** (~2GB) - Research
   - **medic-llama3** (~4GB) - Healthcare
   - **llava** (~5GB) - Vision + language
   - **nomic-embed-text** (~274MB) - Embeddings
4. 🔔 Sends Discord notifications for each deployment
5. ✅ Victory message: "They weren't ready. We are."

**Total download: ~65GB**

---

## Production Deployment Checklist

- [ ] Replace Discord webhook URL in `discord/webhook_config.json`
- [ ] Replace K8s secrets in `k8s/secrets.yaml`
- [ ] Update Discord IDs in `k8s/configmap.yaml`
- [ ] Replace domain in `k8s/ingress.yaml`
- [ ] Use specific image tags instead of `latest` in deployments
- [ ] Set up external secret management (Vault/Sealed Secrets)
- [ ] Configure TLS certificates (cert-manager)
- [ ] Test `-start` in dev environment first
- [ ] Press RED BUTTON `-feed` to deploy models
- [ ] Monitor Discord notifications

---

## Need Help?

- **Full Documentation**: See `STRATEGICKHAOS_OPERATOR_README.md`
- **K8s Setup**: See `k8s/README.md`
- **Security Guide**: See `SECURITY.md`

---

**You absolute legend.**

**You didn't just install software — you deployed a nonprofit AI revolution.**

**The world is now being fed. 🌍**
