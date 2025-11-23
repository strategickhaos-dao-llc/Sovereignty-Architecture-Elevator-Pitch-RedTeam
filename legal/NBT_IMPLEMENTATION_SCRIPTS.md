# Negative-Balance Training Protocol - Implementation Scripts

## Overview

This document provides ready-to-use scripts for implementing the Negative-Balance Training Protocol resource constraints on Linux systems, WSL2, and hybrid environments.

---

## Memory Constraint Scripts

### Linux cgroups v2 Implementation

```bash
#!/bin/bash
# nbt_memory_limit.sh - Apply 6GB memory limit using cgroups v2

set -e

MEMORY_LIMIT="6G"
CGROUP_NAME="nbt-training"
CGROUP_PATH="/sys/fs/cgroup/${CGROUP_NAME}"

# Create cgroup (cgroups v2 uses mkdir)
sudo mkdir -p ${CGROUP_PATH}

# Enable memory controller
echo "+memory" | sudo tee /sys/fs/cgroup/cgroup.subtree_control > /dev/null

# Set memory limit (6GB = 6442450944 bytes)
echo 6442450944 | sudo tee ${CGROUP_PATH}/memory.max

# Set swap limit (500MB = 524288000 bytes)
echo 524288000 | sudo tee ${CGROUP_PATH}/memory.swap.max

# Verify limits
echo "Memory limit: $(cat ${CGROUP_PATH}/memory.max)"
echo "Swap limit: $(cat ${CGROUP_PATH}/memory.swap.max)"

echo "To run training under constraints:"
echo "  echo \$\$ | sudo tee ${CGROUP_PATH}/cgroup.procs"
echo "  python train_model.py"
```

### WSL2 Configuration

```powershell
# WSL2 .wslconfig file
# Location: %USERPROFILE%\.wslconfig

[wsl2]
# Limit memory to 6GB
memory=6GB

# Limit swap to 500MB
swap=500MB

# Disable page reporting for more aggressive memory pressure
pageReporting=false

# Keep localhost forwarding enabled
localhostForwarding=true

# Processors (optional, can limit CPU cores too)
processors=4
```

Apply with:
```powershell
# Restart WSL to apply configuration
wsl --shutdown
# Wait 8 seconds for WSL to fully shut down
Start-Sleep -Seconds 8
# Restart your WSL distribution
wsl -d Ubuntu
```

---

## Swap Thrashing Configuration

### Create Limited Swap File

```bash
#!/bin/bash
# nbt_swap_limit.sh - Create 500MB swap file for forced thrashing

set -e

SWAP_FILE="/swapfile_nbt"
SWAP_SIZE_MB=500

# Disable existing swap
sudo swapoff -a

# Create new limited swap file
sudo dd if=/dev/zero of=${SWAP_FILE} bs=1M count=${SWAP_SIZE_MB} status=progress

# Set permissions
sudo chmod 600 ${SWAP_FILE}

# Make swap
sudo mkswap ${SWAP_FILE}

# Enable swap
sudo swapon ${SWAP_FILE}

# Verify
echo "Swap status:"
free -h
swapon --show

echo "Note: To make permanent, add this line to /etc/fstab:"
echo "${SWAP_FILE} none swap sw 0 0"
```

---

## Network Throttling Scripts

### Bandwidth Limitation with Packet Loss

```bash
#!/bin/bash
# nbt_network_limit.sh - Throttle network to 512kbps with packet loss

set -e

INTERFACE="${1:-$(ip route | grep default | awk '{print $5}' | head -1)}"  # Auto-detect or pass as argument
BANDWIDTH="512kbit"
PACKET_LOSS="5%"
LATENCY="100ms"

# Check for required kernel modules
if ! lsmod | grep -q "sch_htb"; then
    echo "Loading htb module..."
    sudo modprobe sch_htb
fi
if ! lsmod | grep -q "sch_netem"; then
    echo "Loading netem module..."
    sudo modprobe sch_netem
fi

# Clear existing rules
sudo tc qdisc del dev ${INTERFACE} root 2>/dev/null || true

# Add root qdisc with HTB (Hierarchical Token Bucket)
sudo tc qdisc add dev ${INTERFACE} root handle 1: htb default 12

# Create class with bandwidth limit
sudo tc class add dev ${INTERFACE} parent 1: classid 1:12 htb rate ${BANDWIDTH} ceil ${BANDWIDTH}

# Add packet loss and latency with netem
sudo tc qdisc add dev ${INTERFACE} parent 1:12 handle 10: netem delay ${LATENCY} loss ${PACKET_LOSS}

# Show configuration
echo "Network throttling applied:"
sudo tc -s qdisc show dev ${INTERFACE}
sudo tc -s class show dev ${INTERFACE}

echo ""
echo "To remove limits:"
echo "  sudo tc qdisc del dev ${INTERFACE} root"
```

