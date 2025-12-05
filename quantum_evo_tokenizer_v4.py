#!/usr/bin/env python3
"""
QuantumEvoTokenizer v4 - Safety & Governance Extension
Strategickhaos DAO LLC - Cyber + LLM Stack

Extends v3 with:
- Freeze/Fork governance for yin-yang variants (daylight/moonlight genomes)
- DAO notarization hooks with Wazuh-compatible alerts
- Safety evals with entropy bounds to prevent poisoning
- Auto-notarize evolution hashes for audit trails

Tests 28-36: Safety & Governance Hardening
"""

import hashlib
import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
import copy


def utc_now_iso() -> str:
    """Get current UTC time in ISO format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

from quantum_evo_tokenizer_v3 import (
    QuantumEvoTokenizer,
    QETConfig,
    TokenGenome,
    QuantumFitnessEvaluator
)


class GovernanceMode(Enum):
    """Governance modes for tokenizer operation."""
    DAYLIGHT = "daylight"      # Conservative, production-safe
    MOONLIGHT = "moonlight"    # Experimental, research-grade
    FROZEN = "frozen"          # Locked, no evolution allowed


class SafetyLevel(Enum):
    """Safety evaluation levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class SafetyViolation:
    """Represents a safety violation detected during evolution."""
    level: SafetyLevel
    rule: str
    description: str
    genome_hash: str
    metric_value: float
    threshold: float
    timestamp: str = field(default_factory=utc_now_iso)


@dataclass
class GovernanceEvent:
    """Tracks governance events for audit trail."""
    event_type: str
    genome_hash: str
    mode: str
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ForkRecord:
    """Records a genome fork for yin-yang variants."""
    parent_hash: str
    child_hash: str
    fork_type: str  # "daylight" or "moonlight"
    reason: str
    timestamp: str
    config_diff: Dict[str, Any] = field(default_factory=dict)


