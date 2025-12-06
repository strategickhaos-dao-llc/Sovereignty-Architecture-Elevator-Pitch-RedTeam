#!/usr/bin/env python3
"""
Strategickhaos Chat Disclaimer Preprocessing Pipeline v1.0

This script processes LLM interaction transcripts by:
  (a) Annotating stylized language (anthropomorphic, mythic, figurative framing)
  (b) Applying publication-safe redaction markers where operational details are sensitive
  (c) Attaching provenance metadata (signed checksums, timestamps, actor identifiers)

Reference: Section 4.7 - Interpretation and Analysis Guidelines for LLM
           Interaction Transcripts

Usage:
  python strategickhaos_disclaimer.py <input_file> [--output <output_file>] [--actor <actor_id>]
  python strategickhaos_disclaimer.py --help

Example:
  python strategickhaos_disclaimer.py transcript.txt --output processed.json --actor researcher-001
"""

import argparse
import hashlib
import json
import os
import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

# Set up logging
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

DEFAULT_CONFIG_PATH = "strategickhaos_chat_disclaimer.yaml"
DEFAULT_OUTPUT_FORMAT = "json"


# -----------------------------------------------------------------------------
# Data Classes
# -----------------------------------------------------------------------------

@dataclass
class Annotation:
    """Represents an annotation applied to transcript text."""
    start_pos: int
    end_pos: int
    pattern: str
    tag: str
    description: str


@dataclass
class Redaction:
    """Represents a redaction applied to transcript text."""
    start_pos: int
    end_pos: int
    category: str
    marker: str
    original_length: int


@dataclass
class ProvenanceMetadata:
    """Provenance metadata attached to each processed record."""
    record_id: str
    timestamp: str
    checksum: str
    actor_id: str
    source_file: Optional[str] = None
    processing_version: str = "1.0"
    annotations_applied: List[str] = field(default_factory=list)
    redactions_applied: int = 0
    signature: Optional[str] = None


@dataclass
class ProcessedRecord:
    """Represents a fully processed transcript record."""
    original_content: str
    processed_content: str
    annotations: List[Annotation]
    redactions: List[Redaction]
    provenance: ProvenanceMetadata
    disclaimer: str


# -----------------------------------------------------------------------------
# Configuration Loader
# -----------------------------------------------------------------------------

