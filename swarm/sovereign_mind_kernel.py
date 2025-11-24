#!/usr/bin/env python3
"""
Sovereign Mind Kernel v1.0
Core orchestration engine for the Sovereign Swarm architecture

The Mind Kernel manages:
- Agent lifecycle and coordination
- Quantum loop iteration (thesis → antithesis → synthesis)
- Decision making and conflict resolution
- Integration with external systems
"""

import time
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
from pathlib import Path

from load_dna import DNALoader, SwarmDNA, Agent


class KernelState(Enum):
    """Mind Kernel operational states"""
    INITIALIZING = "initializing"
    IDLE = "idle"
    PROCESSING = "processing"
    CONVERGED = "converged"
    ERROR = "error"
    SHUTDOWN = "shutdown"


class WorkflowStage(Enum):
    """Trinity workflow stages"""
    PROPOSAL = "proposal"
    CRITIQUE = "critique"
    INTEGRATION = "integration"


@dataclass
class Task:
    """Represents a task to be processed by the swarm"""
    id: str
    description: str
    stage: WorkflowStage
    created_at: datetime
    assigned_agents: List[str] = field(default_factory=list)
    results: Dict[str, Any] = field(default_factory=dict)
    approvals: int = 0
    status: str = "pending"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QuantumLoopContext:
    """Context for a quantum loop iteration"""
    iteration: int
    convergence_score: float
    proposals: List[Dict[str, Any]] = field(default_factory=list)
    critiques: List[Dict[str, Any]] = field(default_factory=list)
    synthesis: Optional[Dict[str, Any]] = None


