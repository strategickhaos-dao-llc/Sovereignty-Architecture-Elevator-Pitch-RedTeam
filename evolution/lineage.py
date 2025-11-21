#!/usr/bin/env python3
"""
Lineage Tracking and Visualization Module
Tracks ancestry and bloodlines through evolution
"""

import json
from typing import Dict, List, Set, Optional
from pathlib import Path
from collections import defaultdict


class LineageTracker:
    """Tracks and analyzes evolutionary lineages"""
    
    def __init__(self, ledger_path: str = "evolution_ledger.jsonl"):
        self.ledger_path = Path(ledger_path)
        self.lineage_map: Dict[str, Dict] = {}  # heir_id -> lineage info
        self.generation_data: List[Dict] = []
    
    def load_from_ledger(self):
        """Load lineage data from evolution ledger"""
        if not self.ledger_path.exists():
            print(f"⚠️  Ledger not found: {self.ledger_path}")
            return
        
        with open(self.ledger_path, 'r') as f:
            for line in f:
                entry = json.loads(line)
                self.generation_data.append(entry)
                
                # Extract best heir from each generation
                if "best_heir" in entry:
                    heir_data = entry["best_heir"]
                    heir_id = heir_data["id"]
                    
                    self.lineage_map[heir_id] = {
                        "id": heir_id,
                        "generation": heir_data["generation"],
                        "parent_id": heir_data.get("parent_id"),
                        "fitness": heir_data["fitness_score"],
                        "prompt": heir_data["system_prompt"]
                    }
        
        print(f"✅ Loaded {len(self.generation_data)} generations with {len(self.lineage_map)} heirs")
    
    def build_lineage_chain(self, heir_id: str) -> List[str]:
        """Build ancestry chain for a given heir"""
        chain = [heir_id]
        current_id = heir_id
        
        max_depth = 1000  # Prevent infinite loops
        depth = 0
        
        while depth < max_depth:
            if current_id not in self.lineage_map:
                break
            
            parent_id = self.lineage_map[current_id].get("parent_id")
            if not parent_id:
                break
            
            # Handle sexual reproduction (parent_id like "heir1+heir2")
            if "+" in parent_id:
                # For now, just track the first parent
                parent_id = parent_id.split("+")[0]
            
            chain.append(parent_id)
            current_id = parent_id
            depth += 1
        
        return chain
    
    def get_dominant_lineage(self) -> Optional[List[str]]:
        """Find the lineage that appears most in best performers"""
        if not self.generation_data:
            return None
        
        # Get the final generation's best heir
        final_gen = self.generation_data[-1]
        final_best = final_gen.get("best_heir", {}).get("id")
        
        if not final_best:
            return None
        
        return self.build_lineage_chain(final_best)
    
    def analyze_lineages(self) -> Dict:
        """Analyze lineage statistics"""
        if not self.lineage_map:
            return {}
        
        # Find all root ancestors (heirs with no parents)
        roots = [h_id for h_id, data in self.lineage_map.items() 
                if not data.get("parent_id")]
        
        # Count descendants for each root
        root_descendants = defaultdict(int)
        
        for heir_id in self.lineage_map.keys():
            chain = self.build_lineage_chain(heir_id)
            if chain:
                root = chain[-1]  # Oldest ancestor
                root_descendants[root] += 1
        
        # Find most successful lineage
        dominant_root = max(root_descendants.items(), key=lambda x: x[1]) if root_descendants else None
        
        # Calculate average fitness by generation
        fitness_by_gen = defaultdict(list)
        for gen_data in self.generation_data:
            gen_num = gen_data["generation"]
            avg_fit = gen_data["avg_fitness"]
            fitness_by_gen[gen_num].append(avg_fit)
        
        return {
            "total_heirs": len(self.lineage_map),
            "root_ancestors": len(roots),
            "dominant_lineage": {
                "root_id": dominant_root[0] if dominant_root else None,
                "descendant_count": dominant_root[1] if dominant_root else 0
            },
            "generations": len(self.generation_data),
            "final_avg_fitness": self.generation_data[-1]["avg_fitness"] if self.generation_data else 0,
            "final_best_fitness": self.generation_data[-1]["best_fitness"] if self.generation_data else 0
        }
    
    def print_lineage_tree(self, heir_id: str, max_depth: int = 10):
        """Print ASCII tree of lineage"""
        chain = self.build_lineage_chain(heir_id)[:max_depth]
        
        print(f"\n🌳 Lineage Tree for {heir_id}\n")
        
        for i, h_id in enumerate(chain):
            indent = "  " * i
            if h_id in self.lineage_map:
                info = self.lineage_map[h_id]
                gen = info["generation"]
                fitness = info["fitness"]
                print(f"{indent}└─ {h_id} (Gen {gen}, Fitness: {fitness:.3f})")
            else:
                print(f"{indent}└─ {h_id} (data not available)")
    
    def export_lineage_graph(self, output_file: str = "lineage_graph.dot"):
        """Export lineage as Graphviz DOT file for visualization"""
        with open(output_file, 'w') as f:
            f.write("digraph Lineage {\n")
            f.write("  rankdir=BT;\n")  # Bottom to top (oldest at bottom)
            f.write("  node [shape=box];\n\n")
            
            # Add nodes
            for heir_id, data in self.lineage_map.items():
                fitness = data["fitness"]
                gen = data["generation"]
                # Color by fitness
                color = "green" if fitness > 0.7 else "yellow" if fitness > 0.4 else "red"
                f.write(f'  "{heir_id}" [label="{heir_id}\\nGen {gen}\\nFit: {fitness:.2f}" fillcolor={color} style=filled];\n')
            
            f.write("\n")
            
            # Add edges
            for heir_id, data in self.lineage_map.items():
                parent_id = data.get("parent_id")
                if parent_id:
                    if "+" in parent_id:
                        # Sexual reproduction
                        parents = parent_id.split("+")
                        for p in parents:
                            f.write(f'  "{p}" -> "{heir_id}";\n')
                    else:
                        f.write(f'  "{parent_id}" -> "{heir_id}";\n')
            
            f.write("}\n")
        
        print(f"✅ Lineage graph exported to {output_file}")
        print(f"   Visualize with: dot -Tpng {output_file} -o lineage.png")


