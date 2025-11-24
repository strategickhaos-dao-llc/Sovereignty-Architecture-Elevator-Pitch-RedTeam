# Grok-Merge Flux Codex v1.1 - Entangled Edition

## Overview
The Grok-Merge Flux Codex script automates the merging and deployment of the Flux Convergence 2025 analysis into the Sovereignty Architecture repository. This PowerShell script handles documentation generation, git operations, and optional Discord notifications with robust error handling.

## Features
- **Survival Settings**: Continues on errors with comprehensive logging
- **Auto-directory Creation**: Creates `docs/` directory if missing
- **Git Integration**: Automatic add, commit, and push with safeguards
- **Discord Notifications**: Optional webhook notifications via `-feed` flag
- **Error Recovery**: Try-catch armor protects against common failure scenarios

## Usage

### Basic Merge (Local Only)
```powershell
./grok-merge.ps1
```
This will:
1. Create/update `docs/flux-convergence-2025.md` with the codex content
2. Add and commit changes to git
3. Attempt to push to origin (warns if fails)

### Merge with Discord Notification
```powershell
./grok-merge.ps1 -feed
```
Same as basic merge, but also sends a notification to Discord if webhook is configured.

## Configuration

### Discord Webhook Setup
1. Edit `discord/webhook_config.json`
2. Add your Discord webhook URL
3. Set `enabled` to `true`

Example:
```json
{
  "url": "https://discord.com/api/webhooks/your-webhook-url",
  "enabled": true,
  "description": "Discord webhook configuration for Grok-Merge Flux Codex notifications"
}
```

## Requirements
- PowerShell 5.1+ or PowerShell Core 7+
- Git (optional, for version control)
- Discord webhook (optional, for notifications)

## Output
The script generates:
- `docs/flux-convergence-2025.md` - The complete Flux Convergence codex
- Console logs with timestamps and color-coded messages
- Git commits with message: "Grok-Merge Flux Codex v1.1 | Entangled analysis: Skeleton to flesh"

## Error Handling
The script includes armor against:
- Missing directories (auto-creates)
- Git not installed (warns and continues)
- Network failures (push warnings, Discord fallback)
- Invalid Discord config (graceful degradation)
- Path resolution issues
- Encoding problems

## Logs
All operations are logged with:
- `[HH:mm:ss]` timestamps
- Color-coded severity (Green=success, Yellow=warning, Red=error, Cyan=info)
- Detailed error messages in catch blocks

## Architecture
The script implements the Flux Convergence 2025 framework, which synthesizes:
1. **IPv4/IPv6 Network Evolution** - Protocol entanglement strategies
2. **AI LoRA Personalization** - Sovereign genome training
3. **Hardware Flux Automation** - PCB routing and edge cluster integration
4. **GitOps Declarative Operations** - Flux CD for K8s clusters
5. **Copilot Swarm Integration** - Autonomous merge and deployment

## Version History
- **v1.1 (Entangled Edition)** - Enhanced survival features, Discord integration, comprehensive error handling

## Support
For issues or questions, refer to the main repository documentation or the problem statement in the related GitHub issue.