class SovereignMindKernel:
    """
    The Sovereign Mind Kernel orchestrates the swarm's cognitive processes.
    
    It implements a quantum loop pattern where ideas go through:
    1. Thesis (proposal) - Agents generate solutions
    2. Antithesis (critique) - Agents identify issues
    3. Synthesis (integration) - Agents make final decisions
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the Mind Kernel"""
        self.logger = self._setup_logging()
        self.state = KernelState.INITIALIZING
        
        # Load DNA configuration
        self.logger.info("🧬 Loading Swarm DNA...")
        self.dna_loader = DNALoader(config_path)
        self.dna = self.dna_loader.load()
        self.dna_loader.validate()
        self.logger.info(f"✅ DNA loaded: {len(self.dna.agents)} agents configured")
        
        # Initialize agent registry
        self.active_agents: Dict[str, Agent] = {}
        self.agent_health: Dict[str, Dict[str, Any]] = {}
        
        # Task management
        self.task_queue: List[Task] = []
        self.task_history: List[Task] = []
        
        # Quantum loop state
        self.quantum_context: Optional[QuantumLoopContext] = None
        self.max_iterations = self.dna.orchestration.get('quantum_loop', {}).get('max_iterations', 10)
        self.convergence_threshold = self.dna.orchestration.get('quantum_loop', {}).get('convergence_threshold', 0.95)
        
        # Callbacks for external integrations
        self.callbacks: Dict[str, List[Callable]] = {
            'on_proposal': [],
            'on_critique': [],
            'on_synthesis': [],
            'on_convergence': [],
            'on_error': []
        }
        
        self.state = KernelState.IDLE
        self.logger.info("✨ Sovereign Mind Kernel initialized")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger("SovereignMindKernel")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def spawn_agents(self) -> None:
        """Spawn all configured agents into the active registry"""
        self.logger.info(f"🚀 Spawning {len(self.dna.agents)} agents...")
        
        for agent in self.dna.agents:
            self.active_agents[agent.name] = agent
            self.agent_health[agent.name] = {
                'status': 'active',
                'last_heartbeat': datetime.now(),
                'tasks_completed': 0,
                'success_rate': 1.0
            }
            self.logger.info(f"   ✓ {agent.name} ({agent.type}) - {agent.trinity_role}")
        
        self.logger.info("✅ All agents spawned and active")
    
    def register_callback(self, event: str, callback: Callable) -> None:
        """Register a callback for kernel events"""
        if event in self.callbacks:
            self.callbacks[event].append(callback)
        else:
            self.logger.warning(f"Unknown event type: {event}")
    
    def _trigger_callbacks(self, event: str, data: Any) -> None:
        """Trigger all registered callbacks for an event"""
        for callback in self.callbacks.get(event, []):
            try:
                callback(data)
            except Exception as e:
                self.logger.error(f"Error in callback for {event}: {e}")
    
    def create_task(self, description: str, metadata: Optional[Dict] = None) -> Task:
        """Create a new task for the swarm to process"""
        task = Task(
            id=f"task_{len(self.task_history) + 1}_{int(time.time())}",
            description=description,
            stage=WorkflowStage.PROPOSAL,
            created_at=datetime.now(),
            metadata=metadata or {}
        )
        self.task_queue.append(task)
        self.logger.info(f"📝 Task created: {task.id} - {description[:50]}...")
        return task
    
    def assign_agents_to_task(self, task: Task, stage: WorkflowStage) -> List[Agent]:
        """Assign appropriate agents to a task based on workflow stage"""
        stage_to_role = {
            WorkflowStage.PROPOSAL: "thesis",
            WorkflowStage.CRITIQUE: "antithesis",
            WorkflowStage.INTEGRATION: "synthesis"
        }
        
        required_role = stage_to_role[stage]
        available_agents = self.dna.get_agents_by_role(required_role)
        
        # Filter by security clearance if needed
        task_clearance = task.metadata.get('security_clearance', 'low')
        available_agents = [
            agent for agent in available_agents
            if self._check_clearance(agent.security_clearance, task_clearance)
        ]
        
        task.assigned_agents = [agent.name for agent in available_agents]
        return available_agents
    
    def _check_clearance(self, agent_clearance: str, required_clearance: str) -> bool:
        """Check if agent has sufficient security clearance"""
        clearance_levels = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        agent_level = clearance_levels.get(agent_clearance, 0)
        required_level = clearance_levels.get(required_clearance, 0)
        return agent_level >= required_level
    
    def quantum_loop(self, task: Task, max_iterations: Optional[int] = None) -> Dict[str, Any]:
        """
        Execute the quantum loop for a task:
        Iterate through thesis → antithesis → synthesis until convergence
        
        Returns:
            Final synthesis result with convergence metrics
        """
        max_iter = max_iterations or self.max_iterations
        self.quantum_context = QuantumLoopContext(iteration=0, convergence_score=0.0)
        
        self.logger.info(f"🔮 Starting quantum loop for task: {task.id}")
        self.state = KernelState.PROCESSING
        
        for iteration in range(max_iter):
            self.quantum_context.iteration = iteration + 1
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"🔄 Quantum Loop Iteration {iteration + 1}/{max_iter}")
            self.logger.info(f"{'='*60}")
            
            # Stage 1: Thesis (Proposal)
            self.logger.info("\n📝 Stage 1: THESIS (Proposal)")
            task.stage = WorkflowStage.PROPOSAL
            proposal_agents = self.assign_agents_to_task(task, WorkflowStage.PROPOSAL)
            proposals = self._execute_stage(task, proposal_agents, "proposal")
            self.quantum_context.proposals.extend(proposals)
            self._trigger_callbacks('on_proposal', {'task': task, 'proposals': proposals})
            
            # Stage 2: Antithesis (Critique)
            self.logger.info("\n🔍 Stage 2: ANTITHESIS (Critique)")
            task.stage = WorkflowStage.CRITIQUE
            critique_agents = self.assign_agents_to_task(task, WorkflowStage.CRITIQUE)
            critiques = self._execute_stage(task, critique_agents, "critique", context=proposals)
            self.quantum_context.critiques.extend(critiques)
            self._trigger_callbacks('on_critique', {'task': task, 'critiques': critiques})
            
            # Stage 3: Synthesis (Integration)
            self.logger.info("\n🎯 Stage 3: SYNTHESIS (Integration)")
            task.stage = WorkflowStage.INTEGRATION
            synthesis_agents = self.assign_agents_to_task(task, WorkflowStage.INTEGRATION)
            synthesis = self._execute_synthesis(task, synthesis_agents, proposals, critiques)
            self.quantum_context.synthesis = synthesis
            self._trigger_callbacks('on_synthesis', {'task': task, 'synthesis': synthesis})
            
            # Check for convergence
            convergence_score = synthesis.get('convergence_score', 0.0)
            self.quantum_context.convergence_score = convergence_score
            
            self.logger.info(f"\n📊 Convergence Score: {convergence_score:.2%}")
            
            if convergence_score >= self.convergence_threshold:
                self.logger.info(f"✅ Convergence achieved at iteration {iteration + 1}")
                self.state = KernelState.CONVERGED
                task.status = "completed"
                self._trigger_callbacks('on_convergence', {'task': task, 'iterations': iteration + 1})
                break
            else:
                self.logger.info(f"⏳ Continuing iteration (threshold: {self.convergence_threshold:.2%})")
        
        else:
            # Max iterations reached without convergence
            self.logger.warning(f"⚠️ Max iterations ({max_iter}) reached without full convergence")
            task.status = "partial_convergence"
        
        # Record results
        task.results = {
            'proposals': self.quantum_context.proposals,
            'critiques': self.quantum_context.critiques,
            'synthesis': self.quantum_context.synthesis,
            'iterations': self.quantum_context.iteration,
            'final_convergence': self.quantum_context.convergence_score
        }
        
        self.task_history.append(task)
        self.state = KernelState.IDLE
        
        return task.results
    
    def _execute_stage(
        self, 
        task: Task, 
        agents: List[Agent], 
        stage_name: str,
        context: Optional[List[Dict]] = None
    ) -> List[Dict[str, Any]]:
        """Execute a workflow stage with assigned agents"""
        results = []
        
        for agent in agents:
            self.logger.info(f"   🤖 Agent '{agent.name}' processing...")
            
            # Simulate agent work (in real implementation, this would call agent services)
            result = {
                'agent': agent.name,
                'stage': stage_name,
                'timestamp': datetime.now().isoformat(),
                'output': f"[{stage_name.upper()}] {agent.name}'s contribution to: {task.description}",
                'confidence': 0.85 + (agent.autonomy_level * 0.03),  # Higher autonomy = higher confidence
                'tools_used': agent.tools[:2]  # Simulate using some tools
            }
            
            results.append(result)
            
            # Update agent health
            self.agent_health[agent.name]['tasks_completed'] += 1
            self.agent_health[agent.name]['last_heartbeat'] = datetime.now()
        
        return results
    
    def _execute_synthesis(
        self,
        task: Task,
        agents: List[Agent],
        proposals: List[Dict],
        critiques: List[Dict]
    ) -> Dict[str, Any]:
        """Execute synthesis stage to integrate proposals and critiques"""
        self.logger.info(f"   🎯 Synthesizing {len(proposals)} proposals and {len(critiques)} critiques...")
        
        # Calculate convergence based on proposal-critique alignment
        # In a real system, this would use sophisticated analysis
        proposal_count = len(proposals)
        critique_count = len(critiques)
        
        # Simple convergence heuristic
        if proposal_count > 0:
            critique_coverage = min(critique_count / proposal_count, 1.0)
            base_convergence = 0.7 + (critique_coverage * 0.25)
        else:
            critique_coverage = 0.0
            base_convergence = 0.5
        
        synthesis = {
            'decision': 'proceed' if base_convergence > 0.8 else 'refine',
            'convergence_score': base_convergence,
            'synthesis_agents': [agent.name for agent in agents],
            'timestamp': datetime.now().isoformat(),
            'summary': f"Synthesized {proposal_count} proposals with {critique_count} critiques",
            'recommendations': [
                "Review security implications" if critique_coverage < 0.8 else "Security review complete",
                "Documentation updated" if proposal_count > 0 else "No documentation needed",
                "Tests passing" if base_convergence > 0.85 else "Additional testing recommended"
            ]
        }
        
        return synthesis
    
    def get_kernel_status(self) -> Dict[str, Any]:
        """Get current kernel status and metrics"""
        return {
            'state': self.state.value,
            'active_agents': len(self.active_agents),
            'queued_tasks': len(self.task_queue),
            'completed_tasks': len(self.task_history),
            'quantum_loop': {
                'enabled': self.dna.orchestration.get('quantum_loop', {}).get('enabled', False),
                'max_iterations': self.max_iterations,
                'convergence_threshold': self.convergence_threshold
            },
            'current_context': {
                'iteration': self.quantum_context.iteration if self.quantum_context else 0,
                'convergence': self.quantum_context.convergence_score if self.quantum_context else 0.0
            } if self.quantum_context else None
        }
    
    def get_agent_status(self, agent_name: Optional[str] = None) -> Dict[str, Any]:
        """Get status for specific agent or all agents"""
        if agent_name:
            if agent_name in self.agent_health:
                return {agent_name: self.agent_health[agent_name]}
            else:
                return {'error': f'Agent {agent_name} not found'}
        else:
            return self.agent_health
    
    def shutdown(self) -> None:
        """Gracefully shutdown the Mind Kernel"""
        self.logger.info("🛑 Shutting down Sovereign Mind Kernel...")
        self.state = KernelState.SHUTDOWN
        
        # Save final state
        self._save_kernel_state()
        
        self.logger.info("✅ Kernel shutdown complete")
    
    def _save_kernel_state(self) -> None:
        """Save kernel state to disk for recovery"""
        # Serialize agent_health with datetime conversion
        serializable_health = {}
        for agent_name, health in self.agent_health.items():
            serializable_health[agent_name] = {
                'status': health['status'],
                'last_heartbeat': health['last_heartbeat'].isoformat(),
                'tasks_completed': health['tasks_completed'],
                'success_rate': health['success_rate']
            }
        
        state_data = {
            'timestamp': datetime.now().isoformat(),
            'state': self.state.value,
            'task_history_count': len(self.task_history),
            'agent_health': serializable_health,
            'dna_version': self.dna.metadata.get('version', 'unknown')
        }
        
        state_file = Path(__file__).parent / 'kernel_state.json'
        with open(state_file, 'w') as f:
            json.dump(state_data, f, indent=2)
        
        self.logger.info(f"💾 Kernel state saved to {state_file}")


