#!/usr/bin/env python3
"""
StrategicKhaos Compiler - Main Entry Point

Usage:
    python -m src.main              # Start REPL
    python -m src.main <file>       # Execute a .khaos file
    python -m src.main --version    # Show version
"""

import sys
import os
from . import get_version, get_chaos_level
from .repl import repl, run_file


def show_version():
    """Display version information."""
    print(f"StrategicKhaos Compiler v{get_version()}")
    print(f"Chaos Level: {get_chaos_level()}")
    print("Born: 2025-11-21")
    print("The empire's first heartbeat has compiled.")


def show_help():
    """Display help information."""
    print("StrategicKhaos Compiler")
    print()
    print("Usage:")
    print("  python -m src.main              Start interactive REPL")
    print("  python -m src.main <file>       Execute a .khaos file")
    print("  python -m src.main --version    Show version information")
    print("  python -m src.main --help       Show this help message")
    print()
    print("Examples:")
    print("  python -m src.main")
    print("  python -m src.main examples/hello.khaos")


def main():
    """Main entry point for the StrategicKhaos compiler."""
    # Parse command line arguments
    args = sys.argv[1:]
    
    # No arguments - start REPL
    if len(args) == 0:
        repl()
        return
    
    # Handle flags
    if args[0] == '--version' or args[0] == '-v':
        show_version()
        return
    
    if args[0] == '--help' or args[0] == '-h':
        show_help()
        return
    
    # Execute a file
    filename = args[0]
    
    # Check if file exists
    if not os.path.exists(filename):
        print(f"Error: File not found: {filename}")
        sys.exit(1)
    
    # Run the file
    run_file(filename)


if __name__ == '__main__':
    main()
