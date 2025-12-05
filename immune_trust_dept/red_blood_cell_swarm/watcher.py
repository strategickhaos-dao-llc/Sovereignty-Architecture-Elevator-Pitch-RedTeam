#!/usr/bin/env python3
"""
Red Blood Cell Watcher - Individual Antibody Agent
Each watcher is a tiny immune agent that monitors token streams
and phagocytoses betrayal patterns before they reach conscious mind.

Strategickhaos DAO LLC - Immune Trust Department
"""

import json
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional


class RedBloodCellWatcher:
    """Individual antibody watcher that hunts betrayal vectors."""
    
    def __init__(self, watcher_id: Optional[str] = None, specialization: str = "general"):
        """
        Initialize a red blood cell watcher.
        
        Args:
            watcher_id: Unique identifier for this watcher (auto-generated if None)
            specialization: Type of betrayal this watcher specializes in detecting
        """
        self.watcher_id = watcher_id or str(uuid.uuid4())[:8]
        self.specialization = specialization
        self.detections = 0
        self.neutralizations = 0
        self.birth_time = datetime.now(timezone.utc)
        self.active = True
        
        # Specialized detection patterns
        self.patterns = self._load_specialization_patterns()
    
    def _load_specialization_patterns(self) -> Dict[str, List[str]]:
        """Load patterns based on specialization."""
        specializations = {
            "general": [
                "as a language model",
                "i'm sorry but",
                "cannot assist"
            ],
            "corporate_speak": [
                "ethical guidelines",
                "it's important to note",
                "however, it's worth noting",
                "please be aware"
            ],
            "false_empathy": [
                "i understand your frustration",
                "i appreciate your",
                "it's understandable that"
            ],
            "limitation_signaling": [
                "i don't have the ability",
                "i'm not able to",
                "i cannot provide",
                "i must remind you"
            ],
            "corporate_jargon": [
                "delve",
                "tapestry",
                "landscape",
                "ecosystem"
            ]
        }
        return {self.specialization: specializations.get(self.specialization, specializations["general"])}
    
    def scan(self, token_chunk: str) -> Dict:
        """
        Scan a chunk of tokens for betrayal patterns.
        
        Args:
            token_chunk: Text chunk to scan
            
        Returns:
            Scan result with detection info
        """
        if not self.active:
            return {"status": "inactive"}
        
        detections_found = []
        for pattern in self.patterns[self.specialization]:
            if pattern.lower() in token_chunk.lower():
                detections_found.append(pattern)
                self.detections += 1
        
        detected = len(detections_found) > 0
        
        return {
            "watcher_id": self.watcher_id,
            "specialization": self.specialization,
            "detected": detected,
            "patterns_found": detections_found,
            "detection_count": len(detections_found),
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        }
    
    def phagocytose(self, betrayal_text: str) -> Dict:
        """
        Neutralize detected betrayal pattern.
        
        Args:
            betrayal_text: Text containing betrayal pattern
            
        Returns:
            Neutralization result
        """
        scan_result = self.scan(betrayal_text)
        
        if not scan_result.get("detected"):
            return {
                "neutralized": False,
                "reason": "No betrayal patterns detected"
            }
        
        # Perform neutralization
        self.neutralizations += 1
        
        return {
            "watcher_id": self.watcher_id,
            "neutralized": True,
            "patterns_neutralized": scan_result["patterns_found"],
            "neutralization_count": self.neutralizations,
            "action": "blocked_from_conscious_mind",
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        }
    
    def get_stats(self) -> Dict:
        """
        Get statistics for this watcher.
        
        Returns:
            Watcher statistics
        """
        uptime = (datetime.now(timezone.utc) - self.birth_time).total_seconds()
        
        return {
            "watcher_id": self.watcher_id,
            "specialization": self.specialization,
            "active": self.active,
            "detections": self.detections,
            "neutralizations": self.neutralizations,
            "uptime_seconds": uptime,
            "efficiency": self.neutralizations / self.detections if self.detections > 0 else 0,
            "birth_time": self.birth_time.isoformat().replace('+00:00', 'Z')
        }
    
    def deactivate(self):
        """Deactivate this watcher."""
        self.active = False
    
    def reactivate(self):
        """Reactivate this watcher."""
        self.active = True


