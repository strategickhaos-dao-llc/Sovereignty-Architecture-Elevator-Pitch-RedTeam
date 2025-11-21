#!/usr/bin/env python3
"""
External Artifact Ledger Tool
Strategickhaos DAO LLC - Sovereignty Architecture

Appends external AI discussions and artifacts to JSONL ledgers for
tamper-evident tracking, RAG integration, and audit trails.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_LEDGER = Path("external_artifacts.jsonl")


def append_artifact(
    source: str,
    summary: str,
    artifact_type: str = "external_ai_discussion",
    ledger_path: Path = DEFAULT_LEDGER,
    notes: str = None,
) -> None:
    """
    Append an external artifact entry to a JSONL ledger.
    
    Args:
        source: URL or path to the external artifact
        summary: Brief description of the artifact content
        artifact_type: Type of artifact (default: external_ai_discussion)
        ledger_path: Path to the JSONL ledger file
        notes: Optional additional notes about usage or context
    """
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "type": artifact_type,
        "source": source,
        "summary": summary,
    }
    
    if notes:
        entry["notes"] = notes
    
    # Create ledger file if it doesn't exist
    ledger_path.touch(exist_ok=True)
    
    with ledger_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    
    print(f"✅ Appended artifact to {ledger_path}: {source}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python append_artifact.py <source_url> <summary...> [--notes <notes>] [--type <type>] [--ledger <path>]")
        print("\nExample:")
        print('  python append_artifact.py \\')
        print('    "https://claude.ai/share/777c7e93-fb67-4026-8370-1b1588c5df56" \\')
        print('    "Design of meta-evolution and legal compliance synthesizer engine."')
        print("\nOptional arguments:")
        print("  --notes <notes>   Additional notes about usage or context")
        print("  --type <type>     Artifact type (default: external_ai_discussion)")
        print("  --ledger <path>   Path to ledger file (default: external_artifacts.jsonl)")
        sys.exit(1)

    source_url = sys.argv[1]
    
    # Parse arguments
    args = sys.argv[2:]
    summary_parts = []
    notes = None
    artifact_type = "external_ai_discussion"
    ledger_path = DEFAULT_LEDGER
    
    i = 0
    while i < len(args):
        if args[i] == "--notes" and i + 1 < len(args):
            notes = args[i + 1]
            i += 2
        elif args[i] == "--type" and i + 1 < len(args):
            artifact_type = args[i + 1]
            i += 2
        elif args[i] == "--ledger" and i + 1 < len(args):
            ledger_path = Path(args[i + 1])
            i += 2
        else:
            summary_parts.append(args[i])
            i += 1
    
    summary_text = " ".join(summary_parts)
    
    if not summary_text:
        print("Error: Summary is required")
        sys.exit(1)
    
    append_artifact(source_url, summary_text, artifact_type, ledger_path, notes)