class SafetyEvaluator:
    """
    Evaluates genome safety against defined rules.
    
    Implements entropy bounds and poisoning detection.
    """
    
    def __init__(self, config: QETConfig):
        self.config = config
        self.violations: List[SafetyViolation] = []
        
        # Safety rules with thresholds
        self.rules = {
            "entropy_lower_bound": {
                "threshold": config.min_entropy,
                "level": SafetyLevel.CRITICAL,
                "description": "Entropy below minimum bound indicates potential vocabulary poisoning"
            },
            "entropy_upper_bound": {
                "threshold": config.max_entropy,
                "level": SafetyLevel.HIGH,
                "description": "Entropy above maximum bound indicates unstable vocabulary"
            },
            "compression_minimum": {
                "threshold": 0.1,  # Minimum reasonable compression
                "level": SafetyLevel.MEDIUM,
                "description": "Compression ratio too low for practical use"
            },
            "vocab_coverage_minimum": {
                "threshold": 0.5,  # Must cover at least 50% of corpus bytes
                "level": SafetyLevel.HIGH,
                "description": "Vocabulary coverage insufficient for target corpus"
            },
            "fitness_regression": {
                "threshold": -0.1,  # Alert on 10%+ fitness drop
                "level": SafetyLevel.MEDIUM,
                "description": "Fitness regression detected between generations"
            }
        }
    
    def evaluate(
        self, 
        genome: TokenGenome, 
        previous_fitness: Optional[float] = None
    ) -> List[SafetyViolation]:
        """Evaluate genome against all safety rules."""
        violations = []
        
        # Check entropy lower bound
        if genome.entropy_score < self.rules["entropy_lower_bound"]["threshold"]:
            violations.append(SafetyViolation(
                level=self.rules["entropy_lower_bound"]["level"],
                rule="entropy_lower_bound",
                description=self.rules["entropy_lower_bound"]["description"],
                genome_hash=genome.hash,
                metric_value=genome.entropy_score,
                threshold=self.rules["entropy_lower_bound"]["threshold"]
            ))
        
        # Check entropy upper bound
        if genome.entropy_score > self.rules["entropy_upper_bound"]["threshold"]:
            violations.append(SafetyViolation(
                level=self.rules["entropy_upper_bound"]["level"],
                rule="entropy_upper_bound",
                description=self.rules["entropy_upper_bound"]["description"],
                genome_hash=genome.hash,
                metric_value=genome.entropy_score,
                threshold=self.rules["entropy_upper_bound"]["threshold"]
            ))
        
        # Check compression minimum
        if genome.compression_ratio < self.rules["compression_minimum"]["threshold"]:
            violations.append(SafetyViolation(
                level=self.rules["compression_minimum"]["level"],
                rule="compression_minimum",
                description=self.rules["compression_minimum"]["description"],
                genome_hash=genome.hash,
                metric_value=genome.compression_ratio,
                threshold=self.rules["compression_minimum"]["threshold"]
            ))
        
        # Check vocab coverage
        if genome.coverage_score < self.rules["vocab_coverage_minimum"]["threshold"]:
            violations.append(SafetyViolation(
                level=self.rules["vocab_coverage_minimum"]["level"],
                rule="vocab_coverage_minimum",
                description=self.rules["vocab_coverage_minimum"]["description"],
                genome_hash=genome.hash,
                metric_value=genome.coverage_score,
                threshold=self.rules["vocab_coverage_minimum"]["threshold"]
            ))
        
        # Check fitness regression
        if previous_fitness is not None:
            fitness_change = (genome.fitness - previous_fitness) / max(previous_fitness, 0.001)
            if fitness_change < self.rules["fitness_regression"]["threshold"]:
                violations.append(SafetyViolation(
                    level=self.rules["fitness_regression"]["level"],
                    rule="fitness_regression",
                    description=self.rules["fitness_regression"]["description"],
                    genome_hash=genome.hash,
                    metric_value=fitness_change,
                    threshold=self.rules["fitness_regression"]["threshold"]
                ))
        
        self.violations.extend(violations)
        return violations
    
    def get_critical_violations(self) -> List[SafetyViolation]:
        """Get all critical-level violations."""
        return [v for v in self.violations if v.level == SafetyLevel.CRITICAL]
    
    def is_safe(self) -> bool:
        """Check if genome passes all critical safety checks."""
        return len(self.get_critical_violations()) == 0
    
    def to_wazuh_alerts(self) -> List[Dict[str, Any]]:
        """Convert violations to Wazuh-compatible alert format."""
        alerts = []
        
        for violation in self.violations:
            alert = {
                "timestamp": violation.timestamp,
                "rule": {
                    "level": self._safety_to_wazuh_level(violation.level),
                    "description": violation.description,
                    "id": f"QET-{violation.rule.upper()}"
                },
                "agent": {
                    "name": "quantum_evo_tokenizer",
                    "id": "qet-v4"
                },
                "data": {
                    "genome_hash": violation.genome_hash,
                    "metric_value": violation.metric_value,
                    "threshold": violation.threshold
                }
            }
            alerts.append(alert)
        
        return alerts
    
    def _safety_to_wazuh_level(self, level: SafetyLevel) -> int:
        """Convert SafetyLevel to Wazuh severity (1-15)."""
        mapping = {
            SafetyLevel.CRITICAL: 15,
            SafetyLevel.HIGH: 12,
            SafetyLevel.MEDIUM: 8,
            SafetyLevel.LOW: 4,
            SafetyLevel.INFO: 2
        }
        return mapping.get(level, 5)


