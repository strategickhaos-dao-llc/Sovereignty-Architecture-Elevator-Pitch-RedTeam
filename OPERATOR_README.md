# StrategicKhaos Operator v2.0 — UNKILLABLE

> "It didn't die. It just went to Valhalla."

A bulletproof PowerShell operator for managing the StrategicKhaos infrastructure with Ollama AI models and Kubernetes deployments.

## 🚀 Features

- **Ollama Management**: Start and monitor Ollama daemon on port 11434
- **Kubernetes Integration**: Deploy and manage Ollama pods in K8s
- **Discord Notifications**: Real-time alerts to Discord webhooks
- **Model Pulling**: Easy AI model deployment via Ollama
- **Nuclear Option**: Complete system teardown when needed
- **Combat-Ready Dashboard**: Retro ASCII art interface
- **Bulletproof Error Handling**: Continues operation under duress

## 📋 Prerequisites

- PowerShell 5.1+ (Windows) or PowerShell Core 7+ (cross-platform)
- Ollama installed and in PATH
- kubectl configured (optional, for K8s features)
- Git (optional, for status reporting)

## 🎯 Quick Start

### Display Dashboard
```powershell
.\operator.ps1 -dashboard
```

### Start Full System
```powershell
.\operator.ps1 -start
```

This will:
1. Display the operator dashboard
2. Start Ollama daemon if not running
3. Apply Kubernetes manifests (if kubectl available)
4. Wait for pods to be ready
5. Send success notification to Discord

### Check Status
```powershell
.\operator.ps1 -status
```

Shows:
- Ollama daemon status (port 11434)
- Kubernetes pod status
- Installed Ollama models
- Current Git branch

### Pull AI Model
```powershell
.\operator.ps1 -pull llama2
.\operator.ps1 -pull mistral
.\operator.ps1 -pull codellama
```

Downloads and installs the specified Ollama model locally.

### Nuclear Option (Teardown)
```powershell
.\operator.ps1 -nuke
```

⚠️ WARNING: This will:
- Delete all K8s deployments
- Stop all Ollama processes
- Send notification to Discord

### Debug Mode
```powershell
.\operator.ps1 -start -debug
```

Enables verbose logging for troubleshooting.

## 🔧 Configuration

### Discord Webhook

Edit `discord/webhook_config.json`:
```json
{
  "url": "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN",
  "description": "Discord webhook for StrategicKhaos Operator notifications"
}
```

Get your webhook URL from Discord:
1. Server Settings → Integrations → Webhooks
2. Create New Webhook
3. Copy Webhook URL

### Kubernetes Deployments

The operator uses manifests in `k8s/deployments/`. Default includes:
- `ollama-deployment.yaml` - Ollama AI backend with 10Gi storage

Add custom deployments by placing YAML files in this directory.

## 📊 Status Indicators

| Indicator | Meaning |
|-----------|---------|
| `[RUNNING]` | Service is active and responding |
| `[DOWN]` | Service is not responding |
| `N/A` | Service not installed or not configured |

## 🎨 Dashboard

The operator displays a retro-styled ASCII art dashboard:

```
╔══════════════════════════════════════════════════════════════╗
║           STRATEGICKHAOS OPERATOR v2.0 — ARMORED             ║
║               23 NOV 2025 — COMBAT READY                     ║
╚══════════════════════════════════════════════════════════════╝

   ██████╗ ██████╗ ███████╗██████╗  █████╗ ████████╗ ██████╗ ██████╗ 
  ██╔═══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
  ██║   ██║██████╔╝█████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝
  ██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗
  ╚██████╔╝██║     ███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║
   ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
```

## 🛡️ Error Handling

The operator uses "survival settings":
```powershell
$ErrorActionPreference = "Continue"  # Keep going despite errors
$ProgressPreference = "SilentlyContinue"  # Silent progress bars
```

Errors are logged but don't stop execution unless fatal.

## 📝 Logging

Log format: `[HH:mm:ss] message`

Colors:
- 🟢 Green: Success operations
- 🔵 Cyan: Informational logs
- 🟡 Yellow: Warnings
- 🔴 Red: Errors
- ⚪ White: General logs

## 🔍 Troubleshooting

### Ollama won't start
```powershell
# Check if Ollama is installed
ollama --version

# Try starting manually
ollama serve
```

### Kubernetes errors
```powershell
# Verify kubectl
kubectl version

# Check cluster connectivity
kubectl cluster-info

# View logs
kubectl logs -l app=ollama
```

### Discord notifications not working
1. Verify webhook URL in `discord/webhook_config.json`
2. Test webhook with curl or Postman
3. Check Discord server permissions

## 🎯 Use Cases

### Daily Operations
```powershell
# Morning startup
.\operator.ps1 -start

# Check health throughout day
.\operator.ps1 -status

# Deploy new model
.\operator.ps1 -pull llama3

# Evening shutdown
.\operator.ps1 -nuke
```

### CI/CD Integration
```powershell
# In your pipeline
pwsh -File operator.ps1 -start -debug
# Run tests...
pwsh -File operator.ps1 -status
pwsh -File operator.ps1 -nuke
```

## 🚨 Security Notes

- Discord webhook URLs contain secrets - keep `webhook_config.json` private
- Add to `.gitignore` if webhook URL is sensitive
- Use Kubernetes secrets for production deployments
- The operator runs with current user permissions

## 📦 File Structure

```
.
├── operator.ps1                    # Main operator script
├── OPERATOR_README.md              # This file
├── discord/
│   └── webhook_config.json         # Discord webhook configuration
└── k8s/
    └── deployments/
        └── ollama-deployment.yaml  # Ollama K8s manifest
```

## 🤝 Contributing

To extend the operator:
1. Add new switch parameters to the `param()` block
2. Implement functionality in a new `elseif` block
3. Update this README with usage examples
4. Test thoroughly before committing

## 📄 License

Part of the StrategicKhaos Sovereignty Architecture project.

---

**Built with ⚡ by StrategicKhaos**  
*"It didn't die. It just went to Valhalla."*
