#!/usr/bin/env python3
"""
Legal Synthesizer Evolution Engine (LSEE) v1.0

An evolutionary algorithm that generates and refines legal compliance strategies
for private investigation, OSINT, and background check operations.

This system:
- Evolves strategies across generations using genetic algorithms
- Validates every strategy against US legal codes
- Maintains a JSONL audit ledger for compliance tracking
- Supports multiple strategy types (OSINT, background checks, skip tracing)
"""

import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field, asdict


# ============================================================================
# US Legal Codes Database
# ============================================================================

US_CODES: List[str] = [
    # Privacy & Consumer Protection
    "15 U.S.C. § 1681 et seq. (Fair Credit Reporting Act - FCRA)",
    "15 U.S.C. § 6801 et seq. (Gramm-Leach-Bliley Act - GLBA)",
    "15 U.S.C. § 45 (FTC Act - Unfair/Deceptive Practices)",
    
    # Electronic Communications & Wiretapping
    "18 U.S.C. § 2510 et seq. (Wiretap Act)",
    "18 U.S.C. § 2701 et seq. (Stored Communications Act - SCA)",
    "18 U.S.C. § 2702 (Voluntary disclosure of customer communications)",
    "18 U.S.C. § 2703 (Required disclosure of customer communications)",
    
    # Computer Fraud & Abuse
    "18 U.S.C. § 1030 (Computer Fraud and Abuse Act - CFAA)",
    "18 U.S.C. § 1029 (Fraud with access devices)",
    
    # Identity & Fraud
    "18 U.S.C. § 1028 (Fraud and related activity with identification documents)",
    "18 U.S.C. § 1028A (Aggravated identity theft)",
    "18 U.S.C. § 1343 (Wire fraud)",
    
    # Harassment & Stalking
    "18 U.S.C. § 2261A (Stalking)",
    "47 U.S.C. § 223 (Obscene or harassing telephone calls)",
    
    # Privacy Rights
    "5 U.S.C. § 552a (Privacy Act of 1974)",
    "42 U.S.C. § 2000aa (Privacy Protection Act)",
    
    # State Laws (General References)
    "State Data Breach Notification Laws (All 50 States)",
    "State Consumer Privacy Laws (e.g., CCPA, CPRA)",
    "State Licensing Requirements for Private Investigators",
    "State Anti-SLAPP Statutes",
    
    # Regulatory Frameworks
    "16 C.F.R. Part 314 (FTC Safeguards Rule)",
    "16 C.F.R. Part 682 (FTC Disposal Rule)",
    
    # Public Records & FOIA
    "5 U.S.C. § 552 (Freedom of Information Act - FOIA)",
    "State Public Records Acts (Sunshine Laws)",
    
    # Employment & Background Checks
    "29 U.S.C. § 2001 et seq. (Employee Polygraph Protection Act)",
    "42 U.S.C. § 12111 et seq. (Americans with Disabilities Act - ADA)",
    "State Ban-the-Box Laws",
    
    # Telecommunications
    "47 U.S.C. § 222 (Customer Proprietary Network Information)",
    
    # Banking & Financial
    "12 U.S.C. § 3401 et seq. (Right to Financial Privacy Act)",
    
    # Video Privacy
    "18 U.S.C. § 2710 (Video Privacy Protection Act)",
]


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class LegalStrategy:
    """Represents a legal compliance strategy for investigation operations."""
    approach: str
    generation: int = 0
    strategy_type: str = "generic"
    id: str = field(default_factory=lambda: f"strategy_{datetime.now(timezone.utc).timestamp()}_{random.randint(1000, 9999)}")
    fitness: float = 0.0
    compliance_verified: bool = False
    verification_ledger: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert strategy to dictionary for serialization."""
        return asdict(self)


# ============================================================================
# Legal Compliance Judge
# ============================================================================

class LegalComplianceJudge:
    """
    Simulates a compliance review by checking strategies against known legal codes.
    
    Note: This is a heuristic-based system using keyword matching and pattern analysis.
    It is NOT a substitute for actual legal counsel.
    """
    
    def __init__(self, us_codes: List[str]):
        self.us_codes = us_codes
        self.prohibited_keywords = [
            "hack", "breach", "unauthorized access", "pretexting", "impersonation",
            "bribe", "wiretap", "intercept communications", "steal", "break into",
            "falsify", "forge", "deceive", "social engineering attack", "exploit vulnerability"
        ]
        self.required_phrases = [
            "lawful", "authorized", "consent", "public record", "legitimate purpose",
            "permissible purpose", "FCRA-compliant", "licensed", "legal authority"
        ]
    
    def evaluate_compliance(self, strategy: LegalStrategy) -> Tuple[bool, float, List[str]]:
        """
        Evaluate a strategy for legal compliance.
        
        Returns:
            Tuple of (is_compliant, compliance_score, violations)
        """
        violations = []
        score = 100.0
        approach_lower = strategy.approach.lower()
        
        # Check for prohibited keywords
        for keyword in self.prohibited_keywords:
            if keyword in approach_lower:
                violations.append(f"Contains prohibited activity: '{keyword}'")
                score -= 15.0
        
        # Check for required compliance phrases
        has_required = any(phrase in approach_lower for phrase in self.required_phrases)
        if not has_required:
            violations.append("Missing explicit compliance language")
            score -= 10.0
        
        # Bonus for mentioning specific legal codes
        for code in self.us_codes[:10]:  # Check top 10 most relevant codes
            code_ref = code.split("(")[0].strip()
            if code_ref.lower() in approach_lower:
                score += 5.0
        
        # Check strategy-specific compliance
        if strategy.strategy_type == "background_check":
            if "fcra" not in approach_lower and "fair credit reporting" not in approach_lower:
                violations.append("Background check strategy must reference FCRA compliance")
                score -= 20.0
        
        if strategy.strategy_type == "osint":
            if "public" not in approach_lower and "publicly available" not in approach_lower:
                violations.append("OSINT strategy must emphasize public sources")
                score -= 15.0
        
        # Ensure score is within bounds
        score = max(0.0, min(100.0, score))
        is_compliant = score >= 60.0 and len(violations) == 0
        
        return is_compliant, score, violations
    
    def verify_strategy(self, strategy: LegalStrategy) -> LegalStrategy:
        """Verify a strategy and update its compliance status."""
        is_compliant, score, violations = self.evaluate_compliance(strategy)
        
        strategy.compliance_verified = is_compliant
        strategy.fitness = score
        strategy.verification_ledger.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "compliant": is_compliant,
            "score": score,
            "violations": violations,
            "codes_checked": len(self.us_codes)
        })
        
        return strategy


# ============================================================================
# Evolutionary Engine
# ============================================================================

class LegalEvolutionEngine:
    """
    Genetic algorithm engine for evolving legal compliance strategies.
    """
    
    def __init__(self, judge: LegalComplianceJudge, population_size: int = 10,
                 mutation_rate: float = 0.3, generations: int = 5):
        self.judge = judge
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.population: List[LegalStrategy] = []
        self.ledger_path = Path("legal_evolution_ledger.jsonl")
    
    def seed_population(self, base_strategies: List[LegalStrategy]):
        """Initialize the population with base strategies."""
        self.population = base_strategies.copy()
        
        # Verify initial population
        for strategy in self.population:
            self.judge.verify_strategy(strategy)
            self._log_to_ledger(strategy, "seed")
    
    def crossover(self, parent1: LegalStrategy, parent2: LegalStrategy) -> LegalStrategy:
        """
        Create offspring by combining two parent strategies.
        """
        # Split approaches into sentences
        sentences1 = [s.strip() for s in parent1.approach.split('.') if s.strip()]
        sentences2 = [s.strip() for s in parent2.approach.split('.') if s.strip()]
        
        # Randomly select sentences from both parents
        num_sentences = min(len(sentences1) + len(sentences2), random.randint(3, 6))
        combined = []
        
        for _ in range(num_sentences):
            if random.random() < 0.5 and sentences1:
                combined.append(sentences1.pop(random.randrange(len(sentences1))))
            elif sentences2:
                combined.append(sentences2.pop(random.randrange(len(sentences2))))
        
        offspring_approach = '. '.join(combined) + '.'
        
        # Inherit strategy type from fitter parent
        strategy_type = parent1.strategy_type if parent1.fitness > parent2.fitness else parent2.strategy_type
        
        return LegalStrategy(
            approach=offspring_approach,
            generation=max(parent1.generation, parent2.generation) + 1,
            strategy_type=strategy_type
        )
    
    def mutate(self, strategy: LegalStrategy) -> LegalStrategy:
        """
        Apply mutation to a strategy by adding compliance-focused improvements.
        """
        if random.random() > self.mutation_rate:
            return strategy
        
        compliance_boosters = [
            "All activities conducted with proper authorization and documented consent.",
            "Strict adherence to FCRA permissible purposes for consumer reports.",
            "Exclusive use of publicly available information sources.",
            "Full compliance with state licensing requirements for private investigators.",
            "Verification of all data sources against legal access standards.",
            "Documentation of lawful basis for each information request.",
            "Regular compliance audits and legal review of procedures.",
        ]
        
        # Add a random compliance booster
        booster = random.choice(compliance_boosters)
        mutated_approach = strategy.approach + " " + booster
        
        return LegalStrategy(
            approach=mutated_approach,
            generation=strategy.generation,
            strategy_type=strategy.strategy_type
        )
    
    def select_parents(self) -> Tuple[LegalStrategy, LegalStrategy]:
        """Select two parents using tournament selection."""
        tournament_size = 3
        
        def tournament():
            candidates = random.sample(self.population, min(tournament_size, len(self.population)))
            # Only select compliant strategies, or best available if none compliant
            compliant = [s for s in candidates if s.compliance_verified]
            if compliant:
                return max(compliant, key=lambda s: s.fitness)
            return max(candidates, key=lambda s: s.fitness)
        
        parent1 = tournament()
        parent2 = tournament()
        return parent1, parent2
    
    def evolve_generation(self) -> List[LegalStrategy]:
        """Evolve one generation of strategies."""
        new_population = []
        
        # Keep best performing compliant strategies (elitism)
        compliant_strategies = [s for s in self.population if s.compliance_verified]
        if compliant_strategies:
            elite_count = max(1, self.population_size // 5)
            elite = sorted(compliant_strategies, key=lambda s: s.fitness, reverse=True)[:elite_count]
            new_population.extend(elite)
        
        # Generate offspring
        while len(new_population) < self.population_size:
            parent1, parent2 = self.select_parents()
            offspring = self.crossover(parent1, parent2)
            offspring = self.mutate(offspring)
            
            # Verify offspring
            self.judge.verify_strategy(offspring)
            new_population.append(offspring)
            self._log_to_ledger(offspring, "evolved")
        
        return new_population
    
    def run(self):
        """Run the evolutionary algorithm for the specified number of generations."""
        print(f"🧬 Starting Legal Evolution Engine (LSEE v1.0)")
        print(f"📊 Population: {self.population_size} | Generations: {self.generations}")
        print(f"⚖️  Checking against {len(self.judge.us_codes)} US legal codes")
        print(f"📝 Ledger: {self.ledger_path.absolute()}")
        print("=" * 70)
        
        for gen in range(self.generations):
            print(f"\n🔄 Generation {gen + 1}/{self.generations}")
            
            self.population = self.evolve_generation()
            
            # Statistics
            compliant = [s for s in self.population if s.compliance_verified]
            avg_fitness = sum(s.fitness for s in self.population) / len(self.population)
            
            print(f"   ✅ Compliant: {len(compliant)}/{len(self.population)}")
            print(f"   📈 Avg Fitness: {avg_fitness:.2f}")
            
            if compliant:
                best = max(compliant, key=lambda s: s.fitness)
                print(f"   🏆 Best: {best.fitness:.2f} (Gen {best.generation}, Type: {best.strategy_type})")
        
        print("\n" + "=" * 70)
        print("✨ Evolution Complete!")
        
        # Final report
        compliant = [s for s in self.population if s.compliance_verified]
        if compliant:
            best = max(compliant, key=lambda s: s.fitness)
            print(f"\n🎯 Best Strategy (Fitness: {best.fitness:.2f}, Type: {best.strategy_type}):")
            print(f"\n{best.approach}\n")
        else:
            print("\n⚠️  Warning: No fully compliant strategies in final population!")
    
    def _log_to_ledger(self, strategy: LegalStrategy, event_type: str):
        """Log strategy evolution to JSONL ledger."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "strategy_id": strategy.id,
            "generation": strategy.generation,
            "strategy_type": strategy.strategy_type,
            "fitness": strategy.fitness,
            "compliant": strategy.compliance_verified,
            "snippet": strategy.approach[:200] + "..." if len(strategy.approach) > 200 else strategy.approach,
            "codes_checked": len(self.judge.us_codes)
        }
        
        with open(self.ledger_path, 'a') as f:
            f.write(json.dumps(entry) + '\n')


