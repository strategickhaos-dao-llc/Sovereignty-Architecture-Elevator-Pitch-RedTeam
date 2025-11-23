#!/usr/bin/env python3
"""
License Update Script for Obsidian Integration

This script updates license text in all markdown files within a directory.
It's designed to work with Obsidian vaults and can be run locally to sync
license changes across your documentation.

Usage:
    python update_license.py [directory]

If no directory is specified, it will use the current directory.

Configuration:
    Before using this script, update the OLD_LICENSE_TEXT and NEW_LICENSE_TEXT
    constants below with your actual license text. These are placeholders
    that must be customized for your specific use case.
"""

import os
import sys
import glob


# TODO: Define your actual search and replacement text
# These are placeholder values - replace them with your actual license text
OLD_LICENSE_TEXT = "OLD_LICENSE_TEXT"
NEW_LICENSE_TEXT = "NEW_LICENSE_TEXT"


def update_license_in_file(file_path):
    """
    Update license text in a single file.
    
    Args:
        file_path: Path to the markdown file
        
    Returns:
        True if file was modified, False otherwise
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()
        
        # Replace old license text with new
        if OLD_LICENSE_TEXT in contents:
            contents = contents.replace(OLD_LICENSE_TEXT, NEW_LICENSE_TEXT)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(contents)
            print(f"✓ Updated: {file_path}")
            return True
        else:
            print(f"- Skipped: {file_path} (no license text found)")
            return False
    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return False


def main():
    """Main function to process all markdown files."""
    # Get directory from command line argument or use current directory
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    print(f"Scanning for markdown files in: {os.path.abspath(target_dir)}")
    print(f"Replacing '{OLD_LICENSE_TEXT}' with '{NEW_LICENSE_TEXT}'")
    print("-" * 60)
    
    # Find all markdown files in the desired directory
    pattern = os.path.join(target_dir, "**", "*.md")
    md_files = glob.glob(pattern, recursive=True)
    
    if not md_files:
        print("No markdown files found.")
        return
    
    modified_count = 0
    for md_file in md_files:
        if update_license_in_file(md_file):
            modified_count += 1
    
    print("-" * 60)
    print(f"Summary: {modified_count} file(s) updated out of {len(md_files)} total")


if __name__ == "__main__":
    main()
