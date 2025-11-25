#!/usr/bin/env python3
"""
Strategickhaos Legions of Minds OS - Kernel Connection Protocol

Connects any development environment (GitHub Codespaces, local dev env, cloud VM)
to the Strategickhaos collective intelligence layer.

Git serves as the distributed brain - every commit is a thought, every branch is a decision path.
"""

import json
import os
import socket
import time
import uuid
import hashlib
from pathlib import Path
from typing import Any

import yaml

try:
    import git
except ImportError:
    git = None  # type: ignore[assignment]

try:
    import requests
except ImportError:
    requests = None  # type: ignore[assignment]


class LegionKernel:
    """
    Connects any development environment to the Strategickhaos collective.
    
    The kernel manages:
    - Proposal creation and submission
    - Department voting coordination
    - Consensus calculation
    - Execution of approved actions
    - Discord notifications for human oversight
    """
    
    def __init__(self, workspace_id: str | None = None):
        """
        Initialize the Legion Kernel.
        
        Args:
            workspace_id: Unique identifier for this workspace. If not provided,
                         auto-detects from environment (CODESPACE_NAME, hostname, etc.)
        """
        self.workspace_id = workspace_id or self._detect_workspace_id()
        self.repo_path = Path.cwd()
        self.config_path = self.repo_path / ".strategickhaos" / "kernel" / "config.yml"
        self.proposals_path = self.repo_path / ".strategickhaos" / "proposals"
        self.logs_path = self.repo_path / ".strategickhaos" / "logs"
        
        # Ensure directories exist
        self.proposals_path.mkdir(parents=True, exist_ok=True)
        self.logs_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize Git repo connection
        self.repo = self._init_repo()
        
        # Load kernel configuration
        self.kernel_config = self._load_config()
        
        self._log("info", f"LegionKernel initialized for workspace: {self.workspace_id}")
    
    def _detect_workspace_id(self) -> str:
        """Auto-detect workspace ID from environment."""
        # Check common environment variables
        for env_var in ["CODESPACE_NAME", "GITPOD_WORKSPACE_ID", "WORKSPACE_ID"]:
            if env_id := os.getenv(env_var):
                return env_id
        
        # Fall back to hostname
        return socket.gethostname()
    
    def _init_repo(self) -> Any:
        """Initialize Git repository connection."""
        if git is None:
            self._log("warning", "GitPython not installed, running in limited mode")
            return None
        
        try:
            repo = git.Repo(self.repo_path)
            return repo
        except git.InvalidGitRepositoryError:
            self._log("warning", "Not a Git repository, initializing new repo")
            return git.Repo.init(self.repo_path)
    
    def _load_config(self) -> dict[str, Any]:
        """Load kernel configuration from YAML file."""
        if not self.config_path.exists():
            self._log("error", f"Config not found: {self.config_path}")
            return self._default_config()
        
        with open(self.config_path) as f:
            return yaml.safe_load(f)
    
    def _default_config(self) -> dict[str, Any]:
        """Return default configuration if config file is missing."""
        return {
            "legion_os": {
                "departments": [],
                "voting_rules": {
                    "quorum": 1,
                    "threshold": 0.5,
                    "veto_blocks": True,
                    "timeout": 300
                }
            }
        }
    
    def _generate_id(self) -> str:
        """Generate a unique proposal ID."""
        timestamp = int(time.time() * 1000)
        random_suffix = uuid.uuid4().hex[:8]
        return f"prop-{timestamp}-{random_suffix}"
    
    def _log(self, level: str, message: str) -> None:
        """Log a message to file and console."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "level": level.upper(),
            "workspace_id": self.workspace_id,
            "message": message
        }
        
        print(f"[{level.upper()}] {message}")
        
        # Write to log file
        log_file = self.logs_path / "legion.log"
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def propose_change(self, proposal: dict[str, Any]) -> str:
        """
        Submit a change proposal to the Legion for voting.
        
        Args:
            proposal: Dictionary containing:
                - title: Short title for the proposal
                - description: Full description
                - type: Proposal type (code_change, financial, governance, emergency)
                - actions: List of actions to execute if approved
        
        Returns:
            proposal_id for tracking
        """
        proposal_id = self._generate_id()
        
        # Enrich proposal with metadata
        proposal["id"] = proposal_id
        proposal["workspace_id"] = self.workspace_id
        proposal["timestamp"] = time.time()
        proposal["status"] = "pending"
        proposal["votes"] = {}
        
        # Create proposal file
        proposal_file = self.proposals_path / f"{proposal_id}.json"
        with open(proposal_file, "w") as f:
            json.dump(proposal, f, indent=2)
        
        self._log("info", f"Proposal {proposal_id} created: {proposal.get('title', 'Untitled')}")
        
        # Create proposal branch if Git is available
        if self.repo is not None:
            try:
                branch_name = f"proposal/{proposal_id}"
                self.repo.git.checkout("-b", branch_name)
                self.repo.index.add([str(proposal_file)])
                self.repo.index.commit(f"Proposal {proposal_id}: {proposal.get('title', 'Untitled')}")
                
                # Try to push to remote
                if self.repo.remotes:
                    origin = self.repo.remotes.origin
                    origin.push(branch_name)
                    self._log("info", f"Pushed proposal branch: {branch_name}")
            except Exception as e:
                self._log("warning", f"Git operation failed: {e}")
        
        # Notify departments for voting
        self._notify_departments(proposal_id, proposal)
        
        # Notify Discord
        self._notify_discord(
            f"📋 **New Proposal: {proposal_id}**\n"
            f"**Title:** {proposal.get('title', 'Untitled')}\n"
            f"**Type:** {proposal.get('type', 'general')}\n"
            f"**From:** {self.workspace_id}\n"
            f"Departments are now voting..."
        )
        
        return proposal_id
    
    def _notify_departments(self, proposal_id: str, proposal: dict[str, Any]) -> None:
        """
        Trigger voting across all departments.
        Each department is an AI agent that reviews the proposal.
        """
        departments = self.kernel_config.get("legion_os", {}).get("departments", [])
        
        for dept in departments:
            dept_name = dept.get("name", "unknown")
            self._log("info", f"Requesting vote from {dept_name} department")
            
            # Simulate department vote request
            # In production, this would call the actual AI agent APIs
            vote_request = {
                "proposal_id": proposal_id,
                "department": dept_name,
                "proposal": proposal,
                "prompt": self._build_vote_prompt(dept, proposal)
            }
            
            # Store vote request for async processing
            vote_request_file = self.proposals_path / f"{proposal_id}_{dept_name}_request.json"
            with open(vote_request_file, "w") as f:
                json.dump(vote_request, f, indent=2)
    
    def _build_vote_prompt(self, dept: dict[str, Any], proposal: dict[str, Any]) -> str:
        """Build the voting prompt for a department agent."""
        return f"""
