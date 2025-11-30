# TrueNAS Scale Setup Guide - DOM_010101 Sovereign Storage

This guide walks through setting up TrueNAS Scale on your 32 TB storage array to serve as the sovereign NAS for the DOM_010101 cluster.

## 📦 What is TrueNAS Scale?

TrueNAS Scale is an enterprise-grade, open-source NAS operating system built on Debian Linux. It provides:
- **ZFS File System**: Copy-on-write, checksumming, snapshots, replication
- **RAID-Z2**: Can survive 2 disk failures without data loss
- **SMB/NFS/iSCSI**: Multiple protocol support
- **Docker/Kubernetes**: Can run containers directly on NAS
- **Web UI**: Easy management interface

## 🔽 Download TrueNAS Scale

1. **Visit Official Website**
   ```
   https://www.truenas.com/download-truenas-scale/
   ```

2. **Download Latest Stable Release**
   ```bash
   # Direct download (check website for latest version)
   wget https://download.truenas.com/truenas-scale/TrueNAS-SCALE-23.10.1/TrueNAS-SCALE-23.10.1.iso
   ```

3. **Verify Checksum (Recommended)**
   ```bash
   # Download SHA256 checksum file
   wget https://download.truenas.com/truenas-scale/TrueNAS-SCALE-23.10.1/TrueNAS-SCALE-23.10.1.iso.sha256
   
   # Verify
   sha256sum -c TrueNAS-SCALE-23.10.1.iso.sha256
   ```

## 💿 Create Bootable USB

### On Linux/macOS

```bash
# Find your USB drive (be careful!)
lsblk
# or
diskutil list

# Write ISO to USB (replace /dev/sdX with your USB device)
sudo dd if=TrueNAS-SCALE-23.10.1.iso of=/dev/sdX bs=4M status=progress && sync
```

### On Windows

**Option 1: Rufus**
1. Download Rufus from https://rufus.ie/
2. Insert USB drive
3. Select TrueNAS ISO
4. Click "START"
5. Use DD image mode

**Option 2: BalenaEtcher**
1. Download from https://etcher.balena.io/
2. Select TrueNAS ISO
3. Select USB drive
4. Flash

## 🚀 Installation Steps

### 1. Boot from USB

1. Insert USB drive into target machine
2. Enter BIOS/UEFI (usually F2, F12, DEL, or ESC during boot)
3. Set USB drive as first boot device
4. Save and reboot

### 2. TrueNAS Scale Installation

1. **Welcome Screen**
   - Select "Install/Upgrade"
   - Press Enter

2. **Select Destination Drive**
   - Choose the OS drive (NOT your 32 TB data drives!)
   - TrueNAS needs a separate drive for OS (min 16 GB recommended)
   - Press Enter

3. **Installation Mode**
   - Select "Fresh Install"
   - Confirm destruction of data on OS drive
   - Press Enter

4. **Root Password**
   - Set a strong root password
   - Confirm password
   - Press Enter

5. **Installation Process**
   - Wait for installation to complete (3-5 minutes)
   - Remove USB drive when prompted
   - Reboot

### 3. Initial Configuration

