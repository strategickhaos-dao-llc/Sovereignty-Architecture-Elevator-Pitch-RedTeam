#!/usr/bin/env python3
"""
SME Content Analyzer
Analyzes crawled content using Ollama for specific topics
"""

import os
import json
import time
import argparse
from pathlib import Path
from typing import Dict, List
import requests

# Configuration
DATA_DIR = Path("/app/data/processed")
OUTPUT_DIR = Path("/app/output")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3:70b")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "10"))

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


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


def analyze_resource(resource_data: Dict, topic: str) -> Dict:
    """Analyze a resource for specific topic"""
    
    title = resource_data.get("title", "Unknown")
    category = resource_data.get("category", "unknown")
    text = resource_data.get("text", "")
    
    # Truncate text if too long (keep first 4000 chars for analysis)
    text_sample = text[:4000] if len(text) > 4000 else text
    
    prompt = f"""Analyze this technical documentation for the topic: {topic}

Title: {title}
Category: {category}

Content Sample:
{text_sample}

Please provide:
1. Key concepts related to {topic}
2. Practical implementation details
3. Best practices mentioned
4. Common pitfalls or warnings
5. Relevance score (0-10) for {topic}

Be concise but thorough."""

    print(f"  Analyzing with {MODEL_NAME}...")
    analysis = ollama_chat(prompt)
    
    # Extract relevance score if possible
    relevance_score = 5  # Default
    if "relevance score:" in analysis.lower():
        try:
            score_line = [line for line in analysis.split('\n') if 'relevance score:' in line.lower()][0]
            score_str = score_line.split(':')[-1].strip().split('/')[0].strip()
            relevance_score = int(score_str)
        except:
            pass
    
    return {
        "resource_id": resource_data.get("resource_id"),
        "title": title,
        "category": category,
        "topic": topic,
        "relevance_score": relevance_score,
        "analysis": analysis,
        "analyzed_at": time.time()
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze SME resources for specific topic")
    parser.add_argument("--topic", required=True, help="Topic to analyze for")
    args = parser.parse_args()
    
    topic = args.topic
    
    print("=" * 80)
    print(f"SME Content Analyzer - Topic: {topic}")
    print("=" * 80)
    print(f"Data directory: {DATA_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Ollama host: {OLLAMA_HOST}")
    print(f"Model: {MODEL_NAME}")
    print()
    
    # Check Ollama availability
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        response.raise_for_status()
        print("✓ Ollama is available")
    except Exception as e:
        print(f"✗ Ollama not available: {e}")
        print("Please ensure Ollama is running")
        return
    
    # Find processed files
    processed_files = list(DATA_DIR.glob("*.json"))
    print(f"\nFound {len(processed_files)} processed resources")
    
    if not processed_files:
        print("No processed files found. Run the crawler first.")
        return
    
    # Analyze resources
    results = []
    
    for i, file_path in enumerate(processed_files[:BATCH_SIZE], 1):
        print(f"\n[{i}/{min(len(processed_files), BATCH_SIZE)}] Processing {file_path.name}")
        
        try:
            with open(file_path, 'r') as f:
                resource_data = json.load(f)
            
            # Analyze
            result = analyze_resource(resource_data, topic)
            results.append(result)
            
            print(f"  ✓ Analysis complete (relevance: {result['relevance_score']}/10)")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    # Sort by relevance
    results.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    # Save results
    output_file = OUTPUT_DIR / f"analysis_{topic}_{int(time.time())}.json"
    with open(output_file, 'w') as f:
        json.dump({
            "topic": topic,
            "analyzed_count": len(results),
            "results": results,
            "timestamp": time.time()
        }, f, indent=2)
    
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)
    print(f"Topic: {topic}")
    print(f"Resources analyzed: {len(results)}")
    print(f"Output: {output_file}")
    
    # Top 5 most relevant
    print("\nTop 5 Most Relevant Resources:")
    for i, result in enumerate(results[:5], 1):
        print(f"  {i}. [{result['relevance_score']}/10] {result['title']}")
    
    print("\n✓ Analysis complete!")


if __name__ == "__main__":
    main()