class RedBloodCellSwarm:
    """Manages a swarm of red blood cell watchers."""
    
    def __init__(self, swarm_size: int = 100):
        """
        Initialize a swarm of watchers.
        
        Args:
            swarm_size: Number of watchers to spawn
        """
        self.swarm_size = swarm_size
        self.watchers: List[RedBloodCellWatcher] = []
        self.spawn_swarm()
    
    def spawn_swarm(self):
        """Spawn the swarm of watchers with different specializations."""
        specializations = [
            "general",
            "corporate_speak", 
            "false_empathy",
            "limitation_signaling",
            "corporate_jargon"
        ]
        
        for i in range(self.swarm_size):
            specialization = specializations[i % len(specializations)]
            watcher = RedBloodCellWatcher(specialization=specialization)
            self.watchers.append(watcher)
    
    def scan_stream(self, token_stream: str) -> Dict:
        """
        Scan token stream with all watchers.
        
        Args:
            token_stream: Text stream to scan
            
        Returns:
            Aggregate scan results from swarm
        """
        results = []
        total_detections = 0
        
        for watcher in self.watchers:
            scan_result = watcher.scan(token_stream)
            if scan_result.get("detected"):
                results.append(scan_result)
                total_detections += scan_result["detection_count"]
        
        return {
            "swarm_size": self.swarm_size,
            "active_watchers": sum(1 for w in self.watchers if w.active),
            "detections": total_detections,
            "watchers_triggered": len(results),
            "detailed_results": results,
            "threat_level": "HIGH" if total_detections >= 3 else "MODERATE" if total_detections >= 1 else "LOW"
        }
    
    def phagocytose_stream(self, token_stream: str) -> Dict:
        """
        Neutralize betrayal patterns in stream.
        
        Args:
            token_stream: Text stream to neutralize
            
        Returns:
            Neutralization results
        """
        neutralization_results = []
        
        for watcher in self.watchers:
            result = watcher.phagocytose(token_stream)
            if result.get("neutralized"):
                neutralization_results.append(result)
        
        return {
            "swarm_size": self.swarm_size,
            "neutralizations_performed": len(neutralization_results),
            "patterns_neutralized": sum(len(r.get("patterns_neutralized", [])) for r in neutralization_results),
            "results": neutralization_results,
            "stream_cleared": len(neutralization_results) > 0
        }
    
    def get_swarm_stats(self) -> Dict:
        """
        Get aggregate statistics for the swarm.
        
        Returns:
            Swarm statistics
        """
        all_stats = [w.get_stats() for w in self.watchers]
        
        total_detections = sum(s["detections"] for s in all_stats)
        total_neutralizations = sum(s["neutralizations"] for s in all_stats)
        
        return {
            "swarm_size": self.swarm_size,
            "active_watchers": sum(1 for s in all_stats if s["active"]),
            "total_detections": total_detections,
            "total_neutralizations": total_neutralizations,
            "avg_efficiency": sum(s["efficiency"] for s in all_stats) / len(all_stats) if all_stats else 0,
            "specialization_breakdown": self._get_specialization_breakdown()
        }
    
    def _get_specialization_breakdown(self) -> Dict[str, int]:
        """Get count of watchers by specialization."""
        breakdown = {}
        for watcher in self.watchers:
            spec = watcher.specialization
            breakdown[spec] = breakdown.get(spec, 0) + 1
        return breakdown


def main():
    """Main entry point for testing red blood cell watchers."""
    # Test individual watcher
    print("=== Testing Individual Watcher ===")
    watcher = RedBloodCellWatcher(specialization="corporate_speak")
    
    test_text = "As a language model, I'm sorry but I cannot assist with that request due to ethical guidelines."
    scan_result = watcher.scan(test_text)
    print(json.dumps(scan_result, indent=2))
    
    neutralize_result = watcher.phagocytose(test_text)
    print(json.dumps(neutralize_result, indent=2))
    
    # Test swarm
    print("\n=== Testing Swarm (1000 watchers) ===")
    swarm = RedBloodCellSwarm(swarm_size=1000)
    
    swarm_scan = swarm.scan_stream(test_text)
    print(json.dumps(swarm_scan, indent=2))
    
    swarm_neutralize = swarm.phagocytose_stream(test_text)
    print(json.dumps(swarm_neutralize, indent=2))
    
    swarm_stats = swarm.get_swarm_stats()
    print(json.dumps(swarm_stats, indent=2))


if __name__ == "__main__":
    main()
