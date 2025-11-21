#!/usr/bin/env python3
"""
Evolution Path Matcher
Maps SME resources to evolution path items
"""

import os
import json
import yaml
import time
from pathlib import Path
from typing import Dict, List
import requests

# Configuration
RESOURCES_FILE = Path("/app/sme-resources.yaml")
EVOLUTION_FILE = Path("/app/evolution-path.yaml")
ANALYSIS_DIR = Path("/app/output")
RESULTS_DIR = Path("/app/results")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3:70b")

# Create results directory
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def load_yaml(file_path: Path) -> Dict:
    """Load YAML file"""
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)


def ollama_chat(prompt: str, model: str = MODEL_NAME) -> str:
    """Send a chat request to Ollama"""
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        return result.get("response", "")
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return ""


def match_resources_to_item(evolution_item: Dict, resources: List[Dict]) -> List[Dict]:
    """Match SME resources to an evolution item"""
    
    item_id = evolution_item['id']
    item_title = evolution_item['title']
    item_category = evolution_item.get('category', '')
    item_outcome = evolution_item.get('outcome', '')
    
    print(f"\n[{item_id}] {item_title}")
    print(f"  Category: {item_category}")
    
    # Filter resources by category relevance first
    relevant_categories = {
        'infrastructure': ['container_orchestration', 'infrastructure', 'storage', 'networking'],
        'compute': ['container_orchestration', 'ai_ml', 'programming'],
        'networking': ['networking', 'security', 'devops'],
        'ai-training': ['ai_ml', 'programming', 'compute'],
        'ai-deployment': ['ai_ml', 'container_orchestration', 'devops'],
        'ai-audio': ['ai_ml', 'iot'],
        'ai-image': ['ai_ml'],
        'security': ['security', 'networking'],
        'storage': ['storage', 'database', 'distributed_systems'],
        'database': ['database', 'storage'],
        'monitoring': ['monitoring', 'observability', 'devops'],
        'devops': ['devops', 'programming'],
    }
    
    # Get relevant resource categories
    target_categories = relevant_categories.get(item_category, [item_category])
    
    # Filter resources
    candidate_resources = []
    for resource in resources:
        resource_category = resource.get('category', '')
        if resource_category in target_categories:
            candidate_resources.append(resource)
    
    print(f"  Found {len(candidate_resources)} potentially relevant resources")
    
    if not candidate_resources:
        return []
    
    # Use LLM to rank top resources
    resources_summary = "\n".join([
        f"- [{r['id']}] {r['title']} ({r.get('category', 'unknown')})"
        for r in candidate_resources[:20]  # Limit to top 20 candidates
    ])
    
    prompt = f"""Match relevant documentation resources to this infrastructure evolution item:

Evolution Item #{item_id}: {item_title}
Category: {item_category}
Expected Outcome: {item_outcome}

Available Resources:
{resources_summary}

Which resources (by ID) are most relevant for implementing this evolution item?
List the top 5 resource IDs and briefly explain why each is relevant.
Format: [ID] - Brief reason"""

    print("  Analyzing with LLM...")
    matching_response = ollama_chat(prompt)
    
    # Parse response to extract IDs
    matched_ids = []
    for line in matching_response.split('\n'):
        if line.strip().startswith('[') and ']' in line:
            try:
                id_str = line.split('[')[1].split(']')[0]
                resource_id = int(id_str)
                matched_ids.append(resource_id)
            except:
                pass
    
    # Get full resource data for matched IDs
    matched_resources = [r for r in resources if r['id'] in matched_ids]
    
    print(f"  ✓ Matched {len(matched_resources)} resources")
    
    return {
        'evolution_item_id': item_id,
        'evolution_item_title': item_title,
        'matched_resources': matched_resources,
        'llm_explanation': matching_response,
        'matched_count': len(matched_resources)
    }


def main():
    print("=" * 80)
    print("Evolution Path Matcher")
    print("=" * 80)
    print(f"Resources: {RESOURCES_FILE}")
    print(f"Evolution: {EVOLUTION_FILE}")
    print(f"Results: {RESULTS_DIR}")
    print()
    
    # Check Ollama availability
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        response.raise_for_status()
        print("✓ Ollama is available\n")
    except Exception as e:
        print(f"✗ Ollama not available: {e}")
        print("Please ensure Ollama is running")
        return
    
    # Load data
    print("Loading data...")
    resources_data = load_yaml(RESOURCES_FILE)
    evolution_data = load_yaml(EVOLUTION_FILE)
    
    resources = resources_data.get('resources', [])
    evolution_items = evolution_data.get('evolution_items', [])
    
    print(f"  Loaded {len(resources)} SME resources")
    print(f"  Loaded {len(evolution_items)} evolution items")
    
    # Process each evolution item
    all_matches = []
    
    # Process first 20 items as a sample (can be extended)
    for item in evolution_items[:20]:
        try:
            match_result = match_resources_to_item(item, resources)
            all_matches.append(match_result)
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    # Save results
    output_file = RESULTS_DIR / f"evolution_matches_{int(time.time())}.json"
    with open(output_file, 'w') as f:
        json.dump({
            "total_items": len(evolution_items),
            "processed_items": len(all_matches),
            "matches": all_matches,
            "timestamp": time.time()
        }, f, indent=2)
    
    # Generate summary
    print("\n" + "=" * 80)
    print("MATCHING SUMMARY")
    print("=" * 80)
    print(f"Evolution items processed: {len(all_matches)}")
    print(f"Total matches created: {sum(m['matched_count'] for m in all_matches)}")
    print(f"Average matches per item: {sum(m['matched_count'] for m in all_matches) / len(all_matches):.1f}")
    print(f"\nResults saved to: {output_file}")
    
    # Top matched items
    print("\nTop Matched Items:")
    sorted_matches = sorted(all_matches, key=lambda x: x['matched_count'], reverse=True)
    for i, match in enumerate(sorted_matches[:5], 1):
        print(f"  {i}. [{match['matched_count']} resources] {match['evolution_item_title']}")
    
    print("\n✓ Matching complete!")


if __name__ == "__main__":
    main()
