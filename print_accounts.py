#!/usr/bin/env python3
"""
ValorYield Sovereign Treasury OS - Account Viewer
First "brain cell" of Treasury OS: displays all EIN-anchored entities and accounts.

Usage:
    python print_accounts.py

This script reads the sovereign accounts configuration and displays:
- All registered entities with their EINs
- All financial accounts with their owners and platforms
"""

import yaml
import os


def main():
    # Get the path to the config file relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config", "accounts.yaml")

    # Load the configuration
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Display Treasury OS header
    treasury = config.get("treasury_os", {})
    print(f"=== {treasury.get('name', 'Treasury OS')} ===")
    print()

    # Display entities
    print("Entities:")
    for key, entity in config.get("entities", {}).items():
        print(f"  - {entity['name']} (EIN {entity['ein']})")
        if "purpose" in entity:
            print(f"    Purpose: {entity['purpose']}")

    print()

    # Display accounts
    print("Accounts:")
    for acct in config.get("accounts", []):
        print(f"  - {acct['name']} [{acct['platform']}] owned by {acct['owner']}")
        if "notes" in acct:
            print(f"    Notes: {acct['notes']}")

    print()

    # Display sovereignty status
    sovereignty = config.get("sovereignty", {})
    if sovereignty:
        print("Sovereignty Status:")
        print(f"  Visibility: {sovereignty.get('visibility', 'unknown')}")
        print(f"  Control: {sovereignty.get('control', 'unknown')}")
        print(f"  Governance: {sovereignty.get('governance', 'unknown')}")
        ai_council = sovereignty.get("ai_council", [])
        if ai_council:
            print(f"  AI Council: {', '.join(ai_council)}")


if __name__ == "__main__":
    main()