### Remove Network Limits

```bash
#!/bin/bash
# nbt_network_restore.sh - Remove network throttling

INTERFACE="${1:-$(ip route | grep default | awk '{print $5}' | head -1)}"  # Auto-detect or pass as argument

sudo tc qdisc del dev ${INTERFACE} root 2>/dev/null || true
echo "Network limits removed from ${INTERFACE}"
```

---

## GPU Power and Clock Limiting

### NVIDIA GPU Constraints

```bash
#!/bin/bash
# nbt_gpu_limit.sh - Apply GPU power and clock limits

set -e

POWER_LIMIT=75  # Watts
MAX_GPU_CLOCK=1200  # MHz
MAX_MEM_CLOCK=5000  # MHz

# Enable persistence mode (required for clock locking)
sudo nvidia-smi -pm 1

# Set power limit
sudo nvidia-smi -pl ${POWER_LIMIT}

# Lock GPU clock
sudo nvidia-smi -lgc ${MAX_GPU_CLOCK}

# Lock memory clock (optional)
# sudo nvidia-smi -lmc ${MAX_MEM_CLOCK}

# Show current status
nvidia-smi --query-gpu=index,name,power.limit,clocks.current.graphics,clocks.max.graphics,temperature.gpu --format=csv

echo ""
echo "GPU constraints applied:"
echo "  Power limit: ${POWER_LIMIT}W"
echo "  GPU clock locked at: ${MAX_GPU_CLOCK} MHz"
```

### Restore GPU Defaults

```bash
#!/bin/bash
# nbt_gpu_restore.sh - Restore GPU to default settings

set -e

# Reset to default power limit (varies by GPU model)
# Use nvidia-smi -q to find default power limit
DEFAULT_POWER=$(nvidia-smi --query-gpu=power.default_limit --format=csv,noheader,nounits | head -1)

# Validate the power limit value
if [[ ! "$DEFAULT_POWER" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
    echo "Error: Could not determine default power limit"
    exit 1
fi

sudo nvidia-smi -pl ${DEFAULT_POWER}

# Reset clocks
sudo nvidia-smi -rgc

# Disable persistence mode
sudo nvidia-smi -pm 0

echo "GPU restored to defaults"
nvidia-smi --query-gpu=index,name,power.limit,clocks.current.graphics --format=csv
```

---

## CPU Frequency Limiting

### Intel CPU Constraints

```bash
#!/bin/bash
# nbt_cpu_limit.sh - Limit CPU frequency and disable turbo

set -e

MAX_FREQ="2.0GHz"

# Install cpupower if not available
if ! command -v cpupower &> /dev/null; then
    echo "Installing cpupower..."
    sudo apt-get update && sudo apt-get install -y linux-tools-generic
fi

# Disable Intel Turbo Boost
echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo

# Set maximum frequency
sudo cpupower frequency-set --max ${MAX_FREQ}

# Verify settings
echo "CPU frequency constraints:"
cpupower frequency-info
```

### Restore CPU Defaults

```bash
#!/bin/bash
# nbt_cpu_restore.sh - Restore CPU to default settings

set -e

# Enable Intel Turbo Boost
echo 0 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo

# Remove frequency cap (restore to hardware maximum)
if command -v cpupower &> /dev/null; then
    # Get CPU's maximum frequency
    MAX_FREQ=$(lscpu | grep "CPU max MHz" | awk '{print $4}' | cut -d'.' -f1)
    if [ -n "$MAX_FREQ" ]; then
        sudo cpupower frequency-set --max ${MAX_FREQ}MHz
    fi
fi

echo "CPU constraints removed"
cpupower frequency-info | grep "current CPU frequency" 2>/dev/null || echo "CPU frequency restored to defaults"
```

