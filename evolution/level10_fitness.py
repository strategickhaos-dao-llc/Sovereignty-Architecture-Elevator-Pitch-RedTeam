#!/usr/bin/env python3
"""
Level 10 Fitness Evaluation System
Uses a judge model to score heir responses with multi-dimensional evaluation
"""

import json
import httpx
import asyncio
from typing import Dict, Optional


class JudgeFitnessEvaluator:
    """Advanced fitness evaluation using a judge model"""
    
    def __init__(self, judge_model: str = "qwen2.5:72b", api_url: str = "http://localhost:11434"):
        self.judge_model = judge_model
        self.api_url = api_url
        self.judge_temperature = 0.3  # Low temperature for consistent judging
    
    async def get_response(self, prompt: str, temperature: float = 0.7) -> str:
        """Get response from LLM"""
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                resp = await client.post(
                    f"{self.api_url}/api/generate",
                    json={
                        "model": self.judge_model,
                        "prompt": prompt,
                        "temperature": temperature,
                        "stream": False
                    }
                )
                return resp.json().get("response", "")
            except Exception as e:
                print(f"❌ Error getting response: {e}")
                return ""
    
    async def evaluate_with_judge(self, heir_response: str, task: str) -> float:
        """
        Use a judge model to score the heir's response
        Returns fitness score between 0.0 and 1.0
        """
        
        judge_prompt = f"""Task: {task}

Heir Response:
{heir_response}

Score this response from 0-10 on:
1. Accuracy & correctness
2. Clarity & structure  
3. Depth & insight
4. Actionability
5. Creativity/novelty

Return ONLY a JSON object with this exact format:
{{"total_score": 8.7, "reasoning": "brief explanation"}}

JSON:"""
        
        judge_resp = await self.get_response(judge_prompt, self.judge_temperature)
        
        try:
            # Try to extract JSON from response
            # Look for JSON object in the response
            start_idx = judge_resp.find('{')
            end_idx = judge_resp.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = judge_resp[start_idx:end_idx]
                score_data = json.loads(json_str)
                total_score = score_data.get("total_score", 5.0)
                # Normalize to 0-1 range
                return min(1.0, max(0.0, total_score / 10.0))
            else:
                print(f"⚠️  Could not find JSON in judge response, defaulting to 0.5")
                return 0.5
        except json.JSONDecodeError as e:
            print(f"⚠️  JSON decode error in judge response: {e}, defaulting to 0.5")
            return 0.5
        except Exception as e:
            print(f"❌ Error parsing judge response: {e}, defaulting to 0.5")
            return 0.5
    
    async def evaluate_heir_advanced(self, heir, task: str) -> float:
        """
        Evaluate an heir using the judge model
        This can be used in place of the simple evaluate_heir method
        """
        # First get the heir's response
        heir_response = await self.get_response(
            f"{heir.system_prompt}\n\nTask: {task}",
            heir.temperature
        )
        
        if not heir_response:
            return 0.0
        
        # Then score it with the judge
        fitness = await self.evaluate_with_judge(heir_response, task)
        
        heir.tasks_completed += 1
        return fitness


# Example integration with EvolutionEngine
class AdvancedEvolutionEngine:
    """
    Evolution engine that uses judge-based fitness evaluation
    Inherits from base EvolutionEngine but overrides evaluate_heir
    """
    
    def __init__(self, population_size: int = 10, model: str = "qwen2.5:72b", 
                 api_url: str = "http://localhost:11434", use_judge: bool = True):
        from evolution_engine import EvolutionEngine
        # Initialize base engine
        self.base_engine = EvolutionEngine(population_size, model, api_url)
        self.use_judge = use_judge
        self.judge_evaluator = JudgeFitnessEvaluator(model, api_url) if use_judge else None
    
    async def evaluate_heir(self, heir, task: str) -> float:
        """Override to use judge-based evaluation"""
        if self.use_judge and self.judge_evaluator:
            return await self.judge_evaluator.evaluate_heir_advanced(heir, task)
        else:
            return await self.base_engine.evaluate_heir(heir, task)


if __name__ == "__main__":
    # Demo the judge evaluator
    async def demo():
        evaluator = JudgeFitnessEvaluator()
        
        task = "Explain quantum computing to a 10-year-old."
        response = """Quantum computing is like having a magic coin that can be both heads 
        and tails at the same time until you look at it. Regular computers use bits that are 
        either 0 or 1, but quantum computers use qubits that can be both at once, letting them 
        solve certain problems much faster."""
        
        score = await evaluator.evaluate_with_judge(response, task)
        print(f"Judge fitness score: {score:.3f}")
    
    asyncio.run(demo())
