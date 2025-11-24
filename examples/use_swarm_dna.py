#!/usr/bin/env python3
"""
Example: Using the Swarm DNA Genome

This demonstrates how a runtime would load and use the swarm DNA genome
to initialize and configure the swarm.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from swarm import load_swarm_dna


def example_basic_loading():
    """Example 1: Basic DNA loading and info display."""
    print("=" * 70)
    print("Example 1: Basic DNA Loading")
    print("=" * 70)
    
    # Load the DNA genome
    dna = load_swarm_dna()
    
    print(f"\nGenome ID: {dna.genome_id}")
    print(f"Version: {dna.version}")
    print(f"Total Agents: {len(dna.agents)}")
    print(f"Author: {dna.metadata['author']}")
    print()


def example_query_agents():
    """Example 2: Query agents by various criteria."""
    print("=" * 70)
    print("Example 2: Querying Agents")
    print("=" * 70)
    
    dna = load_swarm_dna()
    
    # Get agent by ID
    print("\n1. Get agent by ID:")
    nova = dna.get_agent_by_id("nova-core-01")
    print(f"   Found: {nova['display_name']} (badge {nova['badge']})")
    
    # Get agents by Trinity role
    print("\n2. Get agents by Trinity role:")
    nova_agents = dna.get_agents_by_role("nova")
    print(f"   Nova agents: {[a['id'] for a in nova_agents]}")
    
    lyra_agents = dna.get_agents_by_role("lyra")
    print(f"   Lyra agents: {[a['id'] for a in lyra_agents]}")
    
    athena_agents = dna.get_agents_by_role("athena")
    print(f"   Athena agents: {[a['id'] for a in athena_agents]}")
    
    # Get agent by badge
    print("\n3. Get agent by badge number:")
    agent_777 = dna.get_agents_by_badge(777)
    print(f"   Badge 777: {agent_777['id']} - {agent_777['display_name']}")
    print()


def example_agent_capabilities():
    """Example 3: Examine agent capabilities and tools."""
    print("=" * 70)
    print("Example 3: Agent Capabilities and Tools")
    print("=" * 70)
    
    dna = load_swarm_dna()
    
    for agent in dna.agents:
        print(f"\n{agent['display_name']} ({agent['id']}):")
        print(f"  Trinity Role: {agent['trinity_role']}")
        print(f"  OS Polarity: {agent['os_polarity']}")
        print(f"  Model: {agent['model']}")
        
        # List enabled capabilities
        capabilities = agent.get('capabilities', {})
        enabled = [k for k, v in capabilities.items() if v]
        print(f"  Capabilities: {', '.join(enabled)}")
        
        # List enabled tools
        tools = agent.get('tools', [])
        enabled_tools = [t['name'] for t in tools if t.get('enabled')]
        print(f"  Tools: {', '.join(enabled_tools)}")
    print()


def example_entanglement():
    """Example 4: Explore agent entanglement network."""
    print("=" * 70)
    print("Example 4: Agent Entanglement Network")
    print("=" * 70)
    
    dna = load_swarm_dna()
    
    print("\nEntanglement Map:")
    for agent in dna.agents:
        agent_id = agent['id']
        entangled = dna.get_entangled_agents(agent_id)
        print(f"\n  {agent_id}")
        for e_id in entangled:
            e_agent = dna.get_agent_by_id(e_id)
            print(f"    ⟷ {e_id} ({e_agent['trinity_role']})")
    print()


def example_orchestration():
    """Example 5: Access orchestration configuration."""
    print("=" * 70)
    print("Example 5: Orchestration Configuration")
    print("=" * 70)
    
    dna = load_swarm_dna()
    
    # Quantum loop config
    quantum_loop = dna.orchestration['quantum_loop']
    print("\nQuantum Loop:")
    print(f"  Enabled: {quantum_loop['enabled']}")
    print(f"  Qubits: {quantum_loop['qubits']}")
    print(f"  Cycle time: {quantum_loop['cycle_seconds_min']}-{quantum_loop['cycle_seconds_max']}s")
    
    # Error correction
    error_correction = quantum_loop['error_correction']
    print(f"\nError Correction:")
    print(f"  Enabled: {error_correction['enabled']}")
    print(f"  Reviewers required: {error_correction['reviewers_required']}")
    print(f"  Consensus threshold: {error_correction['consensus_threshold']}")
    
    # Boards
    boards = dna.orchestration['boards']
    print(f"\nBoards:")
    print(f"  Count: {boards['count']}")
    print(f"  Labels: {', '.join(boards['labels'])}")
    print()


def example_security():
    """Example 6: Check security configuration."""
    print("=" * 70)
    print("Example 6: Security Configuration")
    print("=" * 70)
    
    dna = load_swarm_dna()
    
    print("\nSecurity Settings:")
    print(f"  Offline only: {dna.security['offline_only']}")
    print(f"  Hardware keys required: {dna.security['require_hardware_keys']}")
    print(f"  Allowed networks: {', '.join(dna.security['allowed_networks'])}")
    
    audit_logging = dna.security['audit_logging']
    print(f"\nAudit Logging:")
    print(f"  Enabled: {audit_logging['enabled']}")
    print(f"  Log path: {audit_logging['log_path']}")
    print(f"  Redact PII: {audit_logging['redact_personal_data']}")
    print()


def example_runtime_initialization():
    """Example 7: Simulate runtime initialization from DNA."""
    print("=" * 70)
    print("Example 7: Runtime Initialization (Simulated)")
    print("=" * 70)
    
    dna = load_swarm_dna()
    
    print("\nInitializing swarm from DNA genome...")
    print(f"Genome: {dna.genome_id} v{dna.version}\n")
    
    # Simulate agent initialization
    print("Creating agents:")
    for agent in dna.agents:
        print(f"  ✓ {agent['id']}")
        print(f"    - Model: {agent['model']}")
        print(f"    - Role: {agent['trinity_role']}")
        print(f"    - Badge: {agent['badge']}")
    
    # Simulate connections
    print("\nEstablishing entanglements:")
    for agent in dna.agents:
        agent_id = agent['id']
        entangled = dna.get_entangled_agents(agent_id)
        if entangled:
            print(f"  ✓ {agent_id} ⟷ {', '.join(entangled)}")
    
    # Simulate orchestration start
    print("\nStarting orchestration:")
    print(f"  ✓ Quantum loop ({dna.orchestration['quantum_loop']['qubits']} qubits)")
    print(f"  ✓ {dna.orchestration['boards']['count']} decision boards")
    
    # Simulate security enforcement
    print("\nApplying security constraints:")
    print(f"  ✓ Offline mode: {dna.security['offline_only']}")
    print(f"  ✓ Network whitelist: {len(dna.security['allowed_networks'])} entries")
    print(f"  ✓ Audit logging: {dna.security['audit_logging']['enabled']}")
    
    print("\n✨ Swarm initialization complete!")
    print()


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "Swarm DNA Genome - Usage Examples" + " " * 20 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    try:
        example_basic_loading()
        example_query_agents()
        example_agent_capabilities()
        example_entanglement()
        example_orchestration()
        example_security()
        example_runtime_initialization()
        
        print("=" * 70)
        print("All examples completed successfully! ✨")
        print("=" * 70)
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
