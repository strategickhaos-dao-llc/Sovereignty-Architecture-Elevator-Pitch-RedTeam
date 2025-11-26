#!/usr/bin/env python3
"""
Audit Chain Integrity Verification
Strategickhaos Sovereign Infrastructure Security Testing Suite

Cryptographic verification of audit logs with:
- Hash chain integrity verification
- Sequence continuity checking
- Timestamp monotonicity validation
- Tamper detection
- Watch mode for continuous monitoring
- Integration with alerting systems
"""

import argparse
import hashlib
import json
import logging
import os
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Generator
import signal

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class AuditEntry:
    """Represents a single audit log entry"""
    sequence: int
    timestamp: str
    event_type: str
    actor: str
    action: str
    resource: str
    outcome: str
    hash: str
    previous_hash: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "AuditEntry":
        return cls(
            sequence=data.get("sequence", 0),
            timestamp=data.get("timestamp", ""),
            event_type=data.get("event_type", ""),
            actor=data.get("actor", ""),
            action=data.get("action", ""),
            resource=data.get("resource", ""),
            outcome=data.get("outcome", ""),
            hash=data.get("hash", ""),
            previous_hash=data.get("previous_hash", ""),
            metadata=data.get("metadata", {})
        )
    
    def compute_hash(self, algorithm: str = "sha256") -> str:
        """Compute hash of this entry (excluding the hash field itself)"""
        data = {
            "sequence": self.sequence,
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "actor": self.actor,
            "action": self.action,
            "resource": self.resource,
            "outcome": self.outcome,
            "previous_hash": self.previous_hash,
            "metadata": self.metadata
        }
        content = json.dumps(data, sort_keys=True, separators=(',', ':'))
        
        if algorithm == "sha256":
            return hashlib.sha256(content.encode()).hexdigest()
        elif algorithm == "sha512":
            return hashlib.sha512(content.encode()).hexdigest()
        elif algorithm == "blake2b":
            return hashlib.blake2b(content.encode()).hexdigest()
        else:
            raise ValueError(f"Unsupported hash algorithm: {algorithm}")


@dataclass
class VerificationResult:
    """Result of verifying a single audit entry"""
    sequence: int
    valid: bool
    errors: List[str]
    warnings: List[str]
    entry_hash: str
    computed_hash: str
    timestamp: str


@dataclass
class ChainVerificationReport:
    """Comprehensive chain verification report"""
    source: str
    total_entries: int
    valid_entries: int
    invalid_entries: int
    chain_intact: bool
    first_sequence: int
    last_sequence: int
    missing_sequences: List[int]
    timestamp_violations: List[Dict]
    hash_mismatches: List[Dict]
    verification_errors: List[str]
    start_time: str
    end_time: str
    duration_seconds: float
    
    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


