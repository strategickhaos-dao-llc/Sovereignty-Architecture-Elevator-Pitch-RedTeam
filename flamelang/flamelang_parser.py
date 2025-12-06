#!/usr/bin/env python3
"""
FlameLang Parser v1.0

Strategickhaos Sovereign Symbolic Language Parser

This module provides the core parsing and execution engine for FlameLang,
a glyph-based domain-specific language for sovereign shell operations.

Usage:
    from flamelang_parser import FlameLangParser
    
    parser = FlameLangParser('glyph_map.json')
    parser.execute('{ll_notes⟐now}')

Command Line:
    python flamelang_parser.py '{ll_notes⟐now}'
    python flamelang_parser.py --list
    python flamelang_parser.py --status
"""

import json
import subprocess
import re
import sys
import os
from pathlib import Path
from datetime import datetime


class FlameLangParser:
    """
    FlameLang glyph parser and executor.
    
    Parses glyph commands in the format {namespace_function⟐modifier}
    and routes them to the appropriate executable scripts.
    """
    
    # Glyph pattern: {word⟐word} or {word_word⟐word}
    GLYPH_PATTERN = re.compile(r'\{([\w_]+)⟐(\w+)\}')
    
    # Binding code pattern: [NNN]
    BINDING_CODE_PATTERN = re.compile(r'\[(\d{3})\]')
    
    def __init__(self, glyph_map_path: str = None):
        """
        Initialize the FlameLang parser.
        
        Args:
            glyph_map_path: Path to the glyph_map.json file.
                           If None, searches in standard locations.
        """
        self.glyph_map_path = self._find_glyph_map(glyph_map_path)
        self.glyph_map = self._load_glyph_map()
        self.binding_codes = self._extract_binding_codes()
        
    def _find_glyph_map(self, path: str = None) -> Path:
        """Find the glyph map file."""
        if path:
            return Path(path)
        
        # Search locations
        search_paths = [
            Path(__file__).parent / 'glyph_map.json',
            Path.cwd() / 'glyph_map.json',
            Path.cwd() / 'flamelang' / 'glyph_map.json',
            Path.home() / 'glyph_map.json',
        ]
        
        for p in search_paths:
            if p.exists():
                return p
                
        raise FileNotFoundError(
            "glyph_map.json not found. Searched: " + 
            ", ".join(str(p) for p in search_paths)
        )
    
    def _load_glyph_map(self) -> dict:
        """Load and parse the glyph map JSON file."""
        with open(self.glyph_map_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _extract_binding_codes(self) -> dict:
        """Extract binding codes from the glyph map metadata."""
        return self.glyph_map.get('_binding_codes', {})
    
    def parse(self, command: str) -> str:
        """
        Parse a glyph command and return the target script path.
        
        Args:
            command: A glyph command like {namespace_function⟐modifier}
            
        Returns:
            The script path if found, None otherwise.
        """
        # Try direct lookup first
        if command in self.glyph_map:
            return self.glyph_map[command]
        
        # Extract glyph pattern
        match = self.GLYPH_PATTERN.match(command)
        if match:
            namespace_function = match.group(1)
            modifier = match.group(2)
            key = f"{{{namespace_function}⟐{modifier}}}"
            
            if key in self.glyph_map:
                return self.glyph_map[key]
        
        return None
    
    def resolve_binding_code(self, code: str) -> str:
        """
        Resolve a binding code to its domain.
        
        Args:
            code: A binding code like '999' or '[999]'
            
        Returns:
            The domain name if found, None otherwise.
        """
        # Strip brackets if present
        clean_code = code.strip('[]')
        return self.binding_codes.get(clean_code)
    
    def execute(self, command: str, dry_run: bool = False) -> bool:
        """
        Execute a glyph command.
        
        Args:
            command: A glyph command like {namespace_function⟐modifier}
            dry_run: If True, print what would be executed without running
            
        Returns:
            True if execution succeeded, False otherwise.
        """
        script = self.parse(command)
        
        if not script:
            print(f"❌ Unknown glyph: {command}")
            self.list_glyphs()
            return False
        
        # Skip metadata entries
        if script.startswith('_'):
            print(f"❌ Cannot execute metadata entry: {command}")
            return False
        
        print(f"🔥 Executing glyph: {command}")
        print(f"  → Target: {script}")
        
        if dry_run:
            print("  (dry run - not actually executing)")
            return True
        
        # Resolve relative paths
        if not os.path.isabs(script):
            script = str(self.glyph_map_path.parent.parent / script)
        
        # Check if script exists
        if not os.path.exists(script):
            print(f"  ⚠️ Script not found: {script}")
            print("  (This is expected if the target hasn't been created yet)")
            return False
        
        # Execute based on file extension
        try:
            if script.endswith('.py'):
                result = subprocess.run(
                    [sys.executable, script],
                    capture_output=False
                )
            elif script.endswith('.ps1'):
                # Try pwsh first, then powershell
                pwsh = 'pwsh' if self._command_exists('pwsh') else 'powershell'
                result = subprocess.run(
                    [pwsh, '-File', script],
                    capture_output=False
                )
            elif script.endswith('.sh'):
                result = subprocess.run(
                    ['bash', script],
                    capture_output=False
                )
            else:
                result = subprocess.run(
                    [script],
                    capture_output=False,
                    shell=True
                )
            
            print(f"\n✨ Neural Sync complete. Resonance achieved.")
            return result.returncode == 0
            
        except FileNotFoundError as e:
            print(f"❌ Execution failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def _command_exists(self, cmd: str) -> bool:
        """Check if a command exists in PATH."""
        import shutil
        return shutil.which(cmd) is not None
    
    def list_glyphs(self):
        """Print all available glyphs."""
        print("\n📜 Available Glyphs:")
        for key, value in self.glyph_map.items():
            if not key.startswith('_'):
                print(f"  {key} → {value}")
        print()
    
    def status(self):
        """Print FlameLang status."""
        print()
        print("🔥 FlameLang Parser Status")
        print(f"  Version: 1.0")
        print(f"  Glyph Map: {self.glyph_map_path}")
        print(f"  Total Glyphs: {len([k for k in self.glyph_map if not k.startswith('_')])}")
        print(f"  Binding Codes: {len(self.binding_codes)}")
        print(f"  Timestamp: {datetime.now().isoformat()}")
        print()
        print("⚔ Ready for sovereign operations.")
        print()


def main():
    """Command-line interface for FlameLang parser."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='FlameLang Parser v1.0 - Sovereign Symbolic Shell',
        epilog='Example: python flamelang_parser.py "{ll_notes⟐now}"'
    )
    parser.add_argument(
        'command',
        nargs='?',
        help='Glyph command to execute (e.g., {flame⟐status})'
    )
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all available glyphs'
    )
    parser.add_argument(
        '--status', '-s',
        action='store_true',
        help='Show FlameLang status'
    )
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Show what would be executed without running'
    )
    parser.add_argument(
        '--glyph-map', '-g',
        help='Path to glyph_map.json'
    )
    
    args = parser.parse_args()
    
    try:
        flamelang = FlameLangParser(args.glyph_map)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    if args.status:
        flamelang.status()
    elif args.list:
        flamelang.list_glyphs()
    elif args.command:
        success = flamelang.execute(args.command, dry_run=args.dry_run)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
