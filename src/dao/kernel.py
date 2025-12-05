#!/usr/bin/env python3
"""
DAO Kernel - Git-Native Multi-Agent Consensus Protocol
Strategickhaos DAO LLC - Core Governance Engine

This kernel implements the consensus mechanism using Git as the
underlying substrate for distributed decision-making.
"""

import hashlib
import json
import time
import subprocess
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional
import uuid


class ProposalStatus(Enum):
    """Lifecycle states for a proposal"""
    DRAFT = "draft"
    VOTING = "voting"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"
    EXPIRED = "expired"


class VoteDecision(Enum):
    """Possible voting decisions"""
    APPROVE = "approve"
    REJECT = "reject"
    ABSTAIN = "abstain"


@dataclass
class Vote:
    """Individual agent vote on a proposal"""
    agent_id: str
    decision: VoteDecision
    confidence: float  # 0.0 to 1.0
    reasoning: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + 'Z')
    signature: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'agent_id': self.agent_id,
            'decision': self.decision.value,
            'confidence': self.confidence,
            'reasoning': self.reasoning,
            'timestamp': self.timestamp,
            'signature': self.signature
        }
    
    def compute_signature(self) -> str:
        """Compute cryptographic signature of vote"""
        vote_data = json.dumps({
            'agent_id': self.agent_id,
            'decision': self.decision.value,
            'confidence': self.confidence,
            'timestamp': self.timestamp
        }, sort_keys=True)
        return hashlib.sha256(vote_data.encode()).hexdigest()


@dataclass
class Proposal:
    """A governance proposal for multi-agent voting"""
    proposal_id: str
    title: str
    description: str
    author: str
    status: ProposalStatus = ProposalStatus.DRAFT
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + 'Z')
    voting_deadline: Optional[str] = None
    votes: list = field(default_factory=list)
    quorum_threshold: float = 0.66  # 66% approval required
    min_voters: int = 3
    git_branch: Optional[str] = None
    git_commit: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'proposal_id': self.proposal_id,
            'title': self.title,
            'description': self.description,
            'author': self.author,
            'status': self.status.value,
            'created_at': self.created_at,
            'voting_deadline': self.voting_deadline,
            'votes': [v.to_dict() if isinstance(v, Vote) else v for v in self.votes],
            'quorum_threshold': self.quorum_threshold,
            'min_voters': self.min_voters,
            'git_branch': self.git_branch,
            'git_commit': self.git_commit
        }


@dataclass
class ConsensusResult:
    """Result of a consensus vote"""
    proposal_id: str
    approved: bool
    approval_rate: float
    total_votes: int
    approve_count: int
    reject_count: int
    abstain_count: int
    quorum_met: bool
    computed_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + 'Z')
    git_commit: Optional[str] = None


