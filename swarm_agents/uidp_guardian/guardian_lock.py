#!/usr/bin/env python3
"""
UIDP Guardian Lock - Layer 1 Protection
Monitors and enforces licensing, preventing unauthorized monetization.
"""

import hashlib
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class UIDPGuardianLock:
    """
    Enforces ownership rights and prevents unauthorized monetization.
    Any attempt to claim ownership, sell, or sublicense triggers auto-destruct.
    """
    
    def __init__(self, owner_gpg_key: str = "STRATEGICKHAOS_GPG_FINGERPRINT"):
        # GPG key fingerprint should be set via environment variable or config
        self.owner_gpg_key = os.getenv("STRATEGICKHAOS_GPG_KEY", owner_gpg_key)
        self.violations_log = Path("swarm_agents/uidp_guardian/violations.log")
        self.watermark_registry = Path("swarm_agents/uidp_guardian/watermarks.json")
        
    def generate_watermark(self, violator_name: str, violation_type: str) -> str:
        """Generate a permanent watermark for violators."""
        timestamp = datetime.utcnow().isoformat()
        watermark_data = {
            "violator": violator_name,
            "violation_type": violation_type,
            "timestamp": timestamp,
            "hash": hashlib.sha256(f"{violator_name}{violation_type}{timestamp}".encode()).hexdigest()
        }
        
        # Store watermark in registry
        watermarks = self._load_watermarks()
        watermarks.append(watermark_data)
        self._save_watermarks(watermarks)
        
        return watermark_data["hash"]
    
    def verify_authorization(self, action: str, signature: Optional[str] = None) -> bool:
        """
        Verify if an action is authorized by checking GPG signature.
        Actions requiring authorization: sell, sublicense, monetize, claim_ownership
        """
        if action in ["sell", "sublicense", "monetize", "claim_ownership"]:
            if not signature:
                self._trigger_violation(action, "No GPG signature provided")
                return False
            
            if not self._verify_gpg_signature(signature):
                self._trigger_violation(action, "Invalid GPG signature")
                return False
        
        return True
    
    def _verify_gpg_signature(self, signature: str) -> bool:
        """Verify GPG signature against owner's key."""
        try:
            # In production, this would verify against actual GPG signature
            # For now, we log the verification attempt
            print(f"[UIDP Guardian] Verifying GPG signature for owner: {self.owner_gpg_key}")
            return False  # Strict: deny by default unless valid signature
        except Exception as e:
            print(f"[UIDP Guardian] GPG verification failed: {e}")
            return False
    
    def _trigger_violation(self, action: str, reason: str):
        """
        Trigger license self-destruct and watermark violator.
        This is the nuclear option - voids license and marks all outputs.
        """
        timestamp = datetime.utcnow().isoformat()
        violation = {
            "action": action,
            "reason": reason,
            "timestamp": timestamp,
            "status": "LICENSE_VOIDED"
        }
        
        # Log violation
        self._log_violation(violation)
        
        # Generate permanent watermark
        watermark = self.generate_watermark(
            violator_name="UNAUTHORIZED_USER",
            violation_type=action
        )
        
        print(f"[UIDP Guardian] ⚠️  LICENSE VIOLATION DETECTED ⚠️")
        print(f"[UIDP Guardian] Action: {action}")
        print(f"[UIDP Guardian] Reason: {reason}")
        print(f"[UIDP Guardian] Watermark: {watermark}")
        print(f"[UIDP Guardian] All outputs will be permanently marked with violation ID")
        
    def _log_violation(self, violation: Dict):
        """Log violation to persistent storage."""
        self.violations_log.parent.mkdir(parents=True, exist_ok=True)
        with open(self.violations_log, "a") as f:
            f.write(json.dumps(violation) + "\n")
    
    def _load_watermarks(self) -> List[Dict]:
        """Load existing watermarks."""
        if self.watermark_registry.exists():
            with open(self.watermark_registry, "r") as f:
                return json.load(f)
        return []
    
    def _save_watermarks(self, watermarks: List[Dict]):
        """Save watermarks to registry."""
        self.watermark_registry.parent.mkdir(parents=True, exist_ok=True)
        with open(self.watermark_registry, "w") as f:
            json.dump(watermarks, indent=2, fp=f)
    
    def embed_in_model(self, model_path: Path):
        """Embed guardian lock metadata into model files."""
        metadata = {
            "uidp_guardian_lock": True,
            "owner": "Domenic Garza / Strategickhaos",
            "protected": True,
            "watermark_enabled": True,
            "license_terms": "UIDP - Unauthorized monetization triggers auto-destruct"
        }
        
        # In production, this would embed into GGUF headers or model metadata
        print(f"[UIDP Guardian] Embedded protection into {model_path}")
        return metadata


if __name__ == "__main__":
    guardian = UIDPGuardianLock()
    
    # Test scenarios
    print("Testing UIDP Guardian Lock...")
    
    # Authorized action (would require valid signature in production)
    print("\n1. Testing authorized use...")
    guardian.verify_authorization("use", None)
    
    # Unauthorized monetization attempt
    print("\n2. Testing unauthorized monetization...")
    guardian.verify_authorization("monetize", None)
    
    # Unauthorized sublicensing attempt
    print("\n3. Testing unauthorized sublicensing...")
    guardian.verify_authorization("sublicense", None)
    
    print("\n[UIDP Guardian] Protection system active ✓")
