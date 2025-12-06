#!/usr/bin/env python3
"""
AI Conversation Evidence Logger
Legal-grade, cryptographically-chained audit trail for AI-assisted work

Usage:
    python evidence_logger.py "https://claude.ai/share/..."
    python evidence_logger.py --interactive
"""

import argparse
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional
import yaml


class ConversationEvidenceLogger:
    """Manages cryptographically-chained evidence ledger for AI conversations"""
    
    def __init__(self, base_dir: Path = None):
        if base_dir is None:
            base_dir = Path(__file__).parent / "evidence"
        
        self.base_dir = Path(base_dir)
        self.ledger_file = self.base_dir / "conversation_ledger.yaml"
        self.conversations_dir = self.base_dir / "conversations"
        self.screenshots_dir = self.base_dir / "screenshots"
        self.schemas_dir = self.base_dir / "schemas"
        
        # Ensure directories exist
        for directory in [self.conversations_dir, self.screenshots_dir, self.schemas_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _infer_interface(self, url: Optional[str]) -> str:
        """Infer the interface from the share URL
        
        Note: This is informational classification only, not security validation.
        The URL matching is intentionally simple for provider detection.
        CodeQL alerts about substring matching are false positives in this context.
        """
        if not url:
            return "local"
        
        url_lower = url.lower()
        if "claude.ai" in url_lower:
            return "claude.ai"
        if "chatgpt.com" in url_lower or "openai.com" in url_lower:
            return "chatgpt.com"
        # Be specific with x.ai patterns to avoid false matches
        if "grok.x.ai" in url_lower or "x.com/i/grok" in url_lower:
            return "grok.x.ai"
        if "poe.com" in url_lower:
            return "poe.com"
        if "gemini.google.com" in url_lower or "bard.google.com" in url_lower:
            return "gemini.google.com"
        
        return "unknown"
    
    def _infer_provider_from_url(self, url: Optional[str]) -> str:
        """Infer the provider from the share URL
        
        Note: This is informational classification only, not security validation.
        The URL matching is intentionally simple for provider detection.
        CodeQL alerts about substring matching are false positives in this context.
        """
        if not url:
            return "other"
        
        url_lower = url.lower()
        
        # Check for specific patterns in order of specificity
        if "claude.ai" in url_lower:
            return "anthropic"
        if "chatgpt.com" in url_lower or "openai.com" in url_lower:
            return "openai"
        # Be specific with grok patterns to avoid false matches
        if "grok.x.ai" in url_lower or "x.com/i/grok" in url_lower:
            return "xai"
        if "gemini.google.com" in url_lower or "bard.google.com" in url_lower:
            return "google"
        if "poe.com" in url_lower:
            return "other"
        
        return "other"
    
    def _load_previous_hash(self) -> Optional[str]:
        """Load the hash of the most recent entry in the ledger"""
        if self.ledger_file.exists():
            with open(self.ledger_file, 'r') as f:
                ledger = yaml.safe_load(f) or {"conversations": []}
                if ledger.get("conversations"):
                    return ledger["conversations"][-1].get("integration", {}).get("ledger_hash")
        return None
    
    def _compute_ledger_hash(self, entry_dict: Dict) -> str:
        """Compute SHA3-256 hash of the canonical YAML representation"""
        # Create a deterministic canonical representation
        canonical = yaml.dump(entry_dict, sort_keys=True, default_flow_style=False)
        return hashlib.sha3_256(canonical.encode('utf-8')).hexdigest()
    
    def _load_ledger(self) -> Dict:
        """Load existing ledger or create new one"""
        if self.ledger_file.exists():
            with open(self.ledger_file, 'r') as f:
                return yaml.safe_load(f) or {"conversations": []}
        return {
            "version": "1.1.0",
            "schema": "conversation_evidence.v1.1.0.yaml",
            "created": datetime.now(timezone.utc).isoformat(),
            "conversations": []
        }
    
    def _save_ledger(self, ledger: Dict):
        """Save ledger to file"""
        with open(self.ledger_file, 'w') as f:
            yaml.dump(ledger, f, sort_keys=False, default_flow_style=False)
    
    def log_conversation(
        self,
        share_url: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        primary_topic: str = "infrastructure",
        analysis_type: str = "validation",
        conclusion: str = "",
        validation_status: str = "confirmed",
        commercial_impact: str = "high",
        verified_by: str = "Human + AI Review",
        confidence_level: str = "high",
        secondary_topics: Optional[List[str]] = None,
        screenshot_paths: Optional[List[str]] = None,
    ) -> Dict:
        """Log a conversation to the evidence ledger"""
        
        # Generate unique ID and timestamps
        conversation_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        timestamp = now.isoformat()
        date_human = now.strftime("%Y-%m-%d")
        
        # Infer provider and interface if not provided
        if provider is None:
            provider = self._infer_provider_from_url(share_url)
        
        interface = self._infer_interface(share_url)
        
        # Build the entry
        entry = {
            "conversation_id": conversation_id,
            "timestamp": timestamp,
            "date_human": date_human,
            "ai_system": {
                "provider": provider,
                "model": model or "unknown",
                "interface": interface,
                "session_type": "web" if share_url else "local"
            },
            "evidence": {
                "share_url": share_url,
                "transcript_path": f"/evidence/conversations/{date_human}_{provider}_{primary_topic}.json" if share_url else None,
                "screenshot_paths": screenshot_paths or [],
                "git_commit": None
            },
            "topic": {
                "primary": primary_topic,
                "secondary": secondary_topics or [],
                "domain": "technical"
            },
            "analysis": {
                "type": analysis_type,
                "conclusion": conclusion,
                "validation_status": validation_status,
                "commercial_impact": commercial_impact
            },
            "legal": {
                "copyright_status": "collaborative",
                "intended_use": "audit",
                "privacy_sanitized": True,
                "contains_pii": False,
                "contains_secrets": False
            },
            "integration": {
                "obsidian_vault": "Legion-Core",
                "obsidian_note_path": f"Evidence/AI-Validations/{date_human}_{provider.title()}_Validation.md",
                "github_issue": None,
                "ledger_hash": "",  # Will be computed after
                "ledger_prev_hash": self._load_previous_hash()
            },
            "attestation": {
                "verified_by": verified_by,
                "verification_method": "direct generation + cryptographic hash",
                "confidence_level": confidence_level,
                "notes": None
            }
        }
        
        # Compute hash for this entry
        entry["integration"]["ledger_hash"] = self._compute_ledger_hash(entry)
        
        # Load ledger and append
        ledger = self._load_ledger()
        ledger["conversations"].append(entry)
        
        # Save ledger
        self._save_ledger(ledger)
        
        print(f"✅ Logged conversation: {conversation_id}")
        print(f"   Provider: {provider}")
        print(f"   Model: {model}")
        print(f"   Hash: {entry['integration']['ledger_hash'][:16]}...")
        if entry["integration"]["ledger_prev_hash"]:
            print(f"   Previous Hash: {entry['integration']['ledger_prev_hash'][:16]}...")
        
        return entry
    
    def verify_chain(self) -> bool:
        """Verify the integrity of the hash chain"""
        ledger = self._load_ledger()
        conversations = ledger.get("conversations", [])
        
        if not conversations:
            print("✅ Empty ledger (valid)")
            return True
        
        print(f"Verifying chain of {len(conversations)} entries...")
        
        for i, entry in enumerate(conversations):
            # Recompute hash by temporarily clearing the hash field
            stored_hash = entry["integration"]["ledger_hash"]
            entry["integration"]["ledger_hash"] = ""
            computed_hash = self._compute_ledger_hash(entry)
            # Restore the original hash
            entry["integration"]["ledger_hash"] = stored_hash
            
            # Check if hash matches
            if computed_hash != stored_hash:
                print(f"❌ Entry {i} hash mismatch!")
                print(f"   Expected: {stored_hash}")
                print(f"   Computed: {computed_hash}")
                return False
            
            # Check if prev_hash matches previous entry's hash
            if i > 0:
                expected_prev = conversations[i-1]["integration"]["ledger_hash"]
                actual_prev = entry["integration"]["ledger_prev_hash"]
                if expected_prev != actual_prev:
                    print(f"❌ Entry {i} chain broken!")
                    print(f"   Expected previous: {expected_prev}")
                    print(f"   Actual previous: {actual_prev}")
                    return False
            
            print(f"✅ Entry {i}: {entry['ai_system']['provider']} - {entry['date_human']}")
        
        print("✅ Chain verification successful!")
        return True
    
    def export_to_json(self, output_file: Optional[Path] = None):
        """Export ledger to JSON format"""
        ledger = self._load_ledger()
        
        if output_file is None:
            output_file = self.base_dir / "conversation_ledger.json"
        
        with open(output_file, 'w') as f:
            json.dump(ledger, f, indent=2)
        
        print(f"✅ Exported ledger to {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="AI Conversation Evidence Logger"
    )
    parser.add_argument(
        "share_url",
        nargs="?",
        help="Share URL from AI conversation (Claude, ChatGPT, Grok, etc.)"
    )
    parser.add_argument(
        "--provider",
        choices=["anthropic", "openai", "xai", "google", "meta", "mistral", "ollama", "other"],
        help="AI provider (auto-detected from URL if not provided)"
    )
    parser.add_argument(
        "--model",
        help="Model name (e.g., claude-3.5-sonnet-20241022)"
    )
    parser.add_argument(
        "--topic",
        default="infrastructure",
        help="Primary topic of conversation"
    )
    parser.add_argument(
        "--conclusion",
        default="",
        help="Analysis conclusion"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify the integrity of the evidence chain"
    )
    parser.add_argument(
        "--export",
        action="store_true",
        help="Export ledger to JSON"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive mode for logging conversations"
    )
    
    args = parser.parse_args()
    
    logger = ConversationEvidenceLogger()
    
    if args.verify:
        logger.verify_chain()
        return
    
    if args.export:
        logger.export_to_json()
        return
    
    if args.interactive:
        print("=== AI Conversation Evidence Logger ===")
        print("Enter conversation details (press Ctrl+C to cancel)\n")
        
        share_url = input("Share URL (or press Enter to skip): ").strip() or None
        provider = input("Provider (anthropic/openai/xai/google/other): ").strip() or None
        model = input("Model name: ").strip() or "unknown"
        topic = input("Primary topic [infrastructure]: ").strip() or "infrastructure"
        conclusion = input("Conclusion: ").strip()
        
        logger.log_conversation(
            share_url=share_url,
            provider=provider,
            model=model,
            primary_topic=topic,
            conclusion=conclusion
        )
        return
    
    if args.share_url:
        logger.log_conversation(
            share_url=args.share_url,
            provider=args.provider,
            model=args.model,
            primary_topic=args.topic,
            conclusion=args.conclusion
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
