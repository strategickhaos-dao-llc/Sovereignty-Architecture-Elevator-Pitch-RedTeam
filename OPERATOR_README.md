# StrategicKhaos Operator v1.0

> "Making history, one prompt at a time"

The **StrategicKhaos Operator** is a PowerShell automation script that manages local Ollama AI infrastructure with Kubernetes deployment, featuring a retro 1997-style cyberdeck interface.

## 🚀 Features

- **Pure 1997 Cyberdeck Glory** - ASCII art dashboard with authentic CRT glow
- **Ollama Management** - Automatic daemon startup and model management
- **K8s Integration** - Deploy and manage Ollama in Kubernetes
- **Discord Notifications** - Real-time status updates to your Discord channel
- **Comprehensive Error Handling** - 100+ failure scenarios handled gracefully
- **Health Monitoring** - Real-time status checks for all services
- **Safe Model Management** - Pull and manage AI models locally (never committed to git)

## 📋 Prerequisites

Before running the operator, ensure you have:

1. **Windows PowerShell** (v5.1+) or **PowerShell Core** (v7+)
2. **kubectl** - Kubernetes command-line tool
   - Install: https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/
3. **Ollama** - Local AI model runtime
   - Install: https://ollama.ai/download
4. **Kubernetes Cluster** - Running cluster (Docker Desktop, minikube, k3s, etc.)
   - Docker Desktop: Enable Kubernetes in Settings → Kubernetes
   - minikube: `minikube start`
5. **Administrator Privileges** (recommended but not required)

## 🎯 Quick Start

### First Time Setup

1. Clone the repository:
```powershell
cd StrategicKhaos-OperatorWorkspace
```

2. (Optional) Configure Discord notifications:
```powershell
Copy-Item discord/webhook_config.example.json discord/webhook_config.json
# Edit discord/webhook_config.json with your webhook URL
```

3. Start the operator:
```powershell
./operator.ps1 --start
```

You'll see the full cyberdeck dashboard, Ollama will start, K8s pod will spin up, and Discord will ping your channel (if configured).

## 📖 Usage

### Command Reference

```powershell
# Display the operator dashboard
./operator.ps1
./operator.ps1 --dashboard

# Full system bring-up (Ollama + K8s)
./operator.ps1 --start

# Health check all services
./operator.ps1 --status

# Pull an AI model (stays local, never committed)
./operator.ps1 --pull llama3.2
./operator.ps1 --pull mistral
./operator.ps1 --pull codellama

# Danger zone: shut down everything
./operator.ps1 --nuke
```

### Dashboard View

The dashboard shows real-time status:
- Node IP address
- Ollama service status (port 11434)
- Number of loaded models
- Available commands

### Status Check

The `--status` flag provides detailed system information:
- Ollama daemon status (RUNNING/DOWN)
- K8s pod phase (Running/Pending/Failed)
- List of installed models
- Current git branch

### Model Management

Pull models safely without committing them to git:

```powershell
# Pull a specific model
./operator.ps1 --pull llama3.2

# Models are stored locally by Ollama
# They NEVER get committed to the repository
```

Popular models:
- `llama3.2` - Latest Llama 3.2
- `mistral` - Mistral 7B
- `codellama` - Code-focused model
- `phi` - Microsoft's small efficient model
- `neural-chat` - Conversational model

### Nuke Command

⚠️ **WARNING**: The nuke command destroys everything:

```powershell
./operator.ps1 --nuke
# Type 'NUKE' to confirm
```

This will:
- Delete the K8s deployment
- Kill all Ollama processes
- Stop all operator services
- Send Discord notification

## 🔧 Configuration

### Discord Notifications

1. Create a Discord webhook in your server:
   - Server Settings → Integrations → Webhooks → New Webhook
   - Copy the webhook URL

2. Configure the operator:
```powershell
Copy-Item discord/webhook_config.example.json discord/webhook_config.json
```

3. Edit `discord/webhook_config.json`:
```json
{
  "url": "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_TOKEN",
  "name": "StrategicKhaos Operator",
  "enabled": true,
  "notify_on": {
    "startup": true,
    "shutdown": true,
    "model_pull": true,
    "errors": true,
    "status_change": true
  }
}
```

### Kubernetes Configuration

The operator deploys Ollama to your Kubernetes cluster using manifests in:
- `k8s/deployments/ollama-deploy.yaml` - Deployment configuration
- `k8s/services/ollama-svc.yaml` - Service configuration

