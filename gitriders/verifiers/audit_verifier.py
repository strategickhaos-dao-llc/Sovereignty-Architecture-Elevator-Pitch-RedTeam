#!/usr/bin/env python3
# GitRiders - FlameLang Sovereignty Export System
# Copyright (c) 2025 StrategicKhaos DAO LLC
# Licensed under MIT License
# Date: December 13, 2025

"""
Standalone audit log verifier CLI.
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sovereign_export.audit import AuditLogger


console = Console()


def verify_audit_log(log_path: Path) -> bool:
    """
    Verify audit log integrity.
    
    Args:
        log_path: Path to audit log file
    
    Returns:
        True if verification succeeds
    """
    try:
        console.print(f"\n[cyan]Loading audit log from:[/cyan] {log_path}")
        
        # Load audit log
        logger = AuditLogger(log_path)
        
        console.print("[cyan]Verifying hash chain integrity...[/cyan]")
        
        # Verify integrity
        try:
            logger.verify_integrity()
            console.print("[green]✓ Audit log integrity verified[/green]")
        except ValueError as e:
            console.print(f"[red]❌ Integrity check failed: {e}[/red]")
            return False
        
        # Read all entries
        entries = logger.read_log()
        
        console.print(f"\n[bold]Audit Log Summary:[/bold]")
        console.print(f"  Total entries: {len(entries)}")
        console.print(f"  Genesis entry: {entries[0]['timestamp']}")
        console.print(f"  Latest entry: {entries[-1]['timestamp']}")
        
        # Show event type breakdown
        event_types = {}
        for entry in entries[1:]:  # Skip genesis
            event_type = entry.get("event_type", "unknown")
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        if event_types:
            console.print("\n[bold]Events by type:[/bold]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Event Type")
            table.add_column("Count", justify="right")
            
            for event_type, count in sorted(event_types.items()):
                table.add_row(event_type, str(count))
            
            console.print(table)
        
        # Show recent entries
        console.print("\n[bold]Recent entries:[/bold]")
        recent_entries = entries[-5:] if len(entries) > 5 else entries[1:]
        
        for entry in recent_entries:
            console.print(
                f"  [{entry['index']}] {entry['timestamp'][:19]} - "
                f"{entry['event_type']}"
            )
        
        console.print()
        console.print(Panel.fit(
            "[bold green]✅ Audit log verification successful![/bold green]\n\n"
            "All hash chains are valid and the audit log has not\n"
            "been tampered with. Chain of custody is intact.",
            title="Verification Complete",
            border_style="green"
        ))
        
        return True
    
    except FileNotFoundError:
        console.print(f"[red]❌ Audit log file not found: {log_path}[/red]")
        return False
    except Exception as e:
        console.print(f"[red]❌ Verification error: {e}[/red]")
        return False


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        console.print("\n[bold]Usage:[/bold]")
        console.print("  python audit_verifier.py <audit_log_file>\n")
        console.print("[bold]Example:[/bold]")
        console.print("  python audit_verifier.py ~/.sovereign-export/keys/audit.log\n")
        sys.exit(1)
    
    log_path = Path(sys.argv[1])
    success = verify_audit_log(log_path)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
