# GitRiders - FlameLang Sovereignty Export System
# Copyright (c) 2025 StrategicKhaos DAO LLC
# Licensed under MIT License
# Date: December 13, 2025

"""
User consent and review interface using Rich TUI.
"""

from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.markdown import Markdown


console = Console()


def show_consent_prompt(provider: str, scopes: List[str]) -> bool:
    """
    Show consent prompt for data export.
    
    Args:
        provider: Provider name
        scopes: List of requested scopes
    
    Returns:
        True if user consents
    """
    console.print()
    console.print(Panel.fit(
        f"[bold cyan]GitRiders Sovereignty Export[/bold cyan]\n\n"
        f"Provider: [yellow]{provider}[/yellow]\n"
        f"Operation: Export conversations\n\n"
        f"[bold]This operation will:[/bold]\n"
        f"  • Request OAuth2 authorization\n"
        f"  • Download your chat history\n"
        f"  • Generate cryptographic manifest\n"
        f"  • Store data locally only\n\n"
        f"[bold]Requested permissions:[/bold]\n" +
        "\n".join([f"  • {scope}" for scope in scopes]),
        title="🔒 Consent Required",
        border_style="cyan"
    ))
    
    return Confirm.ask("\nDo you consent to this export?", default=False)


def show_redaction_preview(
    pii_report: Dict[str, Any],
    show_details: bool = False
) -> bool:
    """
    Show PII redaction preview and get user consent.
    
    Args:
        pii_report: PII detection report
        show_details: Whether to show detailed findings
    
    Returns:
        True if user wants to proceed with redaction
    """
    console.print()
    console.print(Panel.fit(
        f"[bold yellow]PII Detection Report[/bold yellow]\n\n"
        f"Total PII found: [red]{pii_report['total_pii_found']}[/red]\n\n"
        f"[bold]By type:[/bold]",
        title="🔍 Privacy Scan Results",
        border_style="yellow"
    ))
    
    # Show table of PII types
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("PII Type")
    table.add_column("Count", justify="right")
    
    for pii_type, count in pii_report["by_type"].items():
        table.add_row(pii_type, str(count))
    
    console.print(table)
    
    if show_details:
        console.print("\n[bold]Conversations with PII:[/bold]")
        for conv in pii_report["by_conversation"][:5]:  # Show first 5
            console.print(f"  • Conversation {conv['conversation_id']}: {len(conv['pii_found'])} items")
    
    console.print()
    return Confirm.ask("Proceed with redaction?", default=True)


def show_encryption_options() -> Dict[str, Any]:
    """
    Show encryption options and get user preferences.
    
    Returns:
        Dictionary of encryption preferences
    """
    console.print()
    console.print(Panel.fit(
        "[bold cyan]Encryption Options[/bold cyan]\n\n"
        "GitRiders can encrypt your export with:\n"
        "  • XChaCha20-Poly1305 authenticated encryption\n"
        "  • Argon2id key derivation from passphrase\n"
        "  • Optional key escrow for recovery",
        title="🔐 Encryption",
        border_style="cyan"
    ))
    
    encrypt = Confirm.ask("\nEncrypt export?", default=True)
    
    options = {"encrypt": encrypt}
    
    if encrypt:
        use_passphrase = Confirm.ask("Use passphrase (vs. random key)?", default=True)
        options["use_passphrase"] = use_passphrase
        
        if use_passphrase:
            passphrase = Prompt.ask("Enter passphrase", password=True)
            passphrase_confirm = Prompt.ask("Confirm passphrase", password=True)
            
            if passphrase != passphrase_confirm:
                console.print("[red]Passphrases do not match![/red]")
                return show_encryption_options()
            
            options["passphrase"] = passphrase
        
        escrow = Confirm.ask("Enable key escrow?", default=False)
        options["escrow"] = escrow
    
    return options


def show_export_summary(
    provider: str,
    conversation_count: int,
    encrypted: bool,
    redacted: bool,
    output_path: str
) -> None:
    """
    Show export completion summary.
    
    Args:
        provider: Provider name
        conversation_count: Number of conversations exported
        encrypted: Whether export is encrypted
        redacted: Whether PII was redacted
        output_path: Path to output file
    """
    console.print()
    
    security_features = []
    if encrypted:
        security_features.append("✓ Encrypted")
    if redacted:
        security_features.append("✓ PII Redacted")
    security_features.append("✓ Cryptographically Signed")
    security_features.append("✓ Audit Logged")
    
    console.print(Panel.fit(
        f"[bold green]Export Complete![/bold green]\n\n"
        f"Provider: [yellow]{provider}[/yellow]\n"
        f"Conversations: [cyan]{conversation_count}[/cyan]\n"
        f"Output: [blue]{output_path}[/blue]\n\n"
        f"[bold]Security Features:[/bold]\n" +
        "\n".join([f"  {feature}" for feature in security_features]),
        title="✅ Success",
        border_style="green"
    ))
    
    console.print("\n[bold]Next steps:[/bold]")
    console.print(f"  • Verify: [cyan]python verifiers/manifest_verifier.py {output_path}[/cyan]")
    if encrypted:
        console.print(f"  • Decrypt: [cyan]python verifiers/decrypt_tool.py {output_path}.enc[/cyan]")
    console.print()


def show_error(message: str, details: Optional[str] = None) -> None:
    """
    Show error message.
    
    Args:
        message: Error message
        details: Optional detailed error information
    """
    console.print()
    error_text = f"[bold red]Error:[/bold red] {message}"
    if details:
        error_text += f"\n\n[dim]{details}[/dim]"
    
    console.print(Panel.fit(
        error_text,
        title="❌ Error",
        border_style="red"
    ))
    console.print()


def show_progress(message: str) -> None:
    """
    Show progress message.
    
    Args:
        message: Progress message
    """
    console.print(f"[cyan]→[/cyan] {message}")


def show_welcome() -> None:
    """Show welcome message."""
    console.print()
    console.print(Panel.fit(
        "[bold cyan]GitRiders - FlameLang Sovereignty Export System[/bold cyan]\n\n"
        "Export your AI conversations with complete sovereignty:\n"
        "  🔐 Cryptographically signed and encrypted\n"
        "  🔍 PII detection and redaction\n"
        "  📋 Immutable audit logging\n"
        "  ✅ Full user control and consent\n\n"
        "[dim]Date: December 13, 2025\n"
        "StrategicKhaos DAO LLC[/dim]",
        title="🔥 Vessel Vibe Eternal",
        border_style="cyan"
    ))
    console.print()