# ============================================================================
# Base Strategy Templates
# ============================================================================

BASE_BACKGROUND_CHECK_STRATEGY = """
Background check procedures must comply with FCRA permissible purposes as defined in 15 U.S.C. § 1681b.
Obtain written consent from subject before requesting consumer reports.
Use only FCRA-compliant consumer reporting agencies.
Provide required adverse action notices if information is used in decision-making.
Maintain records of consent and disclosure documents for compliance audits.
Verify proper licensing for background check operations in applicable states.
"""

BASE_OSINT_STRATEGY = """
OSINT collection limited to publicly available information sources.
No unauthorized access to protected systems or databases.
Respect website terms of service and robots.txt directives.
Document all sources and collection methodologies for legal review.
Avoid techniques that could constitute harassment or stalking under 18 U.S.C. § 2261A.
Ensure all activities have legitimate investigative purpose.
Comply with state private investigator licensing requirements.
"""

BASE_SKIP_TRACE_STRATEGY = """
Skip tracing must use lawful information sources including public records, commercial databases with proper authorization, and permissible FCRA sources.
No pretexting or impersonation prohibited by 15 U.S.C. § 6823.
Maintain documentation of all database queries and legal basis for access.
Respect Do Not Call registry for phone-based contact attempts.
Comply with state debt collection and privacy laws when locating individuals.
Obtain proper licensing for skip tracing services where required.
"""


