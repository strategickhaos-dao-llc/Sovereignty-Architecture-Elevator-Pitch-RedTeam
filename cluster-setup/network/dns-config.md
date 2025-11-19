# DNS and Network Configuration for DOM_010101 Cluster

This document covers DNS resolution and network setup for the sovereign cluster.

## 🌐 Network Topology

```
┌─────────────────────────────────────────────────────────┐
│                  Local Network (192.168.1.0/24)         │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Router/Gateway: 192.168.1.1                             │
│                                                           │
│  ┌─────────────────────────────────────────────┐        │
│  │  TrueNAS Scale NAS                           │        │
│  │  IP: 192.168.1.200 (Static)                 │        │
│  │  Hostname: truenas.dom010101.local           │        │
│  │  Services: SMB (445), NFS (2049), SSH (22)  │        │
│  └─────────────────────────────────────────────┘        │
│                                                           │
│  ┌─────────────────────────────────────────────┐        │
│  │  ASUS TUF Gaming A15 Nova                    │        │
│  │  IP: 192.168.1.101 (Static recommended)     │        │
│  │  Hostname: dom010101.swarm                   │        │
│  │  Role: Control Plane + Worker               │        │
│  │  RAM: 64 GB                                  │        │
│  └─────────────────────────────────────────────┘        │
│                                                           │
│  ┌─────────────────────────────────────────────┐        │
│  │  Sony Core 15 Lyra                           │        │
│  │  IP: 192.168.1.102 (Static recommended)     │        │
│  │  Hostname: lyra.dom010101.local              │        │
│  │  Role: Worker                                │        │
│  │  RAM: 64 GB                                  │        │
│  └─────────────────────────────────────────────┘        │
│                                                           │
│  ┌─────────────────────────────────────────────┐        │
│  │  Beast #3                                     │        │
│  │  IP: 192.168.1.103 (Static recommended)     │        │
│  │  Hostname: beast3.dom010101.local            │        │
│  │  Role: Worker                                │        │
│  │  RAM: 64 GB                                  │        │
│  └─────────────────────────────────────────────┘        │
│                                                           │
│  ┌─────────────────────────────────────────────┐        │
│  │  Monster #4                                   │        │
│  │  IP: 192.168.1.104 (Static recommended)     │        │
│  │  Hostname: monster4.dom010101.local          │        │
│  │  Role: Worker                                │        │
│  │  RAM: 128 GB                                 │        │
│  └─────────────────────────────────────────────┘        │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

## 🔧 Static IP Configuration

### TrueNAS (Required)

Static IP is **required** for TrueNAS:

1. **Web UI Method**:
   - Login to TrueNAS web UI
   - Navigate to Network → Global Configuration
   - Set DNS servers (e.g., 8.8.8.8, 1.1.1.1)
   - Navigate to Network → Interfaces
   - Edit the primary interface
   - Set IPv4 Address: `192.168.1.200/24`
   - Set IPv4 Gateway: `192.168.1.1`
   - Click Save and Test Changes

2. **Console Method**:
   - At TrueNAS console menu
   - Press `1` for Configure Network Interfaces
   - Follow prompts to set static IP

### Kubernetes Nodes (Recommended)

Static IPs are **recommended** for Kubernetes nodes:

#### Windows (PowerShell as Administrator)

```powershell
# Get network adapter name
Get-NetAdapter

# Set static IP (adjust InterfaceAlias to your adapter name)
New-NetIPAddress -InterfaceAlias "Ethernet" `
    -IPAddress 192.168.1.101 `
    -PrefixLength 24 `
    -DefaultGateway 192.168.1.1

# Set DNS servers
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" `
    -ServerAddresses ("8.8.8.8","1.1.1.1")
```

## 📝 Hosts File Configuration

Add these entries to the hosts file on **all machines**:

### Windows

Location: `C:\Windows\System32\drivers\etc\hosts`

```
# DOM_010101 Sovereign Cluster
192.168.1.200    truenas.dom010101.local truenas
192.168.1.101    dom010101.swarm control-plane
192.168.1.102    lyra.dom010101.local lyra
192.168.1.103    beast3.dom010101.local beast3
192.168.1.104    monster4.dom010101.local monster4
```

### Linux

Location: `/etc/hosts`

```bash
# DOM_010101 Sovereign Cluster
192.168.1.200    truenas.dom010101.local truenas
192.168.1.101    dom010101.swarm control-plane
192.168.1.102    lyra.dom010101.local lyra
192.168.1.103    beast3.dom010101.local beast3
192.168.1.104    monster4.dom010101.local monster4
```

### Automated Hosts File Update

```powershell
# PowerShell script to update hosts file
$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
$hostsEntries = @"

# DOM_010101 Sovereign Cluster
192.168.1.200    truenas.dom010101.local truenas
192.168.1.101    dom010101.swarm control-plane
192.168.1.102    lyra.dom010101.local lyra
192.168.1.103    beast3.dom010101.local beast3
192.168.1.104    monster4.dom010101.local monster4
"@

