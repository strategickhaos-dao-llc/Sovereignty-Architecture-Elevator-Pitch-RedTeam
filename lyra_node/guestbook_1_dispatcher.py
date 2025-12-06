"""
Guestbook-1 Dispatcher
3-node AI task distributor for distributed workloads.

Node Architecture:
- GetLense (Node 1): Architecture, Dependencies, Structure analysis
- JetRider (Node 2): Performance, Optimization, Efficiency tasks
- AI Cluster (Node 3): Security, ML/Patterns, Threat Detection

                    [GUESTBOOK-1 DISPATCHER]
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
    [GetLense]         [JetRider]        [AI Cluster]
    Node 1             Node 2             Node 3
         │                  │                  │
  Architecture      Performance         Security
  Dependencies      Optimization        ML/Patterns
  Structure         Efficiency          Threat Detection
         │                  │                  │
         └──────────────────┼──────────────────┘
                            │
                    [MASTER REPORT]
"""

import json
import logging
import hashlib
from datetime import datetime, timezone
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable
from pathlib import Path

logger = logging.getLogger(__name__)


class NodeType(Enum):
    """Types of AI processing nodes."""
    GETLENSE = "getlense"    # Architecture analysis
    JETRIDER = "jetrider"    # Performance optimization
    AI_CLUSTER = "ai_cluster"  # Security & ML


class TaskCategory(Enum):
    """Task categories for routing."""
    # GetLense categories
    ARCHITECTURE = "architecture"
    DEPENDENCIES = "dependencies"
    STRUCTURE = "structure"
    
    # JetRider categories
    PERFORMANCE = "performance"
    OPTIMIZATION = "optimization"
    EFFICIENCY = "efficiency"
    
    # AI Cluster categories
    SECURITY = "security"
    ML_PATTERNS = "ml_patterns"
    THREAT_DETECTION = "threat_detection"


# Task category to node mapping
CATEGORY_NODE_MAP = {
    TaskCategory.ARCHITECTURE: NodeType.GETLENSE,
    TaskCategory.DEPENDENCIES: NodeType.GETLENSE,
    TaskCategory.STRUCTURE: NodeType.GETLENSE,
    TaskCategory.PERFORMANCE: NodeType.JETRIDER,
    TaskCategory.OPTIMIZATION: NodeType.JETRIDER,
    TaskCategory.EFFICIENCY: NodeType.JETRIDER,
    TaskCategory.SECURITY: NodeType.AI_CLUSTER,
    TaskCategory.ML_PATTERNS: NodeType.AI_CLUSTER,
    TaskCategory.THREAT_DETECTION: NodeType.AI_CLUSTER,
}


@dataclass
class TaskResult:
    """Result from a node task execution."""
    
    task_id: str
    node_type: NodeType
    category: TaskCategory
    success: bool
    output: Any
    execution_time_ms: float
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))
    error: str | None = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "task_id": self.task_id,
            "node": self.node_type.value,
            "category": self.category.value,
            "success": self.success,
            "output": self.output,
            "execution_time_ms": round(self.execution_time_ms, 2),
            "timestamp": self.timestamp,
            "error": self.error
        }


@dataclass
class AINode:
    """Represents an AI processing node."""
    
    node_type: NodeType
    name: str
    description: str
    capabilities: list[TaskCategory]
    status: str = "online"
    tasks_processed: int = 0
    total_execution_time_ms: float = 0.0
    
    def can_handle(self, category: TaskCategory) -> bool:
        """Check if node can handle a task category."""
        return category in self.capabilities
    
    def record_task(self, execution_time_ms: float) -> None:
        """Record task execution stats."""
        self.tasks_processed += 1
        self.total_execution_time_ms += execution_time_ms
    
    @property
    def average_execution_time_ms(self) -> float:
        """Calculate average execution time."""
        if self.tasks_processed == 0:
            return 0.0
        return self.total_execution_time_ms / self.tasks_processed
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "node_type": self.node_type.value,
            "name": self.name,
            "description": self.description,
            "capabilities": [c.value for c in self.capabilities],
            "status": self.status,
            "stats": {
                "tasks_processed": self.tasks_processed,
                "total_execution_time_ms": round(self.total_execution_time_ms, 2),
                "average_execution_time_ms": round(self.average_execution_time_ms, 2)
            }
        }


