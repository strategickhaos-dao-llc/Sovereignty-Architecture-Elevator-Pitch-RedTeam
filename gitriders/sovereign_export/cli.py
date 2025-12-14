# GitRiders - FlameLang Sovereignty Export System
# Copyright (c) 2025 StrategicKhaos DAO LLC
# Licensed under MIT License
# Date: December 13, 2025

"""
Command-line interface for sovereign exports.
"""

import sys
from pathlib import Path
from typing import Optional
import click

from sovereign_export.config import load_config, get_keydir
from sovereign_export.manifest import ManifestGenerator, create_export_package, save_export_package
from sovereign_export.encrypt import EncryptionManager, encrypt_export_package
from sovereign_export.audit import AuditLogger, create_audit_entry
from sovereign_export.redaction import RedactionEngine
from sovereign_export import ui
from sovereign_export.connectors import (
    OpenAIConnector,
    AnthropicConnector,
    GoogleTakeoutConnector,
    XAIGrokConnector,
    PerplexityConnector
)


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """GitRiders - FlameLang Sovereignty Export System"""
    ui.show_welcome()


@cli.command()
@click.option("--output", "-o", required=True, help="Output file path")
@click.option("--encrypt/--no-encrypt", default=True, help="Encrypt the export")
@click.option("--redact-pii/--no-redact-pii", default=False, help="Redact PII")
@click.option("--escrow/--no-escrow", default=False, help="Enable key escrow")
def openai(output: str, encrypt: bool, redact_pii: bool, escrow: bool):
    """Export conversations from OpenAI ChatGPT"""
    _export_provider("openai", OpenAIConnector, output, encrypt, redact_pii, escrow)


@cli.command()
@click.option("--output", "-o", required=True, help="Output file path")
@click.option("--encrypt/--no-encrypt", default=True, help="Encrypt the export")
@click.option("--redact-pii/--no-redact-pii", default=False, help="Redact PII")
@click.option("--escrow/--no-escrow", default=False, help="Enable key escrow")
def anthropic(output: str, encrypt: bool, redact_pii: bool, escrow: bool):
    """Export conversations from Anthropic Claude"""
    _export_provider("anthropic", AnthropicConnector, output, encrypt, redact_pii, escrow)


@cli.command()
@click.option("--takeout-file", "-f", required=True, help="Path to Google Takeout ZIP")
@click.option("--output", "-o", required=True, help="Output file path")
@click.option("--encrypt/--no-encrypt", default=True, help="Encrypt the export")
@click.option("--redact-pii/--no-redact-pii", default=False, help="Redact PII")
def google_takeout(takeout_file: str, output: str, encrypt: bool, redact_pii: bool):
    """Parse Google Takeout export"""
    try:
        ui.show_progress("Parsing Google Takeout file...")
        
        connector = GoogleTakeoutConnector()
        data = connector.parse_takeout_file(Path(takeout_file))
        
        _process_export("google_takeout", data, output, encrypt, redact_pii, False)
        
    except Exception as e:
        ui.show_error("Export failed", str(e))
        sys.exit(1)


@cli.command()
@click.option("--output", "-o", required=True, help="Output file path")
@click.option("--encrypt/--no-encrypt", default=True, help="Encrypt the export")
@click.option("--redact-pii/--no-redact-pii", default=False, help="Redact PII")
@click.option("--escrow/--no-escrow", default=False, help="Enable key escrow")
def grok(output: str, encrypt: bool, redact_pii: bool, escrow: bool):
    """Export conversations from xAI Grok"""
    _export_provider("xai_grok", XAIGrokConnector, output, encrypt, redact_pii, escrow)


@cli.command()
@click.option("--output", "-o", required=True, help="Output file path")
@click.option("--encrypt/--no-encrypt", default=True, help="Encrypt the export")
@click.option("--redact-pii/--no-redact-pii", default=False, help="Redact PII")
@click.option("--escrow/--no-escrow", default=False, help="Enable key escrow")
def perplexity(output: str, encrypt: bool, redact_pii: bool, escrow: bool):
    """Export conversations from Perplexity"""
    _export_provider("perplexity", PerplexityConnector, output, encrypt, redact_pii, escrow)


