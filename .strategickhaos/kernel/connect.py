"""
Strategickhaos Legions OS - Governance Kernel
Strategickhaos DAO LLC

This module implements the LegionKernel class that provides the governance
infrastructure for the DAO. It treats the Git repository as a shared cognitive
substrate and enables multi-agent departmental voting on proposals.
"""

import os
import uuid
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum

import yaml


class VoteDecision(Enum):
    """Possible vote decisions from departments."""
    APPROVE = "approve"
    REJECT = "reject"
    ABSTAIN = "abstain"
    VETO = "veto"


class ProposalStatus(Enum):
    """Status of a governance proposal."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    VOTING = "voting"
    APPROVED = "approved"
    REJECTED = "rejected"
    VETOED = "vetoed"
    MERGED = "merged"


@dataclass
class DepartmentVote:
    """A vote from a department on a proposal."""
    department_id: str
    decision: VoteDecision
    weight: float
    timestamp: datetime = field(default_factory=datetime.utcnow)
    rationale: str = ""
    agent_id: Optional[str] = None


@dataclass
class Proposal:
    """A governance proposal submitted to the kernel."""
    id: str
    title: str
    description: str
    author: str
    status: ProposalStatus = ProposalStatus.DRAFT
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    actions: List[Dict[str, Any]] = field(default_factory=list)
    votes: List[DepartmentVote] = field(default_factory=list)
    branch_name: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert proposal to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "author": self.author,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "actions": self.actions,
            "votes": [
                {
                    "department_id": v.department_id,
                    "decision": v.decision.value,
                    "weight": v.weight,
                    "timestamp": v.timestamp.isoformat(),
                    "rationale": v.rationale,
                    "agent_id": v.agent_id,
                }
                for v in self.votes
            ],
            "branch_name": self.branch_name,
            "metadata": self.metadata,
        }


class LegionKernel:
    """
    The Governance Kernel for Strategickhaos Legions OS.
    
    This kernel provides:
    - Loading of governance configuration from YAML
    - Proposal submission and management
    - Multi-department voting with weighted votes and veto power
    - Consensus evaluation based on quorum and threshold rules
    - Audit logging of all governance actions
    """
    
    def __init__(
        self,
        workspace_id: str = "default",
        repo_path: str = ".",
        config_path: str = ".strategickhaos/kernel/config.yml"
    ):
        """
        Initialize the governance kernel.
        
        Args:
            workspace_id: Identifier for this workspace/session
            repo_path: Path to the repository root
            config_path: Path to the governance configuration file
        """
        self.workspace_id = workspace_id
        self.repo_path = Path(repo_path).resolve()
        self.config_path = config_path
        self.config = self._load_config()
        self.proposals: Dict[str, Proposal] = {}
        self._load_existing_proposals()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load governance configuration from YAML file."""
        config_file = self.repo_path / self.config_path
        
        if not config_file.exists():
            # Return default configuration
            return {
                "departments": {},
                "voting": {
                    "quorum": 0.5,
                    "threshold": 0.6,
                    "veto_timeout_hours": 24,
                    "auto_merge_on_pass": False,
                },
                "integrations": {
                    "github": {"enabled": False},
                    "discord": {"enabled": False},
                    "legal_firewall": {"enabled": True},
                },
                "audit": {
                    "enabled": True,
                    "log_path": "logs/governance_audit.log",
                },
            }
        
        with open(config_file, "r") as f:
            return yaml.safe_load(f)
    
    def _load_existing_proposals(self) -> None:
        """Load existing proposals from the proposals directory."""
        proposals_dir = self.repo_path / ".strategickhaos" / "proposals"
        if not proposals_dir.exists():
            return
        
        for proposal_file in proposals_dir.glob("*.json"):
            try:
                with open(proposal_file, "r") as f:
                    data = json.load(f)
                
                proposal = Proposal(
                    id=data["id"],
                    title=data["title"],
                    description=data["description"],
                    author=data["author"],
                    status=ProposalStatus(data["status"]),
                    created_at=datetime.fromisoformat(data["created_at"]),
                    updated_at=datetime.fromisoformat(data["updated_at"]),
                    actions=data.get("actions", []),
                    branch_name=data.get("branch_name"),
                    metadata=data.get("metadata", {}),
                )
                
                # Load votes
                for vote_data in data.get("votes", []):
                    vote = DepartmentVote(
                        department_id=vote_data["department_id"],
                        decision=VoteDecision(vote_data["decision"]),
                        weight=vote_data["weight"],
                        timestamp=datetime.fromisoformat(vote_data["timestamp"]),
                        rationale=vote_data.get("rationale", ""),
                        agent_id=vote_data.get("agent_id"),
                    )
                    proposal.votes.append(vote)
                
                self.proposals[proposal.id] = proposal
            except (json.JSONDecodeError, KeyError, ValueError):
                continue
    
    def _save_proposal(self, proposal: Proposal) -> None:
        """Save a proposal to disk."""
        proposals_dir = self.repo_path / ".strategickhaos" / "proposals"
        proposals_dir.mkdir(parents=True, exist_ok=True)
        
        proposal_file = proposals_dir / f"{proposal.id}.json"
        with open(proposal_file, "w") as f:
            json.dump(proposal.to_dict(), f, indent=2)
    
    def _log_audit(self, action: str, details: Dict[str, Any]) -> None:
        """Log an audit entry for governance actions."""
        if not self.config.get("audit", {}).get("enabled", True):
            return
        
        log_path = self.repo_path / self.config.get("audit", {}).get(
            "log_path", "logs/governance_audit.log"
        )
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "workspace_id": self.workspace_id,
            "action": action,
            "details": details,
        }
        
        with open(log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
    
    def _generate_proposal_id(self) -> str:
        """Generate a unique proposal ID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        random_suffix = uuid.uuid4().hex[:8]
        return f"prop-{timestamp}-{random_suffix}"
    
    def propose_change(self, proposal_data: Dict[str, Any]) -> str:
        """
        Submit a new governance proposal.
        
        Args:
            proposal_data: Dictionary containing:
                - title: Proposal title
                - description: Detailed description
                - author: Author identifier
                - actions: List of actions to perform if approved
                
        Returns:
            The proposal ID
        """
        proposal_id = self._generate_proposal_id()
        
        proposal = Proposal(
            id=proposal_id,
            title=proposal_data.get("title", "Untitled Proposal"),
            description=proposal_data.get("description", ""),
            author=proposal_data.get("author", self.workspace_id),
            status=ProposalStatus.SUBMITTED,
            actions=proposal_data.get("actions", []),
            branch_name=f"proposal/{proposal_id}",
            metadata=proposal_data.get("metadata", {}),
        )
        
        self.proposals[proposal_id] = proposal
        self._save_proposal(proposal)
        
        self._log_audit("proposal_submitted", {
            "proposal_id": proposal_id,
            "title": proposal.title,
            "author": proposal.author,
        })
        
        return proposal_id
    
    def get_proposal(self, proposal_id: str) -> Optional[Proposal]:
        """Get a proposal by ID."""
        return self.proposals.get(proposal_id)
    
    def list_proposals(
        self,
        status: Optional[ProposalStatus] = None
    ) -> List[Proposal]:
        """List all proposals, optionally filtered by status."""
        proposals = list(self.proposals.values())
        
        if status:
            proposals = [p for p in proposals if p.status == status]
        
        return sorted(proposals, key=lambda p: p.created_at, reverse=True)
    
    def submit_vote(
        self,
        proposal_id: str,
        department_id: str,
        decision: VoteDecision,
        rationale: str = "",
        agent_id: Optional[str] = None
    ) -> bool:
        """
        Submit a vote from a department on a proposal.
        
        Args:
            proposal_id: The proposal to vote on
            department_id: The voting department
            decision: The vote decision
            rationale: Optional explanation for the vote
            agent_id: Optional ID of the AI agent casting the vote
            
        Returns:
            True if vote was recorded, False otherwise
        """
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            return False
        
        if proposal.status not in [ProposalStatus.SUBMITTED, ProposalStatus.VOTING]:
            return False
        
        # Get department configuration
        dept_config = self.config.get("departments", {}).get(department_id, {})
        weight = dept_config.get("weight", 1.0)
        has_veto = dept_config.get("veto_power", False)
        
        # Check for veto
        if decision == VoteDecision.VETO and not has_veto:
            decision = VoteDecision.REJECT
        
        # Create vote
        vote = DepartmentVote(
            department_id=department_id,
            decision=decision,
            weight=weight,
            rationale=rationale,
            agent_id=agent_id,
        )
        
        # Remove any existing vote from this department
        proposal.votes = [v for v in proposal.votes if v.department_id != department_id]
        proposal.votes.append(vote)
        
        # Update proposal status
        proposal.status = ProposalStatus.VOTING
        proposal.updated_at = datetime.utcnow()
        
        self._save_proposal(proposal)
        
        self._log_audit("vote_submitted", {
            "proposal_id": proposal_id,
            "department_id": department_id,
            "decision": decision.value,
            "weight": weight,
        })
        
        # Check for veto
        if decision == VoteDecision.VETO:
            proposal.status = ProposalStatus.VETOED
            self._save_proposal(proposal)
            self._log_audit("proposal_vetoed", {
                "proposal_id": proposal_id,
                "vetoed_by": department_id,
            })
        
        return True
    
    def evaluate_consensus(self, proposal_id: str) -> Dict[str, Any]:
        """
        Evaluate whether a proposal has reached consensus.
        
        Args:
            proposal_id: The proposal to evaluate
            
        Returns:
            Dictionary with consensus evaluation results
        """
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            return {"error": "Proposal not found"}
        
        voting_config = self.config.get("voting", {})
        quorum = voting_config.get("quorum", 0.5)
        threshold = voting_config.get("threshold", 0.6)
        
        departments = self.config.get("departments", {})
        total_departments = len(departments)
        
        if total_departments == 0:
            return {
                "proposal_id": proposal_id,
                "status": "no_departments",
                "can_approve": False,
            }
        
        # Calculate participation
        voted_departments = len(proposal.votes)
        participation = voted_departments / total_departments
        quorum_met = participation >= quorum
        
        # Calculate weighted approval
        total_weight = 0.0
        approval_weight = 0.0
        
        for vote in proposal.votes:
            total_weight += vote.weight
            if vote.decision == VoteDecision.APPROVE:
                approval_weight += vote.weight
        
        approval_ratio = approval_weight / total_weight if total_weight > 0 else 0.0
        threshold_met = approval_ratio >= threshold
        
        # Check for veto
        vetoed = any(v.decision == VoteDecision.VETO for v in proposal.votes)
        
        can_approve = quorum_met and threshold_met and not vetoed
        
        result = {
            "proposal_id": proposal_id,
            "participation": participation,
            "quorum": quorum,
            "quorum_met": quorum_met,
            "approval_ratio": approval_ratio,
            "threshold": threshold,
            "threshold_met": threshold_met,
            "vetoed": vetoed,
            "can_approve": can_approve,
            "status": proposal.status.value,
        }
        
        # Update proposal status if consensus reached
        if can_approve and proposal.status == ProposalStatus.VOTING:
            proposal.status = ProposalStatus.APPROVED
            proposal.updated_at = datetime.utcnow()
            self._save_proposal(proposal)
            
            self._log_audit("proposal_approved", {
                "proposal_id": proposal_id,
                "approval_ratio": approval_ratio,
                "participation": participation,
            })
        
        return result
    
    def execute_proposal(self, proposal_id: str) -> Dict[str, Any]:
        """
        Execute an approved proposal's actions.
        
        Args:
            proposal_id: The proposal to execute
            
        Returns:
            Execution result
        """
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            return {"error": "Proposal not found"}
        
        if proposal.status != ProposalStatus.APPROVED:
            return {"error": f"Proposal not approved (status: {proposal.status.value})"}
        
        results = []
        
        for action in proposal.actions:
            action_type = action.get("type", "unknown")
            
            if action_type == "create_stub":
                # Create a stub file for a requirement
                result = self._execute_create_stub(action)
            elif action_type == "update_registry":
                # Update the component registry
                result = self._execute_update_registry(action)
            elif action_type == "create_file":
                # Create a new file
                result = self._execute_create_file(action)
            else:
                result = {"action": action_type, "status": "skipped", "reason": "Unknown action type"}
            
            results.append(result)
        
        proposal.status = ProposalStatus.MERGED
        proposal.updated_at = datetime.utcnow()
        self._save_proposal(proposal)
        
        self._log_audit("proposal_executed", {
            "proposal_id": proposal_id,
            "actions_count": len(results),
        })
        
        return {
            "proposal_id": proposal_id,
            "status": "executed",
            "results": results,
        }
    
    def _execute_create_stub(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a create_stub action."""
        requirement_id = action.get("requirement_id", "unknown")
        stub_dir = self.repo_path / ".strategickhaos" / "requirements_stubs"
        stub_dir.mkdir(parents=True, exist_ok=True)
        
        stub_file = stub_dir / f"{requirement_id}.md"
        content = f"""# Stub for {requirement_id}

## Status
Generated via governance proposal

## Next Steps
- [ ] Implement the required capability
- [ ] Add tests
- [ ] Update documentation

*Generated: {datetime.utcnow().isoformat()}Z*
"""
        
        with open(stub_file, "w") as f:
            f.write(content)
        
        return {
            "action": "create_stub",
            "status": "success",
            "path": str(stub_file.relative_to(self.repo_path)),
        }
    
    def _execute_update_registry(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an update_registry action."""
        component = action.get("component", {})
        registry_path = self.repo_path / ".strategickhaos" / "component_registry.yml"
        
        if not registry_path.exists():
            return {"action": "update_registry", "status": "failed", "reason": "Registry not found"}
        
        with open(registry_path, "r") as f:
            registry = yaml.safe_load(f)
        
        if "components" not in registry:
            registry["components"] = []
        
        registry["components"].append(component)
        
        with open(registry_path, "w") as f:
            yaml.dump(registry, f, default_flow_style=False)
        
        return {
            "action": "update_registry",
            "status": "success",
            "component_id": component.get("id", "unknown"),
        }
    
    def _execute_create_file(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a create_file action."""
        path = action.get("path", "")
        content = action.get("content", "")
        
        if not path:
            return {"action": "create_file", "status": "failed", "reason": "No path specified"}
        
        file_path = self.repo_path / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, "w") as f:
            f.write(content)
        
        return {
            "action": "create_file",
            "status": "success",
            "path": path,
        }
    
    def get_department_info(self, department_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a department."""
        return self.config.get("departments", {}).get(department_id)
    
    def list_departments(self) -> List[Dict[str, Any]]:
        """List all configured departments."""
        departments = []
        for dept_id, dept_config in self.config.get("departments", {}).items():
            departments.append({
                "id": dept_id,
                "name": dept_config.get("name", dept_id),
                "description": dept_config.get("description", ""),
                "weight": dept_config.get("weight", 1.0),
                "veto_power": dept_config.get("veto_power", False),
            })
        return departments