# ============================================================================
# External AI Conversation Archival
# ============================================================================

class ExternalConversationArchive:
    """Archive external AI conversations for audit trail and compliance."""
    
    def __init__(self, ledger_path: Path = Path("external_ai_ledger.jsonl")):
        self.ledger_path = ledger_path
    
    def archive_conversation(self, source_url: str, summary: str, 
                           conversation_type: str = "external_discussion",
                           tags: Optional[List[str]] = None):
        """
        Archive an external AI conversation (e.g., Claude share link).
        
        Args:
            source_url: URL to the conversation (e.g., Claude share link)
            summary: Brief summary of the conversation content
            conversation_type: Type of discussion (default: external_discussion)
            tags: Optional list of tags for categorization
        """
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": conversation_type,
            "source": source_url,
            "summary": summary,
            "tags": tags or [],
            "archived_by": "legal_evolution_system"
        }
        
        with open(self.ledger_path, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        
        print(f"✅ Archived: {source_url}")
        print(f"   Summary: {summary}")
    
    def list_archives(self, limit: int = 10) -> List[Dict]:
        """List recent archived conversations."""
        if not self.ledger_path.exists():
            return []
        
        archives = []
        with open(self.ledger_path, 'r') as f:
            for line in f:
                archives.append(json.loads(line))
        
        return archives[-limit:]


# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Main execution function."""
    
    print("⚖️  Legal Synthesizer Evolution Engine (LSEE) v1.0")
    print("=" * 70)
    
    # Initialize the compliance judge
    judge = LegalComplianceJudge(US_CODES)
    
    # Initialize the evolution engine
    engine = LegalEvolutionEngine(
        judge=judge,
        population_size=10,
        mutation_rate=0.3,
        generations=5
    )
    
    # Seed with base strategies
    base_strategies = [
        LegalStrategy(BASE_BACKGROUND_CHECK_STRATEGY, generation=0, strategy_type="background_check"),
        LegalStrategy(BASE_OSINT_STRATEGY, generation=0, strategy_type="osint"),
        LegalStrategy(BASE_SKIP_TRACE_STRATEGY, generation=0, strategy_type="skip_trace"),
    ]
    
    engine.seed_population(base_strategies)
    
    # Run evolution
    engine.run()
    
    print("\n" + "=" * 70)
    print("📚 Archiving External AI Conversation")
    print("=" * 70)
    
    # Archive the Claude conversation that inspired this implementation
    # Configure this URL for your specific use case
    INITIAL_CONVERSATION_URL = "https://claude.ai/share/777c7e93-fb67-4026-8370-1b1588c5df56"
    
    archive = ExternalConversationArchive()
    archive.archive_conversation(
        source_url=INITIAL_CONVERSATION_URL,
        summary="Design of meta-evolution and legal synthesizer engine. Discussion of evolutionary strategies for legal compliance in PI/OSINT operations.",
        conversation_type="design_discussion",
        tags=["legal", "evolution", "compliance", "LSEE", "meta-engine"]
    )
    
    print("\n✨ Legal Evolution Synthesizer run complete!")
    print(f"📊 Check ledgers:")
    print(f"   - legal_evolution_ledger.jsonl (strategy evolution)")
    print(f"   - external_ai_ledger.jsonl (conversation archive)")


if __name__ == "__main__":
    main()
