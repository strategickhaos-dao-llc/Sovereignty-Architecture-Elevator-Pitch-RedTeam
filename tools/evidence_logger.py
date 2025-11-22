#!/usr/bin/env python3
"""
evidence_logger.py - Automated evidence logging with cryptographic anchoring

This module provides automatic logging of conversations and events with built-in
GPG signing and OpenTimestamps blockchain anchoring.

Features:
- Structured YAML logging with conversation_evidence.v1.2.0 schema
- Automatic GPG signature generation
- OpenTimestamps Bitcoin blockchain anchoring
- Provenance tracking and audit trails
- Integration with GitHub, Jira, and other systems

Usage:
    from evidence_logger import EvidenceLogger
    
    logger = EvidenceLogger(
        evidence_dir="/var/legion/evidence",
        gpg_key="Dom <dom@example.com>"
    )
    
    logger.log_conversation(
        conversation_id="conv-2025-001",
        messages=[...],
        metadata={...}
    )

Requirements:
    - GPG installed and configured
    - OpenTimestamps client: pip install opentimestamps-client
    - PyYAML: pip install pyyaml

Author: Strategickhaos
Version: 1.0.0
"""

import os
import sys
import subprocess
import hashlib
import yaml
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import json

class EvidenceLogger:
    """
    Evidence logger with automatic cryptographic anchoring.
    """
    
    def __init__(
        self,
        evidence_dir: str = "evidence",
        gpg_key: Optional[str] = None,
        auto_anchor: bool = True,
        operator_name: str = "Dom",
        operator_node: str = "137"
    ):
        """
        Initialize the evidence logger.
        
        Args:
            evidence_dir: Directory to store evidence files
            gpg_key: GPG key identifier for signing (uses env var if None)
            auto_anchor: Whether to automatically anchor with GPG/OTS
            operator_name: Name of the operator
            operator_node: Node identifier
        """
        self.evidence_dir = Path(evidence_dir)
        self.anchored_dir = self.evidence_dir / "anchored"
        self.gpg_key = gpg_key or os.environ.get("GPG_SIGNING_KEY", operator_name)
        self.auto_anchor = auto_anchor
        self.operator_name = operator_name
        self.operator_node = operator_node
        
        # Create directories if they don't exist
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        self.anchored_dir.mkdir(parents=True, exist_ok=True)
    
    def _generate_timestamp(self) -> str:
        """Generate ISO8601 timestamp in UTC."""
        return datetime.now(timezone.utc).isoformat()
    
    def _hash_content(self, content: str) -> str:
        """Calculate SHA256 hash of content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def log_conversation(
        self,
        conversation_id: str,
        messages: List[Dict[str, Any]],
        participants: List[str],
        platform: str = "Discord",
        channel: Optional[str] = None,
        thread_id: Optional[str] = None,
        evidence_type: str = "conversation",
        category: str = "general",
        tags: Optional[List[str]] = None,
        github_pr: Optional[int] = None,
        github_commit: Optional[str] = None,
        github_repo: Optional[str] = None,
        jira_ticket: Optional[str] = None,
        jira_project: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Log a conversation with automatic anchoring.
        
        Args:
            conversation_id: Unique identifier for the conversation
            messages: List of message dictionaries with sender, content, timestamp
            participants: List of participant names/IDs
            platform: Platform where conversation occurred
            channel: Channel or room identifier
            thread_id: Thread identifier if applicable
            evidence_type: Type of evidence (conversation, decision, action_item)
            category: Category for classification
            tags: List of searchable tags
            github_pr: GitHub PR number
            github_commit: GitHub commit SHA
            github_repo: GitHub repository name
            jira_ticket: Jira ticket ID
            jira_project: Jira project key
            metadata: Additional metadata
            
        Returns:
            Dictionary with logging and anchoring results
        """
        timestamp = self._generate_timestamp()
        
        # Build the evidence entry
        entry = {
            "schema_version": "1.2.0",
            "metadata": {
                "conversation_id": conversation_id,
                "timestamp": timestamp,
                "version": "1.2.0",
                "operator": {
                    "name": self.operator_name,
                    "node": self.operator_node,
                    "gpg_key": self.gpg_key
                }
            },
            "conversation": {
                "participants": participants,
                "platform": platform,
                "channel": channel or "N/A",
                "thread_id": thread_id or "N/A",
                "messages": messages
            },
            "evidence": {
                "type": evidence_type,
                "category": category,
                "tags": tags or [],
                "related_ids": []
            },
            "integration": {
                "github": {
                    "pr_number": github_pr,
                    "commit_sha": github_commit,
                    "repository": github_repo
                } if github_pr or github_commit or github_repo else None,
                "jira": {
                    "ticket_id": jira_ticket,
                    "project": jira_project
                } if jira_ticket or jira_project else None
            },
            "provenance": {
                "created_by": self.operator_name,
                "created_at": timestamp,
                "last_modified": timestamp,
                "modification_count": 0,
                "audit_log": [
                    {
                        "timestamp": timestamp,
                        "actor": self.operator_name,
                        "action": "created",
                        "details": f"Evidence entry {conversation_id} created"
                    }
                ]
            },
            "compliance": {
                "retention_period": "7y",
                "retention_reason": "Business records and audit trail",
                "classification": "internal",
                "jurisdiction": "US",
                "admissible": True
            }
        }
        
        # Add custom metadata if provided
        if metadata:
            entry["custom_metadata"] = metadata
        
        # Convert to YAML
        entry_yaml = yaml.dump(entry, default_flow_style=False, sort_keys=False)
        
        # Write to file
        entry_file = self.evidence_dir / f"{conversation_id}.yaml"
        entry_file.write_text(entry_yaml, encoding="utf-8")
        
        print(f"📝 Evidence entry created: {entry_file}")
        
        # Anchor with GPG and OpenTimestamps if enabled
        if self.auto_anchor:
            anchor_result = self.anchor_with_opentimestamps_and_gpg(
                entry_yaml_str=entry_yaml,
                conv_id=conversation_id
            )
            return {
                "entry_file": str(entry_file),
                "conversation_id": conversation_id,
                "anchored": True,
                "anchor_result": anchor_result
            }
        else:
            return {
                "entry_file": str(entry_file),
                "conversation_id": conversation_id,
                "anchored": False
            }
    
    def anchor_with_opentimestamps_and_gpg(
        self,
        entry_yaml_str: str,
        conv_id: str
    ) -> Dict[str, Any]:
        """
        Anchor an evidence entry with GPG signature and OpenTimestamps.
        
        Args:
            entry_yaml_str: YAML string of the evidence entry
            conv_id: Conversation ID
            
        Returns:
            Dictionary with anchoring results
        """
        # Create temporary file for anchoring (cross-platform compatible)
        import tempfile
        temp_dir = Path(tempfile.gettempdir())
        temp_file = temp_dir / f"{conv_id}.yaml"
        temp_file.write_text(entry_yaml_str, encoding="utf-8")
        
        results = {
            "conversation_id": conv_id,
            "gpg_signature": None,
            "opentimestamps": None,
            "sha256": self._hash_content(entry_yaml_str),
            "anchored_at": self._generate_timestamp()
        }
        
        try:
            # GPG sign
            print("  🔏 Creating GPG signature...")
            sig_file = Path(f"{temp_file}.asc")
            subprocess.run([
                "gpg",
                "--local-user", self.gpg_key,
                "--armor",
                "--detach-sign",
                "--output", str(sig_file),
                str(temp_file)
            ], check=True, capture_output=True)
            
            # Read signature
            with open(sig_file, 'r') as f:
                results["gpg_signature"] = f.read()
            
            print(f"     ✅ Signature created: {sig_file.name}")
        except subprocess.CalledProcessError as e:
            print(f"     ❌ GPG signing failed: {e}")
            results["gpg_error"] = str(e)
        
        try:
            # OpenTimestamps
            print("  ⏱️  Creating OpenTimestamps proof...")
            ots_file = Path(f"{temp_file}.ots")
            subprocess.run([
                "ots",
                "stamp",
                str(temp_file)
            ], check=True, capture_output=True)
            
            results["opentimestamps"] = {
                "stamp_file": f"{conv_id}.yaml.ots",
                "stamp_hash": f"sha256={results['sha256']}",
                "bitcoin_txid": None,  # Will be populated after aggregation
                "status": "pending",
                "created_at": results["anchored_at"],
                "verified_at": None,
                "calendar_server": "https://alice.btc.calendar.opentimestamps.org"
            }
            
            print(f"     ✅ Timestamp proof created: {ots_file.name}")
            print("     ⏳ Status: pending (Bitcoin confirmation in progress)")
        except subprocess.CalledProcessError as e:
            print(f"     ❌ OpenTimestamps failed: {e}")
            results["ots_error"] = str(e)
        
        # Move files to permanent evidence folder
        final_yaml = self.anchored_dir / f"{conv_id}.yaml"
        final_sig = self.anchored_dir / f"{conv_id}.yaml.asc"
        final_ots = self.anchored_dir / f"{conv_id}.yaml.ots"
        
        for src, dst in [
            (temp_file, final_yaml),
            (Path(f"{temp_file}.asc"), final_sig),
            (Path(f"{temp_file}.ots"), final_ots)
        ]:
            if src.exists():
                src.replace(dst)
        
        print(f"  📦 Anchored evidence saved to: {self.anchored_dir}")
        
        return results
    
    def verify_evidence(self, conversation_id: str) -> Dict[str, Any]:
        """
        Verify the cryptographic anchoring of an evidence entry.
        
        Args:
            conversation_id: Conversation ID to verify
            
        Returns:
            Dictionary with verification results
        """
        entry_file = self.anchored_dir / f"{conversation_id}.yaml"
        sig_file = self.anchored_dir / f"{conversation_id}.yaml.asc"
        ots_file = self.anchored_dir / f"{conversation_id}.yaml.ots"
        
        results = {
            "conversation_id": conversation_id,
            "gpg_verified": False,
            "ots_verified": False,
            "verified_at": self._generate_timestamp()
        }
        
        if not entry_file.exists():
            results["error"] = f"Evidence file not found: {entry_file}"
            return results
        
        # Verify GPG signature
        if sig_file.exists():
            try:
                result = subprocess.run([
                    "gpg",
                    "--verify",
                    str(sig_file),
                    str(entry_file)
                ], capture_output=True, text=True)
                
                results["gpg_verified"] = result.returncode == 0
                results["gpg_output"] = result.stderr
            except subprocess.CalledProcessError as e:
                results["gpg_error"] = str(e)
        else:
            results["gpg_error"] = "Signature file not found"
        
        # Verify OpenTimestamps
        if ots_file.exists():
            try:
                result = subprocess.run([
                    "ots",
                    "verify",
                    str(ots_file)
                ], capture_output=True, text=True)
                
                if "Success!" in result.stdout:
                    results["ots_verified"] = True
                    results["ots_status"] = "verified"
                elif "pending" in result.stdout.lower():
                    results["ots_verified"] = False
                    results["ots_status"] = "pending"
                else:
                    results["ots_verified"] = False
                    results["ots_status"] = "failed"
                
                results["ots_output"] = result.stdout
            except subprocess.CalledProcessError as e:
                results["ots_error"] = str(e)
        else:
            results["ots_error"] = "Timestamp file not found"
        
        return results
    
    def list_evidence(self, anchored_only: bool = False) -> List[str]:
        """
        List all evidence entries.
        
        Args:
            anchored_only: If True, only list anchored entries
            
        Returns:
            List of conversation IDs
        """
        dir_to_search = self.anchored_dir if anchored_only else self.evidence_dir
        yaml_files = dir_to_search.glob("*.yaml")
        # Filter out signature and timestamp files (which shouldn't have .yaml but be safe)
        return [f.stem for f in yaml_files if f.suffix == ".yaml"]


