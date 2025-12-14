#!/usr/bin/env python3
# GitRiders - FlameLang Sovereignty Export System
# Copyright (c) 2025 StrategicKhaos DAO LLC
# Licensed under MIT License
# Date: December 13, 2025

"""
Standalone manifest verifier CLI.
"""

import sys
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sovereign_export.manifest import verify_manifest, load_export_package


console = Console()


def verify_export(export_path: Path) -> bool:
    """
    Verify an export package.
    
    Args:
        export_path: Path to export file
    
    Returns:
        True if verification succeeds
    """
    try:
        console.print(f"\n[cyan]Loading export from:[/cyan] {export_path}")
        
        # Load package
        package = load_export_package(export_path)
        
        # Extract components
        data = package.get("data")
        manifest = package.get("manifest")
        
        if not data or not manifest:
            console.print("[red]❌ Invalid export format: missing data or manifest[/red]")
            return False
        
        console.print("[cyan]Verifying cryptographic signature...[/cyan]")
        
        # Verify manifest
        try:
            verify_manifest(manifest, data)
            console.print("[green]✓ Signature valid[/green]")
        except ValueError as e:
            console.print(f"[red]❌ Signature verification failed: {e}[/red]")
            return False
        
        # Show manifest details
        console.print("\n[bold]Manifest Details:[/bold]")
        console.print(f"  Version: {manifest.get('version')}")
        console.print(f"  Timestamp: {manifest.get('timestamp')}")
        console.print(f"  Provider: {manifest.get('provider')}")
        console.print(f"  Data Hash: {manifest.get('data_hash')[:16]}...")
        console.print(f"  Public Key: {manifest.get('public_key')[:16]}...")
        
        # Show metadata if present
        if manifest.get("metadata"):
            console.print("\n[bold]Metadata:[/bold]")
            for key, value in manifest["metadata"].items():
                console.print(f"  {key}: {value}")
        
        console.print()
        console.print(Panel.fit(
            "[bold green]✅ Export verification successful![/bold green]\n\n"
            "The export has a valid cryptographic signature and\n"
            "the data integrity has been confirmed.",
            title="Verification Complete",
            border_style="green"
        ))
        
        return True
    
    except FileNotFoundError:
        console.print(f"[red]❌ Export file not found: {export_path}[/red]")
        return False
    except json.JSONDecodeError:
        console.print("[red]❌ Invalid JSON format[/red]")
        return False
    except Exception as e:
        console.print(f"[red]❌ Verification error: {e}[/red]")
        return False


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        console.print("\n[bold]Usage:[/bold]")
        console.print("  python manifest_verifier.py <export_file.json>\n")
        console.print("[bold]Example:[/bold]")
        console.print("  python manifest_verifier.py my-export.json\n")
        sys.exit(1)
    
    export_path = Path(sys.argv[1])
    success = verify_export(export_path)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