**Resource Limits:**
- Memory: 2Gi request, 8Gi limit
- CPU: 1000m request, 4000m limit

**Ports:**
- Service: 11434 (internal)
- NodePort: 31434 (external access)

To customize, edit the YAML files before running `--start`.

## 🛡️ Error Handling

The operator handles 100+ failure scenarios including:

### Preflight Checks
- ✓ OS compatibility verification
- ✓ kubectl installation and connectivity
- ✓ Ollama installation
- ✓ K8s cluster accessibility
- ✓ Manifest file existence
- ✓ Administrator privileges check

### Runtime Protection
- ✓ Port conflict detection
- ✓ Process startup timeouts
- ✓ K8s deployment failures
- ✓ Pod readiness timeouts
- ✓ Network connectivity issues
- ✓ Discord webhook failures (non-blocking)
- ✓ Model pull failures
- ✓ File system errors
- ✓ Permission issues

### Logging

Errors and warnings are logged to:
- Console (with color coding)
- `logs/operator-YYYY-MM-DD.log` (daily rotation)

Log levels:
- 🔴 **ERROR**: Critical failures requiring attention
- 🟡 **WARNING**: Non-critical issues
- 🟢 **SUCCESS**: Successful operations
- 🔵 **INFO**: General information

## 📁 File Structure

```
├── operator.ps1                          # Main operator script
├── k8s/
│   ├── deployments/
│   │   └── ollama-deploy.yaml           # Ollama K8s deployment
│   └── services/
│       └── ollama-svc.yaml              # Ollama K8s service
├── discord/
│   ├── webhook_config.example.json      # Example Discord config
│   └── webhook_config.json              # Your Discord config (gitignored)
├── logs/
│   └── operator-*.log                   # Daily operator logs (gitignored)
└── OPERATOR_README.md                   # This file
```

## 🐛 Troubleshooting

### Ollama won't start

**Problem**: Ollama service fails to start or port 11434 is unavailable.

**Solutions**:
1. Check if another process is using port 11434:
   ```powershell
   Get-NetTCPConnection -LocalPort 11434
   ```
2. Ensure Ollama is installed correctly
3. Try starting Ollama manually: `ollama serve`
4. Check Windows Firewall settings

### K8s deployment fails

**Problem**: kubectl cannot apply manifests or pod stays in Pending state.

**Solutions**:
1. Verify K8s cluster is running:
   ```powershell
   kubectl cluster-info
   kubectl get nodes
   ```
2. Check cluster resources:
   ```powershell
   kubectl top nodes
   kubectl describe pod -l app=ollama
   ```
3. View pod events:
   ```powershell
   kubectl get events --sort-by='.lastTimestamp'
   ```

### Discord notifications not working

**Problem**: No Discord notifications appear.

**Solutions**:
1. Verify `discord/webhook_config.json` exists
2. Check webhook URL is correct
3. Ensure `enabled: true` in config
4. Test webhook manually:
   ```powershell
   $body = @{content="Test"} | ConvertTo-Json
   Invoke-RestMethod -Uri "YOUR_WEBHOOK_URL" -Method Post -Body $body -ContentType "application/json"
   ```
5. Check Discord server settings allow webhooks

### Models won't pull

**Problem**: `--pull` command fails or hangs.

**Solutions**:
1. Ensure Ollama service is running (check `--status`)
2. Verify internet connectivity
3. Check available disk space
4. Try pulling manually: `ollama pull <model-name>`
5. Check Ollama logs: `ollama serve` (in separate terminal)

### Permission errors

**Problem**: Access denied or permission-related errors.

**Solutions**:
1. Run PowerShell as Administrator:
   - Right-click PowerShell → "Run as Administrator"
