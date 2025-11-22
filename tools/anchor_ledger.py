#!/usr/bin/env python3
"""
Ledger Anchoring Tool - GPG + OpenTimestamps
Strategickhaos DAO LLC

One-click script to:
1. Sign any ledger entry with GPG (detached signature)
2. Timestamp it on Bitcoin blockchain via OpenTimestamps
3. Create mathematically unbreakable proof of existence

Usage:
    python anchor_ledger.py <file_path> [--gpg-key <email>]
    python anchor_ledger.py --verify <file_path>
"""

import argparse
import hashlib
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple


class LedgerAnchor:
    """Handles GPG signing and OpenTimestamps anchoring for ledger entries."""
    
    def __init__(self, gpg_key: str = "dom@strategickhaos.com"):
        self.gpg_key = gpg_key
        
    def hash_file(self, file_path: Path) -> str:
        """Calculate SHA256 hash of a file."""
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()
    
    def gpg_sign(self, file_path: Path) -> Tuple[bool, str]:
        """
        Create GPG detached signature for a file.
        
        Returns:
            Tuple of (success: bool, signature_path or error_message: str)
        """
        signature_path = Path(str(file_path) + ".asc")
        
        try:
            result = subprocess.run([
                "gpg", 
                "--local-user", self.gpg_key,
                "--armor",
                "--detach-sign",
                "--output", str(signature_path),
                str(file_path)
            ], 
            check=True,
            capture_output=True,
            text=True)
            
            return True, str(signature_path)
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr or str(e)
            return False, f"GPG signing failed: {error_msg}"
        except FileNotFoundError:
            return False, "GPG not found. Please install GPG: apt-get install gnupg or brew install gnupg"
    
    def opentimestamps_stamp(self, file_path: Path) -> Tuple[bool, str]:
        """
        Create OpenTimestamps proof for a file.
        
        Returns:
            Tuple of (success: bool, ots_path or error_message: str)
        """
        ots_path = Path(str(file_path) + ".ots")
        
        try:
            result = subprocess.run([
                "ots",
                "stamp",
                str(file_path)
            ],
            check=True,
            capture_output=True,
            text=True)
            
            return True, str(ots_path)
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr or str(e)
            return False, f"OpenTimestamps stamping failed: {error_msg}"
        except FileNotFoundError:
            return False, "OpenTimestamps CLI not found. Install: pip install opentimestamps-client"
    
    def opentimestamps_verify(self, ots_path: Path) -> Tuple[bool, str]:
        """
        Verify an OpenTimestamps proof.
        
        Returns:
            Tuple of (success: bool, result_message: str)
        """
        try:
            result = subprocess.run([
                "ots",
                "verify",
                str(ots_path)
            ],
            check=True,
            capture_output=True,
            text=True)
            
            return True, result.stdout
            
        except subprocess.CalledProcessError as e:
            # OTS returns non-zero when timestamp is pending
            if "pending" in (e.stdout + e.stderr).lower():
                return True, "Timestamp pending - Bitcoin block not yet confirmed. Try again later."
            error_msg = e.stderr or str(e)
            return False, f"Verification failed: {error_msg}"
    
    def opentimestamps_upgrade(self, ots_path: Path) -> Tuple[bool, str]:
        """
        Upgrade OpenTimestamps proof with calendar aggregation.
        
        Returns:
            Tuple of (success: bool, result_message: str)
        """
        try:
            result = subprocess.run([
                "ots",
                "upgrade",
                str(ots_path)
            ],
            check=True,
            capture_output=True,
            text=True)
            
            return True, "Timestamp upgraded successfully"
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr or str(e)
            return False, f"Upgrade failed: {error_msg}"
    
    def anchor(self, file_path: Path) -> dict:
        """
        Complete anchoring process: sign + timestamp a file.
        
        Returns:
            Dictionary with results of all operations
        """
        if not file_path.exists():
            return {
                "success": False,
                "error": f"File not found: {file_path}"
            }
        
        file_hash = self.hash_file(file_path)
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        # GPG signature
        gpg_success, gpg_result = self.gpg_sign(file_path)
        
        # OpenTimestamps
        ots_success, ots_result = self.opentimestamps_stamp(file_path)
        
        results = {
            "success": gpg_success and ots_success,
            "file": str(file_path),
            "sha256": file_hash,
            "timestamp": timestamp,
            "gpg": {
                "success": gpg_success,
                "result": gpg_result
            },
            "opentimestamps": {
                "success": ots_success,
                "result": ots_result
            }
        }
        
        return results
    
    def verify(self, file_path: Path) -> dict:
        """
        Verify signatures and timestamps for a file.
        
        Returns:
            Dictionary with verification results
        """
        if not file_path.exists():
            return {
                "success": False,
                "error": f"File not found: {file_path}"
            }
        
        signature_path = Path(str(file_path) + ".asc")
        ots_path = Path(str(file_path) + ".ots")
        
        results = {
            "file": str(file_path),
            "sha256": self.hash_file(file_path),
            "gpg": {},
            "opentimestamps": {}
        }
        
        # Verify GPG signature
        if signature_path.exists():
            try:
                result = subprocess.run([
                    "gpg",
                    "--verify",
                    str(signature_path),
                    str(file_path)
                ],
                check=True,
                capture_output=True,
                text=True)
                results["gpg"]["success"] = True
                results["gpg"]["result"] = "Signature verified"
            except subprocess.CalledProcessError as e:
                results["gpg"]["success"] = False
                results["gpg"]["result"] = f"Signature verification failed: {e.stderr}"
        else:
            results["gpg"]["success"] = False
            results["gpg"]["result"] = "No signature file found"
        
        # Verify OpenTimestamps
        if ots_path.exists():
            ots_success, ots_message = self.opentimestamps_verify(ots_path)
            results["opentimestamps"]["success"] = ots_success
            results["opentimestamps"]["result"] = ots_message
        else:
            results["opentimestamps"]["success"] = False
            results["opentimestamps"]["result"] = "No timestamp file found"
        
        results["success"] = results["gpg"]["success"] and results["opentimestamps"]["success"]
        
        return results