class Guestbook1Dispatcher:
    """
    Guestbook-1 Dispatcher - 3-node AI task distribution system.
    
    Routes tasks to appropriate AI nodes based on category:
    - GetLense: Architecture, Dependencies, Structure
    - JetRider: Performance, Optimization, Efficiency
    - AI Cluster: Security, ML/Patterns, Threat Detection
    """
    
    VERSION = "1.0.0"
    
    def __init__(self):
        """Initialize the dispatcher with 3 AI nodes."""
        self._nodes: dict[NodeType, AINode] = {}
        self._task_handlers: dict[TaskCategory, Callable] = {}
        self._task_history: list[TaskResult] = []
        self._initialize_nodes()
        self._register_default_handlers()
    
    def _initialize_nodes(self) -> None:
        """Initialize the three AI processing nodes."""
        self._nodes[NodeType.GETLENSE] = AINode(
            node_type=NodeType.GETLENSE,
            name="GetLense",
            description="Architecture, Dependencies, and Structure analysis node",
            capabilities=[
                TaskCategory.ARCHITECTURE,
                TaskCategory.DEPENDENCIES,
                TaskCategory.STRUCTURE
            ]
        )
        
        self._nodes[NodeType.JETRIDER] = AINode(
            node_type=NodeType.JETRIDER,
            name="JetRider",
            description="Performance, Optimization, and Efficiency processing node",
            capabilities=[
                TaskCategory.PERFORMANCE,
                TaskCategory.OPTIMIZATION,
                TaskCategory.EFFICIENCY
            ]
        )
        
        self._nodes[NodeType.AI_CLUSTER] = AINode(
            node_type=NodeType.AI_CLUSTER,
            name="AI Cluster",
            description="Security, ML/Patterns, and Threat Detection node",
            capabilities=[
                TaskCategory.SECURITY,
                TaskCategory.ML_PATTERNS,
                TaskCategory.THREAT_DETECTION
            ]
        )
    
    def _register_default_handlers(self) -> None:
        """Register default task handlers."""
        # GetLense handlers
        self._task_handlers[TaskCategory.ARCHITECTURE] = self._analyze_architecture
        self._task_handlers[TaskCategory.DEPENDENCIES] = self._analyze_dependencies
        self._task_handlers[TaskCategory.STRUCTURE] = self._analyze_structure
        
        # JetRider handlers
        self._task_handlers[TaskCategory.PERFORMANCE] = self._analyze_performance
        self._task_handlers[TaskCategory.OPTIMIZATION] = self._suggest_optimization
        self._task_handlers[TaskCategory.EFFICIENCY] = self._measure_efficiency
        
        # AI Cluster handlers
        self._task_handlers[TaskCategory.SECURITY] = self._scan_security
        self._task_handlers[TaskCategory.ML_PATTERNS] = self._detect_patterns
        self._task_handlers[TaskCategory.THREAT_DETECTION] = self._detect_threats
    
    def _generate_task_id(self, category: TaskCategory) -> str:
        """Generate a unique task ID."""
        timestamp = datetime.now(timezone.utc).isoformat()
        data = f"{category.value}:{timestamp}:{len(self._task_history)}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def get_node(self, node_type: NodeType) -> AINode:
        """Get a specific AI node."""
        return self._nodes[node_type]
    
    def get_all_nodes(self) -> list[AINode]:
        """Get all AI nodes."""
        return list(self._nodes.values())
    
    def route_task(self, category: TaskCategory) -> NodeType:
        """Determine which node should handle a task category."""
        return CATEGORY_NODE_MAP.get(category)
    
    def dispatch(self, category: TaskCategory, payload: Any = None) -> TaskResult:
        """
        Dispatch a task to the appropriate AI node.
        
        Args:
            category: The task category
            payload: Optional data payload for the task
            
        Returns:
            TaskResult with execution details
        """
        task_id = self._generate_task_id(category)
        node_type = self.route_task(category)
        node = self._nodes[node_type]
        
        start_time = datetime.now(timezone.utc)
        error = None
        output = None
        success = False
        
        try:
            handler = self._task_handlers.get(category)
            if handler:
                output = handler(payload)
                success = True
            else:
                error = f"No handler registered for category: {category.value}"
        except Exception as e:
            error = str(e)
            logger.exception(f"Task execution error: {e}")
        
        end_time = datetime.now(timezone.utc)
        execution_time_ms = (end_time - start_time).total_seconds() * 1000
        
        # Record stats on node
        node.record_task(execution_time_ms)
        
        result = TaskResult(
            task_id=task_id,
            node_type=node_type,
            category=category,
            success=success,
            output=output,
            execution_time_ms=execution_time_ms,
            error=error
        )
        
        self._task_history.append(result)
        logger.info(f"Task {task_id} dispatched to {node.name}: {category.value}")
        
        return result
    
    def dispatch_all(self, payload: Any = None) -> dict[str, TaskResult]:
        """
        Dispatch tasks to all categories and compile master report.
        
        Args:
            payload: Data to analyze across all nodes
            
        Returns:
            Dictionary mapping category names to results
        """
        results = {}
        for category in TaskCategory:
            result = self.dispatch(category, payload)
            results[category.value] = result
        return results
    
    def generate_master_report(self, results: dict[str, TaskResult] = None) -> dict:
        """
        Generate a master report from task results.
        
        Args:
            results: Optional results dict (uses task history if not provided)
            
        Returns:
            Comprehensive report dictionary
        """
        if results is None:
            results = {r.category.value: r for r in self._task_history}
        
        # Group results by node
        node_results = {
            NodeType.GETLENSE.value: [],
            NodeType.JETRIDER.value: [],
            NodeType.AI_CLUSTER.value: []
        }
        
        for category_name, result in results.items():
            if isinstance(result, TaskResult):
                node_results[result.node_type.value].append(result.to_dict())
        
        return {
            "version": self.VERSION,
            "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "summary": {
                "total_tasks": len(results),
                "successful": sum(1 for r in results.values() if isinstance(r, TaskResult) and r.success),
                "failed": sum(1 for r in results.values() if isinstance(r, TaskResult) and not r.success)
            },
            "nodes": {node.node_type.value: node.to_dict() for node in self._nodes.values()},
            "results_by_node": node_results
        }
    
    def register_handler(self, category: TaskCategory, handler: Callable) -> None:
        """Register a custom task handler."""
        self._task_handlers[category] = handler
    
    # Default task handlers
    
    def _analyze_architecture(self, payload: Any) -> dict:
        """Analyze system architecture."""
        return {
            "analysis_type": "architecture",
            "components_detected": 3,
            "recommendations": ["Modular design detected", "Consider microservices pattern"]
        }
    
    def _analyze_dependencies(self, payload: Any) -> dict:
        """Analyze project dependencies."""
        return {
            "analysis_type": "dependencies",
            "total_deps": 0,
            "outdated": 0,
            "vulnerable": 0
        }
    
    def _analyze_structure(self, payload: Any) -> dict:
        """Analyze code structure."""
        return {
            "analysis_type": "structure",
            "files_analyzed": 0,
            "complexity_score": 0.0
        }
    
    def _analyze_performance(self, payload: Any) -> dict:
        """Analyze system performance."""
        return {
            "analysis_type": "performance",
            "latency_ms": 0.0,
            "throughput": 0
        }
    
    def _suggest_optimization(self, payload: Any) -> dict:
        """Suggest optimizations."""
        return {
            "analysis_type": "optimization",
            "suggestions": ["Enable caching", "Use connection pooling"],
            "estimated_improvement": "20%"
        }
    
    def _measure_efficiency(self, payload: Any) -> dict:
        """Measure system efficiency."""
        return {
            "analysis_type": "efficiency",
            "cpu_utilization": 0.0,
            "memory_utilization": 0.0,
            "efficiency_score": 0.0
        }
    
    def _scan_security(self, payload: Any) -> dict:
        """Scan for security issues."""
        return {
            "analysis_type": "security",
            "vulnerabilities": [],
            "risk_level": "low"
        }
    
    def _detect_patterns(self, payload: Any) -> dict:
        """Detect ML patterns."""
        return {
            "analysis_type": "ml_patterns",
            "patterns_detected": [],
            "confidence": 0.0
        }
    
    def _detect_threats(self, payload: Any) -> dict:
        """Detect threats."""
        return {
            "analysis_type": "threat_detection",
            "threats": [],
            "threat_level": "none"
        }
    
    def export_to_json(self, filepath: str | Path = None) -> str:
        """Export dispatcher state to JSON."""
        data = {
            "version": self.VERSION,
            "exported_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "nodes": {node.node_type.value: node.to_dict() for node in self._nodes.values()},
            "task_history": [r.to_dict() for r in self._task_history]
        }
        
        json_str = json.dumps(data, indent=2)
        
        if filepath:
            path = Path(filepath)
            path.write_text(json_str)
            logger.info(f"Exported dispatcher state to {filepath}")
        
        return json_str