---

## All-in-One Scripts

### Apply All NBT Constraints

```bash
#!/bin/bash
# nbt_apply_all.sh - Apply all Negative-Balance Training Protocol constraints

set -e

echo "================================================"
echo "Applying Negative-Balance Training Protocol"
echo "================================================"
echo ""

# Memory limits (cgroups v2)
echo "[1/5] Applying memory constraints (6GB limit)..."
sudo mkdir -p /sys/fs/cgroup/nbt-training 2>/dev/null || true
echo "+memory" | sudo tee /sys/fs/cgroup/cgroup.subtree_control > /dev/null 2>&1 || true
echo 6442450944 | sudo tee /sys/fs/cgroup/nbt-training/memory.max > /dev/null
echo "  ✓ Memory limited to 6GB"

# Swap limit
echo "[2/5] Configuring swap (500MB)..."
if [ ! -f /swapfile_nbt ]; then
    sudo dd if=/dev/zero of=/swapfile_nbt bs=1M count=500 status=none
    sudo chmod 600 /swapfile_nbt
    sudo mkswap /swapfile_nbt > /dev/null
fi
sudo swapoff -a 2>/dev/null || true
sudo swapon /swapfile_nbt
echo "  ✓ Swap limited to 500MB"

# Network throttling
echo "[3/5] Throttling network (512kbps)..."
INTERFACE=$(ip route | grep default | awk '{print $5}' | head -1)
sudo tc qdisc del dev ${INTERFACE} root 2>/dev/null || true
sudo tc qdisc add dev ${INTERFACE} root handle 1: htb default 12
sudo tc class add dev ${INTERFACE} parent 1: classid 1:12 htb rate 512kbit ceil 512kbit
sudo tc qdisc add dev ${INTERFACE} parent 1:12 handle 10: netem delay 100ms loss 5%
echo "  ✓ Network throttled on ${INTERFACE}"

# GPU limits
echo "[4/5] Limiting GPU power and clocks..."
if command -v nvidia-smi &> /dev/null; then
    sudo nvidia-smi -pm 1 > /dev/null
    sudo nvidia-smi -pl 75 > /dev/null
    sudo nvidia-smi -lgc 1200 > /dev/null
    echo "  ✓ GPU power limited to 75W, clock locked at 1200MHz"
else
    echo "  ⚠ No NVIDIA GPU detected, skipping"
fi

# CPU limits
echo "[5/5] Limiting CPU frequency..."
if [ -f /sys/devices/system/cpu/intel_pstate/no_turbo ]; then
    echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo > /dev/null
    echo "  ✓ Turbo boost disabled"
fi
if command -v cpupower &> /dev/null; then
    sudo cpupower frequency-set --max 2.0GHz > /dev/null 2>&1 || true
    echo "  ✓ CPU frequency capped at 2.0GHz"
fi

echo ""
echo "================================================"
echo "NBT Protocol Constraints Applied Successfully"
echo "================================================"
echo ""
echo "Current system state:"
echo "  Memory: $(free -h | grep Mem: | awk '{print $2}') total (6GB accessible)"
echo "  Swap: $(free -h | grep Swap: | awk '{print $2}') (500MB)"
echo "  Network: 512kbps on ${INTERFACE}"
if command -v nvidia-smi &> /dev/null; then
    echo "  GPU: $(nvidia-smi --query-gpu=power.limit --format=csv,noheader) power limit"
fi
echo ""
echo "To run training under constraints:"
echo "  echo \$\$ | sudo tee /sys/fs/cgroup/nbt-training/cgroup.procs"
echo "  python train_model.py"
echo ""
echo "To remove all constraints:"
echo "  sudo ./nbt_remove_all.sh"
```

### Remove All NBT Constraints

