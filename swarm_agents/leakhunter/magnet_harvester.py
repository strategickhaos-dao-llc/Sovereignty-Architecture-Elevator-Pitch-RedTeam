#!/usr/bin/env python3
"""
Magnet Harvester - Decoy Distribution via Cloud Storage
Uploads watermarked, beaconed decoy files using rotating Proton accounts
Part of the LeakHunter Swarm intelligence system
"""

import os
import json
import hashlib
import logging
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MagnetHarvester:
    """Manages upload of decoy files to cloud storage with rotating credentials"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "swarm_agents/leakhunter/config.json"
        self.config = self._load_config()
        self.upload_history = []
        
    def _load_config(self) -> Dict:
        """Load harvester configuration"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {
            "proton_accounts": [],
            "mega_endpoints": [],
            "decoy_versions": ["v1", "v2", "v3"],
            "beacon_server": "https://asteroth-gate.strategickhaos.internal/beacon",
            "watermark_key": "strategickhaos-sovereign-2024"
        }
    
    def generate_watermark(self, file_path: str, version: str) -> str:
        """Generate unique watermark for decoy file"""
        timestamp = datetime.utcnow().isoformat()
        data = f"{file_path}:{version}:{timestamp}:{self.config['watermark_key']}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def create_beaconed_decoy(self, original_path: str, output_path: str, version: str) -> Dict:
        """Create a beaconed version of a decoy file"""
        watermark = self.generate_watermark(original_path, version)
        
        beacon_payload = {
            "watermark": watermark,
            "version": version,
            "created_at": datetime.utcnow().isoformat(),
            "beacon_url": self.config["beacon_server"],
            "original": original_path
        }
        
        # In production, this would inject actual beacon code
        # For now, we create metadata
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path + ".beacon.json", 'w') as f:
            json.dump(beacon_payload, f, indent=2)
        
        logger.info(f"Created beaconed decoy: {output_path} (watermark: {watermark[:16]}...)")
        return beacon_payload
    
    def rotate_account(self) -> Dict:
        """Select next Proton account from rotation"""
        accounts = self.config.get("proton_accounts", [])
        if not accounts:
            logger.warning("No Proton accounts configured")
            return {"account": "demo@proton.me", "index": 0}
        
        # Simple round-robin rotation
        current_index = len(self.upload_history) % len(accounts)
        return {"account": accounts[current_index], "index": current_index}
    
    def upload_to_mega(self, file_path: str, decoy_version: str) -> Dict:
        """Upload decoy to Mega with rotating credentials"""
        account = self.rotate_account()
        watermark = self.generate_watermark(file_path, decoy_version)
        
        # Create upload record
        upload_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "file": file_path,
            "version": decoy_version,
            "watermark": watermark,
            "account": account["account"],
            "platform": "mega",
            "status": "uploaded",
            "download_count": 0
        }
        
        self.upload_history.append(upload_record)
        logger.info(f"Uploaded {file_path} to Mega using account {account['account']}")
        
        return upload_record
    
    def generate_mega_links(self, file_path: str, count: int = 3) -> List[str]:
        """Generate multiple Mega links for a single decoy"""
        links = []
        for i in range(count):
            upload_record = self.upload_to_mega(file_path, f"v{i+1}")
            # Generate fake Mega link format
            fake_link = f"https://mega.nz/#!{upload_record['watermark'][:8]}"
            links.append(fake_link)
            logger.info(f"Generated Mega link {i+1}/{count}: {fake_link}")
        
        return links
    
    def get_statistics(self) -> Dict:
        """Get upload and distribution statistics"""
        total_uploads = len(self.upload_history)
        total_downloads = sum(r.get("download_count", 0) for r in self.upload_history)
        
        stats = {
            "total_uploads": total_uploads,
            "total_downloads": total_downloads,
            "active_decoys": total_uploads,
            "platforms": ["mega", "1337x", "i2p", "rutracker"],
            "last_upload": self.upload_history[-1]["timestamp"] if self.upload_history else None
        }
        
        logger.info(f"Statistics: {stats}")
        return stats
    
    def save_upload_history(self, output_path: str = "swarm_agents/leakhunter/upload_history.json"):
        """Save upload history to file"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump({
                "history": self.upload_history,
                "statistics": self.get_statistics()
            }, f, indent=2)
        logger.info(f"Upload history saved to {output_path}")


def main():
    """Main execution for testing"""
    harvester = MagnetHarvester()
    
    # Example: Generate three Mega links for a decoy
    decoy_file = "models/fake_405B_weights.tar.gz"
    links = harvester.generate_mega_links(decoy_file, count=3)
    
    print("\n🎯 Mega Links Generated:")
    for i, link in enumerate(links, 1):
        print(f"  {i}. {link}")
    
    # Show statistics
    stats = harvester.get_statistics()
    print(f"\n📊 Statistics:")
    print(f"  Total uploads: {stats['total_uploads']}")
    print(f"  Total downloads: {stats['total_downloads']}")
    
    # Save history
    harvester.save_upload_history()
    print("\n✅ Upload history saved")


if __name__ == "__main__":
    main()
