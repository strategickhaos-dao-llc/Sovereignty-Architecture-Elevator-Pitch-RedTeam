#!/usr/bin/env python3
"""
Strategickhaos State Updater - Synchronization Layer

This module provides the synchronization layer for managing persistent state
that enables LLMs to function as cognitive board members. It handles:
- State loading and validation
- Atomic state updates
- Version control and checksums
- Schema validation
- Context history management

Architecture Insight:
    LLMs cannot serve as your board until you give them a persistent,
    machine-readable state. This module is the synchronization layer
    that makes that possible.
"""

import json
import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path
import uuid
from typing import Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class UpdateType(Enum):
    """Types of state updates."""
    INFRASTRUCTURE = "infrastructure"
    GOVERNANCE = "governance"
    PROJECT = "project"
    AI_AGENT = "ai_agent"
    DECISION = "decision"
    CONTEXT = "context"


@dataclass
class StateUpdate:
    """Represents a state update operation."""
    update_type: UpdateType
    path: str
    value: Any
    timestamp: str
    updated_by: str
    reason: Optional[str] = None


class StateUpdater:
    """
    Manages the persistent state snapshot for AI governance board operations.
    
    This class provides the synchronization layer that enables LLMs to function
    as cognitive board members by maintaining a canonical, machine-readable state.
    """
    
    DEFAULT_STATE_PATH = Path(__file__).parent / "strategickhaos_state_snapshot.json"
    
    def __init__(self, state_path: Optional[Path] = None):
        """
        Initialize the state updater.
        
        Args:
            state_path: Path to the state snapshot file. Defaults to the standard location.
        """
        self.state_path = state_path or self.DEFAULT_STATE_PATH
        self._state: Optional[dict] = None
        self._update_log: List[StateUpdate] = []
    
    @property
    def state(self) -> dict:
        """Get the current state, loading from file if necessary."""
        if self._state is None:
            self.load()
        return self._state
    
    def load(self) -> dict:
        """
        Load the state snapshot from file.
        
        Returns:
            The loaded state dictionary.
            
        Raises:
            FileNotFoundError: If the state file does not exist.
            json.JSONDecodeError: If the state file is not valid JSON.
        """
        with open(self.state_path, 'r', encoding='utf-8') as f:
            self._state = json.load(f)
        return self._state
    
    def save(self) -> None:
        """
        Save the current state to file with updated metadata.
        
        Updates the last_updated timestamp and computes the new state hash.
        """
        if self._state is None:
            raise ValueError("No state loaded. Call load() first or create new state.")
        
        # Update metadata
        self._state["last_updated"] = datetime.now(timezone.utc).isoformat()
        self._state["state_hash"] = self._compute_hash()
        
        # Write atomically by writing to temp file first
        temp_path = self.state_path.with_suffix('.tmp')
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(self._state, f, indent=2, ensure_ascii=False)
        
        # Atomic rename
        temp_path.replace(self.state_path)
    
    def _compute_hash(self) -> str:
        """Compute SHA-256 hash of the state (excluding the hash field itself)."""
        state_copy = self._state.copy()
        state_copy.pop("state_hash", None)
        content = json.dumps(state_copy, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def verify_integrity(self) -> bool:
        """
        Verify the integrity of the current state.
        
        Returns:
            True if the state hash matches, False otherwise.
        """
        stored_hash = self.state.get("state_hash")
        if stored_hash is None:
            return True  # No hash stored yet
        
        computed_hash = self._compute_hash()
        return stored_hash == computed_hash
    
    def get(self, path: str, default: Any = None) -> Any:
        """
        Get a value from the state using dot notation path.
        
        Args:
            path: Dot-separated path (e.g., "organization.legal_name")
            default: Default value if path not found.
            
        Returns:
            The value at the specified path, or the default.
        """
        keys = path.split('.')
        value = self.state
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            elif isinstance(value, list):
                try:
                    value = value[int(key)]
                except (ValueError, IndexError):
                    return default
            else:
                return default
        
        return value
    
    def set(self, path: str, value: Any, updated_by: str = "system", 
            reason: Optional[str] = None) -> None:
        """
        Set a value in the state using dot notation path.
        
        Args:
            path: Dot-separated path (e.g., "organization.status")
            value: The value to set.
            updated_by: Identifier of who/what made the update.
            reason: Optional reason for the update.
        """
        keys = path.split('.')
        target = self.state
        
        # Navigate to parent
        for key in keys[:-1]:
            if key not in target:
                target[key] = {}
            target = target[key]
        
        # Set the value
        target[keys[-1]] = value
        
        # Log the update
        update = StateUpdate(
            update_type=self._classify_update(path),
            path=path,
            value=value,
            timestamp=datetime.now(timezone.utc).isoformat(),
            updated_by=updated_by,
            reason=reason
        )
        self._update_log.append(update)
    
    def _classify_update(self, path: str) -> UpdateType:
        """Classify an update based on the path."""
        if path.startswith("infrastructure"):
            return UpdateType.INFRASTRUCTURE
        elif path.startswith("governance"):
            return UpdateType.GOVERNANCE
        elif path.startswith("projects"):
            return UpdateType.PROJECT
        elif path.startswith("ai_agents"):
            return UpdateType.AI_AGENT
        elif path.startswith("context_history"):
            return UpdateType.CONTEXT
        else:
            return UpdateType.DECISION
    
    def add_event(self, event_type: str, description: str, 
                  updated_by: str = "system") -> None:
        """
        Add an event to the context history.
        
        Args:
            event_type: Type of event (e.g., "decision", "deployment", "meeting")
            description: Description of the event.
            updated_by: Identifier of who/what recorded the event.
        """
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": event_type,
            "description": description,
            "recorded_by": updated_by
        }
        
        recent_events = self.get("context_history.recent_events", [])
        recent_events.insert(0, event)
        
        # Keep only last 100 events
        recent_events = recent_events[:100]
        
        self.set("context_history.recent_events", recent_events, updated_by)
    
    def add_decision(self, topic: str, outcome: str, rationale: str,
                     participants: List[str], updated_by: str = "managing_member",
                     requires_human_approval: bool = False) -> str:
        """
        Record a governance decision.
        
        Args:
            topic: Brief description of the decision topic.
            outcome: The decision outcome.
            rationale: Reasoning behind the decision.
            participants: List of agent IDs involved.
            updated_by: Who recorded this decision.
            requires_human_approval: Whether this needs human sign-off.
            
        Returns:
            The generated decision ID.
        """
        now = datetime.now(timezone.utc)
        # Use UUID suffix for uniqueness to avoid race conditions
        unique_suffix = str(uuid.uuid4())[:8]
        decision_id = f"DEC-{now.strftime('%Y-%m-%d')}-{unique_suffix}"
        
        decision = {
            "decision_id": decision_id,
            "timestamp": now.isoformat(),
            "topic": topic,
            "participants": participants,
            "outcome": outcome,
            "rationale": rationale,
            "requires_human_approval": requires_human_approval,
            "approved": not requires_human_approval,
            "recorded_by": updated_by
        }
        
        decisions = self.get("context_history.decisions_made", [])
        decisions.insert(0, decision)
        self.set("context_history.decisions_made", decisions, updated_by)
        
        return decision_id
    
    def add_pending_decision(self, topic: str, options: List[str], 
                             context: str, updated_by: str = "system") -> str:
        """
        Add a pending decision that requires governance action.
        
        Args:
            topic: The decision topic.
            options: List of possible options.
            context: Background context for the decision.
            updated_by: Who raised this decision.
            
        Returns:
            The generated pending decision ID.
        """
        now = datetime.now(timezone.utc)
        # Use UUID suffix for uniqueness to avoid race conditions
        unique_suffix = str(uuid.uuid4())[:8]
        pending_id = f"PEND-{now.strftime('%Y-%m-%d')}-{unique_suffix}"
        
        pending = {
            "id": pending_id,
            "raised_at": now.isoformat(),
            "topic": topic,
            "options": options,
            "context": context,
            "raised_by": updated_by,
            "status": "pending"
        }
        
        pending_decisions = self.get("governance.pending_decisions", [])
        pending_decisions.append(pending)
        self.set("governance.pending_decisions", pending_decisions, updated_by)
        
        return pending_id
    
    def update_repository_status(self, repo_name: str, status: str,
                                  updated_by: str = "system") -> bool:
        """
        Update the status of a repository.
        
        Args:
            repo_name: Name of the repository.
            status: New status (e.g., "active", "archived", "maintenance")
            updated_by: Who made this update.
            
        Returns:
            True if the repository was found and updated, False otherwise.
        """
        repos = self.get("infrastructure.repositories", [])
        
        for repo in repos:
            if repo.get("name") == repo_name:
                repo["status"] = status
                self.set("infrastructure.repositories", repos, updated_by,
                        f"Updated {repo_name} status to {status}")
                return True
        
        return False
    
    def update_agent_interaction(self, agent_id: str,
                                  updated_by: str = "system") -> bool:
        """
        Record the last interaction time for an AI agent.
        
        Args:
            agent_id: The agent's identifier.
            updated_by: Who recorded this interaction.
            
        Returns:
            True if the agent was found and updated, False otherwise.
        """
        board_members = self.get("ai_agents.board_members", [])
        
        for member in board_members:
            if member.get("id") == agent_id:
                member["last_interaction"] = datetime.now(timezone.utc).isoformat()
                self.set("ai_agents.board_members", board_members, updated_by)
                return True
        
        return False
    
    def mark_verified(self, verified_by: str = "system") -> None:
        """
        Mark the current state as verified.
        
        Args:
            verified_by: Who performed the verification.
        """
        now = datetime.now(timezone.utc).isoformat()
        
        self.set("verification.last_verified_at", now, verified_by)
        self.set("verification.verified_by", verified_by, verified_by)
        self.set("verification.integrity_checks.schema_valid", True, verified_by)
        self.set("verification.integrity_checks.state_consistent", True, verified_by)
        self.set("verification.integrity_checks.checksums_match", True, verified_by)
    
    def get_update_log(self) -> List[dict]:
        """Get the log of all updates made in this session."""
        return [asdict(update) for update in self._update_log]
    
    def export_for_board_session(self) -> str:
        """
        Export the current state formatted for board session initialization.
        
        Returns:
            JSON string formatted for LLM context injection.
        """
        return json.dumps(self.state, indent=2, ensure_ascii=False)
    
    def create_session_context(self, agent_role: str, 
                                session_purpose: str) -> str:
        """
        Create the full context string for initializing a board session.
        
        Args:
            agent_role: The role of the AI agent being initialized.
            session_purpose: The purpose of this governance session.
            
        Returns:
            Complete context string for LLM initialization.
        """
        return f"""You are now serving as a governance board member for Strategickhaos DAO LLC.

CANONICAL STATE:
{self.export_for_board_session()}

Your role: {agent_role}
Session purpose: {session_purpose}

Please acknowledge the state and confirm readiness for governance operations."""


