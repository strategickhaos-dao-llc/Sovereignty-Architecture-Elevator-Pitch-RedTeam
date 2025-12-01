#!/usr/bin/env python3
"""
state_sync.py - Cryptographic State Synchronization for Sovereign AI Governance

This script manages the canonical STATE.yaml file, providing:
- Cryptographic hash generation and verification
- Snapshot creation with timestamped backups
- State validation for decision gates
- Integrity checking for multi-AI governance

Usage:
    python state_sync.py snapshot     # Create a cryptographically signed snapshot
    python state_sync.py verify       # Verify the current state integrity
    python state_sync.py status       # Display current governance status
    python state_sync.py gates        # Check all decision gate statuses

Author: Strategickhaos DAO LLC
"""

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


# Default paths - can be overridden via environment variables
DEFAULT_STATE_PATH = Path(__file__).parent / "governance" / "STATE.yaml"
SNAPSHOTS_DIR = Path(__file__).parent / "governance" / "snapshots"


def get_state_path() -> Path:
    """Get the STATE.yaml path from environment or default."""
    env_path = os.environ.get("STATE_YAML_PATH")
    if env_path:
        return Path(env_path)
    
    # Try relative path first, then check if we're in governance directory
    if DEFAULT_STATE_PATH.exists():
        return DEFAULT_STATE_PATH
    
    local_path = Path(__file__).parent / "STATE.yaml"
    if local_path.exists():
        return local_path
    
    # Check governance subdirectory
    gov_path = Path(__file__).parent / "governance" / "STATE.yaml"
    if gov_path.exists():
        return gov_path
    
    return DEFAULT_STATE_PATH


def compute_state_hash(state_data: dict) -> str:
    """Compute SHA-256 hash of state data, excluding the integrity section."""
    # Create a copy without integrity section for hashing
    hashable_data = {k: v for k, v in state_data.items() if k != "integrity"}
    
    # Serialize to JSON for consistent hashing
    json_str = json.dumps(hashable_data, sort_keys=True, default=str)
    
    return hashlib.sha256(json_str.encode("utf-8")).hexdigest()