def print_results(results: dict, verify_mode: bool = False):
    """Print results in a human-readable format."""
    
    if not results.get("success"):
        print(f"❌ {'Verification' if verify_mode else 'Anchoring'} failed")
        if "error" in results:
            print(f"   Error: {results['error']}")
        return
    
    print(f"✅ {'Verified' if verify_mode else 'Anchored'}: {results['file']}")
    print(f"   SHA256: {results['sha256']}")
    
    if not verify_mode and "timestamp" in results:
        print(f"   Timestamp: {results['timestamp']}")
    
    # GPG results
    if results["gpg"]["success"]:
        print(f"   ✓ GPG Signature: {results['gpg']['result']}")
    else:
        print(f"   ✗ GPG Signature: {results['gpg']['result']}")
    
    # OpenTimestamps results
    if results["opentimestamps"]["success"]:
        print(f"   ✓ OpenTimestamps: {results['opentimestamps']['result']}")
    else:
        print(f"   ✗ OpenTimestamps: {results['opentimestamps']['result']}")
    
    if not verify_mode:
        print("\nNext steps:")
        print("  • Run verification: python anchor_ledger.py --verify <file>")
        print("  • Weekly upgrade (improves proof speed): ots upgrade *.ots")
        print("  • Share proof files (.asc, .ots) with auditors/courts")


def main():
    parser = argparse.ArgumentParser(
        description="Anchor ledger entries with GPG + OpenTimestamps",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Anchor a file
  python anchor_ledger.py evidence/conversation_ledger.yaml

  # Anchor with specific GPG key
  python anchor_ledger.py evidence/entry.yaml --gpg-key "dom@example.com"

  # Verify an anchored file
  python anchor_ledger.py --verify evidence/conversation_ledger.yaml

  # Upgrade timestamps (run weekly)
  ots upgrade evidence/anchored/*.ots
        """
    )
    
    parser.add_argument(
        "file",
        type=str,
        help="Path to the file to anchor or verify"
    )
    
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify existing signatures and timestamps"
    )
    
    parser.add_argument(
        "--gpg-key",
        type=str,
        default="dom@strategickhaos.com",
        help="GPG key email/ID to use for signing (default: dom@strategickhaos.com)"
    )
    
    args = parser.parse_args()
    
    file_path = Path(args.file)
    anchor = LedgerAnchor(gpg_key=args.gpg_key)
    
    if args.verify:
        results = anchor.verify(file_path)
        print_results(results, verify_mode=True)
    else:
        results = anchor.anchor(file_path)
        print_results(results, verify_mode=False)
    
    sys.exit(0 if results.get("success") else 1)


if __name__ == "__main__":
    main()
