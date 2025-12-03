#!/usr/bin/env python3
"""
State Updater CLI - Strategickhaos DAO LLC
Idempotent state management with pluggable collectors.

INTERNAL DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

# Schema version this tool produces
TOOL_VERSION = "1.0.0"
SCHEMA_VERSION = "1.0.0"

# Default paths
DEFAULT_STATE_FILE = "strategickhaos_state_snapshot.json"
DEFAULT_SCHEMA_FILE = "governance/strategickhaos_state_snapshot.schema.json"


def compute_sha256(data: str) -> str:
    """Compute SHA-256 hash of string data."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def compute_file_sha256(filepath: Path) -> str:
    """Compute SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def get_timestamp() -> str:
    """Get current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


def generate_snapshot_id(content: str) -> str:
    """Generate snapshot ID from content hash."""
    return compute_sha256(content)


class Collector(ABC):
    """Base class for data collectors."""

    name: str = "base"

    @abstractmethod
    def collect(self, config: dict) -> dict:
        """Collect data and return normalized records."""

    def get_source_reference(self) -> dict:
        """Get source reference for provenance."""
        return {
            "type": "api",
            "reference": f"collector:{self.name}",
            "retrieved_at": get_timestamp(),
        }


class GitCollector(Collector):
    """Collect repository information from Git."""

    name = "git"

    def collect(self, config: dict) -> dict:
        """Collect Git repository data."""
        repos = {}
        repo_configs = config.get("repositories", [])

        for repo_config in repo_configs:
            repo_path = repo_config.get("path", ".")
            repo_id = repo_config.get("id", Path(repo_path).name)

            try:
                # Get last commit SHA
                result = subprocess.run(
                    ["git", "-C", repo_path, "rev-parse", "HEAD"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                last_commit_sha = result.stdout.strip()

                # Get last commit date
                result = subprocess.run(
                    ["git", "-C", repo_path, "log", "-1", "--format=%cI"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                last_commit_date = result.stdout.strip()

                # Get remote URL
                result = subprocess.run(
                    ["git", "-C", repo_path, "remote", "get-url", "origin"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                url = result.stdout.strip() if result.returncode == 0 else ""

                # Get current branch
                result = subprocess.run(
                    ["git", "-C", repo_path, "branch", "--show-current"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                branch = result.stdout.strip() if result.returncode == 0 else "main"

                repos[repo_id] = {
                    "id": repo_id,
                    "name": repo_config.get("name", repo_id),
                    "url": url,
                    "status": "active",
                    "default_branch": branch,
                    "last_commit_sha": last_commit_sha,
                    "last_commit_date": last_commit_date,
                    "health_score": self._compute_health_score(repo_path),
                    "compliance": self._check_compliance(repo_path),
                }
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                print(f"  Warning: Could not collect Git data for {repo_id}: {e}")
                repos[repo_id] = {
                    "id": repo_id,
                    "name": repo_config.get("name", repo_id),
                    "url": "",
                    "status": "unknown",
                }

        return {"repositories": repos}

    def _compute_health_score(self, repo_path: str) -> float:
        """Compute a basic health score for the repository."""
        score = 50.0  # Base score
        path = Path(repo_path)

        # Check for essential files
        if (path / "README.md").exists():
            score += 10
        if (path / "LICENSE").exists():
            score += 10
        if (path / ".gitignore").exists():
            score += 5
        if (path / "SECURITY.md").exists():
            score += 10
        if (path / "CODEOWNERS").exists() or (path / ".github" / "CODEOWNERS").exists():
            score += 5
        if (path / ".github" / "workflows").exists():
            score += 10

        return min(score, 100.0)

    def _check_compliance(self, repo_path: str) -> dict:
        """Check repository compliance requirements."""
        path = Path(repo_path)
        return {
            "has_license": (path / "LICENSE").exists(),
            "has_readme": (path / "README.md").exists(),
            "has_security_policy": (path / "SECURITY.md").exists(),
            "has_codeowners": (
                (path / "CODEOWNERS").exists()
                or (path / ".github" / "CODEOWNERS").exists()
            ),
        }


class PDFCollector(Collector):
    """Collect and hash PDF documents."""

    name = "pdf"

    def collect(self, config: dict) -> dict:
        """Collect PDF document hashes."""
        facts = []
        pdf_paths = config.get("pdf_paths", [])

        for pdf_config in pdf_paths:
            pdf_path = Path(pdf_config.get("path", ""))
            if pdf_path.exists() and pdf_path.suffix.lower() == ".pdf":
                file_hash = compute_file_sha256(pdf_path)
                facts.append(
                    {
                        "id": f"pdf-{file_hash[:16]}",
                        "type": "document_hash",
                        "subject": pdf_config.get("subject", pdf_path.stem),
                        "predicate": "has_hash",
                        "value": file_hash,
                        "source": {
                            "type": "pdf",
                            "reference": str(pdf_path),
                            "hash": file_hash,
                            "retrieved_at": get_timestamp(),
                        },
                        "confidence": 1.0,
                        "valid_from": get_timestamp(),
                    }
                )
            else:
                print(f"  Warning: PDF not found or invalid: {pdf_path}")

        return {"facts": facts}


class NT8LogCollector(Collector):
    """Collect NinjaTrader 8 export logs."""

    name = "nt8"

    def collect(self, config: dict) -> dict:
        """Collect NT8 trade logs from CSV exports."""
        facts = []
        strategies = {}
        log_paths = config.get("nt8_log_paths", [])

        for log_config in log_paths:
            log_path = Path(log_config.get("path", ""))
            if log_path.exists() and log_path.suffix.lower() == ".csv":
                try:
                    file_hash = compute_file_sha256(log_path)
                    strategy_id = log_config.get("strategy_id", log_path.stem)

                    # Create fact about the log file
                    facts.append(
                        {
                            "id": f"nt8-log-{file_hash[:16]}",
                            "type": "trade_log",
                            "subject": strategy_id,
                            "predicate": "has_log_file",
                            "value": {
                                "path": str(log_path),
                                "hash": file_hash,
                                "format": "nt8_csv",
                            },
                            "source": {
                                "type": "csv",
                                "reference": str(log_path),
                                "hash": file_hash,
                                "retrieved_at": get_timestamp(),
                            },
                            "confidence": 1.0,
                            "valid_from": get_timestamp(),
                        }
                    )

                    # Create or update strategy record
                    if strategy_id not in strategies:
                        strategies[strategy_id] = {
                            "id": strategy_id,
                            "name": log_config.get("name", strategy_id),
                            "type": "trading",
                            "status": log_config.get("status", "active"),
                            "audit_trail": [],
                        }

                    strategies[strategy_id]["audit_trail"].append(
                        {
                            "timestamp": get_timestamp(),
                            "action": "log_ingested",
                            "actor": "state_updater",
                        }
                    )
                except (OSError, IOError) as e:
                    print(f"  Warning: Could not process NT8 log {log_path}: {e}")
            else:
                print(f"  Warning: NT8 log not found: {log_path}")

        return {"facts": facts, "strategies": strategies}


class ZapierLogCollector(Collector):
    """Collect Zapier automation logs."""

    name = "zapier"

    def collect(self, config: dict) -> dict:
        """Collect Zapier log entries."""
        facts = []
        log_paths = config.get("zapier_log_paths", [])

        for log_config in log_paths:
            log_path = Path(log_config.get("path", ""))
            if log_path.exists():
                try:
                    file_hash = compute_file_sha256(log_path)
                    facts.append(
                        {
                            "id": f"zapier-{file_hash[:16]}",
                            "type": "automation_log",
                            "subject": log_config.get("zap_name", "unknown"),
                            "predicate": "has_execution_log",
                            "value": {
                                "path": str(log_path),
                                "hash": file_hash,
                            },
                            "source": {
                                "type": "log",
                                "reference": str(log_path),
                                "hash": file_hash,
                                "retrieved_at": get_timestamp(),
                            },
                            "confidence": 1.0,
                            "valid_from": get_timestamp(),
                        }
                    )
                except (OSError, IOError) as e:
                    print(f"  Warning: Could not process Zapier log {log_path}: {e}")

        return {"facts": facts}


class WalletCollector(Collector):
    """Collect wallet balance information."""

    name = "wallet"

    def collect(self, config: dict) -> dict:
        """Collect wallet balances (mock implementation)."""
        accounts = {}
        wallet_configs = config.get("wallets", [])

        for wallet_config in wallet_configs:
            wallet_id = wallet_config.get("id", str(uuid4())[:8])
            accounts[wallet_id] = {
                "id": wallet_id,
                "type": "crypto_wallet",
                "name": wallet_config.get("name", "Unnamed Wallet"),
                "institution": wallet_config.get("network", "unknown"),
                "status": "active",
                "balance": {
                    "amount": wallet_config.get("balance", 0),
                    "currency": wallet_config.get("currency", "USD"),
                    "as_of": get_timestamp(),
                },
                "masked_identifier": wallet_config.get("address", "")[:8] + "...",
            }

        return {"accounts": accounts}


class SOSPDFCollector(Collector):
    """Collect Secretary of State PDF documents."""

    name = "sos_pdf"

    def collect(self, config: dict) -> dict:
        """Collect and hash SOS filings."""
        facts = []
        sos_paths = config.get("sos_pdf_paths", [])

        for sos_config in sos_paths:
            pdf_path = Path(sos_config.get("path", ""))
            if pdf_path.exists() and pdf_path.suffix.lower() == ".pdf":
                file_hash = compute_file_sha256(pdf_path)
                facts.append(
                    {
                        "id": f"sos-{file_hash[:16]}",
                        "type": "sos_filing",
                        "subject": sos_config.get("entity", "Strategickhaos DAO LLC"),
                        "predicate": "has_filing",
                        "value": {
                            "document_type": sos_config.get("doc_type", "unknown"),
                            "jurisdiction": sos_config.get("jurisdiction", "WY"),
                            "filing_date": sos_config.get("filing_date"),
                            "hash": file_hash,
                        },
                        "source": {
                            "type": "pdf",
                            "reference": str(pdf_path),
                            "hash": file_hash,
                            "retrieved_at": get_timestamp(),
                        },
                        "confidence": 1.0,
                        "valid_from": sos_config.get("filing_date", get_timestamp()),
                    }
                )
            else:
                print(f"  Warning: SOS PDF not found: {pdf_path}")

        return {"facts": facts}


# Registry of available collectors
COLLECTORS: dict[str, type[Collector]] = {
    "git": GitCollector,
    "pdf": PDFCollector,
    "nt8": NT8LogCollector,
    "zapier": ZapierLogCollector,
    "wallet": WalletCollector,
    "sos_pdf": SOSPDFCollector,
}


def load_state(state_file: Path) -> dict:
    """Load existing state or return empty state."""
    if state_file.exists():
        with open(state_file, "r") as f:
            return json.load(f)
    return {}


def validate_schema(state: dict, schema_file: Path) -> tuple[bool, list[str]]:
    """Validate state against JSON schema."""
    errors = []

    if not schema_file.exists():
        return True, ["Schema file not found, skipping validation"]

    try:
        import jsonschema

        with open(schema_file, "r") as f:
            schema = json.load(f)

        jsonschema.validate(state, schema)
        return True, []
    except ImportError:
        return True, ["jsonschema not installed, skipping validation"]
    except Exception as e:
        errors.append(str(e))
        return False, errors


def merge_state(existing: dict, updates: dict) -> dict:
    """Merge updates into existing state (deep merge)."""
    result = existing.copy()

    for key, value in updates.items():
        if key in result:
            if isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = merge_state(result[key], value)
            elif isinstance(result[key], list) and isinstance(value, list):
                # For lists, append new items (dedupe by 'id' if present)
                existing_ids = {
                    item.get("id") for item in result[key] if isinstance(item, dict)
                }
                for item in value:
                    if isinstance(item, dict):
                        if item.get("id") not in existing_ids:
                            result[key].append(item)
                            existing_ids.add(item.get("id"))
                    else:
                        if item not in result[key]:
                            result[key].append(item)
            else:
                result[key] = value
        else:
            result[key] = value

    return result


def compute_checksums(state: dict) -> dict:
    """Compute checksums for the state (excluding checksums field)."""
    state_copy = {k: v for k, v in state.items() if k != "checksums"}
    content = json.dumps(state_copy, sort_keys=True, separators=(",", ":"))

    return {
        "sha256": compute_sha256(content),
        "opentimestamps_pending": True,
    }


def emit_opentimestamps_hook(sha256_hash: str, output_dir: Path) -> str | None:
    """Emit OpenTimestamps hook for the hash."""
    ots_file = output_dir / f"{sha256_hash}.ots.pending"
    try:
        # Check if ots command is available
        result = subprocess.run(["which", "ots"], capture_output=True, check=False)
        if result.returncode == 0:
            # Create timestamp request
            subprocess.run(
                ["ots", "stamp", "-"],
                input=sha256_hash.encode(),
                capture_output=True,
                check=False,
            )
            return str(ots_file)
        else:
            # Just create a pending marker file
            with open(ots_file, "w") as f:
                f.write(f"PENDING: {sha256_hash}\n")
                f.write(f"Created: {get_timestamp()}\n")
                f.write("Run 'ots stamp <hash>' when OpenTimestamps CLI is available\n")
            return str(ots_file)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def run_collectors(
    collectors: list[str], config: dict
) -> tuple[dict, list[dict]]:
    """Run specified collectors and return merged data."""
    merged_data: dict[str, Any] = {}
    collector_runs = []

    for collector_name in collectors:
        if collector_name not in COLLECTORS:
            print(f"  Warning: Unknown collector '{collector_name}', skipping")
            continue

        collector_class = COLLECTORS[collector_name]
        collector = collector_class()

        print(f"  Running collector: {collector_name}")
        started_at = get_timestamp()

        try:
            data = collector.collect(config)
            completed_at = get_timestamp()

            # Count records
            records = sum(
                len(v) if isinstance(v, (list, dict)) else 1 for v in data.values()
            )

            merged_data = merge_state(merged_data, data)

            collector_runs.append(
                {
                    "collector": collector_name,
                    "started_at": started_at,
                    "completed_at": completed_at,
                    "records_processed": records,
                    "errors": 0,
                    "status": "success",
                }
            )
        except Exception as e:
            completed_at = get_timestamp()
            print(f"    Error in collector {collector_name}: {e}")
            collector_runs.append(
                {
                    "collector": collector_name,
                    "started_at": started_at,
                    "completed_at": completed_at,
                    "records_processed": 0,
                    "errors": 1,
                    "status": "failed",
                }
            )

    return merged_data, collector_runs


def generate_diff(old_state: dict, new_state: dict) -> dict:
    """Generate a diff between old and new state."""
    diff: dict[str, Any] = {"added": {}, "modified": {}, "removed": {}}

    # Compare top-level keys
    old_keys = set(old_state.keys())
    new_keys = set(new_state.keys())

    diff["added"] = {k: new_state[k] for k in (new_keys - old_keys)}
    diff["removed"] = {k: old_state[k] for k in (old_keys - new_keys)}

    # Check for modifications in common keys
    for key in old_keys & new_keys:
        if old_state[key] != new_state[key]:
            if isinstance(old_state[key], dict) and isinstance(new_state[key], dict):
                # Count changes in nested dicts
                old_items = set(old_state[key].keys())
                new_items = set(new_state[key].keys())
                diff["modified"][key] = {
                    "added_count": len(new_items - old_items),
                    "removed_count": len(old_items - new_items),
                    "modified_count": sum(
                        1
                        for k in (old_items & new_items)
                        if old_state[key][k] != new_state[key][k]
                    ),
                }
            elif isinstance(old_state[key], list) and isinstance(new_state[key], list):
                diff["modified"][key] = {
                    "old_count": len(old_state[key]),
                    "new_count": len(new_state[key]),
                }
            else:
                diff["modified"][key] = {"changed": True}

    return diff


def main():
    """Main entry point for state updater CLI."""
    parser = argparse.ArgumentParser(
        description="Strategickhaos State Updater - Idempotent state management CLI",
        epilog="INTERNAL DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED",
    )

    parser.add_argument(
        "--state-file",
        type=Path,
        default=Path(DEFAULT_STATE_FILE),
        help=f"Path to state file (default: {DEFAULT_STATE_FILE})",
    )

    parser.add_argument(
        "--schema-file",
        type=Path,
        default=Path(DEFAULT_SCHEMA_FILE),
        help=f"Path to schema file (default: {DEFAULT_SCHEMA_FILE})",
    )

    parser.add_argument(
        "--config",
        type=Path,
        help="Path to collector configuration YAML/JSON file",
    )

    parser.add_argument(
        "--collectors",
        nargs="+",
        choices=list(COLLECTORS.keys()),
        default=["git"],
        help="Collectors to run (default: git)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing state",
    )

    parser.add_argument(
        "--diff",
        action="store_true",
        help="Show diff of changes",
    )

    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip schema validation",
    )

    parser.add_argument(
        "--skip-ots",
        action="store_true",
        help="Skip OpenTimestamps hook",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Output directory for timestamped snapshots",
    )

    parser.add_argument(
        "--operator",
        type=str,
        default=os.environ.get("USER", "unknown"),
        help="Operator identity for provenance",
    )

    args = parser.parse_args()

    print("=" * 60)
    print("STRATEGICKHAOS STATE UPDATER")
    print("=" * 60)
    print(f"Tool Version: {TOOL_VERSION}")
    print(f"Schema Version: {SCHEMA_VERSION}")
    print(f"Timestamp: {get_timestamp()}")
    print(f"Operator: {args.operator}")
    print()

    # Load configuration
    config: dict[str, Any] = {}
    if args.config and args.config.exists():
        try:
            import yaml

            with open(args.config, "r") as f:
                config = yaml.safe_load(f) or {}
        except ImportError:
            try:
                with open(args.config, "r") as f:
                    config = json.load(f)
            except json.JSONDecodeError:
                print(f"Error: Could not parse config file {args.config}")
                sys.exit(1)
        print(f"Loaded configuration from: {args.config}")
    else:
        # Default configuration for current repo
        config = {
            "repositories": [{"path": ".", "id": "sovereignty-architecture"}],
        }
        print("Using default configuration (current repository)")

    # Load existing state
    print(f"\nLoading existing state from: {args.state_file}")
    existing_state = load_state(args.state_file)
    previous_snapshot_id = existing_state.get("snapshot_id")

    if previous_snapshot_id:
        print(f"  Previous snapshot ID: {previous_snapshot_id[:16]}...")
    else:
        print("  No previous snapshot found, creating initial state")

    # Run collectors
    print(f"\nRunning collectors: {', '.join(args.collectors)}")
    collected_data, collector_runs = run_collectors(args.collectors, config)

    # Build new state
    timestamp = get_timestamp()
    new_state: dict[str, Any] = {
        "version": SCHEMA_VERSION,
        "timestamp": timestamp,
        "previous_snapshot_id": previous_snapshot_id,
        "entities": existing_state.get("entities", {}),
        "repositories": existing_state.get("repositories", {}),
        "infrastructure": existing_state.get("infrastructure", {}),
        "accounts": existing_state.get("accounts", {}),
        "strategies": existing_state.get("strategies", {}),
        "risks": existing_state.get("risks", []),
        "anchors": existing_state.get("anchors", []),
        "facts": existing_state.get("facts", []),
        "assertions": existing_state.get("assertions", []),
    }

    # Merge collected data
    new_state = merge_state(new_state, collected_data)

    # Build provenance
    source_refs = [
        {"type": "api", "reference": f"collector:{c}", "retrieved_at": timestamp}
        for c in args.collectors
    ]

    new_state["provenance"] = {
        "created_at": timestamp,
        "created_by": args.operator,
        "tool_version": TOOL_VERSION,
        "sources": source_refs,
        "collector_runs": collector_runs,
    }

    # Compute checksums (before adding snapshot_id)
    checksums = compute_checksums(new_state)
    new_state["checksums"] = checksums

    # Generate snapshot ID from checksums
    new_state["snapshot_id"] = checksums["sha256"]

    # Show diff if requested
    if args.diff or args.dry_run:
        print("\nChanges detected:")
        diff = generate_diff(existing_state, new_state)
        if diff["added"]:
            print(f"  Added keys: {list(diff['added'].keys())}")
        if diff["removed"]:
            print(f"  Removed keys: {list(diff['removed'].keys())}")
        if diff["modified"]:
            print("  Modified:")
            for key, changes in diff["modified"].items():
                print(f"    {key}: {changes}")

    # Validate against schema
    if not args.skip_validation:
        print(f"\nValidating against schema: {args.schema_file}")
        valid, errors = validate_schema(new_state, args.schema_file)
        if valid:
            print("  Schema validation: PASSED")
        else:
            print("  Schema validation: FAILED")
            for error in errors:
                print(f"    - {error}")
            if not args.dry_run:
                sys.exit(1)

    # Dry run stops here
    if args.dry_run:
        print("\n[DRY RUN] No changes written")
        print(f"  New snapshot ID would be: {new_state['snapshot_id'][:16]}...")
        print(f"  SHA256: {checksums['sha256']}")
        sys.exit(0)

    # Write state files
    print("\nWriting state files:")

    # Main state file
    print(f"  Writing: {args.state_file}")
    with open(args.state_file, "w") as f:
        json.dump(new_state, f, indent=2)

    # Timestamped backup
    ts_filename = f"strategickhaos_state_snapshot.{timestamp.replace(':', '-')}.json"
    ts_path = args.output_dir / ts_filename
    print(f"  Writing: {ts_path}")
    with open(ts_path, "w") as f:
        json.dump(new_state, f, indent=2)

    # Emit OpenTimestamps hook
    if not args.skip_ots:
        print("\nOpenTimestamps:")
        ots_result = emit_opentimestamps_hook(checksums["sha256"], args.output_dir)
        if ots_result:
            print(f"  OTS hook created: {ots_result}")
        else:
            print("  OTS hook not created (ots command not available)")

    # Summary
    print("\n" + "=" * 60)
    print("STATE UPDATE COMPLETE")
    print("=" * 60)
    print(f"Snapshot ID: {new_state['snapshot_id']}")
    print(f"SHA256: {checksums['sha256']}")
    print(f"State file: {args.state_file}")
    print(f"Timestamped: {ts_path}")
    print()
    print("Collector Summary:")
    for run in collector_runs:
        status_icon = "✓" if run["status"] == "success" else "✗"
        print(
            f"  {status_icon} {run['collector']}: {run['records_processed']} records"
        )

    print()
    print("INTERNAL DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED")


if __name__ == "__main__":
    main()
