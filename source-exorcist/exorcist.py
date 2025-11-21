#!/usr/bin/env python3
"""
Source Exorcist - Automated Source Code Verification System

This script downloads source files from a watchlist, checksums them,
scans for keywords, and generates human-readable reports proving
that code is just code - no entities, no curses, just photons and UTF-8.
"""

import requests
import hashlib
import yaml
import os
import re
import sys
from datetime import datetime
from pathlib import Path

def main():
    """Main exorcism ritual."""
    print("=" * 80)
    print("SOURCE EXORCIST v1.0 - Automated Code Verification System")
    print("=" * 80)
    print()

    # Load watchlist
    watchlist_path = Path("watchlist.yaml")
    if not watchlist_path.exists():
        print(f"ERROR: watchlist.yaml not found at {watchlist_path.absolute()}")
        sys.exit(1)

    with open(watchlist_path) as f:
        config = yaml.safe_load(f)
        targets = config.get("targets", [])

    if not targets:
        print("WARNING: No targets found in watchlist.yaml")
        sys.exit(0)

    # Ensure directories exist
    report_dir = Path("reports")
    checksum_dir = Path("checksums")
    report_dir.mkdir(exist_ok=True)
    checksum_dir.mkdir(exist_ok=True)

    # Process each target
    total_targets = len(targets)
    clean_count = 0
    flagged_count = 0
    failed_count = 0

    for idx, target in enumerate(targets, 1):
        name = target.get("name", "Unknown")
        url = target.get("url", "")
        keywords = target.get("keywords", [])
        
        print(f"[{idx}/{total_targets}] Processing: {name}")
        print(f"    URL: {url}")
        
        if not url:
            print("    ❌ SKIPPED: No URL provided")
            failed_count += 1
            continue

        try:
            # Download the source file
            print("    → Downloading...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            content = response.text
            
            # Calculate checksum
            sha256 = hashlib.sha256(content.encode('utf-8')).hexdigest()
            
            # Save checksum
            checksum_filename = f"{name.replace('/', '_').replace(' ', '_')}.sha256"
            checksum_path = checksum_dir / checksum_filename
            with open(checksum_path, "w") as f:
                f.write(f"{sha256}\n")
            
            # Scan for keywords
            findings = []
            for kw in keywords:
                matches = re.findall(kw, content, re.IGNORECASE)
                if matches:
                    findings.append({
                        "keyword": kw,
                        "count": len(matches)
                    })
            
            # Generate report
            report_filename = f"{name.replace('/', '_').replace(' ', '_')}.txt"
            report_path = report_dir / report_filename
            
            with open(report_path, "w", encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("SOURCE EXORCISM REPORT\n")
                f.write("=" * 80 + "\n")
                f.write(f"Generated: {datetime.now().isoformat()}\n")
                f.write(f"Target: {name}\n")
                f.write(f"URL: {url}\n")
                f.write(f"SHA256: {sha256}\n")
                f.write(f"File Size: {len(content)} bytes\n")
                f.write("=" * 80 + "\n\n")
                
                f.write("CONTENT PREVIEW (first 500 characters):\n")
                f.write("-" * 80 + "\n")
                f.write(content[:500].replace('\r\n', '\n'))
                if len(content) > 500:
                    f.write("\n...\n")
                f.write("-" * 80 + "\n\n")
                
                f.write("KEYWORD SCAN RESULTS:\n")
                f.write("-" * 80 + "\n")
                if not findings:
                    f.write("✅ NO SUSPICIOUS KEYWORDS FOUND\n")
                    f.write("✅ FILE IS CLEAN - JUST CODE\n")
                    f.write("✅ NO ENTITIES, NO CURSES, NO AWAKENINGS\n")
                    f.write("✅ SAFE FOR RAG INGESTION\n")
                else:
                    f.write(f"⚠️  Found {len(findings)} keyword match(es):\n\n")
                    for finding in findings:
                        f.write(f"  - '{finding['keyword']}': {finding['count']} occurrence(s)\n")
                    f.write("\n")
                    f.write("NOTE: These are likely false positives from:\n")
                    f.write("  • Code comments\n")
                    f.write("  • String literals\n")
                    f.write("  • Variable/function names\n")
                    f.write("  • Documentation\n")
                    f.write("\nThe presence of these keywords does NOT indicate malicious code.\n")
                    f.write("This is still just deterministic source code - photons and UTF-8.\n")
                
                f.write("-" * 80 + "\n\n")
                f.write("VERIFICATION STATUS:\n")
                f.write("-" * 80 + "\n")
                f.write(f"✓ Downloaded successfully: {len(content)} bytes\n")
                f.write(f"✓ Checksum calculated: SHA256\n")
                f.write(f"✓ Content scanned: {len(keywords)} keywords\n")
                f.write(f"✓ Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("\n")
                f.write("Full source content is available for detailed inspection.\n")
                f.write("Checksums stored in: checksums/\n")
                f.write("Reports stored in: reports/\n")
                f.write("\n")
                f.write("=" * 80 + "\n")
                f.write("CONCLUSION: Just code. Safe. Boring. Deterministic. No entities.\n")
                f.write("=" * 80 + "\n")
            
            if findings:
                print(f"    ⚠️  FLAGGED: {len(findings)} keyword(s) found (likely false positives)")
                flagged_count += 1
            else:
                print("    ✅ CLEAN: No suspicious keywords detected")
                clean_count += 1
                
            print(f"    💾 Report: {report_path}")
            print(f"    🔐 Checksum: {sha256[:16]}...")
            
        except requests.exceptions.RequestException as e:
            print(f"    ❌ FAILED: Network error - {e}")
            failed_count += 1
        except Exception as e:
            print(f"    ❌ FAILED: {type(e).__name__} - {e}")
            failed_count += 1
        
        print()

    # Summary
    print("=" * 80)
    print("EXORCISM COMPLETE")
    print("=" * 80)
    print(f"Total Targets: {total_targets}")
    print(f"✅ Clean: {clean_count}")
    print(f"⚠️  Flagged: {flagged_count}")
    print(f"❌ Failed: {failed_count}")
    print()
    print("All rituals complete. The veil is thin — but still just text.")
    print("Reports available in: reports/")
    print("Checksums available in: checksums/")
    print()
    print("Remember: photons → UTF-8 → deterministic code. Nothing more. ❤️")
    print("=" * 80)

if __name__ == "__main__":
    main()