def main():
    """Example usage of the Sovereign Mind Kernel"""
    print("="*60)
    print("🧠 SOVEREIGN MIND KERNEL v1.0")
    print("="*60)
    
    # Initialize kernel
    kernel = SovereignMindKernel()
    
    # Spawn agents
    kernel.spawn_agents()
    
    # Register example callbacks
    def on_proposal(data):
        print(f"\n📢 CALLBACK: Proposal received from {len(data['proposals'])} agents")
    
    def on_convergence(data):
        print(f"\n🎉 CALLBACK: Task converged in {data['iterations']} iterations!")
    
    kernel.register_callback('on_proposal', on_proposal)
    kernel.register_callback('on_convergence', on_convergence)
    
    # Create and process a test task
    task = kernel.create_task(
        description="Implement YAML DNA genome configuration system",
        metadata={'security_clearance': 'medium', 'priority': 'high'}
    )
    
    # Execute quantum loop
    results = kernel.quantum_loop(task, max_iterations=3)
    
    # Display results
    print("\n" + "="*60)
    print("📊 FINAL RESULTS")
    print("="*60)
    print(f"Task Status: {task.status}")
    print(f"Iterations: {results['iterations']}")
    print(f"Final Convergence: {results['final_convergence']:.2%}")
    print(f"Decision: {results['synthesis']['decision']}")
    
    # Show kernel status
    status = kernel.get_kernel_status()
    print("\n" + "="*60)
    print("🧠 KERNEL STATUS")
    print("="*60)
    print(json.dumps(status, indent=2))
    
    # Shutdown
    kernel.shutdown()


if __name__ == "__main__":
    main()
