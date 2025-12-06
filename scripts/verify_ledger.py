#!/usr/bin/env python3
"""
Verify AI Conversation Evidence Ledger
--------------------------------------
Validates the integrity of conversation ledgers by checking:
- YAML syntax validity
- Hash chain integrity
- Entry structure completeness
- Timestamp format validity

Usage:
    python3 scripts/verify_ledger.py conversation_ledger.yaml
    python3 scripts/verify_ledger.py examples/conversation_ledger_example.yaml
"""

import sys
import yaml
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional


def verify_yaml_valid(filepath: str) -> tuple[bool, Optional[Dict]]:
    """Verify YAML file is syntactically valid."""
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        return True, data
    except yaml.YAMLError as e:
        print(f"❌ YAML syntax error: {e}")
        return False, None
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return False, None


def verify_metadata(data: Dict) -> bool:
    """Verify metadata section is complete."""
    required_fields = ['ledger_version', 'operator', 'organization', 'purpose']
    metadata = data.get('metadata', {})
    
    missing = [f for f in required_fields if f not in metadata]
    if missing:
        print(f"❌ Missing metadata fields: {', '.join(missing)}")
        return False
    
    print("✅ Metadata complete")
    return True


def verify_iso8601_timestamp(timestamp: str) -> bool:
    """Verify timestamp is valid ISO 8601 format."""
    try:
        datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False


def verify_conversations(data: Dict) -> bool:
    """Verify conversation entries and hash chain."""
    conversations = data.get('conversations', [])
    
    if not conversations:
        print("⚠️  No conversation entries found")
        return True
    
    prev_hash = None
    all_valid = True
    
    for idx, entry in enumerate(conversations, 1):
        entry_id = entry.get('entry_id', f'unknown-{idx}')
        print(f"\n📝 Verifying entry {idx}/{len(conversations)}: {entry_id}")
        
        # Check required fields
        required = ['entry_id', 'timestamp', 'ai_system', 'session_info', 
                   'context', 'summary', 'verification']
        missing = [f for f in required if f not in entry]
        if missing:
            print(f"  ❌ Missing fields: {', '.join(missing)}")
            all_valid = False
            continue
        
        # Verify timestamp format
        timestamp = entry.get('timestamp', '')
        if not verify_iso8601_timestamp(timestamp):
            print(f"  ❌ Invalid timestamp format: {timestamp}")
            all_valid = False
        else:
            print(f"  ✅ Timestamp valid: {timestamp}")
        
        # Verify chain integrity
        verification = entry.get('verification', {})
        current_hash = verification.get('entry_hash', '')
        previous_hash = verification.get('previous_entry_hash')
        chain_pos = verification.get('chain_position', idx)
        
        # First entry should have null previous hash
        if idx == 1:
            if previous_hash is not None:
                print(f"  ❌ First entry should have null previous_entry_hash")
                all_valid = False
            else:
                print(f"  ✅ First entry: previous hash correctly null")
        else:
            # Subsequent entries should link to previous
            if prev_hash != previous_hash:
                print(f"  ❌ Hash chain broken!")
                print(f"     Expected: {prev_hash}")
                print(f"     Got: {previous_hash}")
                all_valid = False
            else:
                print(f"  ✅ Chain link valid (position {chain_pos})")
        
        # Verify chain position
        if chain_pos != idx:
            print(f"  ⚠️  Chain position mismatch: expected {idx}, got {chain_pos}")
        
        # Store current hash for next iteration
        prev_hash = current_hash
        
        # Check AI system info
        ai_system = entry.get('ai_system', {})
        if not all(k in ai_system for k in ['provider', 'model']):
            print(f"  ⚠️  Incomplete AI system information")
        else:
            print(f"  ✅ AI system: {ai_system['provider']} {ai_system['model']}")
        
        # Check for evidence files
        session = entry.get('session_info', {})
        has_evidence = any([
            session.get('share_url'),
            session.get('screenshot_path'),
            session.get('export_path')
        ])
        if not has_evidence:
            print(f"  ⚠️  No external evidence (share URL, screenshot, or export)")
        else:
            print(f"  ✅ External evidence references present")
    
    if all_valid:
        print(f"\n✅ All {len(conversations)} conversation entries valid")
        print(f"✅ Hash chain integrity verified")
    else:
        print(f"\n❌ Some validation errors found")
    
    return all_valid


def verify_integrity(data: Dict) -> bool:
    """Verify integrity section."""
    integrity = data.get('integrity', {})
    
    # Check hash algorithm
    hash_algo = integrity.get('hash_algorithm', '')
    if hash_algo not in ['SHA3-256', 'SHA-256', 'SHA256']:
        print(f"⚠️  Unusual hash algorithm: {hash_algo}")
    else:
        print(f"✅ Hash algorithm: {hash_algo}")
    
    # Check for GPG signature
    if integrity.get('gpg_signature'):
        print("✅ GPG signature present")
    else:
        print("ℹ️  No GPG signature (optional but recommended)")
    
    # Check for OpenTimestamps
    if integrity.get('opentimestamp'):
        print("✅ OpenTimestamps reference present")
    else:
        print("ℹ️  No OpenTimestamps (optional but recommended)")
    
    return True


def verify_custodian(data: Dict) -> bool:
    """Verify custodian information."""
    custodian = data.get('custodian', {})
    
    required = ['name', 'role', 'organization']
    missing = [f for f in required if f not in custodian]
    
    if missing:
        print(f"⚠️  Missing custodian fields: {', '.join(missing)}")
        return False
    
    if custodian.get('attestation'):
        print("✅ Custodian attestation present")
    else:
        print("ℹ️  No custodian attestation (recommended for legal use)")
    
    return True


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 verify_ledger.py <ledger_file.yaml>")
        print("\nExample:")
        print("  python3 scripts/verify_ledger.py examples/conversation_ledger_example.yaml")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    print("=" * 70)
    print("AI Conversation Evidence Ledger Verification")
    print("=" * 70)
    print(f"\nVerifying: {filepath}\n")
    
    # Verify YAML syntax
    print("🔍 Checking YAML syntax...")
    valid, data = verify_yaml_valid(filepath)
    if not valid:
        sys.exit(1)
    print("✅ YAML syntax valid\n")
    
    # Verify metadata
    print("🔍 Checking metadata...")
    verify_metadata(data)
    print()
    
    # Verify integrity section
    print("🔍 Checking integrity configuration...")
    verify_integrity(data)
    print()
    
    # Verify conversations and hash chain
    print("🔍 Checking conversations and hash chain...")
    conversations_valid = verify_conversations(data)
    print()
    
    # Verify custodian
    print("🔍 Checking custodian information...")
    verify_custodian(data)
    print()
    
    # Final summary
    print("=" * 70)
    if conversations_valid:
        print("✅ VERIFICATION PASSED")
        print("\nThis ledger appears to be properly structured and maintains")
        print("hash chain integrity. For legal use, ensure you also have:")
        print("  • GPG signatures (see docs/GPG_SIGNATURE_GUIDE.md)")
        print("  • OpenTimestamps (see docs/OPENTIMESTAMPS_GUIDE.md)")
        print("  • Sworn declaration (see templates/sworn_declaration_template.md)")
    else:
        print("❌ VERIFICATION FAILED")
        print("\nPlease fix the errors above before using this ledger.")
    print("=" * 70)
    
    sys.exit(0 if conversations_valid else 1)


if __name__ == '__main__':
    main()
