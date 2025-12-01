#!/usr/bin/env python3
"""
state_sync.py - Cryptographic State Management for Multi-AI Governance
Strategickhaos DAO LLC — Single Source of Truth Enforcer

Commands:
    snapshot    Create a cryptographically signed snapshot
    verify      Verify state integrity against stored hash
    update      Update state fields with hash regeneration
    history     Show audit trail of state changes
    gate        Check or update decision gate status
    
Usage:
    python state_sync.py snapshot
    python state_sync.py verify
    python state_sync.py update --field deployed.discord_bot_location --value "IN_CLUSTER"
    python state_sync.py history
    python state_sync.py gate pre_deployment_check --status
    python state_sync.py gate pre_deployment_check --pass infrastructure_verified
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml


def load_state(state_file: str = "STATE.yaml") -> dict:
    """Load the STATE.yaml file."""
    state_path = Path(state_file)
    if not state_path.exists():
        print(f"❌ STATE.yaml not found at {state_path}")
        sys.exit(1)
    
    with open(state_path, 'r') as f:
        return yaml.safe_load(f)


def save_state(state: dict, state_file: str = "STATE.yaml") -> None:
    """Save state to STATE.yaml file."""
    with open(state_file, 'w') as f:
        yaml.dump(state, f, default_flow_style=False, indent=2, sort_keys=False)


def compute_state_hash(state: dict) -> str:
    """Compute SHA256 hash of the state (excluding integrity section)."""
    # Create a copy without integrity section to avoid circular reference
    state_copy = {k: v for k, v in state.items() if k != 'integrity'}
    state_json = json.dumps(state_copy, sort_keys=True, default=str)
    return hashlib.sha256(state_json.encode()).hexdigest()


def create_snapshot(state_file: str = "STATE.yaml") -> None:
    """Create a cryptographically signed snapshot of the current state."""
    state = load_state(state_file)
    
    timestamp = datetime.now(timezone.utc).isoformat() + 'Z'
    
    # Update metadata FIRST (before computing hash)
    state['metadata']['last_modified'] = timestamp
    
    # Increment the truth counter
    state['metadata']['increment'] = state['metadata'].get('increment', 3449) + 1
    
    # Update integrity section (except hash)
    state['integrity']['last_snapshot'] = timestamp
    state['integrity']['snapshot_count'] = state['integrity'].get('snapshot_count', 0) + 1
    
    # Add audit entry BEFORE hash computation
    audit_entry = {
        'timestamp': timestamp,
        'action': 'SNAPSHOT_CREATED',
        'actor': 'state_sync.py',
        'details': f'Increment: {state["metadata"]["increment"]}'
    }
    
    if 'audit_trail' not in state:
        state['audit_trail'] = {'retain_days': 365, 'last_entries': []}
    
    # Keep last 100 entries
    state['audit_trail']['last_entries'] = (
        [audit_entry] + state['audit_trail'].get('last_entries', [])
    )[:100]
    
    # Compute hash LAST after all other changes
    state_hash = compute_state_hash(state)
    state['integrity']['state_hash'] = state_hash
    
    # Note: Don't update audit entry after hash - it would invalidate the hash
    
    save_state(state, state_file)
    
    # Save snapshot to snapshots directory
    snapshots_dir = Path("snapshots")
    snapshots_dir.mkdir(exist_ok=True)
    
    snapshot_file = snapshots_dir / f"state_snapshot_{timestamp.replace(':', '-').replace('.', '-')}.json"
    with open(snapshot_file, 'w') as f:
        json.dump({
            'state': state,
            'hash': state_hash,
            'timestamp': timestamp,
            'increment': state['metadata']['increment']
        }, f, indent=2, default=str)
    
    print("✅ SNAPSHOT CREATED")
    print(f"   Hash: {state_hash}")
    print(f"   Timestamp: {timestamp}")
    print(f"   Increment: {state['metadata']['increment']}")
    print(f"   Snapshot: {snapshot_file}")


def verify_state(state_file: str = "STATE.yaml") -> bool:
    """Verify state integrity against stored hash."""
    state = load_state(state_file)
    
    stored_hash = state.get('integrity', {}).get('state_hash', 'PENDING_FIRST_SNAPSHOT')
    
    if stored_hash == 'PENDING_FIRST_SNAPSHOT':
        print("⚠️  STATE NOT YET SIGNED")
        print("   Run 'python state_sync.py snapshot' to create first signature")
        return False
    
    computed_hash = compute_state_hash(state)
    
    if computed_hash == stored_hash:
        print("✅ STATE VERIFIED - Integrity intact")
        print(f"   Hash: {computed_hash}")
        print(f"   Last snapshot: {state['integrity'].get('last_snapshot')}")
        return True
    else:
        print("❌ STATE INTEGRITY VIOLATION")
        print(f"   Stored hash:   {stored_hash}")
        print(f"   Computed hash: {computed_hash}")
        print("   WARNING: State may have been modified outside of state_sync.py")
        return False


def update_field(field_path: str, value: str, state_file: str = "STATE.yaml") -> None:
    """Update a specific field in the state and regenerate hash."""
    state = load_state(state_file)
    timestamp = datetime.now(timezone.utc).isoformat() + 'Z'
    
    # Navigate to the field
    parts = field_path.split('.')
    target = state
    for part in parts[:-1]:
        if part not in target:
            target[part] = {}
        target = target[part]
    
    old_value = target.get(parts[-1])
    
    # Handle value type conversion
    if value.lower() == 'true':
        value = True
    elif value.lower() == 'false':
        value = False
    elif value.lower() == 'null' or value.lower() == 'none':
        value = None
    
    target[parts[-1]] = value
    
    # Update metadata
    state['metadata']['last_modified'] = timestamp
    state['metadata']['increment'] = state['metadata'].get('increment', 3449) + 1
    state['integrity']['last_snapshot'] = timestamp
    
    # Add audit entry BEFORE hash computation
    audit_entry = {
        'timestamp': timestamp,
        'action': 'FIELD_UPDATED',
        'actor': 'state_sync.py',
        'details': f'{field_path}: {old_value} -> {value}'
    }
    
    state['audit_trail']['last_entries'] = (
        [audit_entry] + state['audit_trail'].get('last_entries', [])
    )[:100]
    
    # Recompute hash LAST after all other changes
    state_hash = compute_state_hash(state)
    state['integrity']['state_hash'] = state_hash
    
    save_state(state, state_file)
    
    print("✅ FIELD UPDATED")
    print(f"   Field: {field_path}")
    print(f"   Old value: {old_value}")
    print(f"   New value: {value}")
    print(f"   New hash: {state_hash}")


def show_history(state_file: str = "STATE.yaml", limit: int = 10) -> None:
    """Show audit trail of state changes."""
    state = load_state(state_file)
    
    entries = state.get('audit_trail', {}).get('last_entries', [])
    
    print("📜 STATE AUDIT TRAIL")
    print("=" * 60)
    
    if not entries:
        print("   No audit entries found")
        return
    
    for entry in entries[:limit]:
        print(f"   [{entry['timestamp']}]")
        print(f"   Action: {entry['action']}")
        print(f"   Actor: {entry['actor']}")
        print(f"   Details: {entry['details']}")
        print("-" * 60)


def check_gate(gate_name: str, state_file: str = "STATE.yaml") -> bool:
    """Check the status of a decision gate."""
    state = load_state(state_file)
    
    gates = state.get('decision_gates', {})
    if gate_name not in gates:
        print(f"❌ Unknown gate: {gate_name}")
        print(f"   Available gates: {', '.join(gates.keys())}")
        return False
    
    gate = gates[gate_name]
    
    print(f"🚦 GATE STATUS: {gate_name}")
    print("=" * 60)
    print(f"   Passed: {'✅ YES' if gate.get('passed') else '❌ NO'}")
    print(f"   Last checked: {gate.get('last_checked', 'Never')}")
    print(f"   Checked by: {gate.get('checked_by', 'N/A')}")
    print("\n   Requirements:")
    
    for req in gate.get('requirements', []):
        status = '✅' if req['status'] else '⬜'
        print(f"     {status} {req['name']}: {req['description']}")
    
    return gate.get('passed', False)


def pass_requirement(gate_name: str, requirement_name: str, state_file: str = "STATE.yaml") -> None:
    """Mark a requirement as passed and update gate status."""
    state = load_state(state_file)
    timestamp = datetime.now(timezone.utc).isoformat() + 'Z'
    
    gates = state.get('decision_gates', {})
    if gate_name not in gates:
        print(f"❌ Unknown gate: {gate_name}")
        return
    
    gate = gates[gate_name]
    
    # Find and update the requirement
    found = False
    for req in gate.get('requirements', []):
        if req['name'] == requirement_name:
            req['status'] = True
            found = True
            break
    
    if not found:
        print(f"❌ Unknown requirement: {requirement_name}")
        return
    
    # Check if all requirements pass
    all_passed = all(req['status'] for req in gate.get('requirements', []))
    gate['passed'] = all_passed
    gate['last_checked'] = timestamp
    gate['checked_by'] = 'state_sync.py'
    
    # Update metadata
    state['metadata']['last_modified'] = timestamp
    state['metadata']['increment'] = state['metadata'].get('increment', 3449) + 1
    state['integrity']['last_snapshot'] = timestamp
    
    # Add audit entry BEFORE hash computation
    audit_entry = {
        'timestamp': timestamp,
        'action': 'REQUIREMENT_PASSED',
        'actor': 'state_sync.py',
        'details': f'{gate_name}.{requirement_name} -> PASSED'
    }
    
    state['audit_trail']['last_entries'] = (
        [audit_entry] + state['audit_trail'].get('last_entries', [])
    )[:100]
    
    # Recompute hash LAST after all other changes
    state_hash = compute_state_hash(state)
    state['integrity']['state_hash'] = state_hash
    
    save_state(state, state_file)
    
    print(f"✅ REQUIREMENT PASSED: {requirement_name}")
    print(f"   Gate '{gate_name}' status: {'✅ ALL PASSED' if all_passed else '⏳ PARTIAL'}")


def show_status(state_file: str = "STATE.yaml") -> None:
    """Show overall state status."""
    state = load_state(state_file)
    
    print("🏛️ SOVEREIGNTY STATE STATUS")
    print("=" * 60)
    print(f"   Version: {state['metadata'].get('version')}")
    print(f"   Increment: {state['metadata'].get('increment')}")
    print(f"   Last Modified: {state['metadata'].get('last_modified')}")
    print(f"   Operator: {state['metadata'].get('operator')}")
    print()
    
    # Integrity
    integrity = state.get('integrity', {})
    print("🔐 INTEGRITY")
    print(f"   Hash: {integrity.get('state_hash', 'N/A')[:32]}...")
    print(f"   Snapshots: {integrity.get('snapshot_count', 0)}")
    print()
    
    # Deployment
    deployed = state.get('deployed', {})
    print("🚀 DEPLOYMENT")
    print(f"   Discord Bot: {deployed.get('discord_bot_location', 'UNKNOWN')}")
    print(f"   Infrastructure: {'✅' if deployed.get('infrastructure_verified') else '❌'}")
    print()
    
    # Gates
    print("🚦 DECISION GATES")
    for gate_name, gate in state.get('decision_gates', {}).items():
        status = '✅' if gate.get('passed') else '❌'
        passed_count = sum(1 for r in gate.get('requirements', []) if r['status'])
        total_count = len(gate.get('requirements', []))
        print(f"   {status} {gate_name}: {passed_count}/{total_count} requirements")
    print()
    
    # AI Council
    council = state.get('ai_council', {})
    active = len([n for n in council.get('active_nodes', []) if n['status'] == 'ACTIVE'])
    muted = len(council.get('muted_nodes', []))
    print("🤖 AI COUNCIL")
    print(f"   Active Nodes: {active}")
    print(f"   Muted Nodes: {muted}")


def main():
    parser = argparse.ArgumentParser(
        description='Cryptographic State Management for Multi-AI Governance'
    )
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Snapshot command
    subparsers.add_parser('snapshot', help='Create a cryptographically signed snapshot')
    
    # Verify command
    subparsers.add_parser('verify', help='Verify state integrity')
    
    # Status command
    subparsers.add_parser('status', help='Show overall state status')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update a state field')
    update_parser.add_argument('--field', required=True, help='Field path (e.g., deployed.discord_bot_location)')
    update_parser.add_argument('--value', required=True, help='New value')
    
    # History command
    history_parser = subparsers.add_parser('history', help='Show audit trail')
    history_parser.add_argument('--limit', type=int, default=10, help='Number of entries to show')
    
    # Gate command
    gate_parser = subparsers.add_parser('gate', help='Check or update decision gates')
    gate_parser.add_argument('gate_name', help='Name of the gate')
    gate_parser.add_argument('--status', action='store_true', help='Show gate status')
    gate_parser.add_argument('--pass', dest='pass_req', metavar='REQUIREMENT', help='Mark requirement as passed')
    
    args = parser.parse_args()
    
    if args.command == 'snapshot':
        create_snapshot()
    elif args.command == 'verify':
        verify_state()
    elif args.command == 'status':
        show_status()
    elif args.command == 'update':
        update_field(args.field, args.value)
    elif args.command == 'history':
        show_history(limit=args.limit)
    elif args.command == 'gate':
        if args.pass_req:
            pass_requirement(args.gate_name, args.pass_req)
        else:
            check_gate(args.gate_name)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
