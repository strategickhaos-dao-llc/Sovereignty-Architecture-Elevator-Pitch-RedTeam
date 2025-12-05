#!/usr/bin/env python3
"""
Example Integration: Demonstrating Swarm DNA + Mind Kernel
Shows how to use the complete swarm architecture for task processing
"""

try:
    from .sovereign_mind_kernel import SovereignMindKernel
    from .load_dna import load_swarm_dna
except ImportError:
    # Fallback for direct script execution
    from sovereign_mind_kernel import SovereignMindKernel
    from load_dna import load_swarm_dna
import json


def example_1_basic_task():
    """Example 1: Basic task processing with quantum loop"""
    print("="*70)
    print("EXAMPLE 1: Basic Task Processing")
    print("="*70)
    
    # Initialize kernel
    kernel = SovereignMindKernel()
    kernel.spawn_agents()
    
    # Create a task (use 'medium' clearance to allow all agents to participate)
    task = kernel.create_task(
        description="Review and improve security posture",
        metadata={'security_clearance': 'medium', 'priority': 'critical'}
    )
    
    # Execute quantum loop with limited iterations
    results = kernel.quantum_loop(task, max_iterations=2)
    
    # Display results
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    print(f"Task ID: {task.id}")
    print(f"Status: {task.status}")
    print(f"Iterations: {results['iterations']}")
    print(f"Final Convergence: {results['final_convergence']:.2%}")
    print(f"Decision: {results['synthesis']['decision']}")
    print(f"\nProposals: {len(results['proposals'])}")
    print(f"Critiques: {len(results['critiques'])}")
    
    kernel.shutdown()
    print("\n✅ Example 1 complete\n")


def example_2_with_callbacks():
    """Example 2: Task processing with event callbacks"""
    print("="*70)
    print("EXAMPLE 2: Task Processing with Callbacks")
    print("="*70)
    
    # Initialize kernel
    kernel = SovereignMindKernel()
    
    # Register callbacks
    def on_proposal(data):
        agents = [p['agent'] for p in data['proposals']]
        print(f"\n📢 [CALLBACK] Proposals received from: {', '.join(agents)}")
    
    def on_critique(data):
        agents = [c['agent'] for c in data['critiques']]
        print(f"🔍 [CALLBACK] Critiques received from: {', '.join(agents)}")
    
    def on_synthesis(data):
        decision = data['synthesis']['decision']
        score = data['synthesis']['convergence_score']
        print(f"🎯 [CALLBACK] Synthesis complete: {decision} (score: {score:.2%})")
    
    def on_convergence(data):
        print(f"🎉 [CALLBACK] CONVERGENCE achieved in {data['iterations']} iterations!")
    
    kernel.register_callback('on_proposal', on_proposal)
    kernel.register_callback('on_critique', on_critique)
    kernel.register_callback('on_synthesis', on_synthesis)
    kernel.register_callback('on_convergence', on_convergence)
    
    # Spawn and process
    kernel.spawn_agents()
    task = kernel.create_task(
        description="Implement new authentication system",
        metadata={'security_clearance': 'medium'}
    )
    
    results = kernel.quantum_loop(task, max_iterations=2)
    
    print(f"\n✅ Task completed: {task.status}")
    kernel.shutdown()
    print("\n✅ Example 2 complete\n")


def example_3_dna_exploration():
    """Example 3: Exploring the DNA configuration"""
    print("="*70)
    print("EXAMPLE 3: DNA Configuration Exploration")
    print("="*70)
    
    # Load DNA
    dna = load_swarm_dna()
    
    print(f"\n📊 DNA Metadata:")
    print(f"   Version: {dna.metadata['version']}")
    print(f"   Created: {dna.metadata['created']}")
    print(f"   Description: {dna.metadata['description']}")
    
    print(f"\n🤖 Agents by Trinity Role:")
    for role in ['thesis', 'antithesis', 'synthesis']:
        agents = dna.get_agents_by_role(role)
        print(f"\n   {role.upper()}:")
        for agent in agents:
            print(f"   • {agent.name} ({agent.type})")
            print(f"     - Security: {agent.security_clearance}")
            print(f"     - Autonomy: {agent.autonomy_level}/5")
            print(f"     - Functions: {', '.join(agent.primary_functions[:2])}...")
            print(f"     - Tools: {', '.join(agent.tools[:3])}...")
    
    print(f"\n🔒 Security Configuration:")
    print(f"   Encryption at rest: {dna.security['encryption']['at_rest']}")
    print(f"   Encryption in transit: {dna.security['encryption']['in_transit']}")
    print(f"   Auth method: {dna.security['authentication']['method']}")
    print(f"   Audit enabled: {dna.security['audit']['enabled']}")
    
    print(f"\n🔄 Orchestration:")
    ql = dna.orchestration['quantum_loop']
    print(f"   Quantum loop enabled: {ql['enabled']}")
    print(f"   Max iterations: {ql['max_iterations']}")
    print(f"   Convergence threshold: {ql['convergence_threshold']:.1%}")
    
    consensus = dna.orchestration['consensus']
    print(f"   Consensus algorithm: {consensus['algorithm']}")
    print(f"   Quorum required: {consensus['quorum_required']:.1%}")
    
    print(f"\n🌐 Integrations:")
    for integration in ['github', 'discord', 'vector_db', 'ci_cd']:
        enabled = dna.integrations.get(integration, {}).get('enabled', False)
        status = "✅ Enabled" if enabled else "❌ Disabled"
        print(f"   {integration}: {status}")
    
    print("\n✅ Example 3 complete\n")


def example_4_agent_health_monitoring():
    """Example 4: Monitoring agent health and status"""
    print("="*70)
    print("EXAMPLE 4: Agent Health Monitoring")
    print("="*70)
    
    # Initialize and spawn
    kernel = SovereignMindKernel()
    kernel.spawn_agents()
    
    # Process a couple tasks
    task1 = kernel.create_task("Task 1: Security audit")
    kernel.quantum_loop(task1, max_iterations=1)
    
    task2 = kernel.create_task("Task 2: Performance optimization")
    kernel.quantum_loop(task2, max_iterations=1)
    
    # Check kernel status
    status = kernel.get_kernel_status()
    print(f"\n📊 Kernel Status:")
    print(f"   State: {status['state']}")
    print(f"   Active agents: {status['active_agents']}")
    print(f"   Queued tasks: {status['queued_tasks']}")
    print(f"   Completed tasks: {status['completed_tasks']}")
    
    # Check agent health
    print(f"\n🏥 Agent Health:")
    agent_health = kernel.get_agent_status()
    for agent_name, health in agent_health.items():
        print(f"\n   {agent_name}:")
        print(f"     Status: {health['status']}")
        print(f"     Tasks completed: {health['tasks_completed']}")
        print(f"     Success rate: {health['success_rate']:.1%}")
    
    kernel.shutdown()
    print("\n✅ Example 4 complete\n")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("SOVEREIGN SWARM INTEGRATION EXAMPLES")
    print("="*70)
    print("\nDemonstrating DNA + Mind Kernel integration\n")
    
    try:
        example_1_basic_task()
        example_2_with_callbacks()
        example_3_dna_exploration()
        example_4_agent_health_monitoring()
        
        print("\n" + "="*70)
        print("✨ ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
