#!/usr/bin/env python3
"""
Asteroth-Gate Honeypot Node
Simulates a torrent seeding node that distributes watermarked decoys
Part of the LeakHunter Swarm intelligence system
"""

import json
import hashlib
import logging
from datetime import datetime
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AsterothGate:
    """Honeypot torrent node for seeding watermarked decoys"""
    
    def __init__(self, node_id: Optional[str] = None):
        self.node_id = node_id or self._generate_node_id()
        self.torrents = []
        self.peer_connections = []
        self.upload_stats = {
            "total_uploaded_gb": 0,
            "total_peers": 0,
            "active_torrents": 0
        }
        
    def _generate_node_id(self) -> str:
        """Generate unique node identifier"""
        timestamp = datetime.utcnow().isoformat()
        data = f"asteroth-gate-{timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def create_torrent(self, name: str, size_gb: float, watermark: str, 
                       decoy_version: str = "v2") -> Dict:
        """
        Create a new torrent for a decoy file
        
        Note: This is a simulation. Real torrent infohashes are based on file content.
        In production, use actual torrent creation tools like transmission or libtorrent.
        """
        torrent_hash = hashlib.sha1(f"{name}:{watermark}".encode()).hexdigest()
        
        torrent = {
            "name": name,
            "infohash": torrent_hash,
            "size_gb": size_gb,
            "watermark": watermark,
            "decoy_version": decoy_version,
            "created_at": datetime.utcnow().isoformat(),
            "seeded_from": self.node_id,
            "peers": [],
            "uploaded_gb": 0,
            "ratio": 0.0,
            "status": "seeding"
        }
        
        self.torrents.append(torrent)
        self.upload_stats["active_torrents"] = len([t for t in self.torrents if t["status"] == "seeding"])
        
        logger.info(f"Created torrent: {name} (hash: {torrent_hash[:16]}...)")
        return torrent
    
    def seed_to_1337x(self, torrent: Dict) -> Dict:
        """Seed torrent to 1337x tracker"""
        magnet_link = self._generate_magnet_link(torrent)
        
        seed_record = {
            "platform": "1337x",
            "torrent_name": torrent["name"],
            "infohash": torrent["infohash"],
            "magnet_link": magnet_link,
            "seeded_at": datetime.utcnow().isoformat(),
            "node_id": self.node_id
        }
        
        logger.info(f"Seeding to 1337x: {torrent['name']}")
        return seed_record
    
    def _generate_magnet_link(self, torrent: Dict) -> str:
        """Generate magnet link for torrent"""
        return (f"magnet:?xt=urn:btih:{torrent['infohash']}"
                f"&dn={torrent['name']}"
                f"&tr=udp://tracker.1337x.org:80/announce")
    
    def register_peer(self, torrent_infohash: str, peer_ip_hash: str) -> Dict:
        """Register a peer connecting to download"""
        connection = {
            "peer_ip_hash": peer_ip_hash,
            "torrent_infohash": torrent_infohash,
            "connected_at": datetime.utcnow().isoformat(),
            "status": "downloading"
        }
        
        self.peer_connections.append(connection)
        
        # Update torrent peer list
        for torrent in self.torrents:
            if torrent["infohash"] == torrent_infohash:
                if peer_ip_hash not in torrent["peers"]:
                    torrent["peers"].append(peer_ip_hash)
        
        self.upload_stats["total_peers"] = len(set(c["peer_ip_hash"] for c in self.peer_connections))
        
        logger.info(f"Peer connected: {peer_ip_hash[:8]}... to {torrent_infohash[:16]}...")
        return connection
    
    def update_upload_stats(self, torrent_infohash: str, uploaded_gb: float):
        """Update upload statistics for a torrent"""
        for torrent in self.torrents:
            if torrent["infohash"] == torrent_infohash:
                torrent["uploaded_gb"] += uploaded_gb
                torrent["ratio"] = torrent["uploaded_gb"] / torrent["size_gb"] if torrent["size_gb"] > 0 else 0
                
        self.upload_stats["total_uploaded_gb"] += uploaded_gb
        logger.info(f"Upload stats updated: +{uploaded_gb:.2f} GB")
    
    def get_node_status(self) -> Dict:
        """Get current status of the honeypot node"""
        return {
            "node_id": self.node_id,
            "status": "online",
            "active_torrents": self.upload_stats["active_torrents"],
            "total_peers": self.upload_stats["total_peers"],
            "total_uploaded_gb": self.upload_stats["total_uploaded_gb"],
            "uptime": "operational"
        }
    
    def print_status(self):
        """Print formatted node status"""
        status = self.get_node_status()
        
        print("\n" + "="*60)
        print("🔥 ASTEROTH-GATE HONEYPOT NODE STATUS")
        print("="*60)
        print(f"Node ID: {status['node_id']}")
        print(f"Status: {status['status'].upper()}")
        print(f"Active Torrents: {status['active_torrents']}")
        print(f"Total Peers: {status['total_peers']}")
        print(f"Total Uploaded: {status['total_uploaded_gb']:.2f} GB")
        print("="*60 + "\n")
        
        if self.torrents:
            print("📦 Active Torrents:")
            for i, torrent in enumerate(self.torrents[:5], 1):
                print(f"  {i}. {torrent['name']} - {len(torrent['peers'])} peers, "
                      f"ratio: {torrent['ratio']:.2f}")
    
    def save_node_data(self, output_path: str = "swarm_agents/leakhunter/asteroth_gate.json"):
        """Save node data to file"""
        import os
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        data = {
            "node_status": self.get_node_status(),
            "torrents": self.torrents,
            "peer_connections": self.peer_connections[-100:],  # Last 100 connections
            "upload_stats": self.upload_stats,
            "exported_at": datetime.utcnow().isoformat()
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Node data saved to {output_path}")


def main():
    """Main execution for testing"""
    # Initialize Asteroth-Gate node
    node = AsterothGate()
    
    print("🚀 Initializing Asteroth-Gate Honeypot Node...")
    
    # Create some decoy torrents
    torrents = [
        node.create_torrent("Strategickhaos-Full-Stack-v2.tar.gz", 85.5, "watermark_001", "v2"),
        node.create_torrent("Sovereignty-Models-405B.tar.gz", 162.0, "watermark_002", "v2"),
        node.create_torrent("AI-Agents-Complete-Bundle.zip", 42.3, "watermark_003", "v2")
    ]
    
    # Seed to 1337x
    for torrent in torrents:
        seed_record = node.seed_to_1337x(torrent)
        print(f"✅ Seeded: {seed_record['magnet_link'][:60]}...")
    
    # Simulate some peer connections
    for i in range(25):
        node.register_peer(torrents[0]["infohash"], f"peer_{i}")
        node.update_upload_stats(torrents[0]["infohash"], 3.2)
    
    # Display status
    node.print_status()
    
    # Save data
    node.save_node_data()
    print("\n✅ Node data saved")


if __name__ == "__main__":
    main()
