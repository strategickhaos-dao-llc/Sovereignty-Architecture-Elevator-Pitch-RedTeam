#!/usr/bin/env python3
# GitRiders - FlameLang Sovereignty Export System
# Copyright (c) 2025 StrategicKhaos DAO LLC
# Licensed under MIT License
# Date: December 13, 2025

"""
Standalone decryption tool CLI.
"""

import sys
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sovereign_export.encrypt import EncryptionManager
from sovereign_export.manifest import save_export_package


console = Console()


def decrypt_export(
    encrypted_path: Path,
    output_path: Path,
    key_file: Path = None,
    passphrase: str = None
) -> bool:
    """
    Decrypt an encrypted export.
    
    Args:
        encrypted_path: Path to encrypted export
        output_path: Path for decrypted output
        key_file: Optional key file path
        passphrase: Optional passphrase
    
    Returns:
        True if decryption succeeds
    """
    try:
        console.print(f"\n[cyan]Loading encrypted export from:[/cyan] {encrypted_path}")
        
        # Load encrypted package
        with open(encrypted_path, 'r') as f:
            encrypted_package = json.load(f)
        
        # Initialize encryption manager
        manager = EncryptionManager()
        
        # Get decryption key
        if key_file:
            console.print(f"[cyan]Loading key from:[/cyan] {key_file}")
            key = manager.load_key(key_file)
        elif passphrase:
            console.print("[cyan]Deriving key from passphrase...[/cyan]")
            salt = bytes.fromhex(encrypted_package.get("encryption_salt", ""))
            if not salt:
                console.print("[red]❌ No salt found in encrypted package[/red]")
                return False
            key, _ = manager.derive_key_from_passphrase(passphrase, salt)
        else:
            # Prompt for passphrase
            passphrase = Prompt.ask("Enter passphrase", password=True)
            salt = bytes.fromhex(encrypted_package.get("encryption_salt", ""))
            if not salt:
                console.print("[red]❌ No salt found in encrypted package[/red]")
                return False
            key, _ = manager.derive_key_from_passphrase(passphrase, salt)
        
        console.print("[cyan]Decrypting...[/cyan]")
        
        # Decrypt
        try:
            decrypted_package = manager.decrypt(encrypted_package, key)
        except ValueError as e:
            console.print(f"[red]❌ Decryption failed: {e}[/red]")
            console.print("[yellow]Possible causes:[/yellow]")
            console.print("  • Incorrect passphrase or key")
            console.print("  • Corrupted encrypted file")
            console.print("  • Wrong key file")
            return False
        
        # Save decrypted package
        console.print(f"[cyan]Saving decrypted export to:[/cyan] {output_path}")
        save_export_package(decrypted_package, output_path)
        
        # Show summary
        data = decrypted_package.get("data", {})
        manifest = decrypted_package.get("manifest", {})
        
        console.print("\n[bold]Decrypted Export Details:[/bold]")
        console.print(f"  Provider: {manifest.get('provider', 'unknown')}")
        console.print(f"  Timestamp: {manifest.get('timestamp', 'unknown')}")
        
        conversations = data.get("conversations", [])
        console.print(f"  Conversations: {len(conversations)}")
        
        console.print()
        console.print(Panel.fit(
            "[bold green]✅ Decryption successful![/bold green]\n\n"
            f"The decrypted export has been saved to:\n"
            f"[blue]{output_path}[/blue]\n\n"
            "You can now verify the manifest with:\n"
            f"[cyan]python verifiers/manifest_verifier.py {output_path}[/cyan]",
            title="Decryption Complete",
            border_style="green"
        ))
        
        return True
    
    except FileNotFoundError as e:
        console.print(f"[red]❌ File not found: {e}[/red]")
        return False
    except json.JSONDecodeError:
        console.print("[red]❌ Invalid JSON format[/red]")
        return False
    except Exception as e:
        console.print(f"[red]❌ Decryption error: {e}[/red]")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        console.print("\n[bold]Usage:[/bold]")
        console.print("  python decrypt_tool.py <encrypted_file> [options]\n")
        console.print("[bold]Options:[/bold]")
        console.print("  --output <file>      Output file path (default: decrypted.json)")
        console.print("  --key-file <file>    Key file path (prompts for passphrase if not provided)")
        console.print("  --passphrase <pass>  Passphrase (not recommended, use prompt instead)\n")
        console.print("[bold]Examples:[/bold]")
        console.print("  python decrypt_tool.py export.json.enc")
        console.print("  python decrypt_tool.py export.json.enc --output decrypted.json")
        console.print("  python decrypt_tool.py export.json.enc --key-file export.key\n")
        sys.exit(1)
    
    encrypted_path = Path(sys.argv[1])
    output_path = Path("decrypted.json")
    key_file = None
    passphrase = None
    
    # Parse arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--output" and i + 1 < len(sys.argv):
            output_path = Path(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--key-file" and i + 1 < len(sys.argv):
            key_file = Path(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--passphrase" and i + 1 < len(sys.argv):
            passphrase = sys.argv[i + 1]
            i += 2
        else:
            console.print(f"[red]Unknown option: {sys.argv[i]}[/red]")
            sys.exit(1)
    
    success = decrypt_export(encrypted_path, output_path, key_file, passphrase)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
