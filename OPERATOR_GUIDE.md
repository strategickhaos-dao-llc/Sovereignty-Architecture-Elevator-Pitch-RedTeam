# StrategicKhaos Operator v3.1 — Final Sanctified Edition

**"Feed the world. One prompt at a time."**

## Overview

The StrategicKhaos Operator is a PowerShell-based control system for deploying and managing AI models through Ollama, with Discord integration for notifications and Kubernetes orchestration support.

## Prerequisites

- **Windows PowerShell** 5.1 or PowerShell Core 7+
- **Ollama** installed and accessible in PATH
- **kubectl** (optional, for Kubernetes integration)
- **Discord Webhook** (optional, for notifications)

## Quick Start

```powershell
# Just look at it
.\StrategicKhaos-Operator.ps1 -dashboard

# Normal bring-up
.\StrategicKhaos-Operator.ps1 -start

# THE FINAL FORM
.\StrategicKhaos-Operator.ps1 -feed
```

## Commands

### `-dashboard`
Displays the operator dashboard with system status.

```powershell
.\StrategicKhaos-Operator.ps1 -dashboard
```

### `-start`
Launches the full stack:
- Starts Ollama daemon if not running
- Applies Kubernetes manifests (if kubectl is available)
- Sends startup notification to Discord

```powershell
.\StrategicKhaos-Operator.ps1 -start
```

### `-status`
Shows the current status of the system, including Ollama daemon status.

```powershell
.\StrategicKhaos-Operator.ps1 -status
```

### `-pull <model>`
Pulls a specific model from Ollama registry.

```powershell
.\StrategicKhaos-Operator.ps1 -pull llama3.2:latest
```

### `-nuke`
Emergency shutdown - kills all Ollama processes and removes Kubernetes resources.

```powershell
.\StrategicKhaos-Operator.ps1 -nuke
```

### `-feed` (THE RED BUTTON)
Activates **NONPROFIT MODE** - deploys all essential open-source AI models:
- llama3.2:latest
- phi3:medium
- gemma2:27b
- qwen2.5:32b
- mistral-nemo
- openhermes2.5
- dolphin-llama3.2
- medic-llama3
- llava
- nomic-embed-text

```powershell
.\StrategicKhaos-Operator.ps1 -feed
```

**Warning**: This will download multiple large AI models. Ensure you have sufficient disk space and bandwidth.

## Configuration

### Discord Integration

1. Create a Discord webhook in your server
2. Edit `discord/webhook_config.json`:

```json
{
  "url": "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN",
  "description": "Replace with your actual Discord webhook URL"
}
```

### Kubernetes Configuration

Place your Kubernetes manifests in the `k8s/` directory. The operator will automatically apply them when using `-start`.

## Features

### Logging
- Timestamped log messages with color coding
- Success (Green), Error (Red), Warning (Yellow), Info (Cyan/Gray)

### Port Testing
- Automatic detection of Ollama daemon on port 11434
- Connection verification before operations

### Discord Notifications
- Model deployment notifications
- System status updates
- Error and warning alerts

### Error Handling
- Graceful error handling with detailed messages
- Discord notification on errors
- System continues operation after recoverable errors

## Architecture

```
StrategicKhaos-Operator.ps1
├── Core Config
│   └── Color schemes, root path
├── Helper Functions
│   ├── Log/Log-Success/Log-Error/Log-Warn
│   ├── Test-Command (check if command exists)
│   ├── Test-Port (check if port is open)
│   └── Notify-Discord (send notifications)
├── Dashboard
│   └── Show-Dashboard (ASCII art display)
├── THE RED BUTTON
│   └── -feed mode (deploy all models)
└── Standard Commands
    ├── -dashboard
    ├── -start
    ├── -status
    ├── -pull
    └── -nuke
```

## Nonprofit Mission

This script embodies the nonprofit mission of democratizing AI:
- **No ads** - Clean, focused operation
- **No paywalls** - All features available to everyone
- **No masters** - Open source, community-driven
- **Feed the world** - Making AI accessible to all 8 billion humans

## Troubleshooting

### Ollama not found
Ensure Ollama is installed and in your system PATH:
```powershell
ollama --version
```

### Port 11434 already in use
Check if Ollama is already running:
```powershell
Get-Process ollama
```

### Discord notifications not working
1. Verify webhook URL in `discord/webhook_config.json`
2. Test the webhook manually
3. Check network connectivity

### kubectl commands failing
Ensure kubectl is installed and configured:
```powershell
kubectl version --client
kubectl config current-context
```

## Security Considerations

- Discord webhook URLs contain sensitive tokens - keep `webhook_config.json` secure
- The `-nuke` command forcefully terminates processes - use with caution
- Kubernetes operations require appropriate cluster permissions

## Contributing

This is now officially the most battle-tested, copy-paste-perfect, nonprofit war-machine launcher in human history. Built by two lunatics who refused to lose.

**They ain't ready, bro. But we are.**

Now press the red button. Let's feed the world.
