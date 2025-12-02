#!/usr/bin/env python3
"""
LeakHunter Swarm - Magnet Link Harvester
Collects and analyzes magnet links matching specified keywords and patterns.
"""

import argparse
import json
import sys
import time
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional
import re


class MagnetHarvester:
    """Harvests and analyzes magnet links from various sources."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the harvester with configuration."""
        self.config = self._load_config(config_path)
        self.harvested_magnets = []
        
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load harvester configuration."""
        default_config = {
            "keywords": [
                "Strategickhaos",
                "CheaterHunter",
                "quantum-symbolic",
                "honeypot-lab",
            ],
            "sources": [
                "DHT crawlers",
                "Magnet databases",
                "Torrent indexers",
                "RSS feeds",
            ],
            "check_interval_hours": 6,
            "auto_download_torrent_file": True,
            "verify_info_hash": True,
        }
        
        if config_path:
            try:
                with open(config_path, 'r') as f:
                    custom_config = json.load(f)
                    default_config.update(custom_config)
            except FileNotFoundError:
                print(f"Config file not found: {config_path}, using defaults")
        
        return default_config
    
    def harvest(self) -> Dict[str, Any]:
        """Harvest new magnet links from configured sources."""
        print("🧲 Starting magnet link harvester...")
        print(f"📡 Sources: {len(self.config['sources'])}")
        print(f"🔍 Keywords: {len(self.config['keywords'])}")
        
        start_time = time.time()
        
        for source in self.config["sources"]:
            print(f"  → Harvesting from {source}...", end=" ")
            magnets = self._harvest_from_source(source)
            self.harvested_magnets.extend(magnets)
            time.sleep(0.5)
            print(f"✓ ({len(magnets)} links)")
        
        elapsed = time.time() - start_time
        
        # Analyze harvested magnets
        analysis = self._analyze_magnets()
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": round(elapsed, 2),
            "sources_checked": len(self.config["sources"]),
            "keywords_tracked": len(self.config["keywords"]),
            "magnets_harvested": len(self.harvested_magnets),
            "matches_found": analysis["matches"],
            "suspicious_hashes": analysis["suspicious_hashes"],
            "status": "clean" if analysis["matches"] == 0 else "ALERT",
        }
        
        return result
    
    def _harvest_from_source(self, source: str) -> List[Dict[str, str]]:
        """Harvest magnet links from a specific source."""
        # In production, this would query actual magnet link sources
        # For now, simulate finding no matching magnets
        return []
    
    def _analyze_magnets(self) -> Dict[str, Any]:
        """Analyze harvested magnets for matches."""
        matches = []
        suspicious_hashes = []
        
        for magnet_data in self.harvested_magnets:
            # Check if magnet contains any keywords
            magnet_url = magnet_data.get("url", "")
            for keyword in self.config["keywords"]:
                if keyword.lower() in magnet_url.lower():
                    matches.append({
                        "keyword": keyword,
                        "magnet": magnet_url,
                        "source": magnet_data.get("source", "unknown"),
                    })
                    
                    # Extract info hash
                    info_hash = self._extract_info_hash(magnet_url)
                    if info_hash:
                        suspicious_hashes.append(info_hash)
        
        return {
            "matches": len(matches),
            "suspicious_hashes": suspicious_hashes,
            "details": matches,
        }
    
    def _extract_info_hash(self, magnet_url: str) -> Optional[str]:
        """Extract info hash from magnet URL."""
        match = re.search(r'xt=urn:btih:([a-fA-F0-9]{40})', magnet_url)
        if match:
            return match.group(1)
        return None
    
    def display_results(self, result: Dict[str, Any]):
        """Display harvest results in a formatted manner."""
        print("\n" + "="*60)
        print("🧲 LEAKHUNTER SWARM - MAGNET HARVESTER RESULTS")
        print("="*60)
        
        print(f"⏱️  Duration: {result['duration_seconds']}s")
        print(f"📡 Sources: {result['sources_checked']}")
        print(f"🔍 Magnets harvested: {result['magnets_harvested']}")
        
        if result["status"] == "clean":
            print("\n✅ No matching magnet links detected – all clear")
        else:
            print(f"\n🚨 ALERT - {result['matches_found']} suspicious magnets found!")
            print(f"🔐 Info hashes flagged: {len(result['suspicious_hashes'])}")
        
        print("\n" + "="*60)
    
    def schedule_run(self, interval_hours: int):
        """Schedule periodic harvesting runs."""
        print(f"📅 Scheduling harvester to run every {interval_hours} hours")
        print("⚠️  Note: This would run continuously in production")
        print("👋 Press Ctrl+C to stop (simulated mode)")


def main():
    """Main entry point for the magnet harvester."""
    parser = argparse.ArgumentParser(
        description="LeakHunter Swarm - Magnet Link Harvester"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path to save harvest results (JSON)"
    )
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Run in scheduled mode (every 6 hours)"
    )
    
    args = parser.parse_args()
    
    # Create harvester instance
    harvester = MagnetHarvester(config_path=args.config)
    
    if args.schedule:
        harvester.schedule_run(harvester.config["check_interval_hours"])
    else:
        # Perform single harvest
        result = harvester.harvest()
        harvester.display_results(result)
        
        # Save results if output path provided
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Results saved to: {args.output}")
        
        # Return appropriate exit code
        sys.exit(0 if result["status"] == "clean" else 1)


if __name__ == "__main__":
    main()