class DAOKernel:
    """
    Core DAO governance kernel using Git as consensus substrate.
    
    This kernel implements:
    - Proposal lifecycle management
    - Multi-agent voting coordination
    - Git-based state persistence
    - Consensus calculation
    """
    
    def __init__(self, repo_path: str = ".", data_dir: str = "governance/proposals"):
        """
        Initialize the DAO kernel.
        
        Args:
            repo_path: Path to the Git repository
            data_dir: Directory for proposal data storage
        """
        self.repo_path = Path(repo_path)
        self.data_dir = self.repo_path / data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.proposals: dict[str, Proposal] = {}
        self._load_proposals()
        
    def _load_proposals(self):
        """Load existing proposals from disk"""
        for proposal_file in self.data_dir.glob("*.json"):
            try:
                with open(proposal_file) as f:
                    data = json.load(f)
                    proposal = self._dict_to_proposal(data)
                    self.proposals[proposal.proposal_id] = proposal
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Warning: Failed to load {proposal_file}: {e}")
                
    def _dict_to_proposal(self, data: dict) -> Proposal:
        """Convert dictionary to Proposal object"""
        votes = []
        for v in data.get('votes', []):
            votes.append(Vote(
                agent_id=v['agent_id'],
                decision=VoteDecision(v['decision']),
                confidence=v['confidence'],
                reasoning=v['reasoning'],
                timestamp=v.get('timestamp', ''),
                signature=v.get('signature')
            ))
        
        return Proposal(
            proposal_id=data['proposal_id'],
            title=data['title'],
            description=data['description'],
            author=data['author'],
            status=ProposalStatus(data['status']),
            created_at=data.get('created_at', ''),
            voting_deadline=data.get('voting_deadline'),
            votes=votes,
            quorum_threshold=data.get('quorum_threshold', 0.66),
            min_voters=data.get('min_voters', 3),
            git_branch=data.get('git_branch'),
            git_commit=data.get('git_commit')
        )
        
    def _save_proposal(self, proposal: Proposal):
        """Save proposal to disk"""
        proposal_file = self.data_dir / f"{proposal.proposal_id}.json"
        with open(proposal_file, 'w') as f:
            json.dump(proposal.to_dict(), f, indent=2)
            
    def _git_command(self, *args) -> tuple[bool, str]:
        """Execute a git command and return success status and output"""
        try:
            result = subprocess.run(
                ['git', *args],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout.strip() or result.stderr.strip()
        except subprocess.TimeoutExpired:
            return False, "Git command timed out"
        except subprocess.SubprocessError as e:
            return False, str(e)
            
    def create_proposal(self, title: str, description: str, author: str,
                       quorum_threshold: float = 0.66, voting_hours: int = 24) -> Proposal:
        """
        Create a new governance proposal.
        
        Args:
            title: Short title for the proposal
            description: Detailed description of the proposal
            author: ID of the proposing agent/user
            quorum_threshold: Required approval percentage (0.0 to 1.0)
            voting_hours: Hours until voting deadline
            
        Returns:
            The created Proposal object
        """
        proposal_id = f"PROP-{uuid.uuid4().hex[:8].upper()}"
        deadline = datetime.utcnow() + timedelta(hours=voting_hours)
        
        proposal = Proposal(
            proposal_id=proposal_id,
            title=title,
            description=description,
            author=author,
            quorum_threshold=quorum_threshold,
            voting_deadline=deadline.isoformat() + 'Z'
        )
        
        # Create Git branch for proposal (non-critical, continue on failure)
        branch_name = f"proposal/{proposal_id.lower()}"
        success, output = self._git_command('checkout', '-b', branch_name)
        if success:
            proposal.git_branch = branch_name
        # Note: Git branch creation failure is non-critical; proposal can still function
            
        self.proposals[proposal_id] = proposal
        self._save_proposal(proposal)
        
        # Commit proposal creation (best-effort, non-critical for core functionality)
        self._git_command('add', str(self.data_dir / f"{proposal_id}.json"))
        self._git_command('commit', '-m', f"[DAO] Create proposal: {title}")
        
        return proposal
        
    def submit_vote(self, proposal_id: str, agent_id: str, 
                    decision: VoteDecision, confidence: float,
                    reasoning: str) -> Vote:
        """
        Submit a vote on a proposal.
        
        Args:
            proposal_id: ID of the proposal to vote on
            agent_id: ID of the voting agent
            decision: The vote decision (approve/reject/abstain)
            confidence: Confidence level (0.0 to 1.0)
            reasoning: Explanation for the vote
            
        Returns:
            The submitted Vote object
            
        Raises:
            ValueError: If proposal not found or not in voting state
        """
        if proposal_id not in self.proposals:
            raise ValueError(f"Proposal {proposal_id} not found")
            
        proposal = self.proposals[proposal_id]
        
        if proposal.status not in [ProposalStatus.DRAFT, ProposalStatus.VOTING]:
            raise ValueError(f"Proposal {proposal_id} is not accepting votes")
            
        # Check if agent already voted using set for O(1) lookup
        voted_agents = {vote.agent_id for vote in proposal.votes}
        if agent_id in voted_agents:
            raise ValueError(f"Agent {agent_id} has already voted")
                
        # Transition to voting state if first vote
        if proposal.status == ProposalStatus.DRAFT:
            proposal.status = ProposalStatus.VOTING
            
        vote = Vote(
            agent_id=agent_id,
            decision=decision,
            confidence=confidence,
            reasoning=reasoning
        )
        vote.signature = vote.compute_signature()
        
        proposal.votes.append(vote)
        self._save_proposal(proposal)
        
        # Commit vote (best-effort, non-critical for core functionality)
        self._git_command('add', str(self.data_dir / f"{proposal_id}.json"))
        self._git_command('commit', '-m', 
                         f"[DAO] Vote: {agent_id} votes {decision.value} on {proposal_id}")
        
        return vote
        
    def calculate_consensus(self, proposal_id: str) -> ConsensusResult:
        """
        Calculate consensus result for a proposal.
        
        Args:
            proposal_id: ID of the proposal
            
        Returns:
            ConsensusResult with voting statistics
            
        Raises:
            ValueError: If proposal not found
        """
        if proposal_id not in self.proposals:
            raise ValueError(f"Proposal {proposal_id} not found")
            
        proposal = self.proposals[proposal_id]
        votes = proposal.votes
        
        total = len(votes)
        approve = sum(1 for v in votes if v.decision == VoteDecision.APPROVE)
        reject = sum(1 for v in votes if v.decision == VoteDecision.REJECT)
        abstain = sum(1 for v in votes if v.decision == VoteDecision.ABSTAIN)
        
        # Calculate approval rate (excluding abstentions)
        voting_count = approve + reject
        approval_rate = approve / voting_count if voting_count > 0 else 0.0
        
        # Check quorum
        quorum_met = total >= proposal.min_voters
        
        return ConsensusResult(
            proposal_id=proposal_id,
            approved=quorum_met and approval_rate >= proposal.quorum_threshold,
            approval_rate=approval_rate,
            total_votes=total,
            approve_count=approve,
            reject_count=reject,
            abstain_count=abstain,
            quorum_met=quorum_met
        )
        
    def finalize_proposal(self, proposal_id: str) -> ConsensusResult:
        """
        Finalize voting and record consensus to Git.
        
        Args:
            proposal_id: ID of the proposal to finalize
            
        Returns:
            Final ConsensusResult
            
        Raises:
            ValueError: If proposal not found or not in voting state
        """
        if proposal_id not in self.proposals:
            raise ValueError(f"Proposal {proposal_id} not found")
            
        proposal = self.proposals[proposal_id]
        
        if proposal.status not in [ProposalStatus.VOTING, ProposalStatus.DRAFT]:
            raise ValueError(f"Proposal {proposal_id} cannot be finalized")
            
        result = self.calculate_consensus(proposal_id)
        
        # Update proposal status
        if result.approved:
            proposal.status = ProposalStatus.APPROVED
        else:
            proposal.status = ProposalStatus.REJECTED
            
        self._save_proposal(proposal)
        
        # Record consensus to Git
        self._git_command('add', str(self.data_dir / f"{proposal_id}.json"))
        
        status = "APPROVED" if result.approved else "REJECTED"
        commit_msg = (
            f"[DAO CONSENSUS] {proposal_id}: {status}\n\n"
            f"Approval Rate: {result.approval_rate:.1%}\n"
            f"Votes: {result.approve_count} approve, "
            f"{result.reject_count} reject, "
            f"{result.abstain_count} abstain\n"
            f"Quorum: {'Met' if result.quorum_met else 'Not met'}"
        )
        
        success, output = self._git_command('commit', '-m', commit_msg)
        if success:
            # Get commit hash
            _, commit_hash = self._git_command('rev-parse', 'HEAD')
            result.git_commit = commit_hash
            proposal.git_commit = commit_hash
            self._save_proposal(proposal)
            
        return result
        
    def get_proposal(self, proposal_id: str) -> Optional[Proposal]:
        """Get a proposal by ID"""
        return self.proposals.get(proposal_id)
        
    def list_proposals(self, status: Optional[ProposalStatus] = None) -> list[Proposal]:
        """List all proposals, optionally filtered by status"""
        proposals = list(self.proposals.values())
        if status:
            proposals = [p for p in proposals if p.status == status]
        return sorted(proposals, key=lambda p: p.created_at, reverse=True)
        
    def get_voting_stats(self) -> dict:
        """Get aggregate voting statistics"""
        total_proposals = len(self.proposals)
        by_status = {}
        for status in ProposalStatus:
            by_status[status.value] = sum(
                1 for p in self.proposals.values() if p.status == status
            )
            
        total_votes = sum(len(p.votes) for p in self.proposals.values())
        
        return {
            'total_proposals': total_proposals,
            'by_status': by_status,
            'total_votes': total_votes,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }


# CLI interface for testing
if __name__ == '__main__':
    import sys
    
    kernel = DAOKernel()
    
    if len(sys.argv) < 2:
        print("Usage: python kernel.py <command> [args]")
        print("Commands: create, vote, finalize, status, list")
        sys.exit(1)
        
    command = sys.argv[1]
    
    if command == 'create':
        if len(sys.argv) < 4:
            print("Usage: python kernel.py create <title> <description>")
            sys.exit(1)
        title = sys.argv[2]
        description = sys.argv[3]
        proposal = kernel.create_proposal(title, description, "cli-user")
        print(f"Created proposal: {proposal.proposal_id}")
        print(f"Branch: {proposal.git_branch}")
        
    elif command == 'vote':
        if len(sys.argv) < 5:
            print("Usage: python kernel.py vote <proposal_id> <agent_id> <approve|reject|abstain>")
            sys.exit(1)
        proposal_id = sys.argv[2]
        agent_id = sys.argv[3]
        decision = VoteDecision(sys.argv[4])
        vote = kernel.submit_vote(proposal_id, agent_id, decision, 0.9, "CLI vote")
        print(f"Vote recorded: {agent_id} votes {decision.value}")
        
    elif command == 'finalize':
        if len(sys.argv) < 3:
            print("Usage: python kernel.py finalize <proposal_id>")
            sys.exit(1)
        proposal_id = sys.argv[2]
        result = kernel.finalize_proposal(proposal_id)
        print(f"Consensus: {'APPROVED' if result.approved else 'REJECTED'}")
        print(f"Approval rate: {result.approval_rate:.1%}")
        print(f"Git commit: {result.git_commit}")
        
    elif command == 'status':
        if len(sys.argv) < 3:
            print("Usage: python kernel.py status <proposal_id>")
            sys.exit(1)
        proposal_id = sys.argv[2]
        proposal = kernel.get_proposal(proposal_id)
        if proposal:
            result = kernel.calculate_consensus(proposal_id)
            print(f"Proposal: {proposal.title}")
            print(f"Status: {proposal.status.value}")
            print(f"Votes: {len(proposal.votes)}")
            print(f"Approval rate: {result.approval_rate:.1%}")
        else:
            print(f"Proposal {proposal_id} not found")
            
    elif command == 'list':
        proposals = kernel.list_proposals()
        print(f"Total proposals: {len(proposals)}")
        for p in proposals:
            print(f"  [{p.status.value}] {p.proposal_id}: {p.title}")
            
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
