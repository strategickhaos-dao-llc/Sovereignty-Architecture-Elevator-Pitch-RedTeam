#!/usr/bin/env python3
"""
zyBooks Solver - Main Entry Point
Process zyBooks content and generate answers

Usage:
    python main.py <input_file> [--format yaml|rapid|json|table|vessel]
    python main.py --stdin [--format yaml|rapid|json|table|vessel]
"""

import sys
import argparse
from pathlib import Path

from parser import ZyBooksParser
from solver import ZyBooksSolver
from responder import ZyBooksResponder


def process_zybooks_content(content: str, output_format: str = "yaml") -> str:
    """
    Main processing pipeline
    1. Parse zyBooks content
    2. Solve questions
    3. Format response
    """
    # Step 1: Parse
    parser = ZyBooksParser()
    parsed = parser.parse(content)
    
    if not parsed.get("detected", False):
        return "❌ ERROR: Content does not appear to be zyBooks format"
    
    section = parsed.get("section", "unknown")
    questions = parsed.get("questions", [])
    
    if not questions:
        return "❌ ERROR: No questions found in content"
    
    # Step 2: Solve
    solver = ZyBooksSolver()
    answers = solver.solve(questions)
    answer_dicts = solver.get_answers()
    
    # Step 3: Respond
    responder = ZyBooksResponder()
    
    if output_format == "vessel":
        return responder.vessel_response(section, answer_dicts)
    else:
        return responder.respond(section, answer_dicts, output_format)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="zyBooks Solver - Auto-process zyBooks content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Process from file
    python main.py input.txt
    
    # Process from stdin
    cat input.txt | python main.py --stdin
    
    # Use different output format
    python main.py input.txt --format rapid
    
    # VESSEL MODE (minimal output)
    python main.py input.txt --format vessel
        """
    )
    
    parser.add_argument(
        "input_file",
        nargs="?",
        help="Input file containing zyBooks content"
    )
    
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read content from stdin instead of file"
    )
    
    parser.add_argument(
        "--format",
        choices=["yaml", "rapid", "json", "table", "vessel"],
        default="yaml",
        help="Output format (default: yaml)"
    )
    
    parser.add_argument(
        "--save",
        help="Save parsed questions to JSON file"
    )
    
    args = parser.parse_args()
    
    # Read input
    if args.stdin:
        content = sys.stdin.read()
    elif args.input_file:
        input_path = Path(args.input_file)
        if not input_path.exists():
            print(f"❌ ERROR: File not found: {args.input_file}", file=sys.stderr)
            sys.exit(1)
        content = input_path.read_text()
    else:
        parser.print_help()
        sys.exit(1)
    
    # Process
    try:
        result = process_zybooks_content(content, args.format)
        print(result)
        
        # Save if requested
        if args.save:
            zyparser = ZyBooksParser()
            zyparser.parse(content)
            zyparser.save_to_file(args.save)
            print(f"\n✅ Saved parsed questions to: {args.save}", file=sys.stderr)
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
