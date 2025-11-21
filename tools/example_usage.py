#!/usr/bin/env python3
"""
example_usage.py - Example usage of the evidence anchoring system

This script demonstrates how to use the evidence_logger and anchor_ledger
modules to create cryptographically anchored evidence entries.

Author: Strategickhaos
Version: 1.0.0
"""

import sys
from pathlib import Path
from datetime import datetime

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from evidence_logger import EvidenceLogger
except ImportError:
    print("❌ Error: Could not import evidence_logger")
    print("Make sure you're running this from the correct directory")
    sys.exit(1)


def example_1_simple_conversation():
    """Example 1: Log a simple conversation without anchoring."""
    print("\n" + "=" * 70)
    print("Example 1: Simple Conversation Logging (No Anchoring)")
    print("=" * 70)
    
    logger = EvidenceLogger(
        evidence_dir="evidence/examples",
        auto_anchor=False  # Disable automatic anchoring for this example
    )
    
    conv_id = f"simple-conv-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    result = logger.log_conversation(
        conversation_id=conv_id,
        messages=[
            {
                "message_id": "msg-001",
                "sender": "Alice",
                "timestamp": logger._generate_timestamp(),
                "content": "Should we proceed with the new feature?",
                "attachments": []
            },
            {
                "message_id": "msg-002",
                "sender": "Bob",
                "timestamp": logger._generate_timestamp(),
                "content": "Yes, I think we should. The requirements are clear.",
                "attachments": []
            }
        ],
        participants=["Alice", "Bob"],
        platform="Discord",
        channel="#product-decisions",
        evidence_type="decision",
        category="product",
        tags=["feature", "decision"]
    )
    
    print(f"\n✅ Logged conversation: {conv_id}")
    print(f"   File: {result['entry_file']}")
    print(f"   Anchored: {result['anchored']}")


def example_2_github_integration():
    """Example 2: Log conversation with GitHub integration."""
    print("\n" + "=" * 70)
    print("Example 2: Conversation with GitHub Integration (No Anchoring)")
    print("=" * 70)
    
    logger = EvidenceLogger(
        evidence_dir="evidence/examples",
        auto_anchor=False
    )
    
    conv_id = f"github-conv-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    result = logger.log_conversation(
        conversation_id=conv_id,
        messages=[
            {
                "message_id": "msg-001",
                "sender": "Developer",
                "timestamp": logger._generate_timestamp(),
                "content": "PR #123 is ready for review",
                "attachments": []
            }
        ],
        participants=["Developer", "Tech Lead"],
        platform="Discord",
        channel="#code-review",
        evidence_type="conversation",
        category="engineering",
        tags=["code-review", "pr"],
        github_pr=123,
        github_commit="abc123def456",
        github_repo="Strategickhaos/Sovereignty-Architecture"
    )
    
    print(f"\n✅ Logged GitHub-linked conversation: {conv_id}")
    print(f"   File: {result['entry_file']}")
    print(f"   GitHub PR: #123")


def example_3_with_metadata():
    """Example 3: Log conversation with custom metadata."""
    print("\n" + "=" * 70)
    print("Example 3: Conversation with Custom Metadata (No Anchoring)")
    print("=" * 70)
    
    logger = EvidenceLogger(
        evidence_dir="evidence/examples",
        auto_anchor=False
    )
    
    conv_id = f"metadata-conv-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    result = logger.log_conversation(
        conversation_id=conv_id,
        messages=[
            {
                "message_id": "msg-001",
                "sender": "Security Engineer",
                "timestamp": logger._generate_timestamp(),
                "content": "We need to address the vulnerability in dependency X",
                "attachments": []
            }
        ],
        participants=["Security Engineer", "Dev Team"],
        platform="Discord",
        channel="#security",
        evidence_type="action_item",
        category="security",
        tags=["vulnerability", "urgent", "dependency"],
        metadata={
            "severity": "high",
            "cve_id": "CVE-2025-12345",
            "affected_components": ["frontend", "api"],
            "sla_hours": 24
        }
    )
    
    print(f"\n✅ Logged conversation with metadata: {conv_id}")
    print(f"   File: {result['entry_file']}")
    print(f"   Custom metadata fields: severity, cve_id, affected_components, sla_hours")


def example_4_list_evidence():
    """Example 4: List all evidence entries."""
    print("\n" + "=" * 70)
    print("Example 4: List All Evidence Entries")
    print("=" * 70)
    
    logger = EvidenceLogger(
        evidence_dir="evidence/examples",
        auto_anchor=False
    )
    
    entries = logger.list_evidence()
    
    print(f"\n📋 Found {len(entries)} evidence entries:")
    for entry in entries:
        print(f"   • {entry}")


def example_5_anchored_conversation():
    """Example 5: Log conversation WITH anchoring (requires GPG and OTS)."""
    print("\n" + "=" * 70)
    print("Example 5: Conversation with Automatic Anchoring")
    print("=" * 70)
    print("\n⚠️  This example requires GPG and OpenTimestamps to be installed.")
    print("    If you don't have them, this will fail gracefully.")
    
    # Check if user wants to proceed
    response = input("\nDo you want to try anchoring? (requires GPG & OTS) [y/N]: ")
    
    if response.lower() != 'y':
        print("Skipping anchored example.")
        return
    
    logger = EvidenceLogger(
        evidence_dir="evidence/examples",
        auto_anchor=True,  # Enable automatic anchoring
        operator_name="Dom",
        operator_node="137"
    )
    
    conv_id = f"anchored-conv-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    try:
        result = logger.log_conversation(
            conversation_id=conv_id,
            messages=[
                {
                    "message_id": "msg-001",
                    "sender": "Alice",
                    "timestamp": logger._generate_timestamp(),
                    "content": "This is a cryptographically anchored decision.",
                    "attachments": []
                }
            ],
            participants=["Alice", "Bob"],
            platform="Discord",
            channel="#decisions",
            evidence_type="decision",
            category="critical",
            tags=["anchored", "crypto-proof"]
        )
        
        print(f"\n✅ Logged and anchored conversation: {conv_id}")
        print(f"   File: {result['entry_file']}")
        print(f"   Anchored: {result['anchored']}")
        
        if result['anchored'] and 'anchor_result' in result:
            anchor = result['anchor_result']
            print(f"   SHA256: {anchor['sha256']}")
            if anchor.get('gpg_signature'):
                print("   ✓ GPG signature created")
            if anchor.get('opentimestamps'):
                print(f"   ✓ OpenTimestamps proof created (status: {anchor['opentimestamps']['status']})")
    
    except Exception as e:
        print(f"\n❌ Anchoring failed: {e}")
        print("   Make sure GPG and OpenTimestamps are installed and configured.")


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("Evidence Anchoring System - Usage Examples")
    print("=" * 70)
    print("\nThis script demonstrates various ways to use the evidence logging system.")
    print("Examples 1-4 don't require GPG or OpenTimestamps.")
    print("Example 5 requires GPG and OpenTimestamps to be installed.\n")
    
    # Run examples
    example_1_simple_conversation()
    example_2_github_integration()
    example_3_with_metadata()
    example_4_list_evidence()
    example_5_anchored_conversation()
    
    print("\n" + "=" * 70)
    print("✅ Examples completed!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Check the evidence/examples/ directory for generated files")
    print("2. Try anchoring with: python tools/anchor_ledger.py evidence/examples/[file].yaml")
    print("3. Read tools/README.md for more information")
    print()


if __name__ == "__main__":
    main()
