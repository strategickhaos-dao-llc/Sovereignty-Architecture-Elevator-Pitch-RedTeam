#!/usr/bin/env python3
"""
Lineage Tracking - Ancestry and Bloodline Analysis
Track which genetic lines dominate over generations
"""

import json
from typing import Dict, List, Set
from pathlib import Path
from collections import defaultdict

class LineageTracker:
    """Tracks heir lineages and bloodlines"""
    
    def __init__(self):
        self.lineages = {}  # heir_id -> lineage list
        self.bloodline_stats = defaultdict(int)  # ancestor_id -> descendant count
        
    def register_heir(self, heir_id: str, parent_id: str = None):
        """
        Register a new heir and track its lineage
        
        Args:
            heir_id: ID of the new heir
            parent_id: ID of parent (None for generation 0)
        """
        if parent_id is None:
            # Generation 0 - founder
            self.lineages[heir_id] = [heir_id]
        elif '+' in parent_id:
            # Sexual reproduction - two parents
            parent_ids = parent_id.split('+')
            # Inherit from first parent's lineage
            parent1_lineage = self.lineages.get(parent_ids[0], [parent_ids[0]])
            self.lineages[heir_id] = parent1_lineage + [heir_id]
            
            # Track both bloodlines
            for p_id in parent_ids:
                if p_id in self.lineages:
                    founder = self.lineages[p_id][0]
                    self.bloodline_stats[founder] += 1
        else:
            # Asexual reproduction - single parent
            parent_lineage = self.lineages.get(parent_id, [parent_id])
            self.lineages[heir_id] = parent_lineage + [heir_id]
            
            # Track bloodline
            founder = parent_lineage[0]
            self.bloodline_stats[founder] += 1
    
    def get_lineage(self, heir_id: str) -> List[str]:
        """Get full lineage for an heir"""
        return self.lineages.get(heir_id, [])
    
    def get_generation_depth(self, heir_id: str) -> int:
        """Get how many generations deep this heir is from its founder"""
        lineage = self.lineages.get(heir_id, [])
        return len(lineage) - 1
    
    def get_founder(self, heir_id: str) -> str:
        """Get the original founder of this heir's bloodline"""
        lineage = self.lineages.get(heir_id, [])
        return lineage[0] if lineage else heir_id
    
    def get_dominant_bloodlines(self, top_n: int = 5) -> List[Dict]:
        """
        Get the most successful bloodlines
        
        Args:
            top_n: Number of top bloodlines to return
            
        Returns:
            List of dicts with bloodline info
        """
        sorted_bloodlines = sorted(
            self.bloodline_stats.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        result = []
        for founder_id, descendant_count in sorted_bloodlines[:top_n]:
            result.append({
                "founder_id": founder_id,
                "descendants": descendant_count,
                "lineage_depth": max(
                    [len(self.lineages.get(heir_id, [])) 
                     for heir_id in self.lineages.keys() 
                     if self.lineages[heir_id][0] == founder_id],
                    default=0
                )
            })
        
        return result
    
    def get_bloodline_diversity(self) -> Dict:
        """Calculate diversity metrics for current population"""
        active_founders = set()
        for lineage in self.lineages.values():
            if lineage:
                active_founders.add(lineage[0])
        
        total_heirs = len(self.lineages)
        unique_bloodlines = len(active_founders)
        
        return {
            "total_heirs": total_heirs,
            "unique_bloodlines": unique_bloodlines,
            "diversity_ratio": unique_bloodlines / total_heirs if total_heirs > 0 else 0,
            "active_founders": list(active_founders)
        }
    
    def analyze_convergence(self) -> Dict:
        """
        Analyze if population is converging to a single bloodline
        
        Returns:
            Dict with convergence analysis
        """
        diversity = self.get_bloodline_diversity()
        dominant = self.get_dominant_bloodlines(top_n=3)
        
        total_descendants = sum(self.bloodline_stats.values())
        
        if not dominant:
            return {
                "converging": False,
                "dominant_bloodline": None,
                "dominance_percent": 0
            }
        
        top_bloodline = dominant[0]
        dominance = (top_bloodline["descendants"] / total_descendants * 100) if total_descendants > 0 else 0
        
        return {
            "converging": dominance > 60,  # If one bloodline has >60% descendants
            "dominant_bloodline": top_bloodline["founder_id"],
            "dominance_percent": dominance,
            "diversity_ratio": diversity["diversity_ratio"],
            "top_bloodlines": dominant
        }
    
    def export_lineage_graph(self, output_file: str = "lineage_graph.json"):
        """
        Export lineage data for visualization
        
        Creates a graph structure suitable for visualization tools
        """
        nodes = []
        edges = []
        
        # Create nodes for each heir
        for heir_id, lineage in self.lineages.items():
            generation = len(lineage) - 1
            founder = lineage[0]
            
            nodes.append({
                "id": heir_id,
                "generation": generation,
                "founder": founder,
                "is_founder": generation == 0
            })
            
            # Create edges from parent to child
            if len(lineage) > 1:
                parent = lineage[-2]
                edges.append({
                    "from": parent,
                    "to": heir_id
                })
        
        graph_data = {
            "nodes": nodes,
            "edges": edges,
            "bloodline_stats": dict(self.bloodline_stats),
            "dominant_bloodlines": self.get_dominant_bloodlines()
        }
        
        with open(output_file, 'w') as f:
            json.dump(graph_data, f, indent=2)
        
        print(f"📊 Lineage graph exported to {output_file}")
        return graph_data
    
    def save_state(self, filename: str = "lineage_state.json"):
        """Save lineage tracker state to file"""
        state = {
            "lineages": self.lineages,
            "bloodline_stats": dict(self.bloodline_stats)
        }
        
        with open(filename, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_state(self, filename: str = "lineage_state.json") -> bool:
        """Load lineage tracker state from file"""
        try:
            with open(filename, 'r') as f:
                state = json.load(f)
            
            self.lineages = state.get("lineages", {})
            self.bloodline_stats = defaultdict(int, state.get("bloodline_stats", {}))
            
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"❌ Error loading lineage state: {e}")
            return False
