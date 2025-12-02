#!/usr/bin/env python3
"""
Simple Quantum Swarm Demo
Demonstrates running a small quantum swarm for testing
"""

import sys
import os
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from swarm.quantum_loop import QuantumAgent, run_quantum_loop
from swarm.consensus import ConsensusChecker

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Run a simple 3-qubit quantum swarm demo"""
    
    print("=" * 60)
    print("  QUANTUM SWARM DEMO - 3 Qubits, 5 Iterations Each")
    print("=" * 60)
    print()
    
    # Configuration
    vault_path = "./demo_vault"
    num_qubits = 3
    max_iterations = 5
    
    config = {
        "think_temperature": 0.7,
        "sleep_min": 1,
        "sleep_max": 3,
    }
    
    logger.info(f"Creating {num_qubits} quantum agents...")
    
    # Create agents
    agents = []
    for i in range(num_qubits):
        agent = QuantumAgent(
            agent_id=f"demo_qubit_{i}",
            model="claude-3-opus",
            vault_path=vault_path,
            config=config
        )
        agents.append(agent)
    
    logger.info(f"Created {len(agents)} agents")
    
    # Create consensus checker
    checker = ConsensusChecker(
        agents,
        threshold=0.66,
        min_reviewers=2
    )
    
    logger.info(f"Created consensus checker (threshold={checker.threshold})")
    print()
    
    # Run each agent for limited iterations
    for agent in agents:
        logger.info(f"🚀 Starting quantum loop for {agent.agent_id}")
        run_quantum_loop(
            agent,
            max_iterations=max_iterations,
            consensus_checker=checker
        )
        print()
    
    # Report results
    print("=" * 60)
    print("  DEMO RESULTS")
    print("=" * 60)
    print()
    
    total_iterations = sum(len(a.state_history) for a in agents)
    print(f"Total iterations completed: {total_iterations}")
    
    # Count notes in vault
    vault = Path(vault_path)
    if vault.exists():
        notes = list(vault.glob("*.md"))
        print(f"Notes in vault: {len(notes)}")
        
        # Count wikilinks
        total_links = 0
        for note in notes:
            content = note.read_text()
            total_links += content.count("[[")
        print(f"Total wikilinks: {total_links}")
    
    # Gate fidelity
    fidelity = checker.get_gate_fidelity()
    print(f"Gate fidelity: {fidelity:.1%}")
    
    print()
    print("=" * 60)
    print(f"  DEMO COMPLETE - Check {vault_path}/ for generated notes")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Demo failed: {e}", exc_info=True)
        sys.exit(1)