1. **Console Setup**
   - TrueNAS boots to console menu
   - Note the IP address displayed (e.g., http://192.168.1.xxx)

2. **Configure Network (Optional)**
   - Press 1 for "Configure Network Interfaces"
   - Set static IP: `192.168.1.200`
   - Set subnet mask: `255.255.255.0`
   - Set gateway: `192.168.1.1` (your router)
   - Set DNS: `8.8.8.8` or your router IP
   - Press Enter to save

3. **Access Web UI**
   - Open browser on another computer on same network
   - Navigate to `http://192.168.1.200`
   - Login with root and the password you set

## 🗄️ Storage Pool Configuration

### Create ZFS Pool with RAID-Z2

1. **Navigate to Storage**
   - Click "Storage" in left sidebar
   - Click "Create Pool"

2. **Pool Configuration**
   - **Name**: `swarm-vault-pool`
   - **Layout**: RAID-Z2
   - **Disks**: Select your 32 TB array disks
   - RAID-Z2 requires minimum 4 disks
   - Can survive 2 disk failures

3. **Pool Settings**
   - **Encryption**: Optional (recommended for sensitive data)
   - **Compression**: LZ4 (recommended - minimal CPU, good compression)
   - **Deduplication**: Off (requires massive RAM)
   - Click "Create"

### Create Dataset

1. **Navigate to Pool**
   - Click on `swarm-vault-pool`
   - Click "Add Dataset"

2. **Dataset Configuration**
   - **Name**: `swarm-vault`
   - **Compression**: Inherit (LZ4)
   - **Quota**: None (or set limit)
   - **Record Size**: 128K (good for mixed workloads)
   - Click "Save"

## 🌐 Share Configuration

### Create SMB Share (Windows)

1. **Navigate to Sharing**
   - Click "Shares" → "Windows Shares (SMB)"
   - Click "Add"

2. **SMB Share Settings**
   - **Path**: `/mnt/swarm-vault-pool/swarm-vault`
   - **Name**: `swarm-vault`
   - **Purpose**: Default share parameters
   - **Enable**: Yes
   - Click "Save"

3. **SMB Service**
   - Toggle "Service" to ON
   - Check "Start Automatically"

### Create NFS Share (Linux/Kubernetes)

1. **Navigate to Sharing**
   - Click "Shares" → "Unix Shares (NFS)"
   - Click "Add"

2. **NFS Share Settings**
   - **Path**: `/mnt/swarm-vault-pool/swarm-vault`
   - **Comment**: DOM_010101 Swarm Vault
   - Click "Add" under Authorized Networks
   - **Network**: `192.168.1.0/24` (adjust for your network)
   - **Maproot User**: root
   - **Maproot Group**: wheel
   - Click "Save"

3. **NFS Service**
   - Toggle "Service" to ON
   - Check "Start Automatically"

## 🔐 User and Permissions

### Create SMB User

1. **Navigate to Credentials**
   - Click "Credentials" → "Local Users"
   - Click "Add"

2. **User Configuration**
   - **Username**: `dom-cluster`
   - **Full Name**: DOM Cluster User
   - **Password**: (strong password)
   - **User ID**: Auto
   - **Primary Group**: Create new group
   - **Samba Authentication**: Yes
   - Click "Save"

### Set Dataset Permissions

1. **Navigate to Dataset**
   - Storage → swarm-vault-pool → swarm-vault
   - Click "Edit Permissions"

2. **Permission Settings**
   - **Owner**: dom-cluster
   - **Group**: dom-cluster
   - **Mode**: 770 (rwxrwx---)
   - **Apply Recursively**: Yes
   - Click "Save"

## 🧪 Test Connectivity

### From Windows

```powershell
# Test SMB connection
Test-NetConnection -ComputerName 192.168.1.200 -Port 445

# Mount share
New-PSDrive -Name Z -PSProvider FileSystem -Root "\\192.168.1.200\swarm-vault" -Persist -Credential (Get-Credential)

# Test write
New-Item -Path Z:\test.txt -ItemType File -Value "DOM_010101 test"
```

### From Linux

```bash
# Test NFS connection
showmount -e 192.168.1.200

# Mount share
sudo mkdir -p /mnt/swarm-vault
sudo mount -t nfs 192.168.1.200:/mnt/swarm-vault-pool/swarm-vault /mnt/swarm-vault

# Test write
echo "DOM_010101 test" | sudo tee /mnt/swarm-vault/test.txt
```

## 📊 Monitoring and Maintenance

### Web UI Dashboard

- **System Stats**: CPU, RAM, Network
- **Storage**: Pool status, disk health
- **Services**: SMB, NFS, SSH status
- **Alerts**: Email notifications for issues

### Storage Health

1. **Navigate to Storage**
   - Check pool status (should be "ONLINE")
   - Check disk SMART status
   - Review I/O statistics

### Snapshots (Recommended)

1. **Navigate to Data Protection**
   - Click "Periodic Snapshot Tasks"
   - Click "Add"
   - **Dataset**: swarm-vault
   - **Schedule**: Daily, Weekly, Monthly as needed
   - **Retention**: Keep last 7 days, 4 weeks, 12 months
   - Click "Save"

### Scrubs (Data Integrity)

1. **Navigate to Data Protection**
   - Click "Scrub Tasks"
   - Click "Add"
   - **Pool**: swarm-vault-pool
   - **Schedule**: Monthly (recommended)
   - Click "Save"

## 🔧 Advanced Configuration

### Enable iSCSI (Optional)

For block storage:
1. Navigate to "Shares" → "Block Shares (iSCSI)"
2. Configure portal, target, and extent
3. Use for high-performance workloads

### TrueNAS Apps (Kubernetes)

TrueNAS Scale includes built-in Kubernetes:
1. Navigate to "Apps"
2. Can run containerized apps directly on NAS
3. Useful for running services alongside storage

### Replication

For backup to another TrueNAS:
1. Navigate to "Data Protection" → "Replication Tasks"
2. Configure ZFS replication to backup NAS
3. Can replicate over SSH or local

## 🚨 Backup Strategy

### Critical: Backup Your Data

Even with RAID-Z2, maintain 3-2-1 backup rule:
- **3** copies of data
- **2** different media types
- **1** offsite copy

### Recommended Backup Methods

1. **Cloud Sync**
   - TrueNAS → Cloud provider
   - Use encryption for privacy

2. **Replication**
   - TrueNAS → Another TrueNAS
   - ZFS send/receive

3. **Rsync**
   - TrueNAS → External USB drive
   - Scheduled tasks

## 📖 Additional Resources

- **Official Documentation**: https://www.truenas.com/docs/scale/
- **Community Forums**: https://forums.truenas.com/
- **YouTube Channel**: TrueNAS Official
- **GitHub**: https://github.com/truenas

## ✅ Post-Installation Checklist

- [ ] TrueNAS Scale installed and accessible
- [ ] Static IP configured (192.168.1.200)
- [ ] ZFS pool created (RAID-Z2)
- [ ] Dataset created (swarm-vault)
- [ ] SMB share configured and accessible
- [ ] NFS share configured and accessible
- [ ] User and permissions set
- [ ] Connectivity tested from all 4 machines
- [ ] Periodic snapshots configured
- [ ] Monthly scrub task scheduled
- [ ] Email alerts configured (optional)

## 🎉 Next Steps

Your TrueNAS Scale NAS is now ready! Proceed to:
- [Kubernetes Setup](../kubernetes/setup-control-plane.ps1)
- [Mount NAS on All Nodes](../network/mount-nas.ps1)
- [Deploy Love Swarm](../docker-swarm/deploy-love-swarm.ps1)

---

**The sovereign storage foundation is complete. 32 TB of indestructible, ZFS-protected glory.** 🗄️⚡