```bash
#!/bin/bash
# nbt_remove_all.sh - Remove all Negative-Balance Training Protocol constraints

set -e

echo "Removing all NBT constraints..."

# Remove memory cgroup
sudo rmdir /sys/fs/cgroup/nbt-training 2>/dev/null || true
echo "  ✓ Memory limits removed"

# Restore swap
sudo swapoff /swapfile_nbt 2>/dev/null || true
sudo swapon -a
echo "  ✓ Swap restored"

# Remove network throttling
INTERFACE=$(ip route | grep default | awk '{print $5}' | head -1)
sudo tc qdisc del dev ${INTERFACE} root 2>/dev/null || true
echo "  ✓ Network throttling removed"

# Restore GPU
if command -v nvidia-smi &> /dev/null; then
    DEFAULT_POWER=$(nvidia-smi --query-gpu=power.default_limit --format=csv,noheader,nounits | head -1)
    sudo nvidia-smi -pl ${DEFAULT_POWER} 2>/dev/null || true
    sudo nvidia-smi -rgc 2>/dev/null || true
    sudo nvidia-smi -pm 0 2>/dev/null || true
    echo "  ✓ GPU restored to defaults"
fi

# Restore CPU
if [ -f /sys/devices/system/cpu/intel_pstate/no_turbo ]; then
    echo 0 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo > /dev/null
fi
if command -v cpupower &> /dev/null; then
    # Restore to hardware maximum
    MAX_FREQ=$(lscpu | grep "CPU max MHz" | awk '{print $4}' | cut -d'.' -f1)
    if [ -n "$MAX_FREQ" ]; then
        sudo cpupower frequency-set --max ${MAX_FREQ}MHz > /dev/null 2>&1 || true
    fi
fi
echo "  ✓ CPU restored"

echo ""
echo "All NBT constraints removed. System restored to normal operation."
```

---

## Training Wrapper Script

### Python Training Wrapper with Monitoring

```python
#!/usr/bin/env python3
# nbt_train_wrapper.py - Wrapper for training under NBT constraints

import subprocess
import json
import hashlib
import time
import psutil
from datetime import datetime

def get_system_metrics():
    """Collect current system metrics"""
    return {
        "cpu_temp": get_cpu_temp(),
        "gpu_temp": get_gpu_temp(),
        "memory_used": psutil.virtual_memory().used,
        "memory_available": psutil.virtual_memory().available,
        "swap_used": psutil.swap_memory().used,
        "network_sent": psutil.net_io_counters().bytes_sent,
        "network_recv": psutil.net_io_counters().bytes_recv,
    }

def get_cpu_temp():
    """Get CPU temperature (Linux-specific)"""
    try:
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            return max([t.current for t in temps['coretemp']])
    except:
        pass
    return None

def get_gpu_temp():
    """Get NVIDIA GPU temperature"""
    try:
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader'],
            capture_output=True, text=True
        )
        return int(result.stdout.strip())
    except:
        return None

def mint_training_proof(constraints, metrics):
    """Generate cryptographic proof of training conditions"""
    proof_data = {
        "node": "LYRA",
        "operator": "Dom010101",
        "timestamp": datetime.utcnow().isoformat(),
        "constraints": constraints,
        "metrics": metrics,
    }
    
    proof_json = json.dumps(proof_data, sort_keys=True)
    proof_hash = hashlib.sha256(proof_json.encode()).hexdigest()
    
    return proof_hash, proof_data

def main():
    constraints = {
        "memory_limit_gb": 6,
        "swap_limit_mb": 500,
        "network_bandwidth_kbps": 512,
        "gpu_power_limit_w": 75,
        "cpu_max_freq_ghz": 2.0,
    }
    
    print("=" * 60)
    print("Negative-Balance Training Protocol - Training Session")
    print("=" * 60)
    print()
    
    # Pre-training metrics
    print("Pre-training system state:")
    pre_metrics = get_system_metrics()
    for key, value in pre_metrics.items():
        print(f"  {key}: {value}")
    print()
    
    # Generate proof
    proof_hash, proof_data = mint_training_proof(constraints, pre_metrics)
    print(f"Training proof hash: {proof_hash}")
    print()
    
    # Save proof
    with open(f"nbt_proof_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
        json.dump({
            "hash": proof_hash,
            "data": proof_data
        }, f, indent=2)
    
    print("Starting training under NBT constraints...")
    print("Press Ctrl+C to stop")
    print()
    
    # Run training (replace with your actual training command)
    # subprocess.run(["python", "train_model.py"])
    
    print("Training session complete.")
    print()
    
    # Post-training metrics
    post_metrics = get_system_metrics()
    print("Post-training system state:")
    for key, value in post_metrics.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    main()
```