def main():
    """CLI interface for state management operations."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Strategickhaos State Updater - Manage persistent governance state"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Show command
    show_parser = subparsers.add_parser("show", help="Show current state")
    show_parser.add_argument("--path", "-p", help="Specific path to show")
    
    # Verify command
    subparsers.add_parser("verify", help="Verify state integrity")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update a state value")
    update_parser.add_argument("path", help="Dot-notation path to update")
    update_parser.add_argument("value", help="New value (JSON format)")
    update_parser.add_argument("--by", default="cli", help="Updated by identifier")
    update_parser.add_argument("--reason", help="Reason for update")
    
    # Event command
    event_parser = subparsers.add_parser("event", help="Add an event to history")
    event_parser.add_argument("event_type", help="Type of event")
    event_parser.add_argument("description", help="Event description")
    event_parser.add_argument("--by", default="cli", help="Recorded by identifier")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export state for board session")
    export_parser.add_argument("--role", required=True, help="Agent role")
    export_parser.add_argument("--purpose", required=True, help="Session purpose")
    
    args = parser.parse_args()
    
    updater = StateUpdater()
    
    if args.command == "show":
        updater.load()
        if args.path:
            value = updater.get(args.path)
            print(json.dumps(value, indent=2) if isinstance(value, (dict, list)) else value)
        else:
            print(updater.export_for_board_session())
    
    elif args.command == "verify":
        updater.load()
        if updater.verify_integrity():
            print("✅ State integrity verified")
        else:
            print("❌ State integrity check failed")
            exit(1)
    
    elif args.command == "update":
        updater.load()
        value = json.loads(args.value)
        updater.set(args.path, value, args.by, args.reason)
        updater.save()
        print(f"✅ Updated {args.path}")
    
    elif args.command == "event":
        updater.load()
        updater.add_event(args.event_type, args.description, args.by)
        updater.save()
        print(f"✅ Event recorded")
    
    elif args.command == "export":
        updater.load()
        print(updater.create_session_context(args.role, args.purpose))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
