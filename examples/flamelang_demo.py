#!/usr/bin/env python3
"""
FlameLang ZyBooks Solver - Demonstration Script
Artifact: INV-083
Operator: Domenic Garza | Strategickhaos DAO LLC
"""

import yaml
import sys
from pathlib import Path

def load_solver():
    """Load the FlameLang ZyBooks Solver pattern rules"""
    solver_path = Path(__file__).parent.parent / "flamelang_zybooks_solver_v1.yaml"
    with open(solver_path, 'r') as f:
        return yaml.safe_load(f)

def classify_question(question, solver):
    """Layer 1: Classify question type"""
    classification = solver['layer_1_classification']
    
    for qtype, config in classification.items():
        for trigger in config['triggers']:
            if trigger.lower() in question.lower():
                return {
                    'type': qtype,
                    'output_type': config['output_type'],
                    'trigger': trigger
                }
    
    return {'type': 'unknown', 'output_type': 'UNKNOWN', 'trigger': None}

def match_pattern(question, solver):
    """Layer 3: Match pattern rules"""
    rules = solver['layer_3_rules']
    q_lower = question.lower()
    
    # Check bar chart rules
    if 'bar chart' in q_lower or 'chart' in q_lower:
        for rule in rules['bar_chart_rules']:
            pattern_keywords = [k.strip() for k in rule['pattern'].split('+')]
            # Check if all keywords are present in question
            if all(keyword in q_lower for keyword in pattern_keywords):
                return rule
    
    # Check orientation rules
    if 'horizontal' in q_lower or 'vertical' in q_lower:
        for rule in rules['orientation_rules']:
            pattern_keywords = [k.strip() for k in rule['pattern'].split('+')]
            if all(keyword in q_lower for keyword in pattern_keywords):
                return rule
    
    # Check trend rules
    if any(word in q_lower for word in ['increased', 'decreased', 'trend', 'over time']):
        for rule in rules['trend_rules']:
            pattern_keywords = [k.strip() for k in rule['pattern'].split('+')]
            if all(keyword in q_lower for keyword in pattern_keywords):
                return rule
    
    # Fallback: Check for gridlines
    if 'gridline' in q_lower:
        for rule in rules['bar_chart_rules']:
            if 'gridline' in rule['pattern']:
                return rule
    
    # Fallback: Check for precise values
    if 'precise' in q_lower and 'value' in q_lower:
        for rule in rules['bar_chart_rules']:
            if 'precise values' in rule['pattern']:
                return rule
    
    # Fallback: Check for relative values
    if 'relative' in q_lower and 'value' in q_lower:
        for rule in rules['bar_chart_rules']:
            if 'relative values' in rule['pattern']:
                return rule
    
    # Fallback: Check for long labels
    if 'long' in q_lower and 'label' in q_lower:
        for rule in rules['orientation_rules']:
            if 'long labels' in rule['pattern']:
                return rule
    
    return None

def calculate_confidence(rule, question):
    """Layer 4: Calculate confidence score"""
    if not rule:
        return 0.5
    
    # High confidence for direct matches
    if 'true or false' in question.lower():
        return 0.95
    
    # Medium confidence for pattern matches
    return 0.80

def solve_question(question):
    """
    Solve a zyBooks question using the FlameLang pattern compiler
    
    Args:
        question: Natural language question string
        
    Returns:
        dict: {answer, confidence, reason}
    """
    solver = load_solver()
    
    # Layer 1: Classify
    qtype = classify_question(question, solver)
    print(f"📊 Question Type: {qtype['type']}")
    
    # Layer 2: Extract semantic roots (simplified)
    print(f"🔤 Semantic Analysis: Processing...")
    
    # Layer 3: Match pattern
    rule = match_pattern(question, solver)
    if not rule:
        return {
            'answer': 'UNKNOWN',
            'confidence': 0.0,
            'reason': 'No matching pattern rule found'
        }
    
    print(f"✓ Pattern Matched: {rule['pattern']}")
    
    # Layer 4: Confidence
    confidence = calculate_confidence(rule, question)
    
    # Layer 5: Output
    result = {
        'answer': rule['answer'],
        'confidence': confidence,
        'reason': rule['reason']
    }
    
    return result

def demo():
    """Run demonstration with example questions"""
    print("=" * 80)
    print("🔥 FLAMELANG ZYBOOKS SOLVER v1.0 - DEMONSTRATION")
    print("=" * 80)
    print()
    
    examples = [
        "A bar chart excels at showing precise values. True or False?",
        "Horizontal bar charts are preferable when you have long category labels. True or False?",
        "Adding more gridlines to a chart always makes it better. True or False?",
    ]
    
    for i, question in enumerate(examples, 1):
        print(f"\n{'─' * 80}")
        print(f"Question {i}:")
        print(f"  {question}")
        print()
        
        result = solve_question(question)
        
        print()
        print("📝 ANSWER:")
        print(f"  answer: {result['answer']}")
        print(f"  confidence: {result['confidence']:.2f}")
        print(f"  reason: \"{result['reason']}\"")
    
    print()
    print("=" * 80)
    print("✓ Demonstration Complete")
    print("=" * 80)

def interactive():
    """Interactive mode for testing questions"""
    print("=" * 80)
    print("🔥 FLAMELANG ZYBOOKS SOLVER v1.0 - INTERACTIVE MODE")
    print("=" * 80)
    print()
    print("Enter questions (or 'quit' to exit):")
    print()
    
    while True:
        try:
            question = input("❓ Question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                break
            
            if not question:
                continue
            
            print()
            result = solve_question(question)
            print()
            print("📝 ANSWER:")
            print(f"  answer: {result['answer']}")
            print(f"  confidence: {result['confidence']:.2f}")
            print(f"  reason: \"{result['reason']}\"")
            print()
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n✓ Goodbye!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive()
    else:
        demo()