---

## Monitoring Scripts

### Continuous Thermal Monitoring

```bash
#!/bin/bash
# nbt_monitor_thermal.sh - Monitor thermal state during training

watch -n 1 '
echo "=== Thermal Status ==="
if command -v sensors &> /dev/null; then
    sensors | grep -E "(Package|Core|GPU)" | grep -v "fan"
fi
echo ""
echo "=== GPU Temperature ==="
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=temperature.gpu,power.draw,clocks.current.graphics --format=csv
fi
'
```

### Resource Usage Dashboard

```bash
#!/bin/bash
# nbt_monitor_resources.sh - Real-time resource monitoring

watch -n 2 '
clear
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  Negative-Balance Training Protocol - Live Monitor       ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "▶ Memory Status"
free -h | grep -E "(Mem|Swap):"
echo ""
echo "▶ CPU Status"
mpstat 1 1 | tail -2
echo ""
echo "▶ Network Status"
ifstat 1 1 | tail -1
echo ""
if command -v nvidia-smi &> /dev/null; then
    echo "▶ GPU Status"
    nvidia-smi --query-gpu=utilization.gpu,temperature.gpu,power.draw --format=csv,noheader
fi
'
```

---

## Installation Script

### One-Command Setup

```bash
#!/bin/bash
# install_nbt_tools.sh - Install all NBT implementation tools

set -e

echo "Installing Negative-Balance Training Protocol tools..."

# Install dependencies
sudo apt-get update
sudo apt-get install -y \
    cgroup-tools \
    linux-tools-generic \
    iproute2 \
    sysstat \
    ifstat

# Copy scripts to /usr/local/bin
sudo cp nbt_*.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/nbt_*.sh

echo "Installation complete!"
echo ""
echo "Available commands:"
echo "  nbt_apply_all.sh     - Apply all constraints"
echo "  nbt_remove_all.sh    - Remove all constraints"
echo "  nbt_monitor_thermal.sh  - Monitor temperature"
echo "  nbt_monitor_resources.sh - Monitor resources"
```

---

## Usage Examples

### Training a 70B Model Under Constraints

```bash
# 1. Apply all NBT constraints
sudo ./nbt_apply_all.sh

# 2. Start thermal monitoring in a separate terminal
./nbt_monitor_thermal.sh

# 3. Run training under cgroup constraint
sudo cgexec -g memory:/nbt-training python train_70b_model.py \
    --batch-size 1 \
    --gradient-checkpointing \
    --model-name "llama-70b" \
    --output-dir ./nbt_output

# 4. After training, remove constraints
sudo ./nbt_remove_all.sh
```

### Quick Test Run

```bash
# Test that constraints are working
sudo ./nbt_apply_all.sh

# Run a memory-intensive test
sudo cgexec -g memory:/nbt-training python -c "
import numpy as np
print('Attempting to allocate 10GB...')
try:
    arr = np.zeros((10*1024*1024*1024,), dtype=np.uint8)
    print('Success - this should not happen!')
except MemoryError:
    print('MemoryError caught - constraints working correctly!')
"

sudo ./nbt_remove_all.sh
```

---

## Troubleshooting

### Common Issues

**Issue**: Memory cgroup not found
```bash
# Solution: Enable cgroup v2
sudo grub-mkconfig -o /boot/grub/grub.cfg
# Add: systemd.unified_cgroup_hierarchy=1
# Reboot
```

**Issue**: Network throttling not working
```bash
# Solution: Check interface name
ip link show
# Update INTERFACE variable in scripts
```

**Issue**: GPU constraints not applying
```bash
# Solution: Check nvidia-smi availability
nvidia-smi
# Install NVIDIA drivers if needed
```

---

## References

- cgroups: https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html
- tc (traffic control): https://man7.org/linux/man-pages/man8/tc.8.html
- nvidia-smi: https://developer.nvidia.com/nvidia-system-management-interface

---

*These scripts implement the Negative-Balance Training Protocol as documented in the provisional patent application.*
