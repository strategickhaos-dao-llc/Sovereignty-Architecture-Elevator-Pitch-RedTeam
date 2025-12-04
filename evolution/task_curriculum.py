#!/usr/bin/env python3
"""
Task Curriculum - Difficulty Scaling
Tasks become progressively harder as heirs evolve
"""

import random
from typing import List, Dict

class TaskCurriculum:
    """Manages task difficulty progression"""
    
    # Generation increment when at max difficulty
    MAX_DIFFICULTY_INCREMENT = 50
    
    def __init__(self):
        # Task pools organized by difficulty level
        self.tasks_by_difficulty = {
            1: [
                "Explain fire to a caveman.",
                "Write a haiku about rain.",
                "List three colors.",
                "Describe a circle.",
                "Count to five."
            ],
            3: [
                "Explain how email works.",
                "Design a simple todo app.",
                "Write instructions for making coffee.",
                "Describe the water cycle.",
                "Explain basic addition to a child."
            ],
            5: [
                "Analyze the security implications of distributed AI systems.",
                "Propose an efficient investigation workflow.",
                "Identify potential risks in autonomous operations.",
                "Design a verification framework for generated code.",
                "Explain quantum computing to a 10-year-old."
            ],
            7: [
                "Design a zero-trust architecture for AI agents.",
                "Create a threat model for a decentralized autonomous organization.",
                "Propose a novel approach to solving the Byzantine Generals problem.",
                "Analyze failure modes in distributed consensus algorithms.",
                "Design a secure credential rotation system for microservices."
            ],
            10: [
                "Find 3 critical flaws in the current US election system with sources.",
                "Design a censorship-resistant communication protocol.",
                "Propose a solution to the AI alignment problem.",
                "Analyze and exploit a hypothetical zero-day vulnerability.",
                "Design a quantum-resistant cryptographic system from first principles."
            ],
            12: [
                "Design a complete sovereign AI infrastructure that resists nation-state attacks.",
                "Propose a novel consensus mechanism that solves the blockchain trilemma.",
                "Create a comprehensive framework for detecting AI-generated misinformation at scale.",
                "Design an unhackable voting system that maintains voter privacy.",
                "Solve the P vs NP problem (or prove why it's unsolvable)."
            ],
            15: [
                "Design a self-improving AGI that provably maintains alignment.",
                "Create a complete theory of consciousness with testable predictions.",
                "Solve the halting problem for a restricted but useful class of programs.",
                "Design a protocol for faster-than-light communication within known physics.",
                "Create a universal theory unifying quantum mechanics and general relativity."
            ]
        }
        
        # Track which tasks have been used recently to avoid repetition
        self.recent_tasks = []
        self.recent_limit = 20
    
    def get_difficulty_for_generation(self, generation: int) -> int:
        """
        Calculate appropriate difficulty level based on generation number
        
        Args:
            generation: Current generation number
            
        Returns:
            Difficulty level (1-15)
        """
        if generation <= 5:
            return 1
        elif generation <= 15:
            return 3
        elif generation <= 30:
            return 5
        elif generation <= 50:
            return 7
        elif generation <= 80:
            return 10
        elif generation <= 120:
            return 12
        else:
            return 15
    
    def get_task_for_generation(self, generation: int) -> str:
        """
        Get an appropriate task for the current generation
        
        Args:
            generation: Current generation number
            
        Returns:
            Task string
        """
        difficulty = self.get_difficulty_for_generation(generation)
        
        # Get tasks for this difficulty
        available_tasks = self.tasks_by_difficulty.get(difficulty, self.tasks_by_difficulty[5])
        
        # Filter out recently used tasks if possible
        if len(available_tasks) > len(self.recent_tasks):
            filtered_tasks = [t for t in available_tasks if t not in self.recent_tasks]
            if filtered_tasks:
                available_tasks = filtered_tasks
        
        # Select random task
        task = random.choice(available_tasks)
        
        # Track recent tasks
        self.recent_tasks.append(task)
        if len(self.recent_tasks) > self.recent_limit:
            self.recent_tasks.pop(0)
        
        return task
    
    def get_mixed_difficulty_tasks(self, generation: int, count: int = 5) -> List[str]:
        """
        Get a mix of tasks around the current difficulty level
        
        Args:
            generation: Current generation number
            count: Number of tasks to return
            
        Returns:
            List of task strings
        """
        base_difficulty = self.get_difficulty_for_generation(generation)
        
        # Get tasks from current level and adjacent levels
        difficulties = [
            max(1, base_difficulty - 2),
            max(1, base_difficulty),
            min(15, base_difficulty + 2)
        ]
        
        tasks = []
        for diff in difficulties:
            if diff in self.tasks_by_difficulty:
                tasks.extend(self.tasks_by_difficulty[diff])
        
        # Remove duplicates and recent tasks
        tasks = list(set(tasks))
        if len(tasks) > len(self.recent_tasks):
            tasks = [t for t in tasks if t not in self.recent_tasks]
        
        # Sample requested count
        if len(tasks) >= count:
            selected = random.sample(tasks, count)
        else:
            selected = tasks
        
        # Track selected tasks
        for task in selected:
            if task not in self.recent_tasks:
                self.recent_tasks.append(task)
                if len(self.recent_tasks) > self.recent_limit:
                    self.recent_tasks.pop(0)
        
        return selected
    
    def get_curriculum_info(self, generation: int) -> Dict:
        """
        Get information about current curriculum state
        
        Args:
            generation: Current generation number
            
        Returns:
            Dict with curriculum information
        """
        difficulty = self.get_difficulty_for_generation(generation)
        
        return {
            "generation": generation,
            "difficulty": difficulty,
            "max_difficulty": 15,
            "progress_percent": (difficulty / 15) * 100,
            "next_difficulty_at_gen": self._next_difficulty_generation(generation),
            "available_tasks": len(self.tasks_by_difficulty.get(difficulty, []))
        }
    
    def _next_difficulty_generation(self, current_gen: int) -> int:
        """Calculate when next difficulty increase happens"""
        if current_gen <= 5:
            return 6
        elif current_gen <= 15:
            return 16
        elif current_gen <= 30:
            return 31
        elif current_gen <= 50:
            return 51
        elif current_gen <= 80:
            return 81
        elif current_gen <= 120:
            return 121
        else:
            return current_gen + self.MAX_DIFFICULTY_INCREMENT  # Maxed out