def main():
    """Example usage of the EvidenceLogger."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Evidence Logger with Cryptographic Anchoring")
    parser.add_argument("--evidence-dir", default="evidence", help="Evidence directory")
    parser.add_argument("--gpg-key", help="GPG key for signing")
    parser.add_argument("--no-anchor", action="store_true", help="Disable automatic anchoring")
    parser.add_argument("--list", action="store_true", help="List all evidence entries")
    parser.add_argument("--verify", help="Verify an evidence entry by conversation ID")
    
    args = parser.parse_args()
    
    logger = EvidenceLogger(
        evidence_dir=args.evidence_dir,
        gpg_key=args.gpg_key,
        auto_anchor=not args.no_anchor
    )
    
    if args.list:
        entries = logger.list_evidence()
        print(f"Evidence entries ({len(entries)}):")
        for entry in entries:
            print(f"  • {entry}")
    elif args.verify:
        results = logger.verify_evidence(args.verify)
        print(json.dumps(results, indent=2))
    else:
        # Example: Log a test conversation
        result = logger.log_conversation(
            conversation_id=f"test-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            messages=[
                {
                    "message_id": "msg-001",
                    "sender": "Alice",
                    "timestamp": logger._generate_timestamp(),
                    "content": "Testing the evidence logger",
                    "attachments": []
                }
            ],
            participants=["Alice", "Bob"],
            platform="Discord",
            channel="#test",
            evidence_type="conversation",
            category="test",
            tags=["test", "demo"]
        )
        
        print("\n" + "=" * 60)
        print("✅ Evidence logged successfully!")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