def visualize_evolution_progress(ledger_path: str = "evolution_ledger.jsonl"):
    """Print a summary of evolution progress"""
    tracker = LineageTracker(ledger_path)
    tracker.load_from_ledger()
    
    if not tracker.generation_data:
        print("No evolution data available yet.")
        return
    
    print("\n" + "=" * 70)
    print("EVOLUTION PROGRESS REPORT")
    print("=" * 70)
    
    analysis = tracker.analyze_lineages()
    
    print(f"\nGenerations completed: {analysis['generations']}")
    print(f"Total unique heirs: {analysis['total_heirs']}")
    print(f"Root ancestors: {analysis['root_ancestors']}")
    
    if analysis['dominant_lineage']['root_id']:
        print(f"\n🏆 Dominant Lineage:")
        print(f"   Root: {analysis['dominant_lineage']['root_id']}")
        print(f"   Descendants: {analysis['dominant_lineage']['descendant_count']}")
    
    print(f"\n📊 Current Performance:")
    print(f"   Average Fitness: {analysis['final_avg_fitness']:.3f}")
    print(f"   Best Fitness: {analysis['final_best_fitness']:.3f}")
    
    # Show fitness progression
    if len(tracker.generation_data) >= 5:
        print(f"\n📈 Fitness Progression (last 5 generations):")
        for gen_data in tracker.generation_data[-5:]:
            gen = gen_data['generation']
            avg_fit = gen_data['avg_fitness']
            best_fit = gen_data['best_fitness']
            bar_len = int(best_fit * 30)
            bar = "█" * bar_len + "░" * (30 - bar_len)
            print(f"   Gen {gen:3d}: {bar} Avg: {avg_fit:.3f} Best: {best_fit:.3f}")
    
    # Show dominant lineage tree
    dominant = tracker.get_dominant_lineage()
    if dominant and len(dominant) > 1:
        tracker.print_lineage_tree(dominant[0], max_depth=5)
    
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    # Demo lineage tracking
    visualize_evolution_progress()