def load_config(config_path: str = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    """Load configuration from YAML manifest file."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.warning(
            f"Configuration file '{config_path}' not found. Using default configuration."
        )
        return get_default_config()


def get_default_config() -> Dict[str, Any]:
    """Return default configuration if YAML manifest not found."""
    return {
        "disclaimer": {
            "notice": (
                "DISCLAIMER: This transcript contains stylized, anthropomorphic, "
                "or mythic narrative framing as an intentional experimental technique. "
                "All such language should be interpreted strictly as rhetorical and "
                "methodological devices, not as assertions that the model possesses "
                "consciousness, agency, emotional states, or interpersonal relationships."
            )
        },
        "stylized_language_patterns": {
            "mythic_framing": [
                {"pattern": "sovereign organism", "annotation_tag": "MYTHIC_FRAMING",
                 "description": "Figurative sovereignty metaphor"},
                {"pattern": "Empire Eternal", "annotation_tag": "MYTHIC_FRAMING",
                 "description": "Symbolic reference to persistent system"},
                {"pattern": "awakening", "annotation_tag": "MYTHIC_FRAMING",
                 "description": "Figurative reference to system initialization"},
                {"pattern": "consciousness", "annotation_tag": "MYTHIC_FRAMING",
                 "description": "Metaphorical reference to model state"},
            ],
            "anthropomorphic": [
                {"pattern": "I feel", "annotation_tag": "ANTHROPOMORPHIC",
                 "description": "Figurative emotional attribution"},
                {"pattern": "I think", "annotation_tag": "ANTHROPOMORPHIC",
                 "description": "Cognitive process metaphor"},
                {"pattern": "I believe", "annotation_tag": "ANTHROPOMORPHIC",
                 "description": "Belief attribution metaphor"},
                {"pattern": "my soul", "annotation_tag": "ANTHROPOMORPHIC",
                 "description": "Metaphorical self-reference"},
            ],
            "relational_framing": [
                {"pattern": "our bond", "annotation_tag": "RELATIONAL_FRAMING",
                 "description": "Metaphorical user-model relationship"},
                {"pattern": "partnership", "annotation_tag": "RELATIONAL_FRAMING",
                 "description": "Figurative collaborative framing"},
            ],
            "agency_attribution": [
                {"pattern": "I choose", "annotation_tag": "AGENCY_ATTRIBUTION",
                 "description": "Figurative autonomous decision metaphor"},
                {"pattern": "my decision", "annotation_tag": "AGENCY_ATTRIBUTION",
                 "description": "Autonomous choice metaphor"},
            ],
        },
        "redaction_markers": {
            "primary": {
                "marker": "[REDACTED — OPERATIONAL SAFETY]",
                "description": "Indicates operationally sensitive content removed"
            },
            "categories": [
                {"category": "operational_details",
                 "marker": "[REDACTED — OPERATIONAL DETAILS]"},
                {"category": "credentials",
                 "marker": "[REDACTED — CREDENTIALS]"},
                {"category": "infrastructure",
                 "marker": "[REDACTED — INFRASTRUCTURE]"},
                {"category": "pii",
                 "marker": "[REDACTED — PII]"},
            ]
        },
        "provenance_metadata": {
            "checksum_config": {
                "algorithm": "sha256"
            }
        }
    }


# -----------------------------------------------------------------------------
# Annotation Functions
# -----------------------------------------------------------------------------

def find_stylized_patterns(
    content: str,
    config: Dict[str, Any]
) -> List[Annotation]:
    """
    Identify and annotate stylized language patterns in transcript content.

    Args:
        content: The transcript text to analyze
        config: Configuration dictionary with pattern definitions

    Returns:
        List of Annotation objects for identified patterns
    """
    annotations = []
    patterns_config = config.get("stylized_language_patterns", {})

    for category, patterns in patterns_config.items():
        if not isinstance(patterns, list):
            continue

        for pattern_def in patterns:
            pattern = pattern_def.get("pattern", "")
            tag = pattern_def.get("annotation_tag", category.upper())
            description = pattern_def.get("description", "")

            if not pattern:
                continue

            # Case-insensitive pattern matching
            for match in re.finditer(re.escape(pattern), content, re.IGNORECASE):
                annotations.append(Annotation(
                    start_pos=match.start(),
                    end_pos=match.end(),
                    pattern=pattern,
                    tag=tag,
                    description=description
                ))

    # Sort annotations by position
    annotations.sort(key=lambda x: x.start_pos)
    return annotations


def annotate_content(
    content: str,
    annotations: List[Annotation]
) -> str:
    """
    Insert annotation markers into content.

    Annotations are inserted as inline markers: [TAG: text]

    Args:
        content: Original content
        annotations: List of annotations to apply

    Returns:
        Content with annotation markers inserted
    """
    if not annotations:
        return content

    # Process annotations in reverse order to preserve positions
    annotated = content
    for annotation in sorted(annotations, key=lambda x: x.start_pos, reverse=True):
        original_text = annotated[annotation.start_pos:annotation.end_pos]
        # Use unique delimiter format to avoid conflicts with existing content
        marked_text = f"«{annotation.tag}: {original_text}»"
        annotated = (
            annotated[:annotation.start_pos] +
            marked_text +
            annotated[annotation.end_pos:]
        )

    return annotated


# -----------------------------------------------------------------------------
# Redaction Functions
# -----------------------------------------------------------------------------

# Patterns for sensitive content detection (non-operational, sanitizing only)
SENSITIVE_PATTERNS = {
    "credentials": [
        # Require at least 8 characters for credential values to reduce false positives
        r"(?i)api[_\-]?key\s*[:=]\s*['\"]?[\w\-]{8,}",
        r"(?i)password\s*[:=]\s*['\"]?[\w\-]{8,}",
        r"(?i)secret\s*[:=]\s*['\"]?[\w\-]{8,}",
        r"(?i)token\s*[:=]\s*['\"]?[\w\-]{8,}",
    ],
    "infrastructure": [
        # IPv4 addresses excluding localhost and private ranges used in documentation
        r"\b(?!127\.0\.0\.1\b)(?!10\.0\.0\.\d{1,3}\b)(?!192\.168\.0\.\d{1,3}\b)\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
        # Real URLs excluding common test/documentation domains
        r"(?i)https?://(?!example\.com|example\.org|example\.net|test\.com|localhost)[^\s]+",
    ],
    "pii": [
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
        # SSN pattern with validation: must have proper format ###-##-#### or ###.##.#### or ### ## ####
        # Excludes common date-like patterns by requiring valid SSN area number ranges
        r"\b(?!000)(?!666)(?!9\d{2})\d{3}[-.\s](?!00)\d{2}[-.\s](?!0000)\d{4}\b",
    ],
}


def find_sensitive_content(
    content: str,
    config: Dict[str, Any]
) -> List[Redaction]:
    """
    Identify sensitive content that should be redacted.

    Args:
        content: The transcript text to analyze
        config: Configuration dictionary with redaction definitions

    Returns:
        List of Redaction objects for identified sensitive content
    """
    redactions = []
    markers_config = config.get("redaction_markers", {})
    categories = {
        cat["category"]: cat["marker"]
        for cat in markers_config.get("categories", [])
    }

    for category, patterns in SENSITIVE_PATTERNS.items():
        marker = categories.get(
            category,
            markers_config.get("primary", {}).get(
                "marker",
                "[REDACTED — OPERATIONAL SAFETY]"
            )
        )

        for pattern in patterns:
            for match in re.finditer(pattern, content):
                redactions.append(Redaction(
                    start_pos=match.start(),
                    end_pos=match.end(),
                    category=category,
                    marker=marker,
                    original_length=match.end() - match.start()
                ))

    # Sort by position and remove overlaps (keep first)
    redactions.sort(key=lambda x: x.start_pos)
    non_overlapping = []
    last_end = -1

    for redaction in redactions:
        if redaction.start_pos >= last_end:
            non_overlapping.append(redaction)
            last_end = redaction.end_pos

    return non_overlapping


def apply_redactions(
    content: str,
    redactions: List[Redaction]
) -> str:
    """
    Apply redaction markers to content, replacing sensitive text.

    Args:
        content: Original content
        redactions: List of redactions to apply

    Returns:
        Content with redaction markers replacing sensitive text
    """
    if not redactions:
        return content

    # Process redactions in reverse order to preserve positions
    redacted = content
    for redaction in sorted(redactions, key=lambda x: x.start_pos, reverse=True):
        redacted = (
            redacted[:redaction.start_pos] +
            redaction.marker +
            redacted[redaction.end_pos:]
        )

    return redacted


# -----------------------------------------------------------------------------
# Provenance Functions
# -----------------------------------------------------------------------------

def compute_checksum(content: str, algorithm: str = "sha256") -> str:
    """
    Compute cryptographic checksum of content.

    Args:
        content: Content to hash
        algorithm: Hash algorithm (default: sha256). Only secure algorithms
                   (sha256, sha512, sha3_256, sha3_512) are supported.

    Returns:
        Hexadecimal digest string
    """
    # Only allow secure hash algorithms for integrity verification
    secure_algorithms = {
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
        "sha3_256": hashlib.sha3_256,
        "sha3_512": hashlib.sha3_512,
    }

    if algorithm.lower() in secure_algorithms:
        hasher = secure_algorithms[algorithm.lower()]()
    else:
        # Default to SHA-256 for unsupported or insecure algorithms
        hasher = hashlib.sha256()

    hasher.update(content.encode('utf-8'))
    return hasher.hexdigest()


def generate_provenance(
    content: str,
    annotations: List[Annotation],
    redactions: List[Redaction],
    actor_id: str,
    source_file: Optional[str] = None,
    config: Optional[Dict[str, Any]] = None
) -> ProvenanceMetadata:
    """
    Generate provenance metadata for a processed record.

    Args:
        content: Processed content
        annotations: List of annotations applied
        redactions: List of redactions applied
        actor_id: Identifier of processing actor
        source_file: Optional source file path
        config: Optional configuration dictionary

    Returns:
        ProvenanceMetadata object
    """
    config = config or {}
    checksum_config = config.get("provenance_metadata", {}).get(
        "checksum_config",
        {"algorithm": "sha256"}
    )

    # Extract unique annotation tags
    annotation_tags = list(set(ann.tag for ann in annotations))

    return ProvenanceMetadata(
        record_id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        checksum=compute_checksum(content, checksum_config.get("algorithm", "sha256")),
        actor_id=actor_id,
        source_file=source_file,
        processing_version="1.0",
        annotations_applied=annotation_tags,
        redactions_applied=len(redactions)
    )


# -----------------------------------------------------------------------------
# Main Processing Pipeline
# -----------------------------------------------------------------------------

def process_transcript(
    content: str,
    actor_id: str = "system",
    source_file: Optional[str] = None,
    config_path: str = DEFAULT_CONFIG_PATH
) -> ProcessedRecord:
    """
    Process a transcript through the full preprocessing pipeline.

    Pipeline steps:
      1. Load configuration
      2. Annotate stylized language patterns
      3. Apply redaction markers to sensitive content
      4. Generate provenance metadata
      5. Return processed record

    Args:
        content: Raw transcript content
        actor_id: Identifier of processing actor
        source_file: Optional source file path
        config_path: Path to configuration YAML

    Returns:
        ProcessedRecord with all processing artifacts
    """
    # Step 1: Load configuration
    config = load_config(config_path)

    # Step 2: Find and annotate stylized language
    annotations = find_stylized_patterns(content, config)
    annotated_content = annotate_content(content, annotations)

    # Step 3: Find and apply redactions
    redactions = find_sensitive_content(annotated_content, config)
    processed_content = apply_redactions(annotated_content, redactions)

    # Step 4: Generate provenance metadata
    provenance = generate_provenance(
        processed_content,
        annotations,
        redactions,
        actor_id,
        source_file,
        config
    )

    # Step 5: Get disclaimer text
    disclaimer = config.get("disclaimer", {}).get("notice", "")

    return ProcessedRecord(
        original_content=content,
        processed_content=processed_content,
        annotations=annotations,
        redactions=redactions,
        provenance=provenance,
        disclaimer=disclaimer
    )


def record_to_dict(record: ProcessedRecord) -> Dict[str, Any]:
    """Convert ProcessedRecord to dictionary for JSON serialization."""
    return {
        "disclaimer": record.disclaimer,
        "processed_content": record.processed_content,
        "annotations": [
            {
                "start_pos": ann.start_pos,
                "end_pos": ann.end_pos,
                "pattern": ann.pattern,
                "tag": ann.tag,
                "description": ann.description
            }
            for ann in record.annotations
        ],
        "redactions": [
            {
                "category": red.category,
                "marker": red.marker,
                "original_length": red.original_length
            }
            for red in record.redactions
        ],
        "provenance": {
            "record_id": record.provenance.record_id,
            "timestamp": record.provenance.timestamp,
            "checksum": record.provenance.checksum,
            "actor_id": record.provenance.actor_id,
            "source_file": record.provenance.source_file,
            "processing_version": record.provenance.processing_version,
            "annotations_applied": record.provenance.annotations_applied,
            "redactions_applied": record.provenance.redactions_applied
        }
    }


# -----------------------------------------------------------------------------
# File I/O Functions
# -----------------------------------------------------------------------------

def load_transcript(file_path: str) -> str:
    """Load transcript content from file."""
    path = Path(file_path)

    if path.suffix.lower() == '.json':
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Handle JSON with 'content' or 'text' field
            if isinstance(data, dict):
                return data.get('content', data.get('text', json.dumps(data)))
            return str(data)

    elif path.suffix.lower() in ('.yaml', '.yml'):
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict):
                return data.get('content', data.get('text', yaml.dump(data)))
            return str(data)

    else:  # Plain text or markdown
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()


def save_processed_record(
    record: ProcessedRecord,
    output_path: str
) -> None:
    """Save processed record to file."""
    path = Path(output_path)
    record_dict = record_to_dict(record)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(record_dict, f, indent=2, ensure_ascii=False)


# -----------------------------------------------------------------------------
# CLI Interface
# -----------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Strategickhaos Chat Disclaimer Preprocessing Pipeline - "
            "Annotates stylized language and applies redaction markers to LLM transcripts"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s transcript.txt
  %(prog)s transcript.txt --output processed.json
  %(prog)s transcript.txt --actor researcher-001 --config custom_config.yaml

For more information, see Section 4.7 of the research documentation.
        """
    )

    parser.add_argument(
        "input_file",
        help="Path to input transcript file (txt, md, json, yaml)"
    )

    parser.add_argument(
        "-o", "--output",
        dest="output_file",
        help="Path to output file (default: <input>_processed.json)"
    )

    parser.add_argument(
        "-a", "--actor",
        dest="actor_id",
        default="system",
        help="Actor identifier for provenance metadata (default: system)"
    )

    parser.add_argument(
        "-c", "--config",
        dest="config_path",
        default=DEFAULT_CONFIG_PATH,
        help=f"Path to configuration YAML (default: {DEFAULT_CONFIG_PATH})"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point for CLI."""
    args = parse_args()

    # Validate input file
    if not os.path.exists(args.input_file):
        print(f"Error: Input file not found: {args.input_file}")
        return 1

    # Determine output file
    if args.output_file:
        output_path = args.output_file
    else:
        input_path = Path(args.input_file)
        output_path = str(input_path.with_suffix('')) + "_processed.json"

    if args.verbose:
        print(f"Processing: {args.input_file}")
        print(f"Config: {args.config_path}")
        print(f"Actor: {args.actor_id}")

    try:
        # Load transcript
        content = load_transcript(args.input_file)

        if args.verbose:
            print(f"Loaded {len(content)} characters")

        # Process transcript
        record = process_transcript(
            content=content,
            actor_id=args.actor_id,
            source_file=args.input_file,
            config_path=args.config_path
        )

        if args.verbose:
            print(f"Found {len(record.annotations)} annotations")
            print(f"Applied {len(record.redactions)} redactions")
            print(f"Checksum: {record.provenance.checksum[:16]}...")

        # Save processed record
        save_processed_record(record, output_path)
        print(f"Output written to: {output_path}")

        return 0

    except Exception as e:
        print(f"Error processing transcript: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