def load_state(state_path: Path) -> dict:
    """Load STATE.yaml file."""
    if not state_path.exists():
        print(f"ERROR: STATE.yaml not found at {state_path}")
        sys.exit(1)
    
    with open(state_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_state(state_data: dict, state_path: Path) -> None:
    """Save STATE.yaml file with proper formatting."""
    with open(state_path, "w", encoding="utf-8") as f:
        yaml.dump(
            state_data,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=120
        )


def create_snapshot(state_path: Path) -> str:
    """Create a cryptographically signed snapshot of the current state."""
    state = load_state(state_path)
    timestamp = datetime.now(timezone.utc).isoformat()
    
    # Update integrity section (without hash first)
    if "integrity" not in state:
        state["integrity"] = {}
    
    snapshot_count = state["integrity"].get("snapshot_count", 0) + 1
    state["integrity"]["hash_algorithm"] = "sha256"
    state["integrity"]["last_snapshot"] = timestamp
    state["integrity"]["snapshot_count"] = snapshot_count
    
    # Update last_modified
    state["last_modified"] = timestamp
    
    # Update audit
    if "audit" not in state:
        state["audit"] = {}
    state["audit"]["last_modified_by"] = "state_sync.py"
    state["audit"]["modification_reason"] = "snapshot_creation"
    
    # Compute hash AFTER all other changes (excluding integrity.state_hash)
    state_hash = compute_state_hash(state)
    state["integrity"]["state_hash"] = state_hash
    
    # Save updated state
    save_state(state, state_path)
    
    # Create snapshot backup
    snapshots_dir = state_path.parent / "snapshots"
    snapshots_dir.mkdir(exist_ok=True)
    
    snapshot_filename = f"STATE_{timestamp.replace(':', '-').replace('+', '_')}_{state_hash[:8]}.yaml"
    snapshot_path = snapshots_dir / snapshot_filename
    shutil.copy2(state_path, snapshot_path)
    
    print("=" * 60)
    print("SNAPSHOT CREATED SUCCESSFULLY")
    print("=" * 60)
    print(f"Timestamp:      {timestamp}")
    print(f"State Hash:     {state_hash}")
    print(f"Snapshot #:     {snapshot_count}")
    print(f"Snapshot File:  {snapshot_path}")
    print("=" * 60)
    
    return state_hash


def verify_state(state_path: Path) -> bool:
    """Verify the integrity of the current state."""
    state = load_state(state_path)
    
    stored_hash = state.get("integrity", {}).get("state_hash")
    if not stored_hash:
        print("WARNING: No stored hash found. Run 'snapshot' first.")
        return False
    
    computed_hash = compute_state_hash(state)
    
    print("=" * 60)
    print("STATE INTEGRITY VERIFICATION")
    print("=" * 60)
    print(f"Stored Hash:    {stored_hash}")
    print(f"Computed Hash:  {computed_hash}")
    
    if stored_hash == computed_hash:
        print("Status:         ✓ VERIFIED - State integrity confirmed")
        print("=" * 60)
        return True
    else:
        print("Status:         ✗ MISMATCH - State may have been modified!")
        print("=" * 60)
        return False


def show_status(state_path: Path) -> None:
    """Display current governance status."""
    state = load_state(state_path)
    
    governance = state.get("governance", {})
    deployed = state.get("deployed", {})
    override = state.get("operator_override", {})
    
    print("=" * 60)
    print("SOVEREIGNTY GOVERNANCE STATUS")
    print("=" * 60)
    print(f"Tick:           {governance.get('tick', 'N/A')}")
    print(f"Authority:      {governance.get('authority', 'N/A')}")
    print(f"Last Modified:  {state.get('last_modified', 'N/A')}")
    print("-" * 60)
    print("DEPLOYMENT STATUS")
    print("-" * 60)
    print(f"Discord Bot:    {deployed.get('discord_bot_location', 'UNKNOWN')}")
    print(f"Bot Version:    {deployed.get('discord_bot_version', 'N/A')}")
    print(f"K8s Namespace:  {deployed.get('kubernetes_namespace', 'N/A')}")
    print("-" * 60)
    print("OPERATOR OVERRIDE")
    print("-" * 60)
    print(f"Enabled:        {override.get('enabled', False)}")
    if override.get("enabled"):
        print(f"Reason:         {override.get('reason', 'N/A')}")
        print(f"Authorized By:  {override.get('authorized_by', 'N/A')}")
    print("=" * 60)


def check_gates(state_path: Path) -> bool:
    """Check all decision gate statuses."""
    state = load_state(state_path)
    gates = state.get("decision_gates", {})
    
    all_passed = True
    
    print("=" * 60)
    print("DECISION GATES STATUS")
    print("=" * 60)
    
    for gate_name, gate_data in gates.items():
        status = gate_data.get("status", "unknown")
        required = gate_data.get("required_approvals", [])
        approved = gate_data.get("approvals", [])
        blockers = gate_data.get("blockers", [])
        
        icon = "✓" if status == "passed" else "○" if status == "pending" else "✗"
        print(f"\n{icon} {gate_name.upper()}")
        print(f"  Status: {status}")
        print(f"  Required: {', '.join(required) if required else 'None'}")
        print(f"  Approved: {', '.join(approved) if approved else 'None'}")
        if blockers:
            print(f"  Blockers: {', '.join(blockers)}")
        
        if status != "passed":
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("ALL GATES PASSED - AI nodes may provide advice")
    else:
        print("GATES PENDING - AI advice restricted per council rules")
    print("=" * 60)
    
    return all_passed


def approve_gate(state_path: Path, gate_name: str, approval: str) -> None:
    """Add an approval to a decision gate."""
    state = load_state(state_path)
    
    if "decision_gates" not in state:
        print(f"ERROR: No decision gates found in state")
        sys.exit(1)
    
    if gate_name not in state["decision_gates"]:
        print(f"ERROR: Gate '{gate_name}' not found")
        print(f"Available gates: {', '.join(state['decision_gates'].keys())}")
        sys.exit(1)
    
    gate = state["decision_gates"][gate_name]
    
    if approval not in gate.get("required_approvals", []):
        print(f"WARNING: '{approval}' is not a required approval for {gate_name}")
    
    if approval not in gate.get("approvals", []):
        if "approvals" not in gate:
            gate["approvals"] = []
        gate["approvals"].append(approval)
        gate["last_check"] = datetime.now(timezone.utc).isoformat()
        
        # Check if all required approvals are met
        if set(gate.get("required_approvals", [])) <= set(gate["approvals"]):
            gate["status"] = "passed"
        
        save_state(state, state_path)
        print(f"Added approval '{approval}' to {gate_name}")
        
        if gate["status"] == "passed":
            print(f"✓ {gate_name} now PASSED")
    else:
        print(f"Approval '{approval}' already exists for {gate_name}")


def increment_tick(state_path: Path) -> int:
    """Increment the governance tick counter."""
    state = load_state(state_path)
    
    if "governance" not in state:
        state["governance"] = {}
    
    current_tick = state["governance"].get("tick", 0)
    new_tick = current_tick + 1
    state["governance"]["tick"] = new_tick
    state["last_modified"] = datetime.now(timezone.utc).isoformat()
    
    save_state(state, state_path)
    print(f"Tick incremented: {current_tick} → {new_tick}")
    
    return new_tick


def main():
    parser = argparse.ArgumentParser(
        description="Cryptographic State Synchronization for Sovereign AI Governance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python state_sync.py snapshot           Create signed snapshot
    python state_sync.py verify             Verify state integrity
    python state_sync.py status             Show governance status
    python state_sync.py gates              Check decision gates
    python state_sync.py approve pre_deployment_check infrastructure_review
    python state_sync.py tick               Increment governance tick

Environment Variables:
    STATE_YAML_PATH     Path to STATE.yaml file (default: ./governance/STATE.yaml)
        """
    )
    
    parser.add_argument(
        "command",
        choices=["snapshot", "verify", "status", "gates", "approve", "tick"],
        help="Command to execute"
    )
    parser.add_argument(
        "args",
        nargs="*",
        help="Additional arguments for the command"
    )
    parser.add_argument(
        "--state-path",
        type=Path,
        default=None,
        help="Path to STATE.yaml file"
    )
    
    args = parser.parse_args()
    
    state_path = args.state_path or get_state_path()
    
    if args.command == "snapshot":
        create_snapshot(state_path)
    elif args.command == "verify":
        success = verify_state(state_path)
        sys.exit(0 if success else 1)
    elif args.command == "status":
        show_status(state_path)
    elif args.command == "gates":
        all_passed = check_gates(state_path)
        sys.exit(0 if all_passed else 1)
    elif args.command == "approve":
        if len(args.args) < 2:
            print("Usage: state_sync.py approve <gate_name> <approval>")
            sys.exit(1)
        approve_gate(state_path, args.args[0], args.args[1])
    elif args.command == "tick":
        increment_tick(state_path)


if __name__ == "__main__":
    main()
