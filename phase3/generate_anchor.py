#!/usr/bin/env python3
"""
Anchor File Generator - Cryptographic Verification Proof Generator

This script generates signed anchor files that provide verifiable proof
of document state at specific points in time. These anchors form a chain
of verification that can be independently validated.

Usage:
    python generate_anchor.py <document_path> [options]
    
Options:
    --output DIR       Output directory for anchor files
    --key KEYID        GPG key ID for signing (default: 261AEA44C0AF89CD)
    --previous FILE    Previous anchor file for chain linking
    --sign            Generate GPG signature
    
Example:
    python generate_anchor.py evidence_dossier.md --sign --output anchors/

Environment Variables:
    GPG_KEY_ID: Default GPG key ID for signing
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def calculate_hash(file_path: str) -> str:
    """Calculate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def calculate_content_hash(content: str) -> str:
    """Calculate SHA-256 hash of string content."""
    return hashlib.sha256(content.encode()).hexdigest()


def load_previous_anchor(anchor_path: str) -> Optional[dict]:
    """Load and parse a previous anchor file."""
    if not os.path.exists(anchor_path):
        return None
    
    # Simple YAML-like parsing (avoiding external dependencies)
    anchor_data = {}
    current_section = None
    
    with open(anchor_path, 'r') as f:
        for line in f:
            line = line.rstrip()
            if not line or line.startswith('#'):
                continue
            
            if ':' in line and not line.startswith(' '):
                key = line.split(':')[0].strip()
                value = ':'.join(line.split(':')[1:]).strip()
                if value:
                    anchor_data[key] = value.strip('"\'')
                else:
                    current_section = key
                    anchor_data[current_section] = {}
            elif current_section and ':' in line:
                key = line.split(':')[0].strip()
                value = ':'.join(line.split(':')[1:]).strip().strip('"\'')
                anchor_data[current_section][key] = value
    
    return anchor_data


def gpg_sign(content: str, key_id: str) -> Optional[str]:
    """Sign content using GPG."""
    try:
        result = subprocess.run(
            ['gpg', '--armor', '--detach-sign', '--default-key', key_id, '-'],
            input=content.encode(),
            capture_output=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout.decode()
        else:
            print(f"GPG signing failed: {result.stderr.decode()}", file=sys.stderr)
            return None
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"GPG signing error: {e}", file=sys.stderr)
        return None


def generate_anchor(
    document_path: str,
    output_dir: str = ".",
    key_id: str = "261AEA44C0AF89CD",
    previous_anchor: Optional[str] = None,
    sign: bool = False,
    purpose: str = "verification"
) -> dict:
    """Generate an anchor file for a document."""
    
    # Validate document exists
    if not os.path.exists(document_path):
        raise FileNotFoundError(f"Document not found: {document_path}")
    
    # Calculate document hash
    doc_hash = calculate_hash(document_path)
    doc_name = os.path.basename(document_path)
    doc_size = os.path.getsize(document_path)
    
    # Generate timestamp
    timestamp = datetime.now(timezone.utc)
    timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
    timestamp_iso = timestamp.isoformat()
    
    # Load previous anchor if specified
    previous_hash = None
    previous_file = None
    chain_length = 1
    
    if previous_anchor and os.path.exists(previous_anchor):
        prev_data = load_previous_anchor(previous_anchor)
        if prev_data:
            previous_file = os.path.basename(previous_anchor)
            # Calculate hash of previous anchor file
            previous_hash = calculate_hash(previous_anchor)
            # Try to get chain length
            if 'chain' in prev_data and 'length' in prev_data['chain']:
                chain_length = int(prev_data['chain']['length']) + 1
    
    # Build anchor structure
    anchor = {
        "anchor": {
            "version": "1.0",
            "timestamp": timestamp_iso,
            "generator": "generate_anchor.py",
            "purpose": purpose
        },
        "content": {
            "document_name": doc_name,
            "document_path": document_path,
            "document_hash": f"sha256:{doc_hash}",
            "document_size": doc_size,
            "hash_algorithm": "SHA-256"
        },
        "verification": {
            "signer_key": key_id,
            "signed": sign,
            "signature_type": "GPG-ARMOR" if sign else "NONE"
        },
        "chain": {
            "length": chain_length,
            "previous_anchor": previous_file,
            "previous_hash": f"sha256:{previous_hash}" if previous_hash else None
        },
        "metadata": {
            "generated_at": timestamp_iso,
            "generator_version": "1.0.0",
            "repository": "Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-"
        }
    }
    
    # Generate anchor file name
    anchor_filename = f"anchor_{timestamp_str}.yaml"
    anchor_path = os.path.join(output_dir, anchor_filename)
    
    # Convert to YAML-like format (manual to avoid dependencies)
    yaml_content = generate_yaml(anchor)
    
    # Sign if requested
    signature = None
    if sign:
        signature = gpg_sign(yaml_content, key_id)
        if signature:
            anchor["verification"]["signed"] = True
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Write anchor file
    with open(anchor_path, 'w') as f:
        f.write(yaml_content)
    
    # Write signature file if signed
    if signature:
        sig_path = anchor_path + ".sig"
        with open(sig_path, 'w') as f:
            f.write(signature)
        print(f"Signature written to: {sig_path}")
    
    print(f"Anchor file generated: {anchor_path}")
    print(f"Document hash: {doc_hash}")
    print(f"Chain length: {chain_length}")
    
    return anchor


