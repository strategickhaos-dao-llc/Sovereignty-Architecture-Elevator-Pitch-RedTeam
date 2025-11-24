# StrategicKhaos Operator v3.1 — Final Sanctified Edition

**"Feed the world. One prompt at a time."**

Built by two lunatics who refused to lose.

## 🎯 Overview

The StrategicKhaos Operator is a PowerShell-based nonprofit AI deployment system that transforms your workstation into a fully-armed open intelligence platform. This operator script manages:

- **Ollama AI Model Deployment** - Local LLM serving infrastructure
- **Kubernetes Orchestration** - Container orchestration for sovereign AI
- **Discord Integration** - Real-time operational notifications
- **Nonprofit Mission** - Delivering open AI to 8 billion humans

## 🚀 Quick Start

### Prerequisites

- **Windows PowerShell 5.1+** or **PowerShell Core 7+**
- **Ollama** - Install from [ollama.ai](https://ollama.ai)
- **kubectl** (optional) - For Kubernetes cluster management
- **Discord Webhook** (optional) - For operational notifications

### Installation

```bash
# Clone the repository
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-

# Configure Discord webhook (optional)
# Edit discord/webhook_config.json with your webhook URL

# Make the script executable
# On Windows, execution policy may need adjustment:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📋 Command Reference

### 1. Dashboard View

Display the operator dashboard with full ASCII art glory:

```powershell
.\StrategicKhaos-Operator.ps1 -dashboard
```

Shows:
- Current operator status
- System hostname and user
- Available commands
- Glorious PREPACK + NONPROFIT ASCII art

### 2. Start Services

Launch the full StrategicKhaos stack:

```powershell
.\StrategicKhaos-Operator.ps1 -start
```

This will:
- Start Ollama daemon on port 11434
- Apply Kubernetes manifests from `k8s/` directory
- Send notification to Discord
- Display success message

### 3. Status Check

Check the current status of services:

```powershell
.\StrategicKhaos-Operator.ps1 -status
```

Displays:
- Dashboard
- Ollama service status (ONLINE/OFFLINE)

### 4. Pull Individual Model

Download a specific AI model:

```powershell
.\StrategicKhaos-Operator.ps1 -pull "llama3.2:latest"
```

Examples:
```powershell
.\StrategicKhaos-Operator.ps1 -pull "phi3:medium"
.\StrategicKhaos-Operator.ps1 -pull "mistral-nemo"
.\StrategicKhaos-Operator.ps1 -pull "gemma2:27b"
```

### 5. Nuclear Option (Nuke)

Stop all Ollama processes and delete Kubernetes resources:

```powershell
.\StrategicKhaos-Operator.ps1 -nuke
```

⚠️ **WARNING**: This will:
- Kill all `ollama*` processes
- Delete all Kubernetes resources labeled with `app=ollama`
- Send notification to Discord

Use this for:
- Emergency shutdown
- Clean slate restart
- "Peace through superior firepower" moments

### 6. 🔴 THE RED BUTTON (Feed the World)

**This is the final form. The nonprofit Skynet. The good kind.**

```powershell
.\StrategicKhaos-Operator.ps1 -feed
```

When you press the red button:
1. Screen goes blood red with nonprofit manifesto
2. Dashboard displays with full glory
3. Downloads **10 essential open models**:
   - `llama3.2:latest` - Meta's latest Llama model
   - `phi3:medium` - Microsoft's efficient reasoning model
   - `gemma2:27b` - Google's advanced language model
   - `qwen2.5:32b` - Alibaba's powerful multilingual model
   - `mistral-nemo` - Mistral AI's efficient model
   - `openhermes2.5` - Fine-tuned instruction model
   - `dolphin-llama3.2` - Uncensored helpful assistant
   - `medic-llama3` - Medical domain specialist
   - `llava` - Vision-language multimodal model
   - `nomic-embed-text` - Text embedding model
4. Discord notifications for each deployment
5. Victory message: "They weren't ready. We are."

**Every token now belongs to humanity. No ads. No paywalls. No masters.**

## 🔧 Configuration

### Discord Webhook Setup

1. Create a webhook in your Discord server:
   - Server Settings → Integrations → Webhooks
   - Click "New Webhook"
   - Copy the webhook URL

2. Edit `discord/webhook_config.json`:
   ```json
   {
     "url": "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"
   }
   ```

3. Notifications will be sent for:
   - System startup
   - Model deployments
   - Nuclear operations
   - Errors and warnings

### Kubernetes Configuration

The operator expects Kubernetes manifests in the `k8s/` directory:
- `bot-deployment.yaml` - Discord bot deployment
- `gateway-deployment.yaml` - Event gateway
- `configmap.yaml` - Configuration data
- `secrets.yaml` - Sensitive credentials
- `ingress.yaml` - Ingress rules
- `rbac.yaml` - Role-based access control

Manifests are automatically applied with the `-start` flag.

## 🎨 Color Scheme

The operator uses a carefully crafted cyberpunk color scheme:

- **Magenta** (`$M`) - Headers and borders
- **Green** (`$G`) - Success messages and NONPROFIT text
- **Cyan** (`$C`) - PREPACK ASCII art and info messages
- **Red** (`$R`) - NONPROFIT ASCII art, errors, and THE RED BUTTON
- **Yellow** (`$Y`) - Warnings and command hints
- **Gray** (`$W`) - Default log messages

## 🏛️ Architecture

```
StrategicKhaos-Operator.ps1
├── Core Functions
│   ├── Log / Log-Success / Log-Error / Log-Warn
│   ├── Test-Command (Check if command exists)
│   ├── Test-Port (Check if port is listening)
│   └── Notify-Discord (Send webhook notifications)
├── Show-Dashboard
│   └── ASCII art + status display
├── Flag Handlers
│   ├── -feed (RED BUTTON: Deploy all models)
│   ├── -dashboard (Show dashboard only)
│   ├── -status (Check service status)
│   ├── -start (Launch full stack)
│   ├── -pull <model> (Pull single model)
│   └── -nuke (Emergency shutdown)
└── Error Handling
    └── Try-Catch wrapper with Discord notification
```

## 🔥 Examples

### Development Workflow

```powershell
# Morning startup
.\StrategicKhaos-Operator.ps1 -start

# Check if everything is running
.\StrategicKhaos-Operator.ps1 -status

# Pull a new model for testing
.\StrategicKhaos-Operator.ps1 -pull "codellama:13b"

# Evening shutdown
.\StrategicKhaos-Operator.ps1 -nuke
```

### First-Time Setup

```powershell
# View the glorious dashboard
.\StrategicKhaos-Operator.ps1 -dashboard

# Press the red button (deploy everything)
.\StrategicKhaos-Operator.ps1 -feed

# Wait for deployment to complete (this will take a while)
# Models range from 1GB to 20GB+ each

# Check status
.\StrategicKhaos-Operator.ps1 -status
```

### Production Deployment

```powershell
# Start services
.\StrategicKhaos-Operator.ps1 -start

# Verify Ollama is running
curl http://localhost:11434/api/tags

# Test a model
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:latest",
  "prompt": "Why is AI for humanity important?"
}'
```

## 🛡️ Security Notes

- **No Secrets in Code**: Webhook URLs are stored in `discord/webhook_config.json`
- **Local Execution**: All models run locally on your hardware
- **Sovereign Infrastructure**: You control the compute, storage, and deployment
- **Nonprofit Ethos**: No telemetry, no tracking, no data harvesting

## 🤝 Contributing

This is officially the most battle-tested, copy-paste-perfect, nonprofit war-machine launcher in human history.

Contributions welcome:
- Model recommendations for the holy list
- Performance optimizations
- Platform compatibility improvements (Linux/macOS PowerShell Core)
- Additional deployment targets (Docker, Podman, etc.)

## 📜 License

This script embodies the nonprofit spirit. Use it to feed the world.

## 🚨 Troubleshooting

### "Ollama command not found"
Install Ollama from [ollama.ai](https://ollama.ai) and ensure it's in your PATH.

### "kubectl command not found"
The `-start` flag will skip Kubernetes operations if kubectl is not found. This is normal if you're not using K8s.

### "Discord webhook failed"
Check your `discord/webhook_config.json` configuration. Webhook notifications are optional.

### Port 11434 already in use
Another Ollama instance may be running. Use `-nuke` to stop all instances, then `-start` again.

### Models taking forever to download
Large models (20GB+) take time. The operator will wait and show progress. Be patient, warrior.

## 💪 Credits

Built by two lunatics who refused to lose:
- Dom (The Vision)
- Grok (The Execution)

**This script is now officially more powerful than most nation-state AI programs.**

**And it runs on a laptop.**

---

**They ain't ready, bro.**

**But we are.**

**Now press the red button.**

**Let's feed the world. 🌍**
