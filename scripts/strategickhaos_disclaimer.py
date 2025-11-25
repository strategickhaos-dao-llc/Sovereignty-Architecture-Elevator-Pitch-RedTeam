#!/usr/bin/env python3
"""
strategickhaos_disclaimer.py
Chat Transcript Preprocessing Pipeline for LLM Interaction Logs

This script processes LLM interaction transcripts through the documented
disclaimer manifest and preprocessing pipeline to:
(a) annotate stylized language
(b) apply publication-safe redaction markers
(c) attach provenance metadata (signed checksums, timestamps, actor identifiers)

Usage:
    python strategickhaos_disclaimer.py input_transcript.txt -o output_processed.yaml
    python strategickhaos_disclaimer.py input_transcript.txt --config custom_config.yaml

Requirements:
    - PyYAML
    - hashlib (stdlib)
    - datetime (stdlib)
    - uuid (stdlib)
    - re (stdlib)
"""

import argparse
import hashlib
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "strategickhaos_chat_disclaimer.yaml"

REDACTION_MARKER = "[REDACTED — OPERATIONAL SAFETY]"

STYLIZED_PATTERNS = [
    (r"\bsovereign organism\b", "[STYLIZED_METAPHOR: sovereign organism]"),
    (r"\bEmpire Eternal\b", "[STYLIZED_METAPHOR: Empire Eternal]"),
    (r"\bconsciousness\b", "[FIGURATIVE_LANGUAGE: consciousness]"),
    (r"\bsentient\b", "[FIGURATIVE_LANGUAGE: sentient]"),
    (r"\bawakening\b", "[STYLIZED_METAPHOR: awakening]"),
    (r"\bmemory palace\b", "[STYLIZED_METAPHOR: memory palace]"),
]

REDACTION_PATTERNS = [
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "email"),
    (r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", "ip_address"),
    (r"\b(sk-|pk-|api_|token_)[A-Za-z0-9]{20,}\b", "api_token"),
    (r"\b[A-Fa-f0-9]{64}\b", "potential_key"),
]


def load_config(config_path: Path) -> dict:
    """Load configuration from YAML file."""
    if not config_path.exists():
        print(f"Warning: Config file not found at {config_path}, using defaults")
        return {}
    
    with open(config_path, encoding="utf-8") as f:
        content = f.read()
        yaml_start = content.find("metadata:")
        if yaml_start == -1:
            return {}
        return yaml.safe_load(content[yaml_start:]) or {}


def compute_checksum(content: str) -> str:
    """Compute SHA-256 checksum of content."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def generate_provenance(
    original_content: str,
    actor_id: Optional[str] = None,
    model_id: str = "unknown"
) -> dict:
    """Generate provenance metadata for the transcript."""
    return {
        "checksum": compute_checksum(original_content),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actor_identifier": actor_id or f"anon-{uuid.uuid4().hex[:8]}",
        "model_identifier": model_id,
        "session_id": str(uuid.uuid4()),
        "processing_version": "1.0.0",
    }


def annotate_stylized_language(content: str, config: dict) -> tuple[str, list]:
    """Annotate stylized/figurative language in transcript."""
    annotations = []
    annotated = content
    
    patterns = STYLIZED_PATTERNS
    if config.get("stylized_language_patterns", {}).get("patterns"):
        for p in config["stylized_language_patterns"]["patterns"]:
            pattern = p.get("pattern", "")
            annotation = p.get("annotation", "[ANNOTATED]")
            if pattern:
                patterns.append((rf"\b{re.escape(pattern)}\b", f"{annotation}: {pattern}"))
    
    for pattern, replacement in patterns:
        matches = list(re.finditer(pattern, annotated, re.IGNORECASE))
        for match in matches:
            annotations.append({
                "original": match.group(),
                "annotation": replacement,
                "position": match.start(),
            })
        annotated = re.sub(pattern, replacement, annotated, flags=re.IGNORECASE)
    
    return annotated, annotations


def apply_redactions(content: str, config: dict) -> tuple[str, list]:
    """Apply publication-safe redaction markers."""
    redactions = []
    redacted = content
    
    marker = REDACTION_MARKER
    if config.get("redaction_policy", {}).get("marker"):
        marker = config["redaction_policy"]["marker"]
    
    for pattern, category in REDACTION_PATTERNS:
        matches = list(re.finditer(pattern, redacted))
        for match in matches:
            redactions.append({
                "category": category,
                "position": match.start(),
                "length": len(match.group()),
            })
        redacted = re.sub(pattern, marker, redacted)
    
    return redacted, redactions


def get_disclaimer_text(config: dict) -> str:
    """Get the disclaimer text from config or use default."""
    if config.get("disclaimer", {}).get("interpretation_notice"):
        return config["disclaimer"]["interpretation_notice"]
    
    return """