def generate_yaml(data: dict, indent: int = 0) -> str:
    """Generate YAML-like string from dictionary."""
    lines = []
    prefix = "  " * indent
    
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{prefix}{key}:")
            lines.append(generate_yaml(value, indent + 1))
        elif isinstance(value, list):
            lines.append(f"{prefix}{key}:")
            for item in value:
                if isinstance(item, dict):
                    lines.append(f"{prefix}  -")
                    lines.append(generate_yaml(item, indent + 2))
                else:
                    lines.append(f"{prefix}  - {item}")
        elif value is None:
            lines.append(f"{prefix}{key}: null")
        elif isinstance(value, bool):
            lines.append(f"{prefix}{key}: {str(value).lower()}")
        elif isinstance(value, (int, float)):
            lines.append(f"{prefix}{key}: {value}")
        else:
            # Quote strings that might need it
            if any(c in str(value) for c in [':', '#', '{', '}', '[', ']', ',', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`']):
                lines.append(f'{prefix}{key}: "{value}"')
            else:
                lines.append(f"{prefix}{key}: {value}")
    
    return "\n".join(lines)


def verify_anchor(anchor_path: str, document_path: str) -> bool:
    """Verify an anchor file against its document."""
    if not os.path.exists(anchor_path):
        print(f"Anchor file not found: {anchor_path}")
        return False
    
    if not os.path.exists(document_path):
        print(f"Document not found: {document_path}")
        return False
    
    # Load anchor
    anchor_data = load_previous_anchor(anchor_path)
    if not anchor_data or 'content' not in anchor_data:
        print("Invalid anchor file format")
        return False
    
    # Get stored hash
    stored_hash = anchor_data['content'].get('document_hash', '')
    if stored_hash.startswith('sha256:'):
        stored_hash = stored_hash[7:]
    
    # Calculate current hash
    current_hash = calculate_hash(document_path)
    
    # Compare
    if stored_hash == current_hash:
        print(f"✓ Document verified: hashes match")
        print(f"  Hash: {current_hash}")
        return True
    else:
        print(f"✗ Document verification failed: hashes do not match")
        print(f"  Stored:  {stored_hash}")
        print(f"  Current: {current_hash}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate cryptographic anchor files for document verification"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate anchor file")
    gen_parser.add_argument("document", help="Path to document to anchor")
    gen_parser.add_argument("--output", "-o", default=".", help="Output directory")
    gen_parser.add_argument("--key", "-k", default=os.environ.get("GPG_KEY_ID", "261AEA44C0AF89CD"),
                          help="GPG key ID for signing")
    gen_parser.add_argument("--previous", "-p", help="Previous anchor file for chain")
    gen_parser.add_argument("--sign", "-s", action="store_true", help="Sign the anchor")
    gen_parser.add_argument("--purpose", default="verification", help="Purpose description")
    
    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Verify document against anchor")
    verify_parser.add_argument("anchor", help="Path to anchor file")
    verify_parser.add_argument("document", help="Path to document to verify")
    
    # Chain command
    chain_parser = subparsers.add_parser("chain", help="Show anchor chain")
    chain_parser.add_argument("anchor", help="Path to latest anchor file")
    
    args = parser.parse_args()
    
    if args.command == "generate":
        try:
            anchor = generate_anchor(
                document_path=args.document,
                output_dir=args.output,
                key_id=args.key,
                previous_anchor=args.previous,
                sign=args.sign,
                purpose=args.purpose
            )
            print("\n✓ Anchor file generated successfully")
            
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error generating anchor: {e}", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == "verify":
        success = verify_anchor(args.anchor, args.document)
        sys.exit(0 if success else 1)
    
    elif args.command == "chain":
        # Walk the chain and display
        current = args.anchor
        chain = []
        
        while current and os.path.exists(current):
            data = load_previous_anchor(current)
            if not data:
                break
            
            chain.append({
                "file": os.path.basename(current),
                "timestamp": data.get("anchor", {}).get("timestamp", "unknown"),
                "document": data.get("content", {}).get("document_name", "unknown"),
                "hash": data.get("content", {}).get("document_hash", "unknown")
            })
            
            prev = data.get("chain", {}).get("previous_anchor")
            if prev:
                current = os.path.join(os.path.dirname(args.anchor), prev)
            else:
                break
        
        print("Anchor Chain:")
        print("=" * 60)
        for i, entry in enumerate(chain):
            print(f"\n[{i+1}] {entry['file']}")
            print(f"    Timestamp: {entry['timestamp']}")
            print(f"    Document:  {entry['document']}")
            print(f"    Hash:      {entry['hash'][:40]}...")
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