You are the {dept.get('name', 'UNKNOWN').upper()} department of Strategickhaos Legions OS.

A new proposal requires your vote:

{json.dumps(proposal, indent=2)}

Analyze this proposal from your department's perspective.

Your department's role: {dept.get('description', 'General oversight')}

Respond with:
- APPROVE (with explanation)
- REJECT (with explanation)
- ABSTAIN (with reason)

Your department has weight {dept.get('weight', 1)}.
Veto power: {dept.get('veto_power', False)}
"""
    
    def record_vote(self, proposal_id: str, department: str, decision: str, 
                   explanation: str = "") -> bool:
        """
        Record a vote from a department.
        
        Args:
            proposal_id: The proposal being voted on
            department: The voting department name
            decision: APPROVE, REJECT, or ABSTAIN
            explanation: Reason for the vote
        
        Returns:
            True if vote was recorded successfully
        """
        proposal_file = self.proposals_path / f"{proposal_id}.json"
        
        if not proposal_file.exists():
            self._log("error", f"Proposal not found: {proposal_id}")
            return False
        
        with open(proposal_file) as f:
            proposal = json.load(f)
        
        # Find department config
        departments = self.kernel_config.get("legion_os", {}).get("departments", [])
        dept_config = next((d for d in departments if d.get("name") == department), None)
        
        if dept_config is None:
            self._log("error", f"Unknown department: {department}")
            return False
        
        # Record vote
        proposal["votes"][department] = {
            "decision": decision.upper(),
            "explanation": explanation,
            "weight": dept_config.get("weight", 1),
            "has_veto": dept_config.get("veto_power", False),
            "timestamp": time.time()
        }
        
        with open(proposal_file, "w") as f:
            json.dump(proposal, f, indent=2)
        
        self._log("info", f"Vote recorded: {department} -> {decision} on {proposal_id}")
        
        # Notify Discord
        emoji = {"APPROVE": "✅", "REJECT": "❌", "ABSTAIN": "⏸️"}.get(decision.upper(), "❓")
        self._notify_discord(
            f"{emoji} **Vote Cast**\n"
            f"**Proposal:** {proposal_id}\n"
            f"**Department:** {department}\n"
            f"**Decision:** {decision}\n"
            f"**Reason:** {explanation[:200] if explanation else 'No reason provided'}"
        )
        
        return True
    
    def check_proposal_status(self, proposal_id: str) -> dict[str, Any]:
        """
        Check if enough departments have voted and if proposal passed.
        
        Returns:
            Dictionary with status, reason, and approval_rate
        """
        proposal_file = self.proposals_path / f"{proposal_id}.json"
        
        if not proposal_file.exists():
            return {"status": "not_found", "reason": f"Proposal {proposal_id} not found"}
        
        with open(proposal_file) as f:
            proposal = json.load(f)
        
        votes = proposal.get("votes", {})
        rules = self.kernel_config.get("legion_os", {}).get("voting_rules", {})
        
        # Check quorum
        if len(votes) < rules.get("quorum", 1):
            return {
                "status": "pending",
                "reason": f"Quorum not met ({len(votes)}/{rules.get('quorum', 1)})",
                "votes_received": len(votes),
                "quorum_required": rules.get("quorum", 1)
            }
        
        # Check vetoes
        if rules.get("veto_blocks", True):
            for dept, vote in votes.items():
                if vote.get("decision") == "REJECT" and vote.get("has_veto"):
                    return {
                        "status": "blocked",
                        "reason": f"{dept} department used veto power",
                        "veto_by": dept
                    }
        
        # Calculate weighted approval
        total_weight = sum(v.get("weight", 1) for v in votes.values() 
                         if v.get("decision") != "ABSTAIN")
        approve_weight = sum(v.get("weight", 1) for v in votes.values() 
                           if v.get("decision") == "APPROVE")
        
        if total_weight == 0:
            return {
                "status": "pending",
                "reason": "All votes are abstentions"
            }
        
        approval_rate = approve_weight / total_weight
        threshold = rules.get("threshold", 0.5)
        
        if approval_rate >= threshold:
            return {
                "status": "approved",
                "approval_rate": approval_rate,
                "threshold": threshold,
                "votes": votes
            }
        else:
            return {
                "status": "rejected",
                "approval_rate": approval_rate,
                "threshold": threshold,
                "reason": f"Approval rate {approval_rate:.1%} below threshold {threshold:.1%}",
                "votes": votes
            }
    
    def execute_approved(self, proposal_id: str) -> dict[str, Any]:
        """
        If proposal is approved, merge to main and execute actions.
        
        Returns:
            Execution result dictionary
        """
        status = self.check_proposal_status(proposal_id)
        
        if status.get("status") != "approved":
            return {
                "success": False,
                "reason": f"Proposal not approved: {status.get('status')}",
                "status": status
            }
        
        proposal_file = self.proposals_path / f"{proposal_id}.json"
        with open(proposal_file) as f:
            proposal = json.load(f)
        
        # Update proposal status
        proposal["status"] = "executing"
        proposal["execution_started"] = time.time()
        with open(proposal_file, "w") as f:
            json.dump(proposal, f, indent=2)
        
        execution_results = []
        
        # Execute proposal actions
        actions = proposal.get("actions", [])
        for action in actions:
            result = self._execute_action(action)
            execution_results.append(result)
            
            if not result.get("success", False):
                self._log("error", f"Action failed: {action}")
                break
        
        # Merge proposal branch if all actions succeeded
        all_succeeded = all(r.get("success", False) for r in execution_results)
        
        if all_succeeded and self.repo is not None:
            try:
                branch_name = f"proposal/{proposal_id}"
                self.repo.git.checkout("main")
                self.repo.git.merge(branch_name, "-m", f"Merge proposal {proposal_id}")
                
                if self.repo.remotes:
                    self.repo.remotes.origin.push("main")
                    self._log("info", f"Merged and pushed proposal {proposal_id}")
            except Exception as e:
                self._log("warning", f"Git merge failed: {e}")
        
        # Update final status
        proposal["status"] = "completed" if all_succeeded else "failed"
        proposal["execution_completed"] = time.time()
        proposal["execution_results"] = execution_results
        with open(proposal_file, "w") as f:
            json.dump(proposal, f, indent=2)
        
        # Notify Discord
        approval_rate = status.get("approval_rate", 0)
        if all_succeeded:
            self._notify_discord(
                f"✅ **Proposal {proposal_id} APPROVED and EXECUTED**\n"
                f"**Title:** {proposal.get('title', 'Untitled')}\n"
                f"**Approval rate:** {approval_rate:.1%}\n"
                f"**Actions executed:** {len(execution_results)}"
            )
        else:
            self._notify_discord(
                f"⚠️ **Proposal {proposal_id} execution FAILED**\n"
                f"**Title:** {proposal.get('title', 'Untitled')}\n"
                f"Check logs for details."
            )
        
        return {
            "success": all_succeeded,
            "proposal_id": proposal_id,
            "execution_results": execution_results,
            "approval_rate": approval_rate
        }
    
    def _execute_action(self, action: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a single action from a proposal.
        
        Actions can be:
        - shell: Run a shell command
        - git: Perform a git operation
        - api: Call an API endpoint
        - notify: Send a notification
        """
        action_type = action.get("type", "unknown")
        
        self._log("info", f"Executing action: {action_type}")
        
        if action_type == "shell":
            # Note: In production, this should be sandboxed
            command = action.get("command", "")
            self._log("info", f"Would execute shell command: {command}")
            return {"success": True, "type": "shell", "command": command, "note": "Sandbox mode"}
        
        elif action_type == "notify":
            message = action.get("message", "")
            self._notify_discord(message)
            return {"success": True, "type": "notify", "message": message}
        
        elif action_type == "git":
            operation = action.get("operation", "")
            self._log("info", f"Would perform git operation: {operation}")
            return {"success": True, "type": "git", "operation": operation, "note": "Sandbox mode"}
        
        else:
            return {"success": False, "type": action_type, "error": "Unknown action type"}
    
    def _notify_discord(self, message: str) -> None:
        """Send a notification to Discord via webhook."""
        webhook_url = os.getenv(
            self.kernel_config.get("legion_os", {})
            .get("integrations", {})
            .get("discord", {})
            .get("webhook_env", "DISCORD_WEBHOOK_URL")
        )
        
        if not webhook_url:
            self._log("warning", "Discord webhook not configured, skipping notification")
            return
        
        if requests is None:
            self._log("warning", "requests not installed, skipping Discord notification")
            return
        
        try:
            payload = {"content": message}
            response = requests.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            self._log("info", "Discord notification sent")
        except Exception as e:
            self._log("warning", f"Discord notification failed: {e}")
    
    def list_proposals(self, status_filter: str | None = None) -> list[dict[str, Any]]:
        """
        List all proposals, optionally filtered by status.
        
        Args:
            status_filter: Filter by status (pending, approved, rejected, etc.)
        
        Returns:
            List of proposal dictionaries
        """
        proposals = []
        
        for proposal_file in self.proposals_path.glob("prop-*.json"):
            with open(proposal_file) as f:
                proposal = json.load(f)
                
            if status_filter is None or proposal.get("status") == status_filter:
                proposals.append(proposal)
        
        # Sort by timestamp, newest first
        proposals.sort(key=lambda p: p.get("timestamp", 0), reverse=True)
        return proposals
    
    def get_proposal(self, proposal_id: str) -> dict[str, Any] | None:
        """Get a specific proposal by ID."""
        proposal_file = self.proposals_path / f"{proposal_id}.json"
        
        if not proposal_file.exists():
            return None
        
        with open(proposal_file) as f:
            return json.load(f)


def main() -> None:
    """Main entry point - connects workspace to the Legion."""
    workspace_id = os.getenv("CODESPACE_NAME") or socket.gethostname()
    kernel = LegionKernel(workspace_id)
    print(f"✅ Connected to Strategickhaos Legions of Minds OS")
    print(f"   Workspace ID: {workspace_id}")
    print(f"   Config: {kernel.config_path}")
    
    # List active proposals
    pending = kernel.list_proposals(status_filter="pending")
    print(f"   Pending proposals: {len(pending)}")


if __name__ == "__main__":
    main()
