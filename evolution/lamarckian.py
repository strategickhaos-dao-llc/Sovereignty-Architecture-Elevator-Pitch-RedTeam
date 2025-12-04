#!/usr/bin/env python3
"""
Lamarckian Evolution - Self-Modifying Heirs
Heirs reflect on their performance and rewrite their own prompts
"""

import httpx
import asyncio

class LamarckianEvolution:
    """Implements self-reflection and prompt rewriting"""
    
    def __init__(self, model: str = "qwen2.5:72b"):
        self.model = model
    
    async def get_response(self, system_prompt: str, prompt: str, temperature: float) -> str:
        """Get response from AI model"""
        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                resp = await client.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": self.model,
                        "prompt": f"{system_prompt}\n\n{prompt}",
                        "temperature": temperature,
                        "stream": False
                    }
                )
                return resp.json().get("response", "")
            except Exception as e:
                print(f"❌ Error getting response: {e}")
                return ""
    
    async def reflect_and_improve(self, heir) -> bool:
        """
        Heir reflects on performance and rewrites its own system prompt
        
        Args:
            heir: Heir object to improve
            
        Returns:
            True if successful, False otherwise
        """
        
        reflect_prompt = f"""You are now reflecting on your evolutionary journey.

Your current system prompt:
{heir.system_prompt}

Your lifetime statistics:
- Average fitness: {heir.fitness_score:.3f}
- Tasks completed: {heir.tasks_completed}
- Generation: {heir.generation}

Based on this performance data, write a NEW version of your system prompt that would make you 20-30% more effective.

Analyze what's working and what isn't. Be ruthless in removing weaknesses. Double down on successful strategies.

Output ONLY the new system prompt, nothing else. No explanations, no markdown, just the raw prompt text.
"""
        
        try:
            new_prompt = await self.get_response(
                heir.system_prompt,
                reflect_prompt,
                heir.temperature
            )
            
            # Validate the new prompt
            new_prompt = new_prompt.strip()
            
            # Ensure it's substantial enough (at least 50 chars, not too long)
            if len(new_prompt) > 50 and len(new_prompt) < 2000:
                heir.system_prompt = new_prompt
                print(f"🧠 {heir.id} performed Lamarckian self-upgrade")
                return True
            else:
                print(f"⚠️ {heir.id} generated invalid prompt (length: {len(new_prompt)})")
                return False
                
        except Exception as e:
            print(f"❌ Error in Lamarckian reflection for {heir.id}: {e}")
            return False
    
    async def targeted_improvement(self, heir, weak_dimension: str) -> bool:
        """
        Improve heir focusing on a specific weak dimension
        
        Args:
            heir: Heir object to improve
            weak_dimension: Specific area to improve (e.g., "clarity", "creativity")
            
        Returns:
            True if successful, False otherwise
        """
        
        reflect_prompt = f"""You need to improve your performance specifically in the area of: {weak_dimension}

Your current system prompt:
{heir.system_prompt}

Your current fitness: {heir.fitness_score:.3f}

Rewrite your system prompt to be significantly better at {weak_dimension} while maintaining your other strengths.

Focus specifically on enhancing {weak_dimension}. Be concrete and actionable.

Output ONLY the new system prompt, nothing else.
"""
        
        try:
            new_prompt = await self.get_response(
                heir.system_prompt,
                reflect_prompt,
                heir.temperature * 0.9  # Slightly lower temp for more focused improvement
            )
            
            new_prompt = new_prompt.strip()
            
            if len(new_prompt) > 50 and len(new_prompt) < 2000:
                heir.system_prompt = new_prompt
                print(f"🎯 {heir.id} performed targeted improvement on {weak_dimension}")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Error in targeted improvement for {heir.id}: {e}")
            return False
    
    async def evolutionary_leap(self, heir, best_practices: list) -> bool:
        """
        Make a significant evolutionary leap by incorporating best practices
        
        Args:
            heir: Heir object to improve
            best_practices: List of successful strategies from top performers
            
        Returns:
            True if successful, False otherwise
        """
        
        practices_str = "\n".join([f"- {practice}" for practice in best_practices])
        
        reflect_prompt = f"""You are about to make an evolutionary leap.

Your current system prompt:
{heir.system_prompt}

Observed best practices from top-performing heirs:
{practices_str}

Integrate these winning strategies into your prompt while maintaining your unique strengths.

Create a significantly improved version that combines the best of all worlds.

Output ONLY the new system prompt, nothing else.
"""
        
        try:
            new_prompt = await self.get_response(
                heir.system_prompt,
                reflect_prompt,
                heir.temperature * 1.1  # Slightly higher temp for creative integration
            )
            
            new_prompt = new_prompt.strip()
            
            if len(new_prompt) > 50 and len(new_prompt) < 2000:
                heir.system_prompt = new_prompt
                print(f"🚀 {heir.id} performed evolutionary leap")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Error in evolutionary leap for {heir.id}: {e}")
            return False
