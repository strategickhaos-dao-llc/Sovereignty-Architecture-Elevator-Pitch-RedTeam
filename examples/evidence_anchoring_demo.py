#!/usr/bin/env python3
"""
Evidence Anchoring System - Live Demo
Strategickhaos DAO LLC

This demo shows the complete workflow:
1. Creating a conversation evidence entry
2. Automatic GPG signing and OpenTimestamps anchoring
3. Verification of the anchored evidence

Note: Requires GPG and OpenTimestamps CLI to be installed for full demo.
For testing without these tools, use test_evidence_system.py instead.
"""

import sys
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from evidence_logger import EvidenceLogger


def demo_basic_logging():
    """Demo 1: Basic evidence logging without anchoring."""
    print("=" * 70)
    print("DEMO 1: Basic Evidence Logging (No Anchoring)")
    print("=" * 70)
    
    logger = EvidenceLogger(
        evidence_dir="evidence/anchored",
        gpg_key="dom@strategickhaos.com",
        operator="Domenic Garza"
    )
    
    print("\n📝 Logging a conversation...")
    result = logger.log_conversation(
        conversation_id="demo_basic_001",
        participants=[
            {"name": "Domenic Garza", "role": "CEO/Founder"},
            {"name": "AI Assistant", "role": "Technical Advisor"}
        ],
        transcript="""
        Dom: How can we ensure our business records are legally admissible?
        
        AI: We can use cryptographic anchoring with two layers:
        1. GPG signatures to prove WHO created the record
        2. OpenTimestamps to prove WHEN it existed
        
        This creates a mathematically unbreakable audit trail that's 
        admissible in court and verifiable by anyone.
        
        Dom: Perfect. Let's implement it.
        """,
        context="Strategic planning - Legal compliance discussion",
        summary="Discussed implementing cryptographic evidence anchoring for legal compliance",
        related_documents=[
            "evidence/schemas/conversation_evidence.v1.2.0.yaml",
            "legal/compliance_framework.pdf"
        ],
        auto_anchor=False  # Disable for demo (requires GPG/OTS)
    )
    
    if result["success"]:
        print(f"✅ Evidence logged successfully!")
        print(f"   File: {result['file_path']}")
        print(f"   SHA256: {result['sha256'][:32]}...")
        print(f"   Timestamp: {result['timestamp']}")
    else:
        print(f"❌ Logging failed: {result.get('error')}")
    
    return result


def demo_with_anchoring():
    """Demo 2: Evidence logging WITH anchoring (requires GPG/OTS)."""
    print("\n" + "=" * 70)
    print("DEMO 2: Evidence Logging WITH Anchoring")
    print("=" * 70)
    print("\n⚠️  This demo requires GPG and OpenTimestamps CLI to be installed.")
    print("    If not available, the anchoring steps will fail gracefully.\n")
    
    logger = EvidenceLogger(
        evidence_dir="evidence/anchored",
        gpg_key="dom@strategickhaos.com",
        operator="Domenic Garza"
    )
    
    print("📝 Logging and anchoring a conversation...")
    result = logger.log_conversation(
        conversation_id="demo_anchored_001",
        participants=[
            {"name": "Domenic Garza", "role": "CEO/Founder"},
            {"name": "Investor", "role": "Due Diligence Review"}
        ],
        transcript="""
        Investor: How do you ensure the integrity of your business records?
        
        Dom: Every conversation and document is cryptographically signed with 
        GPG and timestamped on the Bitcoin blockchain via OpenTimestamps.
        
        This means:
        - You can verify I created it (GPG signature)
        - You can verify when it existed (Bitcoin timestamp)
        - Any tampering would be immediately detectable
        
        It's mathematically impossible to forge or backdate.
        
        Investor: That's impressive. Very few companies do this.
        
        Dom: We take transparency and accountability seriously.
        """,
        context="Investor due diligence meeting - Q4 2025",
        summary="Demonstrated cryptographic evidence management to investor",
        attachments=["presentations/due_diligence_Q4_2025.pdf"],
        auto_anchor=True  # Enable full anchoring
    )
    
    if result["success"]:
        print(f"✅ Evidence logged and anchored!")
        print(f"   File: {result['file_path']}")
        print(f"   SHA256: {result['sha256'][:32]}...")
        
        if result.get("anchored"):
            print(f"   🔐 GPG Signed: ✓")
            print(f"   ⏰ Bitcoin Timestamped: ✓")
            
            if "anchoring_details" in result:
                details = result["anchoring_details"]
                if details["gpg"].get("success"):
                    print(f"      GPG signature: {details['gpg']['signature_file']}")
                if details["opentimestamps"].get("success"):
                    print(f"      OTS timestamp: {details['opentimestamps']['ots_file']}")
        else:
            print(f"   ⚠️  Anchoring skipped (GPG/OTS not available)")
    else:
        print(f"❌ Logging failed: {result.get('error')}")
    
    return result


def demo_verification():
    """Demo 3: Verifying anchored evidence."""
    print("\n" + "=" * 70)
    print("DEMO 3: Verification of Anchored Evidence")
    print("=" * 70)
    
    logger = EvidenceLogger(
        evidence_dir="evidence/anchored",
        gpg_key="dom@strategickhaos.com"
    )
    
    # Try to verify the anchored demo
    print("\n🔍 Verifying 'demo_anchored_001'...")
    result = logger.verify_evidence("demo_anchored_001")
    
    if "error" in result:
        print(f"   ⚠️  {result['error']}")
        print("   (Run demo_with_anchoring() first to create the evidence)")
    else:
        print(f"   File: {result['file_path']}")
        
        # GPG verification
        if result["gpg"].get("success"):
            print(f"   ✅ GPG Signature: {result['gpg']['message']}")
        else:
            print(f"   ❌ GPG Signature: {result['gpg']['message']}")
        
        # OTS verification
        if result["opentimestamps"].get("success"):
            print(f"   ✅ OpenTimestamps: {result['opentimestamps']['message']}")
        else:
            print(f"   ⚠️  OpenTimestamps: {result['opentimestamps']['message']}")
        
        if result.get("success"):
            print(f"\n   🎉 Evidence is fully verified and admissible!")
    
    return result


def main():
    """Run all demos."""
    print("\n" + "🔐" * 35)
    print(" " * 15 + "EVIDENCE ANCHORING SYSTEM DEMO")
    print("🔐" * 35)
    print("\nStrategickhaos DAO LLC - Mathematically Unbreakable Audit Trails\n")
    
    try:
        # Demo 1: Basic logging
        demo_basic_logging()
        
        # Demo 2: With anchoring (may fail gracefully if GPG/OTS not installed)
        demo_with_anchoring()
        
        # Demo 3: Verification
        demo_verification()
        
        print("\n" + "=" * 70)
        print("DEMO COMPLETE")
        print("=" * 70)
        print("""
Next Steps:
1. Install dependencies: pip install -r requirements.evidence.txt
2. Set up GPG key: gpg --full-generate-key
3. Run anchoring: python tools/anchor_ledger.py evidence/example_conversation_ledger.yaml
4. Verify anytime: python tools/anchor_ledger.py --verify evidence/example_conversation_ledger.yaml

Documentation:
- Full guide: EVIDENCE_ANCHORING.md
- Schema reference: evidence/schemas/conversation_evidence.v1.2.0.yaml
- Usage examples: evidence/README.md

Your ledger is now harder than 99.999% of corporate audit trails.
Run once → Secured forever.
        """)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
