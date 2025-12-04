#!/usr/bin/env python3
"""
Neural Heir Evolution System (NHES) - Self-Evolving AI
Strategickhaos Sovereignty Architecture

Watches itself get smarter over generations through natural selection.
"""

import json
import random
from datetime import datetime
from pathlib import Path
import httpx
import asyncio

# Evolution ledger
EVOLUTION_LOG = Path("evolution_ledger.jsonl")
POPULATION_FILE = Path("current_population.json")

class Heir:
    """A single AI personality that can evolve"""
    
    def __init__(self, system_prompt: str, temperature: float, generation: int, parent_id: str = None):
        self.id = f"heir_{random.randint(1000, 9999)}"
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.generation = generation
        self.parent_id = parent_id
        self.fitness_score = 0.0
        self.tasks_completed = 0
        
    def to_dict(self):
        return {
            "id": self.id,
            "system_prompt": self.system_prompt,
            "temperature": self.temperature,
            "generation": self.generation,
            "parent_id": self.parent_id,
            "fitness_score": self.fitness_score,
            "tasks_completed": self.tasks_completed
        }
    
    @classmethod
    def from_dict(cls, data):
        heir = cls(data["system_prompt"], data["temperature"], data["generation"], data["parent_id"])
        heir.id = data["id"]
        heir.fitness_score = data["fitness_score"]
        heir.tasks_completed = data["tasks_completed"]
        return heir
    
    def mutate(self):
        """Create offspring with mutations"""
        
        # Mutation options
        mutations = [
            "more aggressive",
            "more cautious", 
            "more creative",
            "more analytical",
            "more concise",
            "more detailed"
        ]
        
        mutation = random.choice(mutations)
        
        new_prompt = f"{self.system_prompt}\n\nEvolutionary adaptation: Be {mutation}."
        new_temp = max(0.1, min(2.0, self.temperature + random.uniform(-0.2, 0.2)))
        
        return Heir(new_prompt, new_temp, self.generation + 1, self.id)

class EvolutionEngine:
    """Manages population evolution"""
    
    def __init__(self, population_size: int = 10):
        self.population_size = population_size
        self.population = []
        self.generation = 0
        
    def initialize_population(self):
        """Create first generation with diverse prompts"""
        
        base_prompts = [
            "You are a tactical analyst. Be direct and actionable.",
            "You are a creative problem solver. Think outside the box.",
            "You are a cautious evaluator. Consider all risks.",
            "You are an aggressive optimizer. Push boundaries.",
            "You are a detail-oriented researcher. Be thorough.",
        ]
        
        self.population = []
        for prompt in base_prompts:
            for temp in [0.5, 0.8, 1.1]:
                heir = Heir(prompt, temp, generation=0)
                self.population.append(heir)
        
        print(f"✅ Initialized population: {len(self.population)} heirs")
    
    async def evaluate_heir(self, heir: Heir, task: str) -> float:
        """Run task and score the response"""
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                resp = await client.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "qwen2.5:72b",
                        "prompt": f"{heir.system_prompt}\n\nTask: {task}",
                        "temperature": heir.temperature,
                        "stream": False
                    }
                )
                
                response_text = resp.json().get("response", "")
                
                # Simple fitness metrics
                length_score = min(len(response_text) / 500, 1.0)  # Prefer substantial responses
                keyword_score = sum(1 for word in ["solution", "approach", "analyze", "recommend"] 
                                  if word in response_text.lower()) / 4.0
                
                fitness = (length_score + keyword_score) / 2.0
                
                heir.tasks_completed += 1
                return fitness
                
            except Exception as e:
                print(f"❌ Error evaluating {heir.id}: {e}")
                return 0.0
    
    async def run_generation(self):
        """Evaluate all heirs on random tasks"""
        
        self.generation += 1
        print(f"\n🧬 Generation {self.generation}")
        
        # Sample tasks
        tasks = [
            "Analyze the security implications of distributed AI systems.",
            "Propose an efficient investigation workflow.",
            "Identify potential risks in autonomous operations.",
            "Design a verification framework for generated code.",
            "Explain quantum computing to a 10-year-old."
        ]
        
        # Evaluate each heir
        for heir in self.population:
            task = random.choice(tasks)
            fitness = await self.evaluate_heir(heir, task)
            # Note: tasks_completed was already incremented in evaluate_heir
            heir.fitness_score = (heir.fitness_score * (heir.tasks_completed - 1) + fitness) / heir.tasks_completed
            
            print(f"  {heir.id} (gen {heir.generation}): fitness={heir.fitness_score:.3f}")
        
        # Log generation
        self.log_generation()
    
    def selection_and_reproduction(self):
        """Natural selection + reproduction"""
        
        # Sort by fitness
        self.population.sort(key=lambda h: h.fitness_score, reverse=True)
        
        # Top 50% survive
        survivors = self.population[:len(self.population)//2]
        
        print(f"\n🏆 Top performers:")
        for heir in survivors[:3]:
            print(f"  {heir.id}: {heir.fitness_score:.3f}")
        
        print(f"\n💀 Culled: {len(self.population) - len(survivors)} heirs")
        
        # Survivors reproduce with mutations
        offspring = []
        while len(survivors) + len(offspring) < self.population_size:
            parent = random.choice(survivors)
            child = parent.mutate()
            offspring.append(child)
        
        self.population = survivors + offspring
        
        print(f"🐣 Created: {len(offspring)} offspring\n")
    
    def log_generation(self):
        """Record generation stats"""
        
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "generation": self.generation,
            "population_size": len(self.population),
            "avg_fitness": sum(h.fitness_score for h in self.population) / len(self.population),
            "best_fitness": max(h.fitness_score for h in self.population),
            "best_heir": max(self.population, key=lambda h: h.fitness_score).to_dict()
        }
        
        with open(EVOLUTION_LOG, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def save_population(self):
        """Save current population to disk"""
        
        data = {
            "generation": self.generation,
            "population": [h.to_dict() for h in self.population]
        }
        
        with open(POPULATION_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_population(self):
        """Load population from disk"""
        
        if not POPULATION_FILE.exists():
            return False
        
        with open(POPULATION_FILE, 'r') as f:
            data = json.load(f)
        
        self.generation = data["generation"]
        self.population = [Heir.from_dict(h) for h in data["population"]]
        
        print(f"✅ Loaded generation {self.generation} with {len(self.population)} heirs")
        return True

async def evolve_forever():
    """Run evolution indefinitely"""
    
    engine = EvolutionEngine(population_size=10)
    
    # Load existing or initialize
    if not engine.load_population():
        engine.initialize_population()
    
    print("\n🧬 Evolution Engine Started")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            # Run generation
            await engine.run_generation()
            
            # Natural selection
            engine.selection_and_reproduction()
            
            # Save state
            engine.save_population()
            
            # Brief pause
            await asyncio.sleep(5)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Evolution stopped")
        print(f"Final generation: {engine.generation}")
        print(f"Best fitness: {max(h.fitness_score for h in engine.population):.3f}")
        engine.save_population()

if __name__ == "__main__":
    asyncio.run(evolve_forever())
