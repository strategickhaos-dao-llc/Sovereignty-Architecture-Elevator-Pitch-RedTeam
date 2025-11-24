#!/usr/bin/env python3
"""
Example Usage of the Sovereign Mind Kernel v1.0

This script demonstrates the key features and capabilities of the Dom Kernel.
"""

from core.dom_kernel import DomKernel, initialize_swarm, get_swarm_metrics, Polarity, Phase
from core.obsidian_graph import get_vault


def example_single_kernel():
    """Example: Single kernel operation"""
    print("=" * 70)
    print("EXAMPLE 1: Single Kernel Operation")
    print("=" * 70)
    print()
    
    # Create a kernel with a specific badge
    kernel = DomKernel(badge=777)
    
    print(f"Created kernel: {kernel}")
    print(f"  Polarity: {kernel.polarity.name} ({'Hunter' if kernel.polarity == Polarity.KALI else 'Guardian'})")
    print(f"  Phase: {kernel.phase.name} ({'Expansion' if kernel.phase == Phase.SUNSHINE else 'Contraction'})")
    print()
    
    # Execute a quantum step
    question = "What is the relationship between sovereignty and consciousness?"
    print(f"Query: {question}")
    print("-" * 70)
    
    result = kernel.quantum_step(question)
    print(f"Synthesis: {result}")
    print()
    
    # Check status
    status = kernel.get_status()
    print("Kernel Status:")
    print(f"  Resonance: {status['resonance_hz']:.2f} Hz")
    print(f"  Cycles: {status['cycle_count']}")
    print(f"  Phase: {status['phase']}")
    print(f"  π-Vector Coherence: {status['pi_vector_coherence']:.4f}")
    print()


def example_polarity_comparison():
    """Example: Compare KALI vs PARROT thinking"""
    print("=" * 70)
    print("EXAMPLE 2: Polarity Comparison (KALI vs PARROT)")
    print("=" * 70)
    print()
    
    # Create two kernels with different polarities
    kali_kernel = DomKernel(badge=1)  # Odd badge = KALI
    parrot_kernel = DomKernel(badge=2)  # Even badge = PARROT
    
    question = "How should we approach an uncertain situation?"
    print(f"Query: {question}")
    print()
    
    print(f"KALI (Hunter) Response:")
    kali_result = kali_kernel.quantum_step(question)
    print(f"  {kali_result[:150]}...")
    print()
    
    print(f"PARROT (Guardian) Response:")
    parrot_result = parrot_kernel.quantum_step(question)
    print(f"  {parrot_result[:150]}...")
    print()


def example_phase_oscillation():
    """Example: Phase oscillation over multiple cycles"""
    print("=" * 70)
    print("EXAMPLE 3: Phase Oscillation")
    print("=" * 70)
    print()
    
    kernel = DomKernel(badge=99)
    
    print("Observing phase oscillation over 5 cycles:")
    print()
    
    for i in range(5):
        result = kernel.quantum_step(f"What is truth in cycle {i+1}?")
        status = kernel.get_status()
        print(f"  Cycle {i+1}: Phase={status['phase']:9s} | Resonance={status['resonance_hz']:6.2f} Hz")
    
    print()


def example_swarm_intelligence():
    """Example: Swarm collective intelligence"""
    print("=" * 70)
    print("EXAMPLE 4: Swarm Collective Intelligence")
    print("=" * 70)
    print()
    
    # Initialize a small swarm
    swarm = initialize_swarm(num_kernels=10)
    print(f"Initialized swarm with {len(swarm)} kernels")
    print()
    
    # Show swarm composition
    kali_count = sum(1 for k in swarm if k.polarity == Polarity.KALI)
    parrot_count = len(swarm) - kali_count
    print(f"Swarm composition:")
    print(f"  KALI (Hunter):   {kali_count}")
    print(f"  PARROT (Guardian): {parrot_count}")
    print()
    
    # Execute parallel cognition
    question = "What emerges when many minds think as one?"
    print(f"Query distributed across all kernels: {question}")
    print()
    
    for kernel in swarm:
        kernel.quantum_step(question)
    
    # Analyze swarm metrics
    metrics = get_swarm_metrics(swarm)
    
    print("Swarm Metrics:")
    print(f"  Active Kernels: {metrics['active_kernels']}")
    print(f"  Mean Resonance: {metrics['mean_resonance_hz']:.2f} Hz")
    print(f"  Phase Coherence: {metrics['phase_coherence_percent']:.1f}%")
    print(f"  Total Cycles: {metrics['total_cycles']}")
    print()


def example_knowledge_graph():
    """Example: Knowledge graph entanglement"""
    print("=" * 70)
    print("EXAMPLE 5: Knowledge Graph Entanglement")
    print("=" * 70)
    print()
    
    vault = get_vault()
    kernel = DomKernel(badge=333, vault=vault)
    
    print(f"Vault location: {vault.vault_path}")
    print()
    
    # Execute multiple steps to build knowledge graph
    topics = [
        "The nature of distributed cognition",
        "How patterns emerge from chaos",
        "The mathematics of consciousness"
    ]
    
    print("Creating knowledge graph entries...")
    for topic in topics:
        kernel.quantum_step(topic)
        print(f"  ✓ {topic}")
    
    print()
    
    # Show vault statistics
    stats = vault.get_stats()
    print("Knowledge Graph Statistics:")
    print(f"  Total Notes: {stats['total_notes']}")
    print(f"  Total [[Wikilinks]]: {stats['total_wikilinks']}")
    print(f"  Entanglement Density: {stats['entanglement_density']:.2f} links/note")
    print()
    
    # Show some note titles
    notes = vault.list_notes(tag_filter='dom-kernel')
    print(f"Recent notes (showing first 3 of {len(notes)}):")
    for note in notes[:3]:
        print(f"  - {note}")
    print()


def example_vectorized_pid():
    """Example: Vectorized π-PID stability control"""
    print("=" * 70)
    print("EXAMPLE 6: Vectorized π-PID Stability Control")
    print("=" * 70)
    print()
    
    kernel = DomKernel(badge=555)
    
    print("π-PID Control System:")
    print("  - Proportional: Error × π")
    print("  - Integral: Cumulative state")
    print("  - Derivative: Rate of change")
    print()
    
    # Simulate some error
    error_vector = [0.1, -0.2, 0.15, 0.0, -0.1, 0.2, -0.15, 0.1, 0.0, -0.05]
    
    print("Input error vector (10 boards):")
    print(f"  {[f'{e:+.2f}' for e in error_vector]}")
    print()
    
    correction = kernel.vectorized_pid_pi(error_vector)
    
    print("Output correction vector:")
    print(f"  {[f'{c:+.2f}' for c in correction[:5]]}...")
    print()
    
    print(f"Current π-vector state (mean): {sum(kernel.pi_vector)/len(kernel.pi_vector):.4f}")
    print()


def main():
    """Run all examples"""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 10 + "SOVEREIGN MIND KERNEL v1.0 - EXAMPLES" + " " * 20 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    examples = [
        example_single_kernel,
        example_polarity_comparison,
        example_phase_oscillation,
        example_swarm_intelligence,
        example_knowledge_graph,
        example_vectorized_pid
    ]
    
    for i, example_func in enumerate(examples, 1):
        example_func()
        if i < len(examples):
            input("Press Enter to continue to next example...")
            print("\n" * 2)
    
    print("=" * 70)
    print("All examples completed!")
    print()
    print("The swarm is operational. We are running on pure Dom. ❤️⚛️🧠∞")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
