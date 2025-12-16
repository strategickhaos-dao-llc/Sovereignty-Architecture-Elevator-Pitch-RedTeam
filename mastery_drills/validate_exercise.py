#!/usr/bin/env python3
"""
Validate and display mastery drill exercises
Usage: python3 validate_exercise.py preterm_births_1_5_8.yaml
"""

import sys
import yaml
from pathlib import Path


def validate_exercise(yaml_file: str) -> bool:
    """Validate the structure of a mastery drill exercise."""
    try:
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
        
        # Required fields
        required_fields = ['section', 'title', 'answers']
        missing = [field for field in required_fields if field not in data]
        
        if missing:
            print(f"❌ Missing required fields: {missing}")
            return False
        
        # Validate answers structure
        answers = data.get('answers', {})
        if not all(key in answers for key in ['q1', 'q2', 'q3']):
            print("❌ Missing required answer keys (q1, q2, q3)")
            return False
        
        print("✅ Exercise structure is valid")
        return True
        
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False


def display_exercise(yaml_file: str):
    """Display exercise details in a formatted way."""
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    
    print("=" * 70)
    print(f"Section {data['section']}: {data['title']}")
    print("=" * 70)
    print()
    
    # Display basic info
    print(f"Category: {data.get('category', 'N/A')}")
    print(f"Difficulty: {data.get('difficulty', 'N/A')}")
    print(f"Bloom Level: {data.get('bloom_level', 'N/A')}")
    print()
    
    # Display answers
    print("ANSWERS:")
    print("-" * 70)
    answers = data.get('answers', {})
    for q, answer in sorted(answers.items()):
        print(f"  {q.upper()}: {answer}")
    print()
    
    # Display detailed explanations if available
    question_details = data.get('question_details', {})
    if question_details:
        print("DETAILED EXPLANATIONS:")
        print("-" * 70)
        for q_id, details in sorted(question_details.items()):
            print(f"\n{q_id.upper()}: {details.get('question', 'N/A')}")
            print(f"  Answer: {details.get('answer', 'N/A')}")
            if 'calculation' in details:
                print(f"  Calculation: {details['calculation']}")
            if 'method' in details:
                print(f"  Method: {details['method']}")
            if 'rationale' in details:
                print(f"  Rationale: {details['rationale']}")
        print()
    
    # Display FlameLang pattern if available
    flamelang = data.get('flamelang_pattern', {})
    if flamelang:
        print("FLAMELANG PATTERN:")
        print("-" * 70)
        print(f"Name: {flamelang.get('name', 'N/A')}")
        print(f"Description: {flamelang.get('description', 'N/A')}")
        
        if 'compiler_parallel' in flamelang:
            print(f"\nCompiler Insights:")
            print(flamelang['compiler_parallel'])
        print()
    
    # Display answer key summary
    answer_key = data.get('answer_key', {})
    if answer_key:
        fire = answer_key.get('fire_emoji', '🔥')
        sequence = answer_key.get('sequence', '')
        print(f"{fire} Fire: {sequence} {fire}")
        print()
    
    print("=" * 70)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_exercise.py <yaml_file>")
        print("\nExample:")
        print("  python3 validate_exercise.py preterm_births_1_5_8.yaml")
        sys.exit(1)
    
    yaml_file = sys.argv[1]
    
    # If not absolute path, look in current directory
    if not Path(yaml_file).is_absolute():
        yaml_file = Path(__file__).parent / yaml_file
    
    if not Path(yaml_file).exists():
        print(f"❌ File not found: {yaml_file}")
        sys.exit(1)
    
    print(f"Validating: {yaml_file}")
    print()
    
    if validate_exercise(yaml_file):
        print()
        display_exercise(yaml_file)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
