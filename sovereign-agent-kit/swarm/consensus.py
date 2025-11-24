"""
Consensus Checker - Quantum Error Correction
Multi-agent voting to prevent hallucinations and drift
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class ConsensusVote:
    """A single agent's vote on a note"""
    agent_id: str
    note_title: str
    approved: bool
    confidence: float  # 0.0 to 1.0
    reasoning: Optional[str] = None


class ConsensusChecker:
    """
    Implements quantum error correction via multi-agent consensus.
    Similar to surface code parity checks in quantum computers.
    """
    
    def __init__(
        self,
        agents: List[Any],
        threshold: float = 0.66,
        min_reviewers: int = 3
    ):
        """
        Args:
            agents: List of QuantumAgent instances
            threshold: Consensus threshold (0.66 = 2/3 agreement)
            min_reviewers: Minimum number of agents that must review
        """
        self.agents = agents
        self.threshold = threshold
        self.min_reviewers = min_reviewers
        self.vote_history: List[ConsensusVote] = []
        
        logger.info(
            f"ConsensusChecker initialized with {len(agents)} agents, "
            f"threshold={threshold}, min_reviewers={min_reviewers}"
        )
    
    def check_note(
        self,
        note_title: str,
        author_agent_id: str,
        vault_path: Optional[Path] = None
    ) -> bool:
        """
        Check if a note reaches consensus among peer agents.
        This is the error correction step.
        
        Args:
            note_title: The note to check
            author_agent_id: The agent who created the note
            vault_path: Path to the Obsidian vault
            
        Returns:
            True if consensus reached, False otherwise
        """
        # Get reviewers (all agents except the author)
        reviewers = [a for a in self.agents if a.agent_id != author_agent_id]
        
        if len(reviewers) < self.min_reviewers:
            logger.warning(
                f"Not enough reviewers ({len(reviewers)}) for note {note_title}. "
                f"Minimum required: {self.min_reviewers}"
            )
            return False
        
        # Limit to min_reviewers to avoid excessive checks
        reviewers = reviewers[:self.min_reviewers]
        
        votes: List[ConsensusVote] = []
        
        for reviewer in reviewers:
            vote = self._get_agent_vote(reviewer, note_title, vault_path)
            votes.append(vote)
            self.vote_history.append(vote)
        
        # Calculate consensus
        consensus = self._calculate_consensus(votes)
        
        logger.info(
            f"Consensus check for {note_title}: "
            f"{len([v for v in votes if v.approved])}/{len(votes)} approved "
            f"(threshold: {self.threshold}) = {'PASS' if consensus else 'FAIL'}"
        )
        
        return consensus
    
    def _get_agent_vote(
        self,
        agent: Any,
        note_title: str,
        vault_path: Optional[Path]
    ) -> ConsensusVote:
        """
        Get a single agent's vote on a note.
        In production, this would have the agent actually review the note.
        """
        # In production, this would:
        # 1. Have the agent read the note
        # 2. Ask the agent to evaluate quality, accuracy, relevance
        # 3. Get a structured response with approval and reasoning
        
        # For now, simulate voting
        # In a real system, you'd call agent.think() with a review prompt
        
        import random
        approved = random.random() > 0.2  # 80% approval rate (simulated)
        confidence = random.uniform(0.7, 0.99)
        
        reasoning = (
            f"Agent {agent.agent_id} reviewed {note_title}. "
            f"{'Approved' if approved else 'Rejected'} with {confidence:.2f} confidence."
        )
        
        logger.debug(f"Agent {agent.agent_id} vote: {approved} ({confidence:.2f})")
        
        return ConsensusVote(
            agent_id=agent.agent_id,
            note_title=note_title,
            approved=approved,
            confidence=confidence,
            reasoning=reasoning
        )
    
    def _calculate_consensus(self, votes: List[ConsensusVote]) -> bool:
        """
        Calculate if votes reach consensus threshold.
        Uses weighted voting by confidence.
        """
        if not votes:
            return False
        
        # Weight votes by confidence
        total_weight = sum(v.confidence for v in votes)
        approval_weight = sum(v.confidence for v in votes if v.approved)
        
        if total_weight == 0:
            return False
        
        agreement = approval_weight / total_weight
        
        return agreement >= self.threshold
    
    def get_gate_fidelity(self) -> float:
        """
        Calculate the overall "gate fidelity" of the swarm.
        This is the quantum computing metric for how well operations succeed.
        
        Returns:
            Fidelity as percentage (0.0 to 1.0)
        """
        if not self.vote_history:
            return 0.0
        
        # Group votes by note
        notes: Dict[str, List[ConsensusVote]] = {}
        for vote in self.vote_history:
            if vote.note_title not in notes:
                notes[vote.note_title] = []
            notes[vote.note_title].append(vote)
        
        # Calculate consensus for each note
        consensus_results = [
            self._calculate_consensus(votes)
            for votes in notes.values()
        ]
        
        if not consensus_results:
            return 0.0
        
        fidelity = sum(consensus_results) / len(consensus_results)
        return fidelity
    
    def surface_code_check(self, note_title: str, vault_path: Path) -> Dict[str, bool]:
        """
        Quantum surface code inspired check for note redundancy.
        A note should have:
        - Incoming links (X-stabilizer in quantum terms)
        - Outgoing links (Z-stabilizer in quantum terms)
        - Multiple agent citations (temporal parity)
        
        Returns:
            Dict with stabilizer check results
        """
        note_path = vault_path / f"{note_title}.md"
        
        if not note_path.exists():
            return {
                "x_stabilizer": False,
                "z_stabilizer": False,
                "temporal_parity": False,
                "passes": False
            }
        
        content = note_path.read_text(encoding="utf-8")
        
        # X-stabilizer: Check for incoming links (simulated)
        # In production, would scan all notes for [[note_title]]
        x_stabilizer = "[[" in content  # Simplified check
        
        # Z-stabilizer: Check for outgoing links
        z_stabilizer = "[[" in content
        
        # Temporal parity: Check if multiple agents referenced it
        # In production, would check git history or state files
        temporal_parity = len([v for v in self.vote_history if v.note_title == note_title]) >= 2
        
        passes = x_stabilizer and z_stabilizer and temporal_parity
        
        result = {
            "x_stabilizer": x_stabilizer,
            "z_stabilizer": z_stabilizer,
            "temporal_parity": temporal_parity,
            "passes": passes
        }
        
        logger.info(f"Surface code check for {note_title}: {result}")
        return result


def consensus_reached(
    note_title: str,
    agents: List[Any],
    author_agent_id: str,
    threshold: float = 0.66
) -> bool:
    """
    Convenience function for quick consensus checks.
    
    Args:
        note_title: Note to check
        agents: List of all agents
        author_agent_id: Agent who created the note
        threshold: Consensus threshold
        
    Returns:
        True if consensus reached
    """
    checker = ConsensusChecker(agents, threshold=threshold)
    return checker.check_note(note_title, author_agent_id)


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    
    # Simulate agents for testing
    class MockAgent:
        def __init__(self, agent_id):
            self.agent_id = agent_id
    
    agents = [MockAgent(f"qubit_{i}") for i in range(5)]
    
    checker = ConsensusChecker(agents, threshold=0.66, min_reviewers=3)
    
    # Test consensus check
    result = checker.check_note("test_note", "qubit_0")
    print(f"Consensus reached: {result}")
    
    # Test gate fidelity
    for i in range(10):
        checker.check_note(f"note_{i}", f"qubit_{i % 5}")
    
    fidelity = checker.get_gate_fidelity()
    print(f"Gate fidelity: {fidelity:.1%}")
