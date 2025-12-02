"""
Sovereign Cognitive OS - Pattern-Dominant Cognitive Architecture Implementation

v1.0 — Core cognitive components for the Sovereign Swarm Intelligence system.

SPL (Sovereign Pattern Language) Specification:
- Pattern Engine: Pattern recognition and synthesis
- Schema Synthesizer: Architecture and schema creation
- Contradiction Resolver: House-style differential diagnosis
- Context Interpreter: Multi-agent mental model
- Externalization Adapter: Vim + absolute-path CLI integration

"The brain does not recall — it reconstructs."
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


class PatternType(Enum):
    """
    SPL Pattern Classification

    Defines the fundamental pattern types recognized by the cognitive system.
    These map to structural elements in transformer architecture.
    """
    STRUCTURAL = "structural"       # Nested hierarchies
    MODULAR = "modular"             # Component boundaries
    PROTOCOL = "protocol"           # Communication patterns
    RITUAL = "ritual"               # Cognitive rituals
    METAPHOR = "metaphor"           # Metaphors-as-infrastructure
    DELTA = "delta"                 # Iterative changes
    ROLE = "role"                   # Role assignments


class ConfidenceLevel(Enum):
    """
    SPL Confidence Levels for Pattern Recognition

    Maps to transformer attention weights conceptually.
    """
    HIGH = "high"           # Strong pattern match (>0.8)
    MEDIUM = "medium"       # Moderate pattern match (0.5-0.8)
    LOW = "low"             # Weak pattern match (0.2-0.5)
    UNCERTAIN = "uncertain" # Below threshold (<0.2)


@dataclass
class Pattern:
    """
    SPL Pattern Representation

    A recognized pattern with its metadata, confidence, and relationships.
    Patterns are the fundamental units of cognitive reconstruction.
    """
    id: str
    type: PatternType
    name: str
    description: str
    confidence: float
    source_context: str
    related_patterns: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def confidence_level(self) -> ConfidenceLevel:
        """Map numeric confidence to SPL confidence level."""
        if self.confidence > 0.8:
            return ConfidenceLevel.HIGH
        elif self.confidence > 0.5:
            return ConfidenceLevel.MEDIUM
        elif self.confidence > 0.2:
            return ConfidenceLevel.LOW
        return ConfidenceLevel.UNCERTAIN


@dataclass
class Schema:
    """
    SPL Schema Representation

    A synthesized architecture schema composed of patterns.
    Schemas are higher-order structures that emerge from pattern composition.
    """
    id: str
    name: str
    description: str
    patterns: List[Pattern]
    hierarchy: Dict[str, List[str]]  # Parent -> Children mapping
    constraints: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Hypothesis:
    """
    SPL Hypothesis for Differential Diagnosis

    House-style hypothesis with supporting and contradicting evidence.
    """
    id: str
    statement: str
    confidence: float
    supporting_evidence: List[str] = field(default_factory=list)
    contradicting_evidence: List[str] = field(default_factory=list)
    tests_proposed: List[str] = field(default_factory=list)
    status: str = "active"  # active, confirmed, rejected, needs_testing


@dataclass
class Context:
    """
    SPL Context Representation

    Multi-perspective context model for interpretation.
    """
    id: str
    name: str
    perspective: str
    agents: List[str]
    shared_knowledge: Dict[str, Any]
    assumptions: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)


class PatternEngine:
    """
    SPL Pattern Engine - Core Pattern Recognition and Synthesis

    The pattern engine is responsible for:
    - Recognizing patterns in input data
    - Synthesizing new patterns from combinations
    - Maintaining pattern relationships
    - Computing pattern confidence scores

    This mirrors the transformer's token-pattern continuation mechanism.

    TODO: Integrate with GPT/Claude for enhanced pattern recognition
    """

    def __init__(self, pattern_library: Optional[Dict[str, Pattern]] = None):
        """
        Initialize the Pattern Engine.

        Args:
            pattern_library: Optional pre-loaded pattern library
        """
        self._patterns: Dict[str, Pattern] = pattern_library or {}
        self._pattern_index: Dict[PatternType, Set[str]] = {
            pt: set() for pt in PatternType
        }
        self._recognition_history: List[Tuple[str, Pattern]] = []

    def recognize(self, input_data: str, context: Optional[str] = None) -> List[Pattern]:
        """
        SPL Pattern Recognition

        Recognize patterns in input data using reconstruction-based cognition.
        Unlike retrieval, this generates pattern matches dynamically.

        Args:
            input_data: Raw input to analyze for patterns
            context: Optional context to influence recognition

        Returns:
            List of recognized patterns with confidence scores
        """
        recognized = []

        # Structural pattern detection
        if self._detect_hierarchy(input_data):
            pattern = Pattern(
                id=f"struct_{len(self._patterns)}",
                type=PatternType.STRUCTURAL,
                name="Hierarchical Structure",
                description="Detected nested hierarchy in input",
                confidence=self._compute_confidence(input_data, PatternType.STRUCTURAL),
                source_context=context or input_data[:100],
            )
            recognized.append(pattern)

        # Modular pattern detection
        if self._detect_modularity(input_data):
            pattern = Pattern(
                id=f"mod_{len(self._patterns)}",
                type=PatternType.MODULAR,
                name="Modular Component",
                description="Detected modular boundary in input",
                confidence=self._compute_confidence(input_data, PatternType.MODULAR),
                source_context=context or input_data[:100],
            )
            recognized.append(pattern)

        # Protocol pattern detection
        if self._detect_protocol(input_data):
            pattern = Pattern(
                id=f"proto_{len(self._patterns)}",
                type=PatternType.PROTOCOL,
                name="Communication Protocol",
                description="Detected protocol pattern in input",
                confidence=self._compute_confidence(input_data, PatternType.PROTOCOL),
                source_context=context or input_data[:100],
            )
            recognized.append(pattern)

        # Store recognized patterns
        for p in recognized:
            self._patterns[p.id] = p
            self._pattern_index[p.type].add(p.id)
            self._recognition_history.append((input_data[:50], p))

        return recognized

    def synthesize(self, patterns: List[Pattern]) -> Pattern:
        """
        SPL Pattern Synthesis

        Combine multiple patterns into a higher-order synthesized pattern.
        This mirrors cognitive reconstruction and generative emergence.

        Args:
            patterns: List of patterns to synthesize

        Returns:
            New synthesized pattern
        """
        if not patterns:
            raise ValueError("Cannot synthesize from empty pattern list")

        # Compute combined confidence
        combined_confidence = sum(p.confidence for p in patterns) / len(patterns)

        # Determine dominant type
        type_counts: Dict[PatternType, int] = {}
        for p in patterns:
            type_counts[p.type] = type_counts.get(p.type, 0) + 1
        dominant_type = max(type_counts, key=lambda k: type_counts[k])

        synthesized = Pattern(
            id=f"synth_{len(self._patterns)}",
            type=dominant_type,
            name=f"Synthesized[{'+'.join(p.name[:10] for p in patterns[:3])}]",
            description=f"Synthesized from {len(patterns)} patterns",
            confidence=combined_confidence,
            source_context="synthesis",
            related_patterns=[p.id for p in patterns],
            metadata={"source_patterns": len(patterns), "type_distribution": type_counts},
        )

        self._patterns[synthesized.id] = synthesized
        return synthesized

    def get_related(self, pattern_id: str, depth: int = 1) -> List[Pattern]:
        """
        Get patterns related to the given pattern.

        Args:
            pattern_id: ID of the pattern to find relations for
            depth: How deep to traverse relationships

        Returns:
            List of related patterns
        """
        if pattern_id not in self._patterns:
            return []

        related = []
        visited = {pattern_id}
        current_level = [pattern_id]

        for _ in range(depth):
            next_level = []
            for pid in current_level:
                pattern = self._patterns.get(pid)
                if pattern:
                    for rel_id in pattern.related_patterns:
                        if rel_id not in visited and rel_id in self._patterns:
                            visited.add(rel_id)
                            next_level.append(rel_id)
                            related.append(self._patterns[rel_id])
            current_level = next_level

        return related

    def _detect_hierarchy(self, input_data: str) -> bool:
        """Detect hierarchical structure patterns."""
        hierarchy_indicators = ["->", "=>", "parent", "child", "contains", "nested", "/"]
        return any(ind in input_data.lower() for ind in hierarchy_indicators)

    def _detect_modularity(self, input_data: str) -> bool:
        """Detect modular component patterns."""
        modular_indicators = ["module", "component", "service", "interface", "boundary", "class"]
        return any(ind in input_data.lower() for ind in modular_indicators)

    def _detect_protocol(self, input_data: str) -> bool:
        """Detect communication protocol patterns."""
        protocol_indicators = ["request", "response", "message", "event", "handler", "protocol"]
        return any(ind in input_data.lower() for ind in protocol_indicators)

    def _compute_confidence(self, input_data: str, pattern_type: PatternType) -> float:
        """
        Compute confidence score for pattern recognition.

        This is a simplified heuristic. In production, this would be
        replaced with transformer-based attention scoring.
        """
        base_confidence = 0.5

        # Length bonus (more context = higher confidence)
        length_bonus = min(len(input_data) / 1000, 0.2)

        # Type-specific adjustments
        type_bonus = 0.1 if pattern_type in [PatternType.STRUCTURAL, PatternType.MODULAR] else 0.05

        return min(base_confidence + length_bonus + type_bonus, 0.95)


class SchemaSynthesizer:
    """
    SPL Schema Synthesizer - Architecture and Schema Creation

    The schema synthesizer builds higher-order architectural structures
    from recognized patterns. It implements:

    - Pattern composition into schemas
    - Hierarchy derivation
    - Constraint inference
    - Architecture documentation generation

    This component externalizes the cognitive process of architecture creation.

    TODO: Integrate with GPT/Claude for enhanced schema generation
    """

    def __init__(self, pattern_engine: PatternEngine):
        """
        Initialize the Schema Synthesizer.

        Args:
            pattern_engine: The pattern engine for pattern operations
        """
        self._pattern_engine = pattern_engine
        self._schemas: Dict[str, Schema] = {}

    def synthesize_schema(
        self,
        name: str,
        patterns: List[Pattern],
        constraints: Optional[List[str]] = None,
    ) -> Schema:
        """
        SPL Schema Synthesis

        Create a schema from a collection of patterns.

        Args:
            name: Name for the schema
            patterns: Patterns to compose into schema
            constraints: Optional constraints on the schema

        Returns:
            Synthesized schema
        """
        # Derive hierarchy from pattern relationships
        hierarchy = self._derive_hierarchy(patterns)

        schema = Schema(
            id=f"schema_{len(self._schemas)}",
            name=name,
            description=f"Schema synthesized from {len(patterns)} patterns",
            patterns=patterns,
            hierarchy=hierarchy,
            constraints=constraints or [],
        )

        self._schemas[schema.id] = schema
        return schema

    def derive_architecture(self, schema: Schema) -> Dict[str, Any]:
        """
        SPL Architecture Derivation

        Generate an architecture document from a schema.

        Args:
            schema: Schema to derive architecture from

        Returns:
            Architecture document as dictionary
        """
        return {
            "name": schema.name,
            "description": schema.description,
            "components": [
                {
                    "name": p.name,
                    "type": p.type.value,
                    "description": p.description,
                    "confidence": p.confidence,
                }
                for p in schema.patterns
            ],
            "hierarchy": schema.hierarchy,
            "constraints": schema.constraints,
            "metadata": {
                "pattern_count": len(schema.patterns),
                "schema_id": schema.id,
                "created_at": schema.created_at.isoformat(),
            },
        }

    def compose(self, schemas: List[Schema]) -> Schema:
        """
        SPL Schema Composition

        Compose multiple schemas into a meta-schema.

        Args:
            schemas: Schemas to compose

        Returns:
            Composed meta-schema
        """
        all_patterns = []
        combined_hierarchy: Dict[str, List[str]] = {}
        combined_constraints = []

        for s in schemas:
            all_patterns.extend(s.patterns)
            combined_hierarchy.update(s.hierarchy)
            combined_constraints.extend(s.constraints)

        return Schema(
            id=f"meta_schema_{len(self._schemas)}",
            name=f"Composed[{'+'.join(s.name[:10] for s in schemas[:3])}]",
            description=f"Meta-schema composed from {len(schemas)} schemas",
            patterns=all_patterns,
            hierarchy=combined_hierarchy,
            constraints=list(set(combined_constraints)),
            metadata={"source_schemas": [s.id for s in schemas]},
        )

    def _derive_hierarchy(self, patterns: List[Pattern]) -> Dict[str, List[str]]:
        """Derive hierarchy from pattern relationships."""
        hierarchy: Dict[str, List[str]] = {}

        # Build hierarchy from related patterns
        for pattern in patterns:
            hierarchy[pattern.id] = pattern.related_patterns.copy()

        return hierarchy


class ContradictionResolver:
    """
    SPL Contradiction Resolver - House-Style Differential Diagnosis Engine

    Implements differential diagnosis reasoning:
    - Generate multiple hypotheses
    - Gather supporting and contradicting evidence
    - Propose tests to differentiate
    - Iteratively refine until resolution

    "Everybody lies. The symptoms never lie."

    TODO: Integrate with GPT/Claude for enhanced reasoning
    """

    def __init__(self):
        """Initialize the Contradiction Resolver."""
        self._hypotheses: Dict[str, Hypothesis] = {}
        self._evidence_log: List[Dict[str, Any]] = []
        self._resolution_history: List[Tuple[str, str]] = []
        self._hypothesis_counter: int = 0

    def generate_hypotheses(
        self,
        symptoms: List[str],
        context: Optional[str] = None,
    ) -> List[Hypothesis]:
        """
        SPL Hypothesis Generation

        Generate multiple hypotheses to explain observed symptoms.

        Args:
            symptoms: List of observed symptoms/observations
            context: Optional context for hypothesis generation

        Returns:
            List of generated hypotheses
        """
        hypotheses = []

        # Generate hypotheses based on symptom patterns
        # In production, this would use LLM-based reasoning

        if any("error" in s.lower() or "fail" in s.lower() for s in symptoms):
            self._hypothesis_counter += 1
            h = Hypothesis(
                id=f"hyp_{self._hypothesis_counter}",
                statement="System configuration error causing failures",
                confidence=0.6,
                supporting_evidence=["Error patterns detected"],
                tests_proposed=["Check configuration files", "Review recent changes"],
            )
            hypotheses.append(h)

        if any("slow" in s.lower() or "timeout" in s.lower() for s in symptoms):
            self._hypothesis_counter += 1
            h = Hypothesis(
                id=f"hyp_{self._hypothesis_counter}",
                statement="Resource exhaustion causing performance degradation",
                confidence=0.5,
                supporting_evidence=["Performance symptoms detected"],
                tests_proposed=["Check resource utilization", "Profile bottlenecks"],
            )
            hypotheses.append(h)

        if any("inconsistent" in s.lower() or "random" in s.lower() for s in symptoms):
            self._hypothesis_counter += 1
            h = Hypothesis(
                id=f"hyp_{self._hypothesis_counter}",
                statement="Race condition or timing-dependent behavior",
                confidence=0.4,
                supporting_evidence=["Non-deterministic symptoms detected"],
                tests_proposed=["Add synchronization logging", "Stress test concurrency"],
            )
            hypotheses.append(h)

        # Default hypothesis if no specific patterns match
        if not hypotheses:
            self._hypothesis_counter += 1
            h = Hypothesis(
                id=f"hyp_{self._hypothesis_counter}",
                statement="Unknown condition requiring further investigation",
                confidence=0.3,
                supporting_evidence=symptoms,
                tests_proposed=["Gather more diagnostic data", "Review system logs"],
            )
            hypotheses.append(h)

        for h in hypotheses:
            self._hypotheses[h.id] = h

        return hypotheses

    def add_evidence(
        self,
        hypothesis_id: str,
        evidence: str,
        supports: bool,
    ) -> Hypothesis:
        """
        SPL Evidence Addition

        Add supporting or contradicting evidence to a hypothesis.

        Args:
            hypothesis_id: ID of the hypothesis to update
            evidence: Evidence statement
            supports: Whether evidence supports (True) or contradicts (False)

        Returns:
            Updated hypothesis
        """
        if hypothesis_id not in self._hypotheses:
            raise ValueError(f"Hypothesis {hypothesis_id} not found")

        hypothesis = self._hypotheses[hypothesis_id]

        if supports:
            hypothesis.supporting_evidence.append(evidence)
            # Increase confidence with supporting evidence
            hypothesis.confidence = min(hypothesis.confidence + 0.1, 0.95)
        else:
            hypothesis.contradicting_evidence.append(evidence)
            # Decrease confidence with contradicting evidence
            hypothesis.confidence = max(hypothesis.confidence - 0.15, 0.05)

        self._evidence_log.append({
            "hypothesis_id": hypothesis_id,
            "evidence": evidence,
            "supports": supports,
            "timestamp": datetime.now().isoformat(),
        })

        return hypothesis

    def propose_test(self, hypothesis_id: str) -> List[str]:
        """
        SPL Test Proposal

        Propose tests to differentiate or confirm a hypothesis.

        Args:
            hypothesis_id: ID of the hypothesis to test

        Returns:
            List of proposed tests
        """
        if hypothesis_id not in self._hypotheses:
            return []

        hypothesis = self._hypotheses[hypothesis_id]
        return hypothesis.tests_proposed

    def resolve(self, hypothesis_id: str, resolution: str) -> None:
        """
        SPL Hypothesis Resolution

        Mark a hypothesis as confirmed or rejected.

        Args:
            hypothesis_id: ID of the hypothesis to resolve
            resolution: Either "confirmed" or "rejected"
        """
        if hypothesis_id not in self._hypotheses:
            raise ValueError(f"Hypothesis {hypothesis_id} not found")

        if resolution not in ["confirmed", "rejected"]:
            raise ValueError(f"Resolution must be 'confirmed' or 'rejected'")

        self._hypotheses[hypothesis_id].status = resolution
        self._resolution_history.append((hypothesis_id, resolution))

    def get_ranked_hypotheses(self) -> List[Hypothesis]:
        """
        Get all active hypotheses ranked by confidence.

        Returns:
            List of hypotheses sorted by confidence (descending)
        """
        active = [h for h in self._hypotheses.values() if h.status == "active"]
        return sorted(active, key=lambda h: h.confidence, reverse=True)

    def differential_diagnosis(self, symptoms: List[str]) -> Dict[str, Any]:
        """
        SPL Full Differential Diagnosis

        Run a complete differential diagnosis cycle.

        Args:
            symptoms: List of observed symptoms

        Returns:
            Diagnosis results including hypotheses and recommendations
        """
        # Generate hypotheses
        hypotheses = self.generate_hypotheses(symptoms)

        # Rank by confidence
        ranked = self.get_ranked_hypotheses()

        # Collect all proposed tests
        all_tests = set()
        for h in ranked:
            all_tests.update(h.tests_proposed)

        return {
            "symptoms": symptoms,
            "hypotheses": [
                {
                    "id": h.id,
                    "statement": h.statement,
                    "confidence": h.confidence,
                    "supporting_evidence": h.supporting_evidence,
                    "contradicting_evidence": h.contradicting_evidence,
                }
                for h in ranked
            ],
            "recommended_tests": list(all_tests),
            "most_likely": ranked[0].statement if ranked else "Insufficient data",
        }


class ContextInterpreter:
    """
    SPL Context Interpreter - Multi-Agent Mental Model

    Manages multi-perspective context interpretation:
    - Maintain multiple agent perspectives
    - Share knowledge across contexts
    - Interpret inputs from different viewpoints
    - Synthesize unified understanding

    This mirrors the transformer's persona space simulation.

    TODO: Integrate with GPT/Claude for enhanced context modeling
    """

    def __init__(self):
        """Initialize the Context Interpreter."""
        self._contexts: Dict[str, Context] = {}
        self._active_context: Optional[str] = None

    def create_context(
        self,
        name: str,
        perspective: str,
        agents: List[str],
        shared_knowledge: Optional[Dict[str, Any]] = None,
    ) -> Context:
        """
        SPL Context Creation

        Create a new interpretation context with specified perspective.

        Args:
            name: Context name
            perspective: Primary perspective for this context
            agents: Agents participating in this context
            shared_knowledge: Initial shared knowledge base

        Returns:
            Created context
        """
        context = Context(
            id=f"ctx_{len(self._contexts)}",
            name=name,
            perspective=perspective,
            agents=agents,
            shared_knowledge=shared_knowledge or {},
        )

        self._contexts[context.id] = context
        return context

    def interpret(
        self,
        input_data: str,
        context_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        SPL Context Interpretation

        Interpret input data within a specific context.

        Args:
            input_data: Data to interpret
            context_id: Optional context ID (uses active context if not specified)

        Returns:
            Interpretation results
        """
        ctx_id = context_id or self._active_context

        if ctx_id is None or ctx_id not in self._contexts:
            # Default interpretation without context
            return {
                "input": input_data,
                "interpretation": input_data,
                "perspective": "neutral",
                "confidence": 0.5,
            }

        context = self._contexts[ctx_id]

        # Apply perspective-based interpretation
        interpretation = self._apply_perspective(input_data, context)

        return {
            "input": input_data,
            "interpretation": interpretation,
            "perspective": context.perspective,
            "agents": context.agents,
            "confidence": 0.7,
            "context_id": ctx_id,
        }

    def share_knowledge(
        self,
        context_id: str,
        key: str,
        value: Any,
    ) -> None:
        """
        SPL Knowledge Sharing

        Share knowledge within a context.

        Args:
            context_id: Context to share knowledge in
            key: Knowledge key
            value: Knowledge value
        """
        if context_id not in self._contexts:
            raise ValueError(f"Context {context_id} not found")

        self._contexts[context_id].shared_knowledge[key] = value

    def switch_context(self, context_id: str) -> None:
        """
        Switch to a different active context.

        Args:
            context_id: Context to switch to
        """
        if context_id not in self._contexts:
            raise ValueError(f"Context {context_id} not found")

        self._active_context = context_id

    def get_multi_perspective(
        self,
        input_data: str,
        context_ids: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        SPL Multi-Perspective Analysis

        Get interpretations from multiple context perspectives.

        Args:
            input_data: Data to interpret
            context_ids: Contexts to use (all if not specified)

        Returns:
            List of interpretations from different perspectives
        """
        ids = context_ids or list(self._contexts.keys())

        return [self.interpret(input_data, ctx_id) for ctx_id in ids]

    def _apply_perspective(self, input_data: str, context: Context) -> str:
        """Apply perspective-based transformation to input."""
        # Simple perspective application
        # In production, this would use LLM-based transformation
        perspective_prefix = f"[{context.perspective}] "
        return perspective_prefix + input_data


class ExternalizationAdapter:
    """
    SPL Externalization Adapter - Vim + Absolute-Path CLI Integration

    Provides externalization of cognitive processes through:
    - File-based output with absolute paths
    - Vim-compatible formatting
    - CLI command generation
    - Mind map export

    This is the interface between internal cognition and external tools.

    TODO: Integrate with GPT/Claude for enhanced output generation
    """

    def __init__(self, output_base_path: Optional[Path] = None):
        """
        Initialize the Externalization Adapter.

        Args:
            output_base_path: Base path for file outputs
        """
        self._output_base = output_base_path or Path.cwd()
        self._output_history: List[Dict[str, Any]] = []

    def externalize_pattern(self, pattern: Pattern, output_path: Optional[Path] = None) -> Path:
        """
        SPL Pattern Externalization

        Write a pattern to file in Vim-compatible format.

        Args:
            pattern: Pattern to externalize
            output_path: Optional output path (auto-generated if not specified)

        Returns:
            Absolute path to output file
        """
        if output_path is None:
            output_path = self._output_base / "patterns" / f"{pattern.id}.md"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        content = self._format_pattern_markdown(pattern)

        output_path.write_text(content, encoding="utf-8")

        self._output_history.append({
            "type": "pattern",
            "id": pattern.id,
            "path": str(output_path.absolute()),
            "timestamp": datetime.now().isoformat(),
        })

        return output_path.absolute()

    def externalize_schema(self, schema: Schema, output_path: Optional[Path] = None) -> Path:
        """
        SPL Schema Externalization

        Write a schema to file in Vim-compatible format.

        Args:
            schema: Schema to externalize
            output_path: Optional output path (auto-generated if not specified)

        Returns:
            Absolute path to output file
        """
        if output_path is None:
            output_path = self._output_base / "schemas" / f"{schema.id}.md"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        content = self._format_schema_markdown(schema)

        output_path.write_text(content, encoding="utf-8")

        self._output_history.append({
            "type": "schema",
            "id": schema.id,
            "path": str(output_path.absolute()),
            "timestamp": datetime.now().isoformat(),
        })

        return output_path.absolute()

    def externalize_diagnosis(
        self,
        diagnosis: Dict[str, Any],
        output_path: Optional[Path] = None,
    ) -> Path:
        """
        SPL Diagnosis Externalization

        Write a differential diagnosis to file.

        Args:
            diagnosis: Diagnosis results to externalize
            output_path: Optional output path

        Returns:
            Absolute path to output file
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self._output_base / "diagnoses" / f"diagnosis_{timestamp}.md"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        content = self._format_diagnosis_markdown(diagnosis)

        output_path.write_text(content, encoding="utf-8")

        self._output_history.append({
            "type": "diagnosis",
            "path": str(output_path.absolute()),
            "timestamp": datetime.now().isoformat(),
        })

        return output_path.absolute()

    def generate_cli_command(self, action: str, **kwargs: Any) -> str:
        """
        SPL CLI Command Generation

        Generate a CLI command for an action.

        Args:
            action: Action to perform
            **kwargs: Parameters for the action

        Returns:
            CLI command string
        """
        base_cmd = "sovereign-cognitive"

        if action == "recognize":
            input_file = kwargs.get("input", "-")
            return f"{base_cmd} pattern recognize --input {input_file}"

        elif action == "synthesize":
            patterns = kwargs.get("patterns", [])
            pattern_args = " ".join(f"--pattern {p}" for p in patterns)
            return f"{base_cmd} schema synthesize {pattern_args}"

        elif action == "diagnose":
            symptoms = kwargs.get("symptoms", [])
            symptom_args = " ".join(f"--symptom '{s}'" for s in symptoms)
            return f"{base_cmd} diagnose {symptom_args}"

        elif action == "export":
            output_path = kwargs.get("output", str(self._output_base / "export"))
            return f"{base_cmd} export --output {output_path}"

        return f"{base_cmd} {action}"

    def get_vim_quickfix(self, items: List[Dict[str, Any]]) -> str:
        """
        SPL Vim Quickfix Format

        Generate Vim quickfix format for navigation.

        Args:
            items: Items to include in quickfix list

        Returns:
            Quickfix formatted string
        """
        lines = []
        for item in items:
            path = item.get("path", "")
            line = item.get("line", 1)
            col = item.get("col", 1)
            msg = item.get("message", "")
            lines.append(f"{path}:{line}:{col}: {msg}")
        return "\n".join(lines)

    def _format_list(self, items: List[str]) -> str:
        """
        Format a list of items as markdown bullet points.

        Args:
            items: List of strings to format

        Returns:
            Formatted string with newline-separated bullet points
        """
        if not items:
            return ""
        return "\n".join(f"- {item}" for item in items)

    def _format_pattern_markdown(self, pattern: Pattern) -> str:
        """Format pattern as Markdown."""
        return f"""# Pattern: {pattern.name}

**ID:** {pattern.id}
**Type:** {pattern.type.value}
**Confidence:** {pattern.confidence:.2f} ({pattern.confidence_level().value})
**Created:** {pattern.created_at.isoformat()}

## Description

{pattern.description}

## Source Context

```
{pattern.source_context}
```

## Related Patterns

{self._format_list(pattern.related_patterns) or "None"}

## Metadata

```json
{pattern.metadata}
```
"""

    def _format_schema_markdown(self, schema: Schema) -> str:
        """Format schema as Markdown."""
        patterns_list = "\n".join(
            f"- **{p.name}** ({p.type.value}): {p.description}"
            for p in schema.patterns
        )

        return f"""# Schema: {schema.name}

**ID:** {schema.id}
**Created:** {schema.created_at.isoformat()}

## Description

{schema.description}

## Patterns

{patterns_list}

## Hierarchy

```
{schema.hierarchy}
```

## Constraints

{self._format_list(schema.constraints) or "None"}
"""

    def _format_diagnosis_markdown(self, diagnosis: Dict[str, Any]) -> str:
        """Format diagnosis as Markdown."""
        symptoms = "\n".join(f"- {s}" for s in diagnosis.get("symptoms", []))

        hypotheses_parts = []
        for h in diagnosis.get("hypotheses", []):
            supporting = self._format_list(h.get("supporting_evidence", [])) or "None"
            contradicting = self._format_list(h.get("contradicting_evidence", [])) or "None"
            hypotheses_parts.append(
                f"""### {h.get('statement', 'Unknown')}

**Confidence:** {h.get('confidence', 0):.2f}

**Supporting Evidence:**
{supporting}

**Contradicting Evidence:**
{contradicting}
"""
            )
        hypotheses = "\n".join(hypotheses_parts)

        tests = "\n".join(f"- {t}" for t in diagnosis.get("recommended_tests", []))

        return f"""# Differential Diagnosis Report

## Symptoms

{symptoms}

## Hypotheses

{hypotheses}

## Recommended Tests

{tests}

## Most Likely Diagnosis

**{diagnosis.get('most_likely', 'Unknown')}**
"""


class CognitiveOS:
    """
    SPL Cognitive OS - Unified Interface

    The Cognitive OS integrates all components into a unified
    pattern-dominant cognitive system:

    - Pattern Engine for recognition and synthesis
    - Schema Synthesizer for architecture creation
    - Contradiction Resolver for differential diagnosis
    - Context Interpreter for multi-perspective modeling
    - Externalization Adapter for output generation

    This is the externalization of your cognitive methodology.

    Usage:
        cos = CognitiveOS()
        patterns = cos.recognize("input data")
        schema = cos.create_schema("My Schema", patterns)
        diagnosis = cos.diagnose(["symptom1", "symptom2"])
        cos.export(schema)
    """

    def __init__(self, output_path: Optional[Path] = None):
        """
        Initialize the Cognitive OS.

        Args:
            output_path: Base path for externalized outputs
        """
        self._pattern_engine = PatternEngine()
        self._schema_synthesizer = SchemaSynthesizer(self._pattern_engine)
        self._contradiction_resolver = ContradictionResolver()
        self._context_interpreter = ContextInterpreter()
        self._externalization_adapter = ExternalizationAdapter(output_path)

    @property
    def pattern_engine(self) -> PatternEngine:
        """Access the pattern engine."""
        return self._pattern_engine

    @property
    def schema_synthesizer(self) -> SchemaSynthesizer:
        """Access the schema synthesizer."""
        return self._schema_synthesizer

    @property
    def resolver(self) -> ContradictionResolver:
        """Access the contradiction resolver."""
        return self._contradiction_resolver

    @property
    def interpreter(self) -> ContextInterpreter:
        """Access the context interpreter."""
        return self._context_interpreter

    @property
    def adapter(self) -> ExternalizationAdapter:
        """Access the externalization adapter."""
        return self._externalization_adapter

    def recognize(self, input_data: str, context: Optional[str] = None) -> List[Pattern]:
        """
        Recognize patterns in input data.

        Args:
            input_data: Data to analyze
            context: Optional context

        Returns:
            List of recognized patterns
        """
        return self._pattern_engine.recognize(input_data, context)

    def create_schema(
        self,
        name: str,
        patterns: List[Pattern],
        constraints: Optional[List[str]] = None,
    ) -> Schema:
        """
        Create a schema from patterns.

        Args:
            name: Schema name
            patterns: Patterns to include
            constraints: Optional constraints

        Returns:
            Created schema
        """
        return self._schema_synthesizer.synthesize_schema(name, patterns, constraints)

    def diagnose(self, symptoms: List[str]) -> Dict[str, Any]:
        """
        Run differential diagnosis.

        Args:
            symptoms: Observed symptoms

        Returns:
            Diagnosis results
        """
        return self._contradiction_resolver.differential_diagnosis(symptoms)

    def interpret(
        self,
        input_data: str,
        context_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Interpret input in context.

        Args:
            input_data: Data to interpret
            context_id: Optional context ID

        Returns:
            Interpretation results
        """
        return self._context_interpreter.interpret(input_data, context_id)

    def export(
        self,
        artifact: Any,
        output_path: Optional[Path] = None,
    ) -> Path:
        """
        Export an artifact to file.

        Args:
            artifact: Pattern, Schema, or diagnosis to export
            output_path: Optional output path

        Returns:
            Absolute path to exported file
        """
        if isinstance(artifact, Pattern):
            return self._externalization_adapter.externalize_pattern(artifact, output_path)
        elif isinstance(artifact, Schema):
            return self._externalization_adapter.externalize_schema(artifact, output_path)
        elif isinstance(artifact, dict):
            return self._externalization_adapter.externalize_diagnosis(artifact, output_path)
        else:
            raise TypeError(f"Cannot export artifact of type {type(artifact)}")


# Entry point for module testing
if __name__ == "__main__":
    # Initialize the Cognitive OS
    cos = CognitiveOS()

    # Example: Pattern Recognition
    print("=== Pattern Recognition ===")
    patterns = cos.recognize(
        "The service module handles request-response protocol with nested component hierarchy"
    )
    for p in patterns:
        print(f"  {p.name} ({p.type.value}): {p.confidence:.2f}")

    # Example: Schema Synthesis
    print("\n=== Schema Synthesis ===")
    if patterns:
        schema = cos.create_schema("Service Architecture", patterns)
        print(f"  Created: {schema.name} with {len(schema.patterns)} patterns")

    # Example: Differential Diagnosis
    print("\n=== Differential Diagnosis ===")
    diagnosis = cos.diagnose([
        "Service returns timeout errors intermittently",
        "CPU usage spikes during failures",
        "Random connection drops observed",
    ])
    print(f"  Most likely: {diagnosis['most_likely']}")
    print(f"  Hypotheses: {len(diagnosis['hypotheses'])}")

    print("\n=== Cognitive OS Ready ===")