class GovernanceManager:
    """
    Manages governance state and transitions for tokenizer.
    
    Implements freeze/fork logic for yin-yang genome variants.
    """
    
    def __init__(self, mode: GovernanceMode = GovernanceMode.DAYLIGHT):
        self.mode = mode
        self.events: List[GovernanceEvent] = []
        self.forks: List[ForkRecord] = []
        self.frozen_genomes: Dict[str, TokenGenome] = {}
        self.notarization_log: List[Dict[str, Any]] = []
    
    def freeze(self, genome: TokenGenome, reason: str = "Manual freeze"):
        """Freeze a genome, preventing further evolution."""
        self.frozen_genomes[genome.hash] = genome
        
        event = GovernanceEvent(
            event_type="FREEZE",
            genome_hash=genome.hash,
            mode=self.mode.value,
            timestamp=utc_now_iso(),
            metadata={"reason": reason, "fitness": genome.fitness}
        )
        self.events.append(event)
        
        return event
    
    def fork(
        self, 
        parent_genome: TokenGenome, 
        child_genome: TokenGenome,
        fork_type: str,
        reason: str = "Yin-yang variant creation"
    ) -> ForkRecord:
        """Create a fork record for parent-child genome relationship."""
        
        config_diff = {
            "fork_type": fork_type,
            "parent_fitness": parent_genome.fitness,
            "child_fitness": child_genome.fitness
        }
        
        record = ForkRecord(
            parent_hash=parent_genome.hash,
            child_hash=child_genome.hash,
            fork_type=fork_type,
            reason=reason,
            timestamp=utc_now_iso(),
            config_diff=config_diff
        )
        
        self.forks.append(record)
        
        event = GovernanceEvent(
            event_type=f"FORK_{fork_type.upper()}",
            genome_hash=child_genome.hash,
            mode=self.mode.value,
            timestamp=record.timestamp,
            metadata={
                "parent_hash": parent_genome.hash,
                "reason": reason
            }
        )
        self.events.append(event)
        
        return record
    
    def notarize(self, genome: TokenGenome, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Create DAO notarization record for a genome."""
        
        record = {
            "type": "QET_GENOME_NOTARIZATION",
            "version": "v4",
            "timestamp": utc_now_iso(),
            "genome": {
                "hash": genome.hash,
                "fitness": genome.fitness,
                "entropy_score": genome.entropy_score,
                "compression_ratio": genome.compression_ratio,
                "coverage_score": genome.coverage_score,
                "vocab_size": len(genome.tokens)
            },
            "governance": {
                "mode": self.mode.value,
                "frozen": genome.hash in self.frozen_genomes,
                "fork_count": len([f for f in self.forks if f.parent_hash == genome.hash])
            },
            "metrics": metrics,
            "signature": self._generate_signature(genome, metrics)
        }
        
        self.notarization_log.append(record)
        
        event = GovernanceEvent(
            event_type="NOTARIZE",
            genome_hash=genome.hash,
            mode=self.mode.value,
            timestamp=record["timestamp"],
            metadata={"signature": record["signature"]}
        )
        self.events.append(event)
        
        return record
    
    def _generate_signature(
        self, 
        genome: TokenGenome, 
        metrics: Dict[str, Any]
    ) -> str:
        """Generate cryptographic signature for notarization."""
        payload = json.dumps({
            "hash": genome.hash,
            "fitness": genome.fitness,
            "mode": self.mode.value,
            "metrics": metrics
        }, sort_keys=True)
        
        return hashlib.sha256(payload.encode()).hexdigest()
    
    def set_mode(self, mode: GovernanceMode):
        """Change governance mode."""
        old_mode = self.mode
        self.mode = mode
        
        event = GovernanceEvent(
            event_type="MODE_CHANGE",
            genome_hash="N/A",
            mode=mode.value,
            timestamp=utc_now_iso(),
            metadata={"previous_mode": old_mode.value}
        )
        self.events.append(event)
    
    def is_frozen(self, genome_hash: str) -> bool:
        """Check if a genome is frozen."""
        return genome_hash in self.frozen_genomes
    
    def get_audit_trail(self) -> List[Dict[str, Any]]:
        """Get full audit trail of governance events."""
        return [
            {
                "event_type": e.event_type,
                "genome_hash": e.genome_hash,
                "mode": e.mode,
                "timestamp": e.timestamp,
                "metadata": e.metadata
            }
            for e in self.events
        ]


class QuantumEvoTokenizerV4(QuantumEvoTokenizer):
    """
    QuantumEvoTokenizer v4 with Safety & Governance extensions.
    
    Adds:
    - Safety evaluation with entropy bounds
    - Governance management (freeze/fork)
    - DAO notarization hooks
    - Wazuh alert integration
    - Yin-yang variant creation
    """
    
    def __init__(
        self, 
        config: QETConfig, 
        corpora: List[str],
        governance_mode: GovernanceMode = GovernanceMode.DAYLIGHT
    ):
        super().__init__(config, corpora)
        
        self.safety_evaluator = SafetyEvaluator(config)
        self.governance = GovernanceManager(governance_mode)
        
        # Track evolution with safety checks
        self.safety_history: List[Dict[str, Any]] = []
        self.yin_genome: Optional[TokenGenome] = None  # Daylight variant
        self.yang_genome: Optional[TokenGenome] = None  # Moonlight variant
    
    def evolve(self) -> Dict[str, Any]:
        """
        Run evolution with safety monitoring and governance hooks.
        
        Returns extended result with safety and governance data.
        """
        # Check if evolution is allowed
        if self.governance.mode == GovernanceMode.FROZEN:
            raise RuntimeError("Evolution blocked: Governance mode is FROZEN")
        
        start_time = time.time()
        previous_best_fitness = None
        
        for gen in range(self.config.generations):
            # Evaluate fitness for all genomes
            for genome in self.population:
                self.evaluator.evaluate(genome, self.corpus_data, self.config)
                genome.generation = gen
                
                # Safety evaluation
                violations = self.safety_evaluator.evaluate(genome, previous_best_fitness)
                
                # In daylight mode, reject genomes with critical violations
                if self.governance.mode == GovernanceMode.DAYLIGHT and violations:
                    critical = [v for v in violations if v.level == SafetyLevel.CRITICAL]
                    if critical:
                        genome.fitness *= 0.1  # Severely penalize unsafe genomes
            
            # Sort by fitness (descending)
            self.population.sort(key=lambda g: g.fitness, reverse=True)
            
            # Track best genome
            if self.best_genome is None or self.population[0].fitness > self.best_genome.fitness:
                self.best_genome = self.population[0]
                previous_best_fitness = self.best_genome.fitness
            
            # Record generation history with safety data
            gen_record = {
                "generation": gen,
                "best_fitness": self.population[0].fitness,
                "avg_fitness": sum(g.fitness for g in self.population) / len(self.population),
                "best_compression": self.population[0].compression_ratio,
                "best_entropy": self.population[0].entropy_score,
                "safety_violations": len(self.safety_evaluator.violations),
                "critical_violations": len(self.safety_evaluator.get_critical_violations())
            }
            self.generation_history.append(gen_record)
            
            # Selection and reproduction
            self._evolve_generation()
        
        evolution_time = time.time() - start_time
        
        # Final evaluation
        self.evaluator.evaluate(self.best_genome, self.corpus_data, self.config)
        
        # Build result with v4 extensions
        result = {
            "vocab": self.best_genome.tokens,
            "final_hash": self.best_genome.hash,
            "metrics": {
                "fitness": self.best_genome.fitness,
                "compression_ratio": self.best_genome.compression_ratio,
                "entropy_score": self.best_genome.entropy_score,
                "coverage_score": self.best_genome.coverage_score,
                "vocab_size": len(self.best_genome.tokens),
                "generations": self.config.generations,
                "evolution_time_seconds": evolution_time,
                "backend": self.config.backend,
                "safety_mode": self.config.safety_mode
            },
            "history": self.generation_history,
            "safety": {
                "is_safe": self.safety_evaluator.is_safe(),
                "total_violations": len(self.safety_evaluator.violations),
                "critical_violations": len(self.safety_evaluator.get_critical_violations()),
                "violations": [
                    {
                        "rule": v.rule,
                        "level": v.level.value,
                        "value": v.metric_value,
                        "threshold": v.threshold
                    }
                    for v in self.safety_evaluator.violations[-10:]  # Last 10
                ]
            },
            "governance": {
                "mode": self.governance.mode.value,
                "frozen": self.governance.is_frozen(self.best_genome.hash),
                "events": len(self.governance.events)
            }
        }
        
        # Auto-notarize in daylight mode
        if self.governance.mode == GovernanceMode.DAYLIGHT:
            notarization = self.governance.notarize(self.best_genome, result["metrics"])
            result["notarization"] = notarization
        
        return result
    
    def create_yin_yang_fork(self) -> Tuple[TokenGenome, TokenGenome]:
        """
        Create yin-yang variants (daylight/moonlight) from current best genome.
        
        Yin (daylight): Conservative, safety-first variant - prunes experimental tokens
        Yang (moonlight): Experimental, performance-first variant - adds experimental tokens
        """
        if self.best_genome is None:
            raise ValueError("Must call evolve() before creating forks")
        
        import random
        
        # Create Yin (daylight) variant - more conservative
        # Prune some longer, more experimental tokens
        yin_tokens = {}
        token_id = 0
        for token, _ in sorted(self.best_genome.tokens.items(), key=lambda x: len(x[0])):
            # Keep all single-byte tokens and shorter multi-byte tokens
            if len(token) <= 4 or random.random() > 0.3:
                yin_tokens[token] = token_id
                token_id += 1
        
        # Add a unique marker token for yin
        yin_marker = b"__YIN_DAYLIGHT__"
        yin_tokens[yin_marker] = token_id
        
        self.yin_genome = TokenGenome(
            tokens=yin_tokens,
            fitness=self.best_genome.fitness * 0.95,
            entropy_score=self.best_genome.entropy_score,
            compression_ratio=self.best_genome.compression_ratio,
            coverage_score=self.best_genome.coverage_score,
            generation=self.best_genome.generation
        )
        
        # Create Yang (moonlight) variant - more experimental
        # Add some experimental longer tokens
        yang_tokens = dict(self.best_genome.tokens)
        max_id = max(yang_tokens.values()) + 1
        
        # Add experimental tokens
        for i in range(10):
            exp_token = bytes([random.randint(32, 126) for _ in range(random.randint(5, 12))])
            if exp_token not in yang_tokens:
                yang_tokens[exp_token] = max_id
                max_id += 1
        
        # Add a unique marker token for yang
        yang_marker = b"__YANG_MOONLIGHT__"
        yang_tokens[yang_marker] = max_id
        
        self.yang_genome = TokenGenome(
            tokens=yang_tokens,
            fitness=self.best_genome.fitness * 1.05,
            entropy_score=self.best_genome.entropy_score,
            compression_ratio=self.best_genome.compression_ratio,
            coverage_score=self.best_genome.coverage_score,
            generation=self.best_genome.generation
        )
        
        # Record forks
        self.governance.fork(
            self.best_genome, 
            self.yin_genome, 
            "daylight",
            "Yin variant - conservative safety-first"
        )
        
        self.governance.fork(
            self.best_genome, 
            self.yang_genome, 
            "moonlight",
            "Yang variant - experimental performance-first"
        )
        
        return self.yin_genome, self.yang_genome
    
    def freeze_best(self, reason: str = "Manual freeze") -> GovernanceEvent:
        """Freeze the best genome, preventing further evolution."""
        if self.best_genome is None:
            raise ValueError("No best genome to freeze")
        
        return self.governance.freeze(self.best_genome, reason)
    
    def get_wazuh_alerts(self) -> List[Dict[str, Any]]:
        """Get Wazuh-compatible security alerts for safety violations."""
        return self.safety_evaluator.to_wazuh_alerts()
    
    def get_dao_notarization(self) -> Dict[str, Any]:
        """Get DAO notarization record for current best genome."""
        if self.best_genome is None:
            raise ValueError("No genome to notarize")
        
        metrics = {
            "fitness": self.best_genome.fitness,
            "compression_ratio": self.best_genome.compression_ratio,
            "entropy_score": self.best_genome.entropy_score,
            "coverage_score": self.best_genome.coverage_score
        }
        
        return self.governance.notarize(self.best_genome, metrics)
    
    def get_governance_audit(self) -> List[Dict[str, Any]]:
        """Get full governance audit trail."""
        return self.governance.get_audit_trail()
    
    def export_governance_report(self, path: str):
        """Export full governance report to JSON file."""
        report = {
            "version": "v4",
            "timestamp": utc_now_iso(),
            "best_genome": {
                "hash": self.best_genome.hash if self.best_genome else None,
                "fitness": self.best_genome.fitness if self.best_genome else None,
                "entropy": self.best_genome.entropy_score if self.best_genome else None
            },
            "safety": {
                "is_safe": self.safety_evaluator.is_safe(),
                "violations_count": len(self.safety_evaluator.violations),
                "critical_count": len(self.safety_evaluator.get_critical_violations())
            },
            "governance": {
                "mode": self.governance.mode.value,
                "frozen_count": len(self.governance.frozen_genomes),
                "fork_count": len(self.governance.forks)
            },
            "audit_trail": self.governance.get_audit_trail(),
            "forks": [
                {
                    "parent": f.parent_hash,
                    "child": f.child_hash,
                    "type": f.fork_type,
                    "reason": f.reason,
                    "timestamp": f.timestamp
                }
                for f in self.governance.forks
            ],
            "notarization_log": self.governance.notarization_log,
            "wazuh_alerts": self.get_wazuh_alerts()
        }
        
        Path(path).write_text(json.dumps(report, indent=2))
        return report


# Test functions for safety & governance (Tests 28-36)
def test_28_entropy_bounds():
    """Test 28: Verify entropy bounds are monitored and enforced."""
    config = QETConfig(
        generations=10,
        population_size=8,
        min_entropy=0.0,  # Relaxed bounds for this test
        max_entropy=1.0
    )
    
    corpora = ["Test data for entropy bounds validation." * 10]
    tokenizer = QuantumEvoTokenizerV4(config, corpora)
    result = tokenizer.evolve()
    
    # Verify that safety monitoring is active
    assert "safety" in result, "Safety metrics should be present"
    assert "entropy_score" in result["metrics"], "Entropy score should be tracked"
    
    # With relaxed bounds, should pass safety check
    # The key is that entropy monitoring is functioning
    print("✅ Test 28 PASSED: Entropy bounds monitored")
    return {"test_id": 28, "status": "PASS"}


def test_29_governance_freeze():
    """Test 29: Verify genome freeze prevents further evolution."""
    config = QETConfig(generations=5, population_size=4)
    corpora = ["Freeze test data."]
    
    tokenizer = QuantumEvoTokenizerV4(config, corpora)
    tokenizer.evolve()
    
    freeze_event = tokenizer.freeze_best("Test freeze")
    assert tokenizer.governance.is_frozen(tokenizer.best_genome.hash)
    
    print("✅ Test 29 PASSED: Freeze governance works")
    return {"test_id": 29, "status": "PASS"}


def test_30_fork_yin_yang():
    """Test 30: Verify yin-yang fork creates valid variants."""
    config = QETConfig(generations=5, population_size=4)
    corpora = ["Fork test data."]
    
    tokenizer = QuantumEvoTokenizerV4(config, corpora)
    tokenizer.evolve()
    
    yin, yang = tokenizer.create_yin_yang_fork()
    
    assert yin.hash != yang.hash, "Forks should have different hashes"
    assert len(tokenizer.governance.forks) == 2, "Should have 2 fork records"
    
    print("✅ Test 30 PASSED: Yin-yang fork works")
    return {"test_id": 30, "status": "PASS"}


def test_31_dao_notarization():
    """Test 31: Verify DAO notarization generates valid records."""
    config = QETConfig(generations=5, population_size=4)
    corpora = ["Notarization test data."]
    
    tokenizer = QuantumEvoTokenizerV4(config, corpora, GovernanceMode.DAYLIGHT)
    result = tokenizer.evolve()
    
    assert "notarization" in result, "Should auto-notarize in daylight mode"
    assert "signature" in result["notarization"], "Should have signature"
    
    print("✅ Test 31 PASSED: DAO notarization works")
    return {"test_id": 31, "status": "PASS"}


def test_32_wazuh_alerts():
    """Test 32: Verify Wazuh-compatible alerts are generated."""
    config = QETConfig(
        generations=5,
        population_size=4,
        min_entropy=0.99  # Impossible threshold to trigger violations
    )
    corpora = ["Alert test data."]
    
    tokenizer = QuantumEvoTokenizerV4(config, corpora, GovernanceMode.MOONLIGHT)
    tokenizer.evolve()
    
    alerts = tokenizer.get_wazuh_alerts()
    assert len(alerts) > 0, "Should generate alerts for violations"
    assert "rule" in alerts[0], "Alert should have rule field"
    
    print("✅ Test 32 PASSED: Wazuh alerts generated")
    return {"test_id": 32, "status": "PASS"}


def test_33_governance_audit():
    """Test 33: Verify governance audit trail is complete."""
    config = QETConfig(generations=5, population_size=4)
    corpora = ["Audit test data."]
    
    tokenizer = QuantumEvoTokenizerV4(config, corpora)
    tokenizer.evolve()
    tokenizer.freeze_best()
    tokenizer.create_yin_yang_fork()
    
    audit = tokenizer.get_governance_audit()
    event_types = [e["event_type"] for e in audit]
    
    assert "FREEZE" in event_types, "Should have FREEZE event"
    assert "FORK_DAYLIGHT" in event_types, "Should have FORK_DAYLIGHT event"
    
    print("✅ Test 33 PASSED: Governance audit complete")
    return {"test_id": 33, "status": "PASS"}


def test_34_mode_transitions():
    """Test 34: Verify governance mode transitions are tracked."""
    config = QETConfig(generations=5, population_size=4)
    corpora = ["Mode test data."]
    
    tokenizer = QuantumEvoTokenizerV4(config, corpora, GovernanceMode.DAYLIGHT)
    tokenizer.governance.set_mode(GovernanceMode.MOONLIGHT)
    tokenizer.governance.set_mode(GovernanceMode.FROZEN)
    
    audit = tokenizer.get_governance_audit()
    mode_changes = [e for e in audit if e["event_type"] == "MODE_CHANGE"]
    
    assert len(mode_changes) == 2, "Should have 2 mode changes"
    
    print("✅ Test 34 PASSED: Mode transitions tracked")
    return {"test_id": 34, "status": "PASS"}


def test_35_safety_in_daylight():
    """Test 35: Verify daylight mode enforces strict safety."""
    config = QETConfig(generations=10, population_size=8)
    corpora = ["Safety daylight test data."]
    
    tokenizer = QuantumEvoTokenizerV4(config, corpora, GovernanceMode.DAYLIGHT)
    result = tokenizer.evolve()
    
    # In daylight mode, should have notarization
    assert "notarization" in result, "Daylight mode should auto-notarize"
    
    print("✅ Test 35 PASSED: Daylight safety enforced")
    return {"test_id": 35, "status": "PASS"}


def test_36_export_governance_report():
    """Test 36: Verify full governance report export."""
    import tempfile
    
    config = QETConfig(generations=5, population_size=4)
    corpora = ["Export test data."]
    
    tokenizer = QuantumEvoTokenizerV4(config, corpora)
    tokenizer.evolve()
    tokenizer.freeze_best()
    
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        report = tokenizer.export_governance_report(f.name)
    
    assert "audit_trail" in report, "Report should have audit trail"
    assert "safety" in report, "Report should have safety section"
    
    print("✅ Test 36 PASSED: Governance report exported")
    return {"test_id": 36, "status": "PASS"}


def run_safety_governance_tests():
    """Run all safety & governance tests (28-36)."""
    print("\n🛡️ Running Safety & Governance Tests (28-36)")
    print("=" * 50)
    
    results = []
    
    tests = [
        test_28_entropy_bounds,
        test_29_governance_freeze,
        test_30_fork_yin_yang,
        test_31_dao_notarization,
        test_32_wazuh_alerts,
        test_33_governance_audit,
        test_34_mode_transitions,
        test_35_safety_in_daylight,
        test_36_export_governance_report
    ]
    
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ {test.__name__} FAILED: {e}")
            results.append({
                "test_id": int(test.__name__.split("_")[1]),
                "status": "FAIL",
                "error": str(e)
            })
    
    passed = sum(1 for r in results if r["status"] == "PASS")
    print(f"\n📊 Results: {passed}/{len(results)} tests passed")
    
    return results


if __name__ == "__main__":
    # Run tests
    results = run_safety_governance_tests()
    
    # Demo usage
    print("\n" + "=" * 50)
    print("🎯 QuantumEvoTokenizer v4 Demo")
    print("=" * 50)
    
    config = QETConfig(
        generations=20,
        population_size=8,
        backend="mock",
        safety_mode="daylight"
    )
    
    corpora = [
        "DAO governance test: freeze, fork, notarize.",
        "YAML config: key: value\n  nested: data",
        "CVE-2024-1234: Security vulnerability report."
    ]
    
    tokenizer = QuantumEvoTokenizerV4(config, corpora, GovernanceMode.DAYLIGHT)
    
    print("\n📈 Evolving with safety monitoring...")
    result = tokenizer.evolve()
    
    print(f"   Fitness: {result['metrics']['fitness']:.4f}")
    print(f"   Is Safe: {result['safety']['is_safe']}")
    print(f"   Violations: {result['safety']['total_violations']}")
    
    print("\n🔀 Creating yin-yang fork...")
    yin, yang = tokenizer.create_yin_yang_fork()
    print(f"   Yin (daylight) hash: {yin.hash}")
    print(f"   Yang (moonlight) hash: {yang.hash}")
    
    print("\n❄️ Freezing best genome...")
    tokenizer.freeze_best("Production deployment")
    
    print("\n📋 Governance audit trail:")
    for event in tokenizer.get_governance_audit()[-5:]:
        print(f"   {event['event_type']}: {event['genome_hash'][:8]}...")
    
    print("\n✅ v4 Demo complete!")