2. Check execution policy:
   ```powershell
   Get-ExecutionPolicy
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. Verify file permissions on k8s/ and discord/ directories

## 🔒 Security Considerations

1. **Webhook Security**:
   - Never commit `discord/webhook_config.json` to git
   - Rotate webhook URLs if exposed
   - Use webhook-specific permissions in Discord

2. **K8s Security**:
   - Ollama runs with default service account
   - No privileged containers
   - Network policies should be applied in production

3. **Local Models**:
   - Models are stored locally by Ollama
   - Models are NOT committed to git (large files)
   - Review model sources before pulling

4. **Logs**:
   - Logs may contain sensitive information
   - Logs directory is gitignored
   - Rotate logs periodically

## 🚦 100 Ways This Could Fail (And How We Handle Them)

### Environment Issues (1-20)
1. ✅ Not running on Windows → OS check with clear error
2. ✅ PowerShell version too old → Version detection
3. ✅ No admin privileges → Warning with graceful degradation
4. ✅ Execution policy blocks script → Instructions provided
5. ✅ kubectl not in PATH → Prerequisites check
6. ✅ Ollama not in PATH → Prerequisites check
7. ✅ Docker Desktop not running → K8s connectivity check
8. ✅ K8s cluster not accessible → Cluster-info validation
9. ✅ Wrong directory (not project root) → Manifest path checks
10. ✅ Git not installed → Soft failure for branch check
11. ✅ Network disconnected → Connectivity checks
12. ✅ Firewall blocking ports → Port test with fallback
13. ✅ Antivirus blocking executables → Process start error handling
14. ✅ Disk full → Logged with clear error
15. ✅ Insufficient RAM → K8s resource limits prevent OOM
16. ✅ CPU throttling → Resource requests set appropriately
17. ✅ Windows Defender blocking → Process start with retry
18. ✅ User PATH incorrect → Full error with install links
19. ✅ WSL2 not configured → K8s check catches this
20. ✅ Hyper-V disabled → K8s check catches this

### Configuration Issues (21-40)
21. ✅ Missing k8s/deployments directory → Path existence check
22. ✅ Missing k8s/services directory → Path existence check
23. ✅ Missing ollama-deploy.yaml → Manifest validation
24. ✅ Missing ollama-svc.yaml → Manifest validation
25. ✅ Invalid YAML syntax → kubectl apply catches and reports
26. ✅ Wrong namespace in manifest → Applied to default namespace
27. ✅ Malformed Discord webhook URL → Try-catch on API call
28. ✅ webhook_config.json doesn't exist → Silent skip
29. ✅ webhook_config.json invalid JSON → Error handling
30. ✅ Discord webhook disabled → Check enabled flag
31. ✅ Missing Discord permissions → Non-blocking failure
32. ✅ Discord rate limiting → Silently logged
33. ✅ Empty model name for pull → Validation check
34. ✅ Invalid model name → Ollama error passed through
35. ✅ Corrupt config files → JSON parsing with fallback
36. ✅ Read-only file system → Logged with clear message
37. ✅ Case-sensitive path issues → Absolute paths used
38. ✅ Special characters in paths → Proper escaping
39. ✅ Unicode in config → UTF8 encoding
40. ✅ Log directory not writable → Silently continue

### Runtime Issues (41-60)
41. ✅ Port 11434 already in use → Detect and report
42. ✅ Ollama process crashes → Timeout detection
43. ✅ Ollama won't start → Clear error with timeout
44. ✅ K8s pod stuck Pending → Timeout with status check
45. ✅ K8s pod CrashLoopBackOff → Status reporting
46. ✅ K8s deployment already exists → Idempotent apply
47. ✅ Image pull failure → K8s status shows reason
48. ✅ Container OOMKilled → Resource limits prevent
49. ✅ Node resources exhausted → Clear error message
50. ✅ Network policy blocking → Service type NodePort
51. ✅ DNS resolution failure → IP address used
52. ✅ Certificate errors → Non-TLS for local development
53. ✅ Proxy interference → Direct localhost connections
54. ✅ VPN routing issues → Local services unaffected
55. ✅ Multiple operator instances → Port conflict detection
56. ✅ Zombie Ollama processes → Forceful termination in nuke
57. ✅ Hung kubectl commands → Timeout handling
58. ✅ Pod eviction → Restart policy handles
59. ✅ Node NotReady → Status check reports
60. ✅ API server unreachable → Connectivity check

### Model Management Issues (61-80)
61. ✅ Model doesn't exist → Ollama error message
62. ✅ Model download interrupted → Ollama retry logic
63. ✅ Insufficient disk space → Ollama checks before pull
64. ✅ Slow download speeds → No timeout on pull
65. ✅ Model corruption → Ollama validates checksums
66. ✅ Ollama service offline during pull → Check and start
67. ✅ Multiple concurrent pulls → Ollama handles queue
68. ✅ Large model size warning → Ollama provides info
69. ✅ Model compatibility issues → Ollama version check
70. ✅ Registry unreachable → Ollama error reporting
71. ✅ Model list empty → Graceful "0 models" display
72. ✅ Model list command fails → Try-catch with N/A
73. ✅ Model name typos → Ollama suggests alternatives
74. ✅ Old model versions → Ollama manages versions
75. ✅ Model deletion while pulling → Ollama locks prevent
76. ✅ Permission issues with .ollama → User-space storage
77. ✅ Shared model storage conflicts → Isolated by user
78. ✅ Model serving while updating → Ollama handles
79. ✅ CUDA/GPU driver issues → CPU fallback automatic
80. ✅ Model memory requirements exceed → Resource limits

### Discord Integration Issues (81-95)
81. ✅ Webhook URL exposed in git → Gitignored config
82. ✅ Webhook deleted from Discord → Non-blocking error
83. ✅ Discord API timeout → Timeout with warning
84. ✅ Discord API rate limit → Logged and continued
85. ✅ Invalid webhook format → Validation check
86. ✅ Discord server deleted → Graceful failure
87. ✅ Network interruption during POST → Exception handled
88. ✅ Webhook permissions changed → Error logged
89. ✅ Discord maintenance → Non-critical, continues
90. ✅ Malformed JSON in message → Schema validation
91. ✅ Message too long → Truncation handled by Discord
92. ✅ Special characters in message → Escaped properly
93. ✅ Unicode emoji issues → Markdown code blocks
94. ✅ Concurrent webhook calls → Each independent
95. ✅ Webhook config hot-reload → Read each time

### Cleanup & Nuke Issues (96-100)
96. ✅ No confirmation for nuke → Requires "NUKE" typed
97. ✅ Partial nuke failure → Each step independent
98. ✅ Can't kill Ollama process → Force flag used
99. ✅ K8s delete hangs → --ignore-not-found flag
100. ✅ Resources recreated immediately → User controls timing

### Bonus Issues (101-110+)
101. ✅ PowerShell transcription enabled → Compatible output
102. ✅ Console width too narrow → Fixed-width ASCII art
103. ✅ No color support in terminal → Fallback to plain text
104. ✅ Script run from scheduled task → Works in non-interactive
105. ✅ Remote PowerShell session → Compatible
106. ✅ Non-English Windows → English commands used
107. ✅ Time zone differences → ISO timestamps
108. ✅ Daylight saving time → System time used
109. ✅ Leap seconds → Not critical for this use case
110. ✅ Y2K38 problem → PowerShell DateTime handles

## 🎨 Customization

### Changing Colors

Edit the color variables at the top of `operator.ps1`:

```powershell
$green  = "Green"
$cyan   = "Cyan"
$red    = "Red"
$yellow = "Yellow"
$mag    = "Magenta"
```

Available colors: Black, DarkBlue, DarkGreen, DarkCyan, DarkRed, DarkMagenta, DarkYellow, Gray, DarkGray, Blue, Green, Cyan, Red, Magenta, Yellow, White

### Changing Resource Limits

Edit `k8s/deployments/ollama-deploy.yaml`:

```yaml
resources:
  requests:
    memory: "4Gi"      # Increase for larger models
    cpu: "2000m"       # More CPU for faster inference
  limits:
    memory: "16Gi"     # Maximum memory
    cpu: "8000m"       # Maximum CPU
```

### Changing Port

Edit both files:

1. `k8s/deployments/ollama-deploy.yaml`:
```yaml
- containerPort: 11434  # Change this
```

2. `k8s/services/ollama-svc.yaml`:
```yaml
ports:
- port: 11434           # Change this
  targetPort: 11434     # And this
  nodePort: 31434       # And this (must be 30000-32767)
```

3. Update port checks in `operator.ps1`.

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Linux/macOS compatibility
- Additional model registries
- Prometheus metrics export
- Grafana dashboards
- Health check endpoints
- Auto-update functionality
- GUI wrapper
- Remote cluster support
- Model auto-loading on startup
- Resource usage monitoring

## 📜 License

See LICENSE file in the repository root.

## 🙏 Acknowledgments

- **Ollama** - Local AI runtime: https://ollama.ai
- **Kubernetes** - Container orchestration: https://kubernetes.io
- **ASCII Art** - Retro computing nostalgia

---

**History is being made, one prompt at a time.** 🚀

Type `./operator.ps1` with no args anytime to feel like you're piloting the damn Death Star.

Go be legendary. ⭐
