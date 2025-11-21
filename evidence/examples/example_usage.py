#!/usr/bin/env python3
"""
Example usage of the ConversationEvidenceLogger class
Demonstrates programmatic logging of AI conversations
"""

import sys
from pathlib import Path

# Add parent directory to path to import evidence_logger
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from evidence_logger import ConversationEvidenceLogger


def main():
    print("=== AI Conversation Evidence Logger - Python API Example ===\n")
    
    # Initialize the logger
    logger = ConversationEvidenceLogger()
    
    # Example 1: Log a Claude conversation
    print("1. Logging Claude infrastructure audit...")
    claude_entry = logger.log_conversation(
        share_url="https://claude.ai/share/8ea1d23d-e97a-45e5-a994-35e0988a0d75",
        provider="anthropic",
        model="claude-sonnet-4-20250514",
        primary_topic="infrastructure-audit",
        analysis_type="audit",
        conclusion="Commercially viable infrastructure with proven 4000× cost reduction",
        validation_status="confirmed",
        commercial_impact="high",
        verified_by="Claude-Sonnet-4 (Anthropic)",
        confidence_level="high",
        secondary_topics=["cost-analysis", "productivity-metrics"]
    )
    print(f"   Conversation ID: {claude_entry['conversation_id']}\n")
    
    # Example 2: Log a GPT conversation
    print("2. Logging GPT security validation...")
    gpt_entry = logger.log_conversation(
        share_url="https://chatgpt.com/share/b4c7e9d2-5f8a-4b1d-9c3e-6a7d8f0e2b5c",
        provider="openai",
        model="gpt-4o-2024-11-20",
        primary_topic="security-validation",
        analysis_type="security",
        conclusion="Console nursery is genius-level safe AI containment",
        validation_status="confirmed",
        commercial_impact="high",
        verified_by="GPT-4o (OpenAI)",
        confidence_level="high",
        secondary_topics=["architecture", "threat-model"]
    )
    print(f"   Conversation ID: {gpt_entry['conversation_id']}\n")
    
    # Example 3: Log a Grok conversation
    print("3. Logging Grok schema improvement...")
    grok_entry = logger.log_conversation(
        share_url="https://x.com/i/grok/share/f4a7d8c1-2b9e-4a1d-9f3a-8e7c5b6d4f2a",
        provider="xai",
        model="grok-4-2025",
        primary_topic="schema-improvement",
        analysis_type="validation",
        conclusion="Improved evidence ledger with cryptographic chaining",
        validation_status="confirmed",
        commercial_impact="high",
        verified_by="Grok-4 (xAI)",
        confidence_level="high",
        secondary_topics=["legal-evidence", "audit-trail", "cryptographic-ledger"]
    )
    print(f"   Conversation ID: {grok_entry['conversation_id']}\n")
    
    # Verify the chain
    print("4. Verifying cryptographic chain integrity...")
    is_valid = logger.verify_chain()
    print()
    
    if is_valid:
        # Export to JSON
        print("5. Exporting to JSON format...")
        logger.export_to_json()
        print()
        
        print("✅ All examples completed successfully!")
        print()
        print("Check the results:")
        print("  - YAML ledger: evidence/conversation_ledger.yaml")
        print("  - JSON export: evidence/conversation_ledger.json")
    else:
        print("❌ Chain verification failed!")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