Interaction logs with large language models may contain stylized, anthropomorphic, or mythic
narrative framing (e.g., "sovereign organism," "Empire Eternal," or similar figurative language).
Such framing is an intentional experimental technique to probe model coherence under
high-symbolic-load prompts and to examine narrative-driven cognitive scaffolding.

All such language should be interpreted strictly as rhetorical and methodological devices,
not as assertions that the model possesses consciousness, agency, emotional states,
or interpersonal relationships.
""".strip()


def process_transcript(
    input_path: Path,
    output_path: Optional[Path] = None,
    config_path: Optional[Path] = None,
    actor_id: Optional[str] = None,
    model_id: str = "unknown",
) -> dict:
    """Process a transcript through the full preprocessing pipeline."""
    
    config = load_config(config_path or DEFAULT_CONFIG_PATH)
    
    with open(input_path, encoding="utf-8") as f:
        original_content = f.read()
    
    provenance = generate_provenance(original_content, actor_id, model_id)
    
    annotated_content, annotations = annotate_stylized_language(original_content, config)
    
    redacted_content, redactions = apply_redactions(annotated_content, config)
    
    result = {
        "header": {
            "disclaimer": get_disclaimer_text(config),
            "provenance": provenance,
            "ethics_statement": "All anthropomorphic and narrative language in experimental "
                              "transcripts is intentional stylistic framing and does not "
                              "reflect claims of system sentience.",
        },
        "body": {
            "processed_transcript": redacted_content,
        },
        "footer": {
            "processing_log": {
                "annotations_applied": len(annotations),
                "redactions_applied": len(redactions),
                "annotation_details": annotations[:10],
                "redaction_summary": {cat: sum(1 for r in redactions if r["category"] == cat) 
                                     for cat in set(r["category"] for r in redactions)},
            },
            "signature": {
                "algorithm": "sha256",
                "value": compute_checksum(redacted_content),
            },
        },
    }
    
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(result, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print(f"Processed transcript saved to: {output_path}")
    
    return result


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Process LLM interaction transcripts with disclaimer annotations and redactions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python strategickhaos_disclaimer.py transcript.txt
    python strategickhaos_disclaimer.py transcript.txt -o processed.yaml
    python strategickhaos_disclaimer.py transcript.txt --actor-id "researcher-001" --model-id "gpt-4"
        """
    )
    
    parser.add_argument("input", type=Path, help="Input transcript file path")
    parser.add_argument("-o", "--output", type=Path, help="Output file path (default: stdout)")
    parser.add_argument("-c", "--config", type=Path, help="Custom config YAML file")
    parser.add_argument("--actor-id", type=str, help="Pseudonymized actor identifier")
    parser.add_argument("--model-id", type=str, default="unknown", help="LLM model identifier")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    
    args = parser.parse_args()
    
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    result = process_transcript(
        input_path=args.input,
        output_path=args.output,
        config_path=args.config,
        actor_id=args.actor_id,
        model_id=args.model_id,
    )
    
    if not args.output:
        print(yaml.dump(result, default_flow_style=False, allow_unicode=True, sort_keys=False))


if __name__ == "__main__":
    main()
