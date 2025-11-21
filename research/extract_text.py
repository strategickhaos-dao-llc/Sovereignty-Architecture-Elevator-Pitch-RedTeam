#!/usr/bin/env python3
"""
Text Extraction for Research Automation
Extracts clean text from HTML pages for embedding/RAG pipelines
"""

import os
import sys
import json
import argparse
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
import re


class TextExtractor(HTMLParser):
    """Simple HTML text extractor"""
    
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.in_script = False
        self.in_style = False
        
    def handle_starttag(self, tag, attrs):
        if tag.lower() in ['script', 'style']:
            self.in_script = True
            self.in_style = True
            
    def handle_endtag(self, tag):
        if tag.lower() in ['script', 'style']:
            self.in_script = False
            self.in_style = False
            
    def handle_data(self, data):
        if not (self.in_script or self.in_style):
            self.text_parts.append(data)
            
    def get_text(self):
        return ' '.join(self.text_parts)


def clean_text(text):
    """Clean and normalize extracted text"""
    # Unescape HTML entities
    text = unescape(text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove excessive punctuation
    text = re.sub(r'[^\w\s.,;:!?()\-\'\"]+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def extract_text_from_html(html_content):
    """Extract clean text from HTML"""
    try:
        parser = TextExtractor()
        parser.feed(html_content)
        raw_text = parser.get_text()
        return clean_text(raw_text)
    except Exception as e:
        print(f"Warning: Error extracting text: {e}", file=sys.stderr)
        return ""


def process_department(dept_name, raw_pages_dir, output_dir):
    """Process all HTML files for a department"""
    dept_dir = raw_pages_dir / dept_name
    
    if not dept_dir.exists():
        print(f"Error: Department directory not found: {dept_dir}")
        return False
        
    output_dept_dir = output_dir / dept_name
    output_dept_dir.mkdir(parents=True, exist_ok=True)
    
    html_files = sorted(dept_dir.glob("page_*.html"))
    
    if not html_files:
        print(f"Warning: No HTML files found in {dept_dir}")
        return False
    
    print(f"Processing {len(html_files)} files for department: {dept_name}")
    
    processed = 0
    failed = 0
    total_chars = 0
    
    for html_file in html_files:
        try:
            # Read HTML
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()
            
            # Extract text
            text = extract_text_from_html(html_content)
            
            if len(text) > 100:  # Only save if we got meaningful text
                # Save extracted text
                output_file = output_dept_dir / html_file.name.replace('.html', '.txt')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                processed += 1
                total_chars += len(text)
            else:
                failed += 1
                
        except Exception as e:
            print(f"Error processing {html_file}: {e}", file=sys.stderr)
            failed += 1
    
    # Save metadata
    metadata = {
        "department": dept_name,
        "total_files": len(html_files),
        "processed": processed,
        "failed": failed,
        "total_characters": total_chars,
        "avg_chars_per_file": total_chars // processed if processed > 0 else 0,
        "output_directory": str(output_dept_dir)
    }
    
    with open(output_dept_dir / "extraction_metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"  ✓ Processed: {processed}/{len(html_files)} files")
    print(f"  ✓ Total characters: {total_chars:,}")
    print(f"  ✓ Avg chars/file: {metadata['avg_chars_per_file']:,}")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Extract text from HTML pages for embedding pipelines'
    )
    parser.add_argument(
        'departments',
        nargs='*',
        help='Departments to process (default: all)'
    )
    parser.add_argument(
        '--raw-dir',
        default='raw_pages',
        help='Directory containing raw HTML pages (default: raw_pages)'
    )
    parser.add_argument(
        '--output-dir',
        default='extracted_text',
        help='Output directory for extracted text (default: extracted_text)'
    )
    
    args = parser.parse_args()
    
    # Resolve paths
    script_dir = Path(__file__).parent
    raw_pages_dir = script_dir / args.raw_dir
    output_dir = script_dir / args.output_dir
    
    if not raw_pages_dir.exists():
        print(f"Error: Raw pages directory not found: {raw_pages_dir}")
        return 1
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine departments to process
    if args.departments:
        departments = args.departments
    else:
        # Auto-detect departments
        departments = [d.name for d in raw_pages_dir.iterdir() 
                      if d.is_dir() and (d / 'metadata.json').exists()]
    
    if not departments:
        print("Error: No departments found to process")
        return 1
    
    print("=" * 60)
    print("Text Extraction for Research Automation")
    print("=" * 60)
    print(f"Departments: {', '.join(departments)}")
    print(f"Input: {raw_pages_dir}")
    print(f"Output: {output_dir}")
    print("=" * 60)
    print()
    
    # Process each department
    success_count = 0
    for dept in departments:
        if process_department(dept, raw_pages_dir, output_dir):
            success_count += 1
        print()
    
    # Summary
    print("=" * 60)
    print(f"Extraction Complete: {success_count}/{len(departments)} departments")
    print(f"Extracted text saved to: {output_dir}")
    print("=" * 60)
    print()
    print("Next Steps:")
    print("  1. Review extracted text in extracted_text/")
    print("  2. Feed into vector embedding pipeline")
    print("  3. Configure RAG system with embedded knowledge")
    
    return 0 if success_count > 0 else 1


if __name__ == '__main__':
    sys.exit(main())
