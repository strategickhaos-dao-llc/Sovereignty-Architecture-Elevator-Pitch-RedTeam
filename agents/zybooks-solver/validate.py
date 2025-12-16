#!/usr/bin/env python3
"""
Validation script for zyBooks solver
Compares solver output against expected answers
"""

import sys
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from parser import parse_zybooks_content
from solver import solve_questions


def validate_answers(content_file: str, expected_file: str) -> dict:
    """
    Validate solver answers against expected results
    
    Returns:
        dict with validation results
    """
    # Load content
    with open(content_file, 'r') as f:
        content = f.read()
    
    # Load expected answers
    with open(expected_file, 'r') as f:
        expected = yaml.safe_load(f)
    
    # Parse and solve
    questions = parse_zybooks_content(content)
    answers = solve_questions(questions)
    
    # Compare
    results = {
        'total': len(answers),
        'correct': 0,
        'incorrect': 0,
        'details': []
    }
    
    for answer in answers:
        qid = answer.question_id
        expected_answer = expected['answers'].get(qid, {}).get('answer')
        
        # Normalize for comparison
        actual = str(answer.answer).upper().strip()
        if expected_answer is not None:
            # Handle boolean values from YAML (True/False)
            if isinstance(expected_answer, bool):
                expected_str = str(expected_answer).upper()
            else:
                expected_str = str(expected_answer).upper().strip()
        else:
            expected_str = None
        
        # For numeric answers, compare values not strings
        if answer.type == 'numeric' and expected_str:
            try:
                is_correct = float(actual) == float(expected_str)
            except ValueError:
                is_correct = actual == expected_str
        else:
            is_correct = actual == expected_str
        
        if is_correct:
            results['correct'] += 1
            status = '✓'
        else:
            results['incorrect'] += 1
            status = '✗'
        
        results['details'].append({
            'question_id': qid,
            'expected': expected_str,
            'actual': actual,
            'correct': is_correct,
            'confidence': answer.confidence,
            'status': status
        })
    
    return results


def print_validation_report(results: dict):
    """Print a formatted validation report"""
    print("=" * 60)
    print("zyBooks Solver Validation Report")
    print("=" * 60)
    print()
    
    accuracy = (results['correct'] / results['total'] * 100) if results['total'] > 0 else 0
    
    print(f"Total Questions: {results['total']}")
    print(f"Correct: {results['correct']} ✓")
    print(f"Incorrect: {results['incorrect']} ✗")
    print(f"Accuracy: {accuracy:.1f}%")
    print()
    
    if results['incorrect'] > 0:
        print("Details of incorrect answers:")
        print("-" * 60)
        for detail in results['details']:
            if not detail['correct']:
                print(f"{detail['status']} {detail['question_id']}:")
                print(f"  Expected: {detail['expected']}")
                print(f"  Actual:   {detail['actual']}")
                print(f"  Confidence: {detail['confidence']:.2f}")
                print()
    else:
        print("🎉 All answers correct!")
    
    print("=" * 60)
    
    return accuracy


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate zyBooks solver accuracy')
    parser.add_argument('content', help='Path to content file')
    parser.add_argument('expected', help='Path to expected answers YAML')
    
    args = parser.parse_args()
    
    try:
        results = validate_answers(args.content, args.expected)
        accuracy = print_validation_report(results)
        
        # Exit with error code if accuracy is below 80%
        sys.exit(0 if accuracy >= 80.0 else 1)
        
    except Exception as e:
        print(f"❌ Validation failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)
