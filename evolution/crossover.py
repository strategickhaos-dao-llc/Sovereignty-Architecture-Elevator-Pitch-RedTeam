#!/usr/bin/env python3
"""
Sexual Reproduction via Genetic Crossover
Two parents combine traits to create offspring
"""

import random
from typing import Tuple

class GeneticCrossover:
    """Implements sexual reproduction for AI heirs"""
    
    @staticmethod
    def crossover_prompts(parent1_prompt: str, parent2_prompt: str) -> str:
        """
        Combine two system prompts using genetic crossover
        
        Splits prompts into sentences/lines and recombines them
        """
        # Split prompts into meaningful units (lines)
        p1_lines = [line for line in parent1_prompt.split('\n') if line.strip()]
        p2_lines = [line for line in parent2_prompt.split('\n') if line.strip()]
        
        # If no lines, return a mix
        if not p1_lines and not p2_lines:
            return parent1_prompt
        if not p1_lines:
            return parent2_prompt
        if not p2_lines:
            return parent1_prompt
        
        child_lines = []
        
        # Uniform crossover - randomly pick from each parent
        max_len = max(len(p1_lines), len(p2_lines))
        
        for i in range(max_len):
            # Get line from each parent if available
            p1_line = p1_lines[i] if i < len(p1_lines) else None
            p2_line = p2_lines[i] if i < len(p2_lines) else None
            
            if p1_line and p2_line:
                # Both parents have a line at this position - choose randomly
                if random.random() < 0.5:
                    child_lines.append(p1_line)
                else:
                    child_lines.append(p2_line)
            elif p1_line:
                # Only parent1 has a line
                if random.random() < 0.7:  # 70% chance to include
                    child_lines.append(p1_line)
            elif p2_line:
                # Only parent2 has a line
                if random.random() < 0.7:  # 70% chance to include
                    child_lines.append(p2_line)
        
        # Add some random lines from the other parent for diversity
        if len(p2_lines) > 0 and random.random() < 0.3:
            extra_lines = random.sample(p2_lines, k=min(random.randint(1, 2), len(p2_lines)))
            child_lines.extend(extra_lines)
        
        return "\n".join(child_lines)
    
    @staticmethod
    def crossover_temperature(parent1_temp: float, parent2_temp: float) -> float:
        """
        Combine temperatures using weighted average with mutation
        """
        # Average with slight mutation
        avg_temp = (parent1_temp + parent2_temp) / 2.0
        mutation = random.uniform(-0.1, 0.1)
        
        # Clamp to valid range
        new_temp = max(0.1, min(2.0, avg_temp + mutation))
        
        return new_temp
    
    @staticmethod
    def multi_point_crossover(parent1_prompt: str, parent2_prompt: str) -> str:
        """
        Advanced multi-point crossover
        
        Splits prompts at multiple points and alternates between parents
        """
        p1_lines = [line for line in parent1_prompt.split('\n') if line.strip()]
        p2_lines = [line for line in parent2_prompt.split('\n') if line.strip()]
        
        if not p1_lines:
            return parent2_prompt
        if not p2_lines:
            return parent1_prompt
        
        # Determine crossover points
        max_len = max(len(p1_lines), len(p2_lines))
        num_crossover_points = random.randint(1, 3)
        
        crossover_points = sorted(random.sample(range(1, max_len), 
                                                k=min(num_crossover_points, max_len - 1)))
        
        child_lines = []
        current_parent = 1  # Start with parent1
        last_point = 0
        
        for point in crossover_points + [max_len]:
            # Take segment from current parent
            if current_parent == 1:
                segment = p1_lines[last_point:min(point, len(p1_lines))]
            else:
                segment = p2_lines[last_point:min(point, len(p2_lines))]
            
            child_lines.extend(segment)
            
            # Switch parent
            current_parent = 2 if current_parent == 1 else 1
            last_point = point
        
        return "\n".join(child_lines)
    
    @staticmethod
    def create_offspring(parent1, parent2, generation: int):
        """
        Create offspring heir from two parents using sexual reproduction
        
        Args:
            parent1: First parent Heir object
            parent2: Second parent Heir object
            generation: Generation number for offspring
            
        Returns:
            New Heir object combining traits from both parents
        """
        # Import Heir class (avoid circular import)
        from evolution_engine import Heir
        
        # Choose crossover method randomly
        if random.random() < 0.5:
            child_prompt = GeneticCrossover.crossover_prompts(
                parent1.system_prompt, 
                parent2.system_prompt
            )
        else:
            child_prompt = GeneticCrossover.multi_point_crossover(
                parent1.system_prompt,
                parent2.system_prompt
            )
        
        # Combine temperatures
        child_temp = GeneticCrossover.crossover_temperature(
            parent1.temperature,
            parent2.temperature
        )
        
        # Create child heir
        child = Heir(child_prompt, child_temp, generation)
        child.parent_id = f"{parent1.id}+{parent2.id}"
        
        return child