class AuditChainVerifier:
    """
    Verifies the integrity of cryptographic audit chains.
    
    Features:
    - Hash chain verification
    - Sequence continuity
    - Timestamp monotonicity
    - Tamper detection
    - Real-time monitoring (watch mode)
    """
    
    GENESIS_HASH = "0" * 64  # Genesis block previous hash
    
    def __init__(
        self,
        hash_algorithm: str = "sha256",
        strict_mode: bool = False,
        allow_gaps: bool = False
    ):
        self.hash_algorithm = hash_algorithm
        self.strict_mode = strict_mode
        self.allow_gaps = allow_gaps
        self.verification_results: List[VerificationResult] = []
        
    def load_entries_from_file(self, filepath: str) -> Generator[AuditEntry, None, None]:
        """Load audit entries from NDJSON file"""
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        data = json.loads(line)
                        yield AuditEntry.from_dict(data)
                    except json.JSONDecodeError as e:
                        logger.warning(f"Failed to parse line: {e}")
    
    def load_entries_from_json(self, filepath: str) -> Generator[AuditEntry, None, None]:
        """Load audit entries from JSON array file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                for entry in data:
                    yield AuditEntry.from_dict(entry)
            elif isinstance(data, dict) and "entries" in data:
                for entry in data["entries"]:
                    yield AuditEntry.from_dict(entry)
    
    def verify_entry(
        self,
        entry: AuditEntry,
        previous_entry: Optional[AuditEntry] = None
    ) -> VerificationResult:
        """Verify a single audit entry"""
        errors = []
        warnings = []
        
        # Compute expected hash
        computed_hash = entry.compute_hash(self.hash_algorithm)
        
        # Check hash integrity
        if entry.hash != computed_hash:
            errors.append(f"Hash mismatch: expected {computed_hash[:16]}..., got {entry.hash[:16]}...")
        
        # Check chain continuity
        if previous_entry:
            # Previous hash should match
            if entry.previous_hash != previous_entry.hash:
                errors.append(f"Chain broken: previous_hash doesn't match previous entry's hash")
            
            # Sequence should be consecutive (unless gaps allowed)
            expected_sequence = previous_entry.sequence + 1
            if entry.sequence != expected_sequence:
                if self.allow_gaps:
                    warnings.append(f"Sequence gap: expected {expected_sequence}, got {entry.sequence}")
                else:
                    errors.append(f"Sequence discontinuity: expected {expected_sequence}, got {entry.sequence}")
            
            # Timestamp should be monotonically increasing
            try:
                prev_ts = datetime.fromisoformat(previous_entry.timestamp.replace('Z', '+00:00'))
                curr_ts = datetime.fromisoformat(entry.timestamp.replace('Z', '+00:00'))
                
                if curr_ts < prev_ts:
                    if self.strict_mode:
                        errors.append(f"Timestamp regression: {entry.timestamp} < {previous_entry.timestamp}")
                    else:
                        warnings.append(f"Timestamp regression: {entry.timestamp} < {previous_entry.timestamp}")
            except ValueError as e:
                warnings.append(f"Could not parse timestamps: {e}")
        else:
            # First entry - check genesis hash
            if entry.previous_hash != self.GENESIS_HASH and entry.sequence == 0:
                warnings.append(f"First entry doesn't have genesis hash")
        
        # Validate required fields
        required_fields = ["timestamp", "actor", "action", "outcome"]
        for field in required_fields:
            if not getattr(entry, field, None):
                if self.strict_mode:
                    errors.append(f"Missing required field: {field}")
                else:
                    warnings.append(f"Missing field: {field}")
        
        return VerificationResult(
            sequence=entry.sequence,
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            entry_hash=entry.hash,
            computed_hash=computed_hash,
            timestamp=entry.timestamp
        )
    
    def verify_chain(
        self,
        entries: Generator[AuditEntry, None, None]
    ) -> ChainVerificationReport:
        """Verify entire audit chain"""
        start_time = datetime.now(timezone.utc)
        
        valid_count = 0
        invalid_count = 0
        previous_entry = None
        all_sequences = []
        timestamp_violations = []
        hash_mismatches = []
        verification_errors = []
        first_sequence = None
        last_sequence = None
        
        for entry in entries:
            result = self.verify_entry(entry, previous_entry)
            self.verification_results.append(result)
            
            if first_sequence is None:
                first_sequence = entry.sequence
            last_sequence = entry.sequence
            all_sequences.append(entry.sequence)
            
            if result.valid:
                valid_count += 1
            else:
                invalid_count += 1
                
                for error in result.errors:
                    if "Hash mismatch" in error:
                        hash_mismatches.append({
                            "sequence": entry.sequence,
                            "expected": result.computed_hash,
                            "actual": result.entry_hash,
                            "timestamp": entry.timestamp
                        })
                    elif "Timestamp" in error:
                        timestamp_violations.append({
                            "sequence": entry.sequence,
                            "timestamp": entry.timestamp,
                            "error": error
                        })
                    else:
                        verification_errors.append(f"Seq {entry.sequence}: {error}")
            
            # Log warnings
            for warning in result.warnings:
                logger.warning(f"Seq {entry.sequence}: {warning}")
            
            previous_entry = entry
        
        end_time = datetime.now(timezone.utc)
        
        # Find missing sequences
        missing_sequences = []
        if first_sequence is not None and last_sequence is not None:
            expected_sequences = set(range(first_sequence, last_sequence + 1))
            actual_sequences = set(all_sequences)
            missing_sequences = sorted(list(expected_sequences - actual_sequences))
        
        # Determine if chain is intact
        chain_intact = (
            invalid_count == 0 and
            len(missing_sequences) == 0 and
            len(hash_mismatches) == 0
        )
        
        return ChainVerificationReport(
            source="audit_chain",
            total_entries=valid_count + invalid_count,
            valid_entries=valid_count,
            invalid_entries=invalid_count,
            chain_intact=chain_intact,
            first_sequence=first_sequence or 0,
            last_sequence=last_sequence or 0,
            missing_sequences=missing_sequences,
            timestamp_violations=timestamp_violations,
            hash_mismatches=hash_mismatches,
            verification_errors=verification_errors,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            duration_seconds=(end_time - start_time).total_seconds()
        )
    
    def verify_file(self, filepath: str) -> ChainVerificationReport:
        """Verify audit chain from file"""
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # Determine file format
        if path.suffix == ".ndjson" or path.suffix == ".jsonl":
            entries = self.load_entries_from_file(filepath)
        else:
            entries = self.load_entries_from_json(filepath)
        
        report = self.verify_chain(entries)
        report.source = str(path)
        return report
    
    def watch_file(
        self,
        filepath: str,
        callback: Optional[callable] = None,
        poll_interval: float = 1.0
    ):
        """
        Watch file for new entries and verify continuously.
        
        Args:
            filepath: Path to audit log file
            callback: Function to call on each new entry verification
            poll_interval: Seconds between file checks
        """
        logger.info(f"Starting watch mode on {filepath}")
        
        path = Path(filepath)
        last_position = 0
        last_sequence = -1
        previous_entry = None
        running = True
        
        def signal_handler(signum, frame):
            nonlocal running
            logger.info("Received shutdown signal")
            running = False
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        while running:
            try:
                if not path.exists():
                    time.sleep(poll_interval)
                    continue
                
                current_size = path.stat().st_size
                
                if current_size > last_position:
                    with open(filepath, 'r') as f:
                        f.seek(last_position)
                        
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue
                            
                            try:
                                data = json.loads(line)
                                entry = AuditEntry.from_dict(data)
                                
                                # Skip if we've already processed this sequence
                                if entry.sequence <= last_sequence:
                                    continue
                                
                                result = self.verify_entry(entry, previous_entry)
                                
                                if not result.valid:
                                    logger.error(f"TAMPER DETECTED at sequence {entry.sequence}")
                                    for error in result.errors:
                                        logger.error(f"  {error}")
                                    
                                    if callback:
                                        callback({
                                            "event": "tamper_detected",
                                            "sequence": entry.sequence,
                                            "errors": result.errors,
                                            "timestamp": datetime.now(timezone.utc).isoformat()
                                        })
                                else:
                                    logger.debug(f"Verified sequence {entry.sequence}")
                                
                                previous_entry = entry
                                last_sequence = entry.sequence
                                
                            except json.JSONDecodeError:
                                logger.warning(f"Failed to parse line")
                        
                        last_position = f.tell()
                
                time.sleep(poll_interval)
                
            except Exception as e:
                logger.error(f"Watch error: {e}")
                time.sleep(poll_interval)
        
        logger.info("Watch mode stopped")


def create_sample_chain(num_entries: int = 10) -> List[Dict]:
    """Create a sample audit chain for testing"""
    entries = []
    previous_hash = AuditChainVerifier.GENESIS_HASH
    
    for i in range(num_entries):
        entry = AuditEntry(
            sequence=i,
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_type="access",
            actor=f"user-{i % 3}",
            action="read" if i % 2 == 0 else "write",
            resource=f"/api/v1/resource/{i}",
            outcome="success",
            hash="",  # Will be computed
            previous_hash=previous_hash,
            metadata={"request_id": f"req-{i:04d}"}
        )
        
        # Compute and set hash
        entry.hash = entry.compute_hash()
        previous_hash = entry.hash
        
        entries.append(asdict(entry))
        
        # Small delay for timestamp variation
        time.sleep(0.01)
    
    return entries


def main():
    parser = argparse.ArgumentParser(
        description="Audit Chain Integrity Verification"
    )
    parser.add_argument(
        "--file", "-f",
        help="Audit log file to verify (JSON or NDJSON)"
    )
    parser.add_argument(
        "--output", "-o",
        help="JSON report output file"
    )
    parser.add_argument(
        "--watch", "-w",
        action="store_true",
        help="Watch mode: continuously monitor file for new entries"
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=1.0,
        help="Poll interval for watch mode (seconds)"
    )
    parser.add_argument(
        "--algorithm", "-a",
        choices=["sha256", "sha512", "blake2b"],
        default="sha256",
        help="Hash algorithm (default: sha256)"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Strict mode: treat warnings as errors"
    )
    parser.add_argument(
        "--allow-gaps",
        action="store_true",
        help="Allow gaps in sequence numbers"
    )
    parser.add_argument(
        "--generate-sample",
        type=int,
        metavar="N",
        help="Generate sample chain with N entries for testing"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Generate sample chain if requested
    if args.generate_sample:
        sample = create_sample_chain(args.generate_sample)
        output_file = args.output or "sample_audit_chain.ndjson"
        
        with open(output_file, 'w') as f:
            for entry in sample:
                f.write(json.dumps(entry) + "\n")
        
        logger.info(f"Generated sample chain with {args.generate_sample} entries to {output_file}")
        sys.exit(0)
    
    if not args.file:
        parser.error("--file is required unless using --generate-sample")
    
    verifier = AuditChainVerifier(
        hash_algorithm=args.algorithm,
        strict_mode=args.strict,
        allow_gaps=args.allow_gaps
    )
    
    if args.watch:
        # Watch mode
        def alert_callback(event):
            logger.critical(f"ALERT: {json.dumps(event)}")
            # Could integrate with Discord, PagerDuty, etc.
        
        verifier.watch_file(
            args.file,
            callback=alert_callback,
            poll_interval=args.poll_interval
        )
    else:
        # Single verification
        try:
            report = verifier.verify_file(args.file)
            
            # Output report
            print("\n" + "=" * 60)
            print("AUDIT CHAIN VERIFICATION REPORT")
            print("=" * 60)
            print(f"Source: {report.source}")
            print(f"Duration: {report.duration_seconds:.3f} seconds")
            print(f"Total Entries: {report.total_entries}")
            print(f"Valid: {report.valid_entries}")
            print(f"Invalid: {report.invalid_entries}")
            print()
            
            if report.chain_intact:
                print("✅ CHAIN INTEGRITY: INTACT")
            else:
                print("❌ CHAIN INTEGRITY: COMPROMISED")
            
            print()
            print(f"Sequence Range: {report.first_sequence} - {report.last_sequence}")
            
            if report.missing_sequences:
                print(f"⚠️  Missing Sequences: {report.missing_sequences[:10]}...")
            
            if report.hash_mismatches:
                print()
                print("HASH MISMATCHES:")
                for mismatch in report.hash_mismatches[:5]:
                    print(f"  Seq {mismatch['sequence']}: {mismatch['timestamp']}")
            
            if report.timestamp_violations:
                print()
                print("TIMESTAMP VIOLATIONS:")
                for violation in report.timestamp_violations[:5]:
                    print(f"  Seq {violation['sequence']}: {violation['error']}")
            
            if report.verification_errors:
                print()
                print("VERIFICATION ERRORS:")
                for error in report.verification_errors[:10]:
                    print(f"  {error}")
            
            print("=" * 60)
            
            # Save report
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(report.to_json())
                logger.info(f"Report saved to {args.output}")
            
            # Exit with error if chain is compromised
            if not report.chain_intact:
                sys.exit(1)
            
        except FileNotFoundError as e:
            logger.error(str(e))
            sys.exit(1)
        except Exception as e:
            logger.error(f"Verification failed: {e}")
            sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