def _export_provider(
    provider_name: str,
    connector_class,
    output: str,
    encrypt: bool,
    redact_pii: bool,
    escrow: bool
):
    """
    Common export logic for API-based providers.
    
    Args:
        provider_name: Provider identifier
        connector_class: Connector class to instantiate
        output: Output file path
        encrypt: Whether to encrypt
        redact_pii: Whether to redact PII
        escrow: Whether to enable key escrow
    """
    try:
        # Load configuration
        config = load_config()
        
        # Show consent prompt
        scopes = config["providers"][provider_name].get("scopes", [])
        if not ui.show_consent_prompt(provider_name, scopes):
            ui.show_progress("Export cancelled by user")
            sys.exit(0)
        
        # Initialize connector
        ui.show_progress(f"Connecting to {provider_name}...")
        connector = connector_class()
        
        # Export data
        ui.show_progress("Downloading conversations...")
        data = connector.export_conversations()
        
        # Process export
        _process_export(provider_name, data, output, encrypt, redact_pii, escrow)
        
    except Exception as e:
        ui.show_error("Export failed", str(e))
        sys.exit(1)


def _process_export(
    provider_name: str,
    data: dict,
    output: str,
    encrypt: bool,
    redact_pii: bool,
    escrow: bool
):
    """
    Process export data with signing, encryption, and redaction.
    
    Args:
        provider_name: Provider identifier
        data: Export data
        output: Output file path
        encrypt: Whether to encrypt
        redact_pii: Whether to redact PII
        escrow: Whether to enable key escrow
    """
    # Initialize components
    keydir = get_keydir()
    audit_log = AuditLogger(keydir / "audit.log")
    
    # Redact PII if requested
    if redact_pii:
        ui.show_progress("Scanning for PII...")
        redaction_engine = RedactionEngine()
        pii_report = redaction_engine.generate_redaction_report(data)
        
        if pii_report["total_pii_found"] > 0:
            if ui.show_redaction_preview(pii_report):
                ui.show_progress("Redacting PII...")
                for i, conv in enumerate(data.get("conversations", [])):
                    data["conversations"][i] = redaction_engine.redact_conversation(conv)
                data["redacted"] = True
    
    # Generate manifest and sign
    ui.show_progress("Generating cryptographic manifest...")
    key_path = keydir / f"{provider_name}_signing_key"
    
    if key_path.exists():
        generator = ManifestGenerator.load_key(key_path)
    else:
        generator = ManifestGenerator()
        generator.save_key(key_path)
    
    package = create_export_package(
        data,
        provider_name,
        generator,
        metadata={"redacted": data.get("redacted", False)}
    )
    
    # Save package
    output_path = Path(output)
    
    if encrypt:
        ui.show_progress("Encrypting export...")
        
        # Get encryption options
        encryption_opts = ui.show_encryption_options()
        
        if encryption_opts["encrypt"]:
            passphrase = encryption_opts.get("passphrase")
            
            encrypted_package, key, escrow_package = encrypt_export_package(
                package,
                passphrase=passphrase,
                escrow_keys=[] if escrow else None
            )
            
            # Save encrypted package
            encrypted_path = output_path.with_suffix(output_path.suffix + ".enc")
            save_export_package(encrypted_package, encrypted_path)
            
            # Save key if not using passphrase
            if not passphrase:
                key_file = output_path.with_suffix(".key")
                EncryptionManager().save_key(key, key_file)
                ui.show_progress(f"Encryption key saved to: {key_file}")
            
            output_path = encrypted_path
    else:
        save_export_package(package, output_path)
    
    # Log to audit
    ui.show_progress("Recording audit entry...")
    audit_entry = create_audit_entry(
        "export",
        provider_name,
        "export_conversations",
        True,
        {
            "output": str(output_path),
            "encrypted": encrypt,
            "redacted": redact_pii,
            "conversation_count": len(data.get("conversations", []))
        }
    )
    audit_log.log_event("export", audit_entry)
    
    # Show summary
    ui.show_export_summary(
        provider_name,
        len(data.get("conversations", [])),
        encrypt,
        redact_pii,
        str(output_path)
    )


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
