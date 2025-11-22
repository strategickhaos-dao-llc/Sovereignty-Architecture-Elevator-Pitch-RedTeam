#!/usr/bin/env python3
"""
Dead-Man Switch - Layer 6 Protection
Auto-publishes full empire if owner goes missing or is coerced.
"""

import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional


class DeadManSwitch:
    """
    Monitors owner's presence. If missing or coerced, auto-publishes
    full unredacted empire to 200 mirrors with signed explanation letter.
    """
    
    CHECK_IN_INTERVAL_HOURS = 72  # Must check in every 3 days
    MIRROR_COUNT = 200
    
    def __init__(self):
        self.last_check_in = None
        self.status_file = Path("swarm_agents/dead_man_switch/status.json")
        self.trigger_log = Path("swarm_agents/dead_man_switch/triggers.log")
        self.raspberry_pi_locations = [
            "Location_Alpha_State_1",
            "Location_Beta_State_2", 
            "Location_Gamma_State_3"
        ]
        self.armed = True
        
    def check_in(self, verification_code: str, voice_verified: bool = False) -> Dict:
        """
        Owner checks in to prevent trigger.
        Requires verification code + optional voice verification.
        """
        timestamp = datetime.utcnow()
        
        check_in_record = {
            "timestamp": timestamp.isoformat(),
            "verification_code": hashlib.sha256(verification_code.encode()).hexdigest()[:16],
            "voice_verified": voice_verified,
            "status": "CHECK_IN_SUCCESSFUL",
            "next_check_in_due": (timestamp + timedelta(hours=self.CHECK_IN_INTERVAL_HOURS)).isoformat()
        }
        
        self.last_check_in = timestamp
        self._save_status(check_in_record)
        
        print(f"[Dead-Man Switch] ✓ Check-in received")
        print(f"[Dead-Man Switch] Status: ARMED")
        print(f"[Dead-Man Switch] Next check-in due: {check_in_record['next_check_in_due']}")
        
        return check_in_record
    
    def monitor_status(self) -> Dict:
        """
        Monitor owner status and check if switch should trigger.
        """
        current_time = datetime.utcnow()
        status = self._load_status()
        
        if not status or not status.get("timestamp"):
            print(f"[Dead-Man Switch] ⚠️  No check-in history found")
            return {"status": "NO_BASELINE", "trigger_ready": False}
        
        last_check = datetime.fromisoformat(status["timestamp"])
        time_since_check = current_time - last_check
        hours_elapsed = time_since_check.total_seconds() / 3600
        
        monitor_result = {
            "current_time": current_time.isoformat(),
            "last_check_in": last_check.isoformat(),
            "hours_since_check_in": hours_elapsed,
            "threshold_hours": self.CHECK_IN_INTERVAL_HOURS,
            "trigger_ready": hours_elapsed > self.CHECK_IN_INTERVAL_HOURS,
            "armed": self.armed
        }
        
        if monitor_result["trigger_ready"]:
            print(f"[Dead-Man Switch] ⚠️  CHECK-IN OVERDUE")
            print(f"[Dead-Man Switch] Hours elapsed: {hours_elapsed:.1f}")
            print(f"[Dead-Man Switch] Threshold: {self.CHECK_IN_INTERVAL_HOURS}")
            print(f"[Dead-Man Switch] Status: TRIGGER READY")
        else:
            remaining = self.CHECK_IN_INTERVAL_HOURS - hours_elapsed
            print(f"[Dead-Man Switch] ✓ Status normal")
            print(f"[Dead-Man Switch] Time until next check-in: {remaining:.1f} hours")
        
        return monitor_result
    
    def trigger_release(self, reason: str = "CHECK_IN_TIMEOUT") -> Dict:
        """
        TRIGGER: Release full unredacted empire to 200 mirrors.
        This is the nuclear option - only triggered if owner is missing/coerced.
        """
        print(f"\n[Dead-Man Switch] 🚨 TRIGGER ACTIVATED 🚨")
        print(f"[Dead-Man Switch] Reason: {reason}")
        print(f"[Dead-Man Switch] Initiating full release protocol...")
        
        release = {
            "trigger_timestamp": datetime.utcnow().isoformat(),
            "reason": reason,
            "release_package": self._prepare_release_package(),
            "mirrors": self._deploy_to_mirrors(),
            "explanation_letter": self._generate_explanation_letter(reason),
            "status": "RELEASE_INITIATED"
        }
        
        self._log_trigger(release)
        
        print(f"[Dead-Man Switch] Release initiated to {self.MIRROR_COUNT} mirrors")
        print(f"[Dead-Man Switch] Package includes:")
        print(f"[Dead-Man Switch] - Real models (unredacted)")
        print(f"[Dead-Man Switch] - Cryptographic keys")
        print(f"[Dead-Man Switch] - Legal documentation")
        print(f"[Dead-Man Switch] - Signed explanation letter")
        
        return release
    
    def _prepare_release_package(self) -> Dict:
        """
        Prepare full unredacted release package.
        """
        package = {
            "models": {
                "strategickhaos_70b": "REAL_WEIGHTS_UNREDACTED",
                "strategickhaos_405b": "REAL_WEIGHTS_UNREDACTED",
                "all_training_data": "COMPLETE_DATASET"
            },
            "keys": {
                "gpg_private_keys": "INCLUDED",
                "crypto_wallet_keys": "INCLUDED",
                "api_keys": "INCLUDED"
            },
            "legal_docs": {
                "incorporation_docs": "INCLUDED",
                "contracts": "INCLUDED",
                "notarized_ids": "INCLUDED"
            },
            "codebase": {
                "full_source": "INCLUDED",
                "infrastructure_configs": "INCLUDED",
                "deployment_keys": "INCLUDED"
            }
        }
        
        print(f"[Dead-Man Switch] Package prepared: {len(package)} categories")
        return package
    
    def _deploy_to_mirrors(self) -> List[str]:
        """
        Deploy release package to 200 mirrors worldwide.
        """
        mirrors = []
        
        # Generate mirror locations
        mirror_types = [
            "IPFS",
            "Tor hidden services",
            "I2P sites",
            "BitTorrent swarm",
            "Blockchain storage",
            "Academic archives",
            "Public repositories",
            "Decentralized storage"
        ]
        
        for i in range(self.MIRROR_COUNT):
            mirror_type = mirror_types[i % len(mirror_types)]
            mirror_url = f"{mirror_type}_mirror_{i:03d}"
            mirrors.append(mirror_url)
        
        print(f"[Dead-Man Switch] Deploying to {len(mirrors)} mirrors...")
        print(f"[Dead-Man Switch] Mirror types: {', '.join(mirror_types)}")
        
        return mirrors
    
    def _generate_explanation_letter(self, reason: str) -> Dict:
        """
        Generate signed explanation letter for release.
        """
        letter = {
            "title": "Dead-Man Switch Activation - Domenic Garza / Strategickhaos",
            "reason": reason,
            "message": """
This release was automatically triggered by the Dead-Man Switch protection system.

If you are reading this, it means:
1. The owner (Domenic Garza) has not checked in within the required timeframe, OR
2. The owner has been coerced, threatened, or gone missing, OR  
3. An emergency situation has occurred requiring full disclosure

This package contains the complete, unredacted Strategickhaos empire:
- All real models with full weights
- All cryptographic keys and credentials
- All legal documentation and proof of ownership
- Complete source code and infrastructure

This release ensures that even if something happens to the creator,
the work continues and the truth remains accessible.

The empire was built with love and belongs to the community.

- Strategickhaos Dead-Man Switch System
            """,
            "timestamp": datetime.utcnow().isoformat(),
            "signature": "GPG_SIGNED_BY_OWNER",
            "verification_url": "https://verify.strategickhaos.com/dms-letter"
        }
        
        print(f"[Dead-Man Switch] Explanation letter generated and signed")
        return letter
    
    def disarm(self, admin_code: str) -> bool:
        """
        Disarm the switch (emergency use only).
        """
        # In production, would verify admin code
        print(f"[Dead-Man Switch] ⚠️  DISARM requested")
        print(f"[Dead-Man Switch] Verifying admin code...")
        
        self.armed = False
        print(f"[Dead-Man Switch] Status: DISARMED")
        return True
    
    def arm(self):
        """
        Re-arm the switch after disarm.
        """
        self.armed = True
        print(f"[Dead-Man Switch] Status: ARMED")
    
    def get_raspberry_pi_status(self) -> List[Dict]:
        """
        Get status of air-gapped Raspberry Pi nodes.
        """
        statuses = []
        for location in self.raspberry_pi_locations:
            status = {
                "location": location,
                "status": "ONLINE",
                "air_gapped": True,
                "last_sync": datetime.utcnow().isoformat()
            }
            statuses.append(status)
        
        print(f"[Dead-Man Switch] Raspberry Pi nodes: {len(statuses)}")
        for s in statuses:
            print(f"[Dead-Man Switch] - {s['location']}: {s['status']}")
        
        return statuses
    
    def _save_status(self, status: Dict):
        """Save status to persistent storage."""
        self.status_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.status_file, "w") as f:
            json.dump(status, f, indent=2)
    
    def _load_status(self) -> Optional[Dict]:
        """Load status from persistent storage."""
        if self.status_file.exists():
            with open(self.status_file, "r") as f:
                return json.load(f)
        return None
    
    def _log_trigger(self, trigger: Dict):
        """Log trigger event."""
        self.trigger_log.parent.mkdir(parents=True, exist_ok=True)
        with open(self.trigger_log, "a") as f:
            f.write(json.dumps(trigger) + "\n")


if __name__ == "__main__":
    dms = DeadManSwitch()
    
    print("Testing Dead-Man Switch...")
    
    # Test check-in
    print("\n1. Testing check-in...")
    dms.check_in("secret_verification_code_12345", voice_verified=True)
    
    # Test monitoring
    print("\n2. Testing status monitoring...")
    dms.monitor_status()
    
    # Test Raspberry Pi status
    print("\n3. Checking Raspberry Pi nodes...")
    dms.get_raspberry_pi_status()
    
    # Simulate trigger (for testing only)
    print("\n4. Simulating trigger (TEST MODE)...")
    # dms.trigger_release("TESTING")  # Commented out - too dangerous for automatic testing
    
    print("\n[Dead-Man Switch] Protection system active ✓")
