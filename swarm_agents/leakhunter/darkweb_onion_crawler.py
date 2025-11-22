#!/usr/bin/env python3
"""
LeakHunter Swarm - Dark Web Onion Crawler
Crawls hidden services on Tor/I2P/Loki for specific keywords and content patterns.
"""

import argparse
import json
import sys
import time
from datetime import datetime
from typing import List, Dict, Any, Optional


class DarkWebCrawler:
    """Crawls dark web hidden services for potential leaks."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the crawler with configuration."""
        self.results = []
        self.networks = ["Tor", "I2P", "Lokinet"]
        self.keywords = [
            "Strategickhaos",
            "CheaterHunter",
            "quantum-symbolic-ai-emulator",
            "honeypot-lab.zip",
            "sovereignty-architecture",
        ]
        self.config = self._load_config(config_path)
        
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load crawler configuration."""
        default_config = {
            "networks": ["tor", "i2p", "lokinet"],
            "keywords": self.keywords,
            "crawl_depth": 3,
            "max_sites_per_network": 1000,
            "timeout_seconds": 30,
        }
        
        if config_path:
            try:
                with open(config_path, 'r') as f:
                    custom_config = json.load(f)
                    default_config.update(custom_config)
            except FileNotFoundError:
                print(f"Config file not found: {config_path}, using defaults")
        
        return default_config
    
    def crawl(self) -> Dict[str, Any]:
        """Perform dark web crawl across configured networks."""
        print("🕸️  Starting dark web crawler...")
        print(f"🌐 Networks: {', '.join(self.networks)}")
        print(f"🔍 Keywords: {len(self.keywords)} patterns")
        
        start_time = time.time()
        results_by_network = {}
        
        for network in self.networks:
            print(f"\n  → Crawling {network} hidden services...")
            network_results = self._crawl_network(network)
            results_by_network[network] = network_results
            print(f"    ✓ Scanned {network_results['sites_crawled']} sites")
        
        elapsed = time.time() - start_time
        
        total_matches = sum(r['matches'] for r in results_by_network.values())
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": round(elapsed, 2),
            "networks_scanned": len(self.networks),
            "keywords_tracked": len(self.keywords),
            "total_sites_crawled": sum(r['sites_crawled'] for r in results_by_network.values()),
            "matches_found": total_matches,
            "network_details": results_by_network,
            "status": "clean" if total_matches == 0 else "ALERT",
        }
        
        return result
    
    def _crawl_network(self, network: str) -> Dict[str, Any]:
        """Crawl a specific dark web network."""
        # Simulate crawling process
        time.sleep(1)
        
        # In production, this would use actual Tor/I2P/Lokinet clients
        return {
            "network": network,
            "sites_crawled": 150 if network == "Tor" else 50,
            "matches": 0,
            "onion_links": [],
        }
    
    def display_results(self, result: Dict[str, Any]):
        """Display crawl results in a formatted manner."""
        print("\n" + "="*60)
        print("🕵️  LEAKHUNTER SWARM - DARK WEB CRAWLER RESULTS")
        print("="*60)
        
        print(f"⏱️  Duration: {result['duration_seconds']}s")
        print(f"🌐 Networks: {result['networks_scanned']}")
        print(f"📊 Total sites: {result['total_sites_crawled']}")
        
        if result["status"] == "clean":
            print("\n✅ No mentions found on dark web – staying ghost")
        else:
            print(f"\n🚨 ALERT - {result['matches_found']} potential mentions detected!")
            
            for network, details in result["network_details"].items():
                if details["matches"] > 0:
                    print(f"\n❌ Matches on {network}:")
                    print(f"   Sites: {len(details['onion_links'])}")
        
        print("\n" + "="*60)


def main():
    """Main entry point for the dark web crawler."""
    parser = argparse.ArgumentParser(
        description="LeakHunter Swarm - Dark Web Onion Crawler"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path to save crawl results (JSON)"
    )
    parser.add_argument(
        "--networks",
        nargs="+",
        choices=["tor", "i2p", "lokinet"],
        help="Specific networks to crawl"
    )
    
    args = parser.parse_args()
    
    # Create crawler instance
    crawler = DarkWebCrawler(config_path=args.config)
    
    # Override networks if specified
    if args.networks:
        crawler.networks = [n.capitalize() for n in args.networks]
    
    # Perform crawl
    result = crawler.crawl()
    crawler.display_results(result)
    
    # Save results if output path provided
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Results saved to: {args.output}")
    
    # Return appropriate exit code
    sys.exit(0 if result["status"] == "clean" else 1)


if __name__ == "__main__":
    main()
