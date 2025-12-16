#!/usr/bin/env python3
"""
zyBooks Solver - Main Entry Point
Process zyBooks content and return answers in VESSEL MODE
"""

import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from parser import ZyBooksParser, Question
from solver import ZyBooksSolver, Answer
from responder import ZyBooksResponder


def process_zybooks_content(content: str, output_format: str = 'vessel', 
                            save_results: bool = True) -> str:
    """
    Main processing pipeline for zyBooks content
    
    Args:
        content: Raw zyBooks content text
        output_format: 'vessel', 'yaml', or 'detailed'
        save_results: Whether to save results to training directory
    
    Returns:
        Formatted answer string
    """
    # Step 1: Parse content
    parser = ZyBooksParser()
    
    if not parser.detect_zybooks_content(content):
        return "❌ No zyBooks content detected. Please paste valid zyBooks questions."
    
    questions = parser.parse(content)
    
    if not questions:
        return "❌ No questions found in content."
    
    section = parser.extract_section(content)
    
    # Step 2: Solve questions
    solver = ZyBooksSolver()
    answers = solver.solve(questions)
    
    # Step 3: Format response
    responder = ZyBooksResponder(answers, section)
    
    if output_format == 'vessel':
        output = responder.to_vessel_mode()
    elif output_format == 'yaml':
        output = responder.to_yaml()
    elif output_format == 'detailed':
        output = responder.to_detailed()
    else:
        output = responder.to_vessel_mode()
    
    # Step 4: Save results if requested
    if save_results and section:
        save_training_data(questions, answers, section)
    
    return output


def save_training_data(questions: list, answers: list, section: str):
    """Save processed data for FlameLang training"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create sections directory if not exists
    sections_dir = Path(__file__).parent.parent.parent / 'training' / 'zybooks' / 'sections'
    sections_dir.mkdir(parents=True, exist_ok=True)
    
    # Save section data
    section_file = sections_dir / f"section_{section}_{timestamp}.json"
    
    data = {
        'section': section,
        'timestamp': timestamp,
        'questions': [
            {
                'id': q.id,
                'type': q.type,
                'text': q.text,
                'options': q.options,
                'section': q.section
            }
            for q in questions
        ],
        'answers': [
            {
                'question_id': a.question_id,
                'answer': a.answer,
                'confidence': a.confidence,
                'reasoning': a.reasoning,
                'type': a.type
            }
            for a in answers
        ]
    }
    
    with open(section_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Extract patterns by type
    patterns_dir = sections_dir.parent / 'patterns'
    patterns_dir.mkdir(exist_ok=True)
    
    for question in questions:
        pattern_file = patterns_dir / f"{question.type}_patterns.jsonl"
        with open(pattern_file, 'a') as f:
            f.write(json.dumps({
                'text': question.text,
                'type': question.type,
                'section': section,
                'timestamp': timestamp
            }) + '\n')


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='zyBooks Solver - Auto-process zyBooks content',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process from file
  python main.py training/zybooks/PASTE_HERE.md
  
  # Process from stdin
  cat content.txt | python main.py -
  
  # Output in YAML format
  python main.py content.txt --format yaml
  
  # Detailed output with reasoning
  python main.py content.txt --format detailed
        """
    )
    
    parser.add_argument(
        'input',
        help='Input file path or "-" for stdin'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['vessel', 'yaml', 'detailed'],
        default='vessel',
        help='Output format (default: vessel)'
    )
    
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='Do not save results to training directory'
    )
    
    args = parser.parse_args()
    
    # Read input
    try:
        if args.input == '-':
            content = sys.stdin.read()
        else:
            with open(args.input, 'r') as f:
                content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: File '{args.input}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading input: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Process content
    try:
        output = process_zybooks_content(
            content,
            output_format=args.format,
            save_results=not args.no_save
        )
        print(output)
    except Exception as e:
        print(f"❌ Error processing content: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