Add-Content -Path $hostsPath -Value $hostsEntries
Write-Host "Hosts file updated successfully"
```

## 🔍 DNS Resolution Options

### Option 1: Local DNS Server (Advanced)

Set up a local DNS server (Pi-hole, dnsmasq, or Windows DNS) on your network:

**Advantages**:
- Centralized DNS management
- No need to edit hosts files
- Dynamic updates possible

**Configuration Example (Pi-hole)**:
```
# Add to Pi-hole Local DNS Records
192.168.1.200    truenas.dom010101.local
192.168.1.101    dom010101.swarm
192.168.1.102    lyra.dom010101.local
192.168.1.103    beast3.dom010101.local
192.168.1.104    monster4.dom010101.local
```

### Option 2: Router DNS (Simple)

Many routers allow adding custom DNS entries:

1. Login to router admin panel (usually 192.168.1.1)
2. Find DNS/DHCP settings
3. Add static DHCP reservations with hostnames
4. Set router as DNS server on all machines

### Option 3: Hosts File (Manual but Reliable)

Edit hosts file on each machine as shown above. This is the most reliable method and doesn't depend on any services.

## 🔐 Firewall Configuration

Ensure these ports are open between all cluster nodes:

### Kubernetes Ports

**Control Plane**:
- 6443: Kubernetes API server
- 2379-2380: etcd server client API
- 10250: Kubelet API
- 10259: kube-scheduler
- 10257: kube-controller-manager

**Workers**:
- 10250: Kubelet API
- 30000-32767: NodePort Services

**Flannel (CNI)**:
- 8285: UDP (flannel vxlan)
- 8472: UDP (flannel vxlan)

### Docker Swarm Ports

- 2377: TCP (cluster management)
- 7946: TCP/UDP (node communication)
- 4789: UDP (overlay network)

### TrueNAS Ports

- 22: SSH
- 80/443: Web UI (HTTP/HTTPS)
- 445: SMB/CIFS
- 2049: NFS
- 111: NFS rpcbind (both TCP and UDP)

### Windows Firewall Rules (PowerShell)

```powershell
# Kubernetes Control Plane
New-NetFirewallRule -DisplayName "Kubernetes API Server" -Direction Inbound -LocalPort 6443 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "etcd" -Direction Inbound -LocalPort 2379-2380 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "Kubelet API" -Direction Inbound -LocalPort 10250 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "kube-scheduler" -Direction Inbound -LocalPort 10259 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "kube-controller-manager" -Direction Inbound -LocalPort 10257 -Protocol TCP -Action Allow

# Flannel
New-NetFirewallRule -DisplayName "Flannel VXLAN" -Direction Inbound -LocalPort 8285,8472 -Protocol UDP -Action Allow

# Docker Swarm
New-NetFirewallRule -DisplayName "Docker Swarm Management" -Direction Inbound -LocalPort 2377 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "Docker Swarm Nodes TCP" -Direction Inbound -LocalPort 7946 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "Docker Swarm Nodes UDP" -Direction Inbound -LocalPort 7946 -Protocol UDP -Action Allow
New-NetFirewallRule -DisplayName "Docker Swarm Overlay" -Direction Inbound -LocalPort 4789 -Protocol UDP -Action Allow
```

## 🧪 Connectivity Testing

### Test DNS Resolution

```powershell
# Windows
nslookup truenas.dom010101.local
nslookup dom010101.swarm
ping truenas.dom010101.local
ping dom010101.swarm

# Linux
dig truenas.dom010101.local
dig dom010101.swarm
ping -c 4 truenas.dom010101.local
ping -c 4 dom010101.swarm
```

### Test TrueNAS Services

```powershell
# SMB (port 445)
Test-NetConnection -ComputerName 192.168.1.200 -Port 445

# NFS (port 2049)
Test-NetConnection -ComputerName 192.168.1.200 -Port 2049

# SSH (port 22)
Test-NetConnection -ComputerName 192.168.1.200 -Port 22

# Web UI (port 80)
Test-NetConnection -ComputerName 192.168.1.200 -Port 80
```

### Test Kubernetes Connectivity

```powershell
# From worker node to control plane
Test-NetConnection -ComputerName dom010101.swarm -Port 6443

# From control plane, check all nodes
kubectl get nodes
```

### Test Docker Swarm Connectivity

```powershell
# Check swarm status
docker info | Select-String "Swarm"

# List nodes
docker node ls

# Check node connectivity
docker node inspect <node-name>
```

## 🔧 Troubleshooting

### Cannot Resolve Hostnames

1. **Check hosts file**: Ensure entries are correct
2. **Flush DNS cache**:
   ```powershell
   ipconfig /flushdns
   ```
3. **Verify network connectivity**: `ping 192.168.1.200`

### Cannot Connect to TrueNAS

1. **Check TrueNAS is running**: Access web UI at http://192.168.1.200
2. **Verify services are started**: Check SMB/NFS services in TrueNAS UI
3. **Check firewall**: Ensure ports 445 (SMB) and 2049 (NFS) are open
4. **Test with IP instead of hostname**: Rules out DNS issues

### Kubernetes Nodes Can't Join

1. **Verify control plane is reachable**: `Test-NetConnection dom010101.swarm -Port 6443`
2. **Check token validity**: Tokens expire after 24 hours
3. **Verify hosts file**: Ensure dom010101.swarm resolves correctly
4. **Check firewall**: Ensure Kubernetes ports are open

### Docker Swarm Nodes Can't Join

1. **Check manager node**: Ensure swarm is initialized
2. **Verify ports**: 2377, 7946, 4789 must be open
3. **Check join token**: Get fresh token with `docker swarm join-token worker`
4. **Network connectivity**: All nodes must be on same network or have routes

---

**Network configuration is critical for cluster operation. Take time to set it up correctly!** 🌐⚡
