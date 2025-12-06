#!/usr/bin/env python3
"""
Sexual Reproduction & Crossover Module
Combines traits from two parent heirs to create offspring
"""

import random
from typing import List
from evolution_engine import Heir


class CrossoverOperator:
    """Handles sexual reproduction between heirs"""
    
    @staticmethod
    def crossover(parent1: Heir, parent2: Heir) -> Heir:
        """
        Combine two parents to create a child heir
        Uses line-based crossover and parameter averaging
        """
        # Split prompts into lines
        p1_lines = [line for line in parent1.system_prompt.split('\n') if line.strip()]
        p2_lines = [line for line in parent2.system_prompt.split('\n') if line.strip()]
        
        # Recombine lines from both parents
        child_lines = []
        max_len = max(len(p1_lines), len(p2_lines))
        
        for i in range(max_len):
            # Randomly select from either parent if both have this line
            if i < len(p1_lines) and i < len(p2_lines):
                if random.random() < 0.5:
                    child_lines.append(p1_lines[i])
                else:
                    child_lines.append(p2_lines[i])
            elif i < len(p1_lines):
                if random.random() < 0.7:  # 70% chance to include extra lines
                    child_lines.append(p1_lines[i])
            elif i < len(p2_lines):
                if random.random() < 0.7:
                    child_lines.append(p2_lines[i])
        
        # Occasionally add random lines from either parent
        if random.random() < 0.3:
            extra_lines = random.sample(p2_lines + p1_lines, k=min(2, len(p1_lines + p2_lines)))
            child_lines.extend(extra_lines)
        
        # Create child prompt
        child_prompt = "\n".join(child_lines)
        
        # Average temperatures with small random variation
        child_temp = (parent1.temperature + parent2.temperature) / 2.0
        child_temp += random.uniform(-0.1, 0.1)
        child_temp = max(0.1, min(2.0, child_temp))  # Clamp to valid range
        
        # Child's generation is one more than the max parent generation
        child_generation = max(parent1.generation, parent2.generation) + 1
        
        # Create child heir with both parents tracked
        child = Heir(child_prompt, child_temp, child_generation)
        child.parent_id = f"{parent1.id}+{parent2.id}"
        
        return child
    
    @staticmethod
    def uniform_crossover(parent1: Heir, parent2: Heir) -> Heir:
        """
        Alternative crossover: word-level mixing
        More fine-grained than line-based crossover
        """
        p1_words = parent1.system_prompt.split()
        p2_words = parent2.system_prompt.split()
        
        # Mix words with 50/50 probability
        child_words = []
        max_len = max(len(p1_words), len(p2_words))
        
        for i in range(max_len):
            if i < len(p1_words) and i < len(p2_words):
                child_words.append(p1_words[i] if random.random() < 0.5 else p2_words[i])
            elif i < len(p1_words):
                child_words.append(p1_words[i])
            else:
                child_words.append(p2_words[i])
        
        child_prompt = " ".join(child_words)
        
        # Average parameters
        child_temp = (parent1.temperature + parent2.temperature) / 2.0
        child_temp += random.uniform(-0.1, 0.1)
        child_temp = max(0.1, min(2.0, child_temp))
        
        child_generation = max(parent1.generation, parent2.generation) + 1
        
        child = Heir(child_prompt, child_temp, child_generation)
        child.parent_id = f"{parent1.id}+{parent2.id}"
        
        return child
    
    @staticmethod
    def multi_point_crossover(parent1: Heir, parent2: Heir, num_points: int = 2) -> Heir:
        """
        Multi-point crossover: split prompt at multiple points and alternate
        """
        p1_lines = parent1.system_prompt.split('\n')
        p2_lines = parent2.system_prompt.split('\n')
        
        max_len = max(len(p1_lines), len(p2_lines))
        
        # Choose crossover points
        if max_len > num_points:
            crossover_points = sorted(random.sample(range(max_len), num_points))
        else:
            crossover_points = [max_len // 2]
        
        # Build child by alternating between parents at crossover points
        child_lines = []
        current_parent = 0  # 0 for parent1, 1 for parent2
        crossover_points.append(max_len)  # Add end point
        
        prev_point = 0
        for point in crossover_points:
            if current_parent == 0:
                child_lines.extend(p1_lines[prev_point:point])
            else:
                child_lines.extend(p2_lines[prev_point:point])
            current_parent = 1 - current_parent  # Switch parent
            prev_point = point
        
        child_prompt = "\n".join(child_lines)
        
        # Average parameters
        child_temp = (parent1.temperature + parent2.temperature) / 2.0
        child_temp += random.uniform(-0.1, 0.1)
        child_temp = max(0.1, min(2.0, child_temp))
        
        child_generation = max(parent1.generation, parent2.generation) + 1
        
        child = Heir(child_prompt, child_temp, child_generation)
        child.parent_id = f"{parent1.id}+{parent2.id}"
        
        return child


def selection_and_sexual_reproduction(population: List[Heir], population_size: int) -> List[Heir]:
    """
    Enhanced reproduction using sexual reproduction
    Replaces the mutation-only approach with crossover
    """
    # Sort by fitness
    population.sort(key=lambda h: h.fitness_score, reverse=True)
    
    # Top 50% survive
    survivors = population[:len(population)//2]
    
    print(f"\n🏆 Top performers:")
    for heir in survivors[:3]:
        print(f"  {heir.id}: {heir.fitness_score:.3f}")
    
    print(f"\n💀 Culled: {len(population) - len(survivors)} heirs")
    
    # Create offspring through sexual reproduction
    offspring = []
    crossover_op = CrossoverOperator()
    
    while len(survivors) + len(offspring) < population_size:
        # Tournament selection: pick 2 random parents
        parent1 = random.choice(survivors)
        parent2 = random.choice(survivors)
        
        # Ensure different parents
        max_attempts = 10
        attempts = 0
        while parent1.id == parent2.id and len(survivors) > 1 and attempts < max_attempts:
            parent2 = random.choice(survivors)
            attempts += 1
        
        # Create child through crossover
        if random.random() < 0.7:  # 70% crossover, 30% mutation
            child = crossover_op.crossover(parent1, parent2)
        else:
            # Sometimes just mutate the best parent
            child = parent1.mutate()
        
        offspring.append(child)
    
    new_population = survivors + offspring
    
    print(f"🐣 Created: {len(offspring)} offspring (via crossover and mutation)\n")
    
    return new_population


if __name__ == "__main__":
    # Demo crossover
    parent1 = Heir("You are analytical and careful. Think deeply.", 0.7, 5)
    parent1.fitness_score = 0.85
    
    parent2 = Heir("You are creative and bold. Take risks.", 0.9, 5)
    parent2.fitness_score = 0.78
    
    crossover_op = CrossoverOperator()
    
    print("Parent 1 prompt:")
    print(parent1.system_prompt)
    print(f"Temperature: {parent1.temperature}\n")
    
    print("Parent 2 prompt:")
    print(parent2.system_prompt)
    print(f"Temperature: {parent2.temperature}\n")
    
    child = crossover_op.crossover(parent1, parent2)
    
    print("Child prompt:")
    print(child.system_prompt)
    print(f"Temperature: {child.temperature}")
    print(f"Parent ID: {child.parent_id}")
