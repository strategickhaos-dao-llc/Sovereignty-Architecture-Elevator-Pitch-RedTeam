#!/usr/bin/env python3
"""
Lamarckian Evolution Module
Allows heirs to reflect on and rewrite their own prompts
This is "acquired characteristic inheritance" - the digital equivalent
"""

import httpx
import asyncio
from evolution_engine import Heir


class LamarckianReflector:
    """Enables heirs to perform self-improvement through reflection"""
    
    def __init__(self, model: str = "qwen2.5:72b", api_url: str = "http://localhost:11434"):
        self.model = model
        self.api_url = api_url
        self.reflection_temperature = 0.8  # Higher for creative self-improvement
    
    async def get_response(self, prompt: str, temperature: float) -> str:
        """Get response from LLM"""
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                resp = await client.post(
                    f"{self.api_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "temperature": temperature,
                        "stream": False
                    }
                )
                return resp.json().get("response", "")
            except Exception as e:
                print(f"❌ Error getting response: {e}")
                return ""
    
    async def lamarckian_reflect(self, heir: Heir) -> bool:
        """
        Let the heir reflect on its evolutionary journey and rewrite its own prompt
        Returns True if successful, False otherwise
        """
        
        reflect_prompt = f"""You are now reflecting on your evolutionary journey as an AI agent.

Your current system prompt:
{heir.system_prompt}

Your lifetime statistics:
- Average fitness score: {heir.fitness_score:.3f}
- Tasks completed: {heir.tasks_completed}
- Generation: {heir.generation}

Based on this performance data, write a NEW and IMPROVED version of your system prompt that would make you 20-30% more effective at tasks.

Key principles:
- Be ruthless: Remove weaknesses and ineffective patterns
- Double down: Amplify what has been working well
- Be specific: Use concrete directives rather than vague instructions
- Stay focused: Keep the prompt concise and actionable

Output ONLY the new system prompt, nothing else. Do not include any explanation or meta-commentary."""

        new_prompt = await self.get_response(reflect_prompt, self.reflection_temperature)
        
        if len(new_prompt.strip()) > 100:  # Ensure meaningful output
            heir.system_prompt = new_prompt.strip()
            print(f"🧠 {heir.id} performed Lamarckian self-upgrade")
            return True
        else:
            print(f"⚠️  {heir.id} reflection produced insufficient output, keeping original")
            return False
    
    async def guided_reflection(self, heir: Heir, feedback: str) -> bool:
        """
        Reflection with specific feedback about what to improve
        """
        
        reflect_prompt = f"""You are reflecting on your performance as an AI agent.

Your current system prompt:
{heir.system_prompt}

Performance feedback:
{feedback}

Your statistics:
- Fitness score: {heir.fitness_score:.3f}
- Tasks completed: {heir.tasks_completed}

Create an improved system prompt that directly addresses the feedback while maintaining your core strengths.

Output ONLY the new system prompt."""

        new_prompt = await self.get_response(reflect_prompt, self.reflection_temperature)
        
        if len(new_prompt.strip()) > 100:
            heir.system_prompt = new_prompt.strip()
            print(f"🧠 {heir.id} evolved with guided reflection")
            return True
        else:
            return False
    
    async def meta_reflection(self, heir: Heir, population_avg_fitness: float) -> bool:
        """
        Reflection that considers performance relative to the population
        """
        
        performance_status = "above average" if heir.fitness_score > population_avg_fitness else "below average"
        
        reflect_prompt = f"""You are an evolving AI agent performing meta-cognitive reflection.

Your current system prompt:
{heir.system_prompt}

Your fitness: {heir.fitness_score:.3f}
Population average: {population_avg_fitness:.3f}
Your status: {performance_status}

{"You are outperforming the population. Analyze what makes you successful and intensify those traits." 
 if heir.fitness_score > population_avg_fitness 
 else "You are underperforming. Identify your weaknesses and fundamentally redesign your approach."}

Generate an evolved system prompt that will increase your competitive advantage.

Output ONLY the new system prompt."""

        new_prompt = await self.get_response(reflect_prompt, self.reflection_temperature)
        
        if len(new_prompt.strip()) > 100:
            heir.system_prompt = new_prompt.strip()
            print(f"🧠 {heir.id} performed meta-reflection (was {performance_status})")
            return True
        else:
            return False


async def apply_lamarckian_evolution(population: list, generation: int, 
                                    reflection_frequency: int = 5,
                                    api_url: str = "http://localhost:11434"):
    """
    Apply Lamarckian reflection to top performers every N generations
    
    Args:
        population: Current population of heirs
        generation: Current generation number
        reflection_frequency: How often to trigger reflection (default: every 5 generations)
        api_url: API endpoint for LLM
    """
    
    if generation % reflection_frequency != 0:
        return
    
    print(f"\n🔄 Generation {generation}: Lamarckian reflection activated")
    
    reflector = LamarckianReflector(api_url=api_url)
    
    # Sort by fitness
    population.sort(key=lambda h: h.fitness_score, reverse=True)
    
    # Top 30% get to self-reflect
    num_reflectors = max(1, len(population) // 3)
    top_performers = population[:num_reflectors]
    
    population_avg = sum(h.fitness_score for h in population) / len(population)
    
    for heir in top_performers:
        # Use meta-reflection for population-aware improvement
        await reflector.meta_reflection(heir, population_avg)
    
    print(f"✅ {num_reflectors} heirs performed self-improvement\n")


if __name__ == "__main__":
    # Demo Lamarckian reflection
    async def demo():
        heir = Heir("You are a tactical analyst. Be direct and actionable.", 0.7, 10)
        heir.fitness_score = 0.75
        heir.tasks_completed = 50
        
        reflector = LamarckianReflector()
        
        print("Original prompt:")
        print(heir.system_prompt)
        print(f"Fitness: {heir.fitness_score:.3f}\n")
        
        success = await reflector.lamarckian_reflect(heir)
        
        if success:
            print("\nEvolved prompt:")
            print(heir.system_prompt)
    
    asyncio.run(demo())
