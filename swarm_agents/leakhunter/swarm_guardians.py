#!/usr/bin/env python3
"""
Swarm Guardians - I2P Hidden Service Mirror
Operates I2P mirrors for decoy distribution in the dark net
Part of the LeakHunter Swarm intelligence system
"""

import json
import hashlib
import logging
from datetime import datetime
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SwarmGuardians:
    """I2P hidden service for distributing watermarked decoys"""
    
    def __init__(self, vm_id: Optional[str] = None):
        self.vm_id = vm_id or "swarm_guardians_vm_01"
        self.i2p_address = self._generate_i2p_address()
        self.mirrors = []
        self.access_logs = []
        self.vm_status = "running"
        
    def _generate_i2p_address(self) -> str:
        """Generate I2P address (base32 format)"""
        import base64
        data = f"{self.vm_id}:{datetime.utcnow().isoformat()}"
        hash_bytes = hashlib.sha256(data.encode()).digest()
        # Generate proper base32 encoded I2P address (52 characters)
        # I2P addresses use base32 encoding without padding
        base32_addr = base64.b32encode(hash_bytes).decode('ascii').lower().rstrip('=')[:52]
        return base32_addr + ".b32.i2p"
    
    def create_mirror(self, name: str, size_gb: float, watermark: str,
                     decoy_version: str = "v2") -> Dict:
        """Create a new I2P mirror for a decoy"""
        mirror_id = hashlib.sha256(f"{name}:{watermark}".encode()).hexdigest()[:16]
        
        mirror = {
            "mirror_id": mirror_id,
            "name": name,
            "i2p_address": self.i2p_address,
            "size_gb": size_gb,
            "watermark": watermark,
            "decoy_version": decoy_version,
            "created_at": datetime.utcnow().isoformat(),
            "vm_id": self.vm_id,
            "access_count": 0,
            "download_count": 0,
            "status": "active"
        }
        
        self.mirrors.append(mirror)
        logger.info(f"Created I2P mirror: {name} at {self.i2p_address[:30]}...")
        return mirror
    
    def register_access(self, mirror_id: str, visitor_hash: str, 
                       action: str = "view") -> Dict:
        """Register access to an I2P mirror"""
        access_log = {
            "mirror_id": mirror_id,
            "visitor_hash": visitor_hash,
            "action": action,
            "timestamp": datetime.utcnow().isoformat(),
            "i2p_address": self.i2p_address
        }
        
        self.access_logs.append(access_log)
        
        # Update mirror stats
        for mirror in self.mirrors:
            if mirror["mirror_id"] == mirror_id:
                if action == "download":
                    mirror["download_count"] += 1
                mirror["access_count"] += 1
        
        logger.info(f"Access logged: {action} by {visitor_hash[:8]}... on mirror {mirror_id[:8]}...")
        return access_log
    
    def get_vm_status(self) -> Dict:
        """Get current VM and service status"""
        total_accesses = len(self.access_logs)
        total_downloads = sum(m["download_count"] for m in self.mirrors)
        
        return {
            "vm_id": self.vm_id,
            "vm_status": self.vm_status,
            "i2p_address": self.i2p_address,
            "active_mirrors": len([m for m in self.mirrors if m["status"] == "active"]),
            "total_accesses": total_accesses,
            "total_downloads": total_downloads,
            "uptime": "operational"
        }
    
    def print_status(self):
        """Print formatted VM and service status"""
        status = self.get_vm_status()
        
        print("\n" + "="*60)
        print("🛡️  SWARM GUARDIANS - I2P HIDDEN SERVICE STATUS")
        print("="*60)
        print(f"VM ID: {status['vm_id']}")
        print(f"VM Status: {status['vm_status'].upper()}")
        print(f"I2P Address: {status['i2p_address'][:40]}...")
        print(f"Active Mirrors: {status['active_mirrors']}")
        print(f"Total Accesses: {status['total_accesses']}")
        print(f"Total Downloads: {status['total_downloads']}")
        print("="*60 + "\n")
        
        if self.mirrors:
            print("🔐 Active Mirrors:")
            for i, mirror in enumerate(self.mirrors[:5], 1):
                print(f"  {i}. {mirror['name']} - "
                      f"{mirror['access_count']} accesses, "
                      f"{mirror['download_count']} downloads")
    
    def get_mirror_url(self, mirror_id: str) -> str:
        """Get full I2P URL for a mirror"""
        return f"http://{self.i2p_address}/mirrors/{mirror_id}"
    
    def simulate_darknet_traffic(self, mirror_id: str, visitor_count: int = 50):
        """Simulate dark net traffic to a mirror"""
        for i in range(visitor_count):
            visitor_hash = hashlib.sha256(f"visitor_{i}".encode()).hexdigest()[:16]
            
            # 70% view, 30% download
            action = "download" if i % 10 < 3 else "view"
            self.register_access(mirror_id, visitor_hash, action)
        
        logger.info(f"Simulated {visitor_count} visitors to mirror {mirror_id[:8]}...")
    
    def save_vm_data(self, output_path: str = "swarm_agents/leakhunter/swarm_guardians.json"):
        """Save VM and service data to file"""
        import os
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        data = {
            "vm_status": self.get_vm_status(),
            "mirrors": self.mirrors,
            "access_logs": self.access_logs[-200:],  # Last 200 accesses
            "exported_at": datetime.utcnow().isoformat()
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"VM data saved to {output_path}")


def main():
    """Main execution for testing"""
    # Initialize Swarm Guardians VM
    vm = SwarmGuardians()
    
    print("🚀 Initializing Swarm Guardians I2P Hidden Service...")
    
    # Create some mirrors
    mirrors = [
        vm.create_mirror("Strategickhaos-Complete-v2.7z", 95.2, "watermark_i2p_001", "v2"),
        vm.create_mirror("Sovereign-AI-Stack.tar.xz", 128.5, "watermark_i2p_002", "v2")
    ]
    
    # Simulate dark net traffic
    for mirror in mirrors:
        vm.simulate_darknet_traffic(mirror["mirror_id"], visitor_count=75)
        mirror_url = vm.get_mirror_url(mirror["mirror_id"])
        print(f"✅ Mirror active: {mirror_url}")
    
    # Display status
    vm.print_status()
    
    # Save data
    vm.save_vm_data()
    print("\n✅ VM data saved")


if __name__ == "__main__":
    main()
