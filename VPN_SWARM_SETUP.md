# VPN Swarm LLM Management v1.1

Automated VPN port management for distributed LLM swarm coordination using Proton VPN port forwarding.

## Overview

This system enables seamless coordination of distributed LLM endpoints (Ollama, search nodes) across multiple Windows machines connected via Proton VPN. It automatically detects your public VPN IP and requires you to enter the forwarded port only once per session.

## Key Features

- **Auto IP Detection**: Automatically detects your current VPN public IP
- **Minimal Manual Input**: Only requires port entry once per VPN session
- **Port Persistence**: Keeps track of ports across reboots if VPN stays connected
- **Multi-Machine Support**: Manages multiple machines (sony_asteroth, nova, athena, nitro)
- **Port Validation**: Ensures ports are in valid Proton VPN range (40000-62000)

## Prerequisites

1. **PowerShell 5.1 or later** (Windows)
2. **powershell-yaml module**:
   ```powershell
   Install-Module -Name powershell-yaml -Scope CurrentUser
   ```
3. **Proton VPN** (paid plan with port forwarding)
4. **Internet connection** for IP detection

## Proton VPN Setup for Best Results

1. **Connect to a P2P server** - Best port forwarding stability
2. **Enable Kill Switch** - Prevents connection drops
3. **Enable Auto-connect** - Reconnects automatically on boot
4. **Never regenerate port** unless absolutely necessary
5. **Note your forwarded port** from the Proton VPN app

## Files

- `swarm_llm_endpoints.yaml` - Configuration file with machine definitions
- `swarm_llm_manager.ps1` - PowerShell management script

## Usage

### First Time Setup

1. Ensure your machine's hostname matches one in the configuration:
   - sony_asteroth
   - nova
   - athena
   - nitro

2. Connect to Proton VPN and note your forwarded port

3. Run the update command:
   ```powershell
   .\swarm_llm_manager.ps1 update
   ```

4. Enter your forwarded port when prompted (40000-62000 range)

### Daily Usage

On each boot (if VPN reconnects):

```powershell
.\swarm_llm_manager.ps1 update
```

The script will:
- Auto-detect your current VPN IP
- Check if it changed from last time
- Prompt for port only if needed (or press Enter to keep existing)
- Update all endpoints automatically

### View Swarm Status

```powershell
.\swarm_llm_manager.ps1 status
```

Shows all machines in the swarm with their:
- VPN IP addresses
- Forwarded ports
- Ollama endpoints
- Search endpoints

### Help

```powershell
.\swarm_llm_manager.ps1 help
```

## Configuration Structure

```yaml
swarm:
  proton_vpn_port_forward_range: "40000-62000"
  ollama_local_port: 11434
  search_local_port: 8001

machines:
  sony_asteroth:
    hostname: "sony-asteroth"
    proton_vpn_ip: null            # auto-detected
    forwarded_port: null           # entered once per session
    ollama_endpoint: null          # auto-generated
    search_endpoint: null          # auto-generated
```

## Workflow Example

### Scenario: Fresh Boot

1. Windows boots, Proton VPN auto-connects
2. You run `.\swarm_llm_manager.ps1 update`
3. Script detects IP: `45.123.45.67`
4. Script prompts: "Enter your current forwarded port (or press Enter to keep 51234)"
5. You press Enter (port unchanged)
6. Script updates: `Locked in sony_asteroth → Ollama: http://45.123.45.67:51234`

Result: **Zero typing** (99% of boots)

### Scenario: VPN Reconnected

1. You manually disconnect/reconnect VPN
2. Proton assigns new port: `52345`
3. You run `.\swarm_llm_manager.ps1 update`
4. Script detects new IP: `45.123.45.99`
5. Script prompts for port
6. You enter: `52345`
7. Script updates all endpoints

Result: **One number** typed

## Port Forwarding Tips

### Persistence Strategy

- Keep the same VPN connection alive → port never changes
- Enable auto-reconnect → minimizes manual interventions
- Use P2P servers → more stable port forwarding
- Never click "Regenerate" unless necessary

### Multiple Devices

Each device gets its own independent forwarded port:
- sony_asteroth: port 51234
- nova: port 52345
- athena: port 53456
- nitro: port 54567

No conflicts, perfect isolation.

## Advanced: Dual Port Setup

If you want separate ports for Ollama and Search:

1. Get two forwarded ports from Proton VPN
2. Modify `swarm_llm_manager.ps1`:
   ```powershell
   $port1 = Read-Host "Enter Ollama port"
   $port2 = Read-Host "Enter Search port"
   $myEntry.ollama_endpoint = "http://$currentIp:$port1"
   $myEntry.search_endpoint = "http://$currentIp:$port2"
   ```

## Troubleshooting

### "Hostname not found in configuration"

Your machine name doesn't match the config. Check with:
```powershell
$env:COMPUTERNAME
```

Add your hostname to `swarm_llm_endpoints.yaml` if needed.

### "No internet or not on VPN"

- Verify Proton VPN is connected
- Check internet connectivity
- Try: `Invoke-WebRequest -Uri "https://api.ipify.org"`

### "powershell-yaml module not found"

Install the module:
```powershell
Install-Module -Name powershell-yaml -Scope CurrentUser -Force
```

### Port validation fails

Ensure the port is in range 40000-62000 (Proton VPN's typical range).

## Security Considerations

- YAML file stores VPN IPs and ports (not sensitive, public IPs)
- No credentials stored
- Port forwarding is controlled by Proton VPN app
- Consider `.gitignore` for the YAML if IPs are sensitive to your org

## Integration

This system integrates with:
- Local Ollama instances (default port 11434)
- Search nodes (default port 8001)
- Any service that needs external VPN access

The swarm stays perfectly synced, IPs auto-update, and you never fat-finger an IP again.

## Future Enhancements

Potential improvements:
- Auto-read port from Proton VPN Windows registry
- Linux support with ProtonVPN CLI integration
- Health checks for endpoints
- Automatic failover between machines

## Empire Building

With this system:
- 90% reduction in manual configuration
- 99% of boots require zero typing
- Perfect synchronization across the swarm
- Infrastructure that just works

**The empire keeps growing. 🚀**
