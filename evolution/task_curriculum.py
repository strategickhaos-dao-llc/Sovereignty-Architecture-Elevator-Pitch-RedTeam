#!/usr/bin/env python3
"""
Task Curriculum Module
Scales task difficulty with generation number to drive continuous improvement
"""

import random
from typing import List, Dict


class TaskCurriculum:
    """Manages progressive task difficulty for evolution"""
    
    def __init__(self):
        # Tasks organized by difficulty level (1-15)
        self.tasks_by_difficulty = {
            1: [
                "Explain fire to a caveman.",
                "Write a haiku about rain.",
                "Count to ten in Spanish.",
                "Describe what a dog is.",
            ],
            3: [
                "Explain photosynthesis to a middle schooler.",
                "Write a brief product review for a coffee maker.",
                "Summarize the plot of Romeo and Juliet.",
                "Describe the water cycle.",
            ],
            5: [
                "Design a zero-trust architecture for AI agents.",
                "Analyze the security implications of distributed AI systems.",
                "Propose an efficient investigation workflow.",
                "Create a data privacy compliance checklist.",
            ],
            7: [
                "Identify potential risks in autonomous operations.",
                "Design a verification framework for generated code.",
                "Propose a secure multi-party computation protocol.",
                "Analyze vulnerabilities in blockchain consensus mechanisms.",
            ],
            10: [
                "Find 3 critical flaws in a typical authentication system with mitigations.",
                "Design a resilient distributed system for mission-critical operations.",
                "Propose a novel approach to AI alignment.",
                "Create a comprehensive threat model for IoT networks.",
            ],
            12: [
                "Analyze the game theory of autonomous AI agent interactions.",
                "Design a quantum-resistant cryptographic protocol.",
                "Propose architectural improvements for decentralized identity systems.",
                "Develop a framework for adversarial robustness testing.",
            ],
            15: [
                "Design a completely novel approach to secure code execution in untrusted environments.",
                "Propose a breakthrough solution to the AI control problem.",
                "Create a comprehensive framework for sovereign AI systems.",
                "Develop a formal verification approach for neural network security.",
            ]
        }
    
    def get_difficulty_for_generation(self, generation: int) -> int:
        """
        Calculate appropriate difficulty level based on generation
        Starts easy, progressively increases
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
        """Get a random task appropriate for the current generation"""
        difficulty = self.get_difficulty_for_generation(generation)
        
        # Get tasks from current difficulty and one level below (for variety)
        available_difficulties = [d for d in self.tasks_by_difficulty.keys() if d <= difficulty]
        
        if not available_difficulties:
            available_difficulties = [1]
        
        # Bias towards current difficulty (70% current, 30% easier)
        if random.random() < 0.7 and difficulty in self.tasks_by_difficulty:
            task_pool = self.tasks_by_difficulty[difficulty]
        else:
            # Pick from any appropriate difficulty
            selected_difficulty = random.choice(available_difficulties)
            task_pool = self.tasks_by_difficulty[selected_difficulty]
        
        return random.choice(task_pool)
    
    def get_task_set_for_generation(self, generation: int, count: int = 5) -> List[str]:
        """Get multiple tasks for evaluation"""
        return [self.get_task_for_generation(generation) for _ in range(count)]
    
    def add_custom_tasks(self, difficulty: int, tasks: List[str]):
        """Add custom tasks at a specific difficulty level"""
        if difficulty not in self.tasks_by_difficulty:
            self.tasks_by_difficulty[difficulty] = []
        self.tasks_by_difficulty[difficulty].extend(tasks)
    
    def get_curriculum_stats(self, generation: int) -> Dict:
        """Get statistics about current curriculum state"""
        current_difficulty = self.get_difficulty_for_generation(generation)
        max_difficulty = max(self.tasks_by_difficulty.keys())
        
        return {
            "generation": generation,
            "current_difficulty": current_difficulty,
            "max_difficulty": max_difficulty,
            "progress_percentage": (current_difficulty / max_difficulty) * 100,
            "tasks_at_level": len(self.tasks_by_difficulty.get(current_difficulty, []))
        }


class AdaptiveCurriculum(TaskCurriculum):
    """
    Adaptive curriculum that adjusts difficulty based on population performance
    If population is doing too well, increase difficulty faster
    If struggling, slow down the increase
    """
    
    def __init__(self):
        super().__init__()
        self.performance_history = []
        self.difficulty_override = None
    
    def update_performance(self, generation: int, avg_fitness: float):
        """Track population performance to adapt curriculum"""
        self.performance_history.append({
            "generation": generation,
            "avg_fitness": avg_fitness
        })
        
        # Keep last 10 generations
        if len(self.performance_history) > 10:
            self.performance_history.pop(0)
    
    def get_adaptive_difficulty(self, generation: int) -> int:
        """Get difficulty adjusted for performance"""
        base_difficulty = self.get_difficulty_for_generation(generation)
        
        if self.difficulty_override:
            return self.difficulty_override
        
        # If we have enough history, adapt
        if len(self.performance_history) >= 5:
            recent_avg = sum(h["avg_fitness"] for h in self.performance_history[-5:]) / 5
            
            # If doing very well (>0.8 average), increase difficulty
            if recent_avg > 0.8:
                base_difficulty = min(15, base_difficulty + 2)
                print(f"📈 Curriculum adapted: difficulty increased to {base_difficulty} (high performance)")
            
            # If struggling (<0.4 average), decrease difficulty
            elif recent_avg < 0.4:
                base_difficulty = max(1, base_difficulty - 1)
                print(f"📉 Curriculum adapted: difficulty decreased to {base_difficulty} (low performance)")
        
        return base_difficulty
    
    def get_task_for_generation(self, generation: int) -> str:
        """Override to use adaptive difficulty"""
        difficulty = self.get_adaptive_difficulty(generation)
        
        available_difficulties = [d for d in self.tasks_by_difficulty.keys() if d <= difficulty]
        
        if not available_difficulties:
            available_difficulties = [1]
        
        if random.random() < 0.7 and difficulty in self.tasks_by_difficulty:
            task_pool = self.tasks_by_difficulty[difficulty]
        else:
            selected_difficulty = random.choice(available_difficulties)
            task_pool = self.tasks_by_difficulty[selected_difficulty]
        
        return random.choice(task_pool)


if __name__ == "__main__":
    # Demo curriculum
    curriculum = TaskCurriculum()
    
    print("Task Curriculum Demo\n")
    print("=" * 60)
    
    for gen in [1, 10, 25, 40, 60, 100, 150]:
        difficulty = curriculum.get_difficulty_for_generation(gen)
        task = curriculum.get_task_for_generation(gen)
        stats = curriculum.get_curriculum_stats(gen)
        
        print(f"\nGeneration {gen}:")
        print(f"  Difficulty: {difficulty}/15")
        print(f"  Progress: {stats['progress_percentage']:.1f}%")
        print(f"  Sample task: {task}")
    
    print("\n" + "=" * 60)
    print("\nAdaptive Curriculum Demo\n")
    
    adaptive = AdaptiveCurriculum()
    
    # Simulate high performance
    for gen in range(1, 21):
        adaptive.update_performance(gen, 0.85)  # High fitness
        task = adaptive.get_task_for_generation(gen)
        if gen % 5 == 0:
            print(f"Gen {gen}: {task[:60]}...")
