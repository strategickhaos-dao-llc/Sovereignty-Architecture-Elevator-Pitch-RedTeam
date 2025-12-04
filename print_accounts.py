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

import os
import sys

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required but not installed.")
    print("Please install it with: pip install pyyaml")
    sys.exit(1)


def main():
    # Get the path to the config file relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config", "accounts.yaml")

    # Load the configuration with error handling
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {config_path}")
        print("Please ensure config/accounts.yaml exists.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML format in {config_path}")
        print(f"Details: {e}")
        sys.exit(1)

    # Display Treasury OS header
    treasury = config.get("treasury_os", {})
    print(f"=== {treasury.get('name', 'Treasury OS')} ===")
    print()

    # Get valid entity keys for validation
    entities = config.get("entities", {})
    valid_owners = set(entities.keys())

    # Display entities
    print("Entities:")
    for key, entity in entities.items():
        print(f"  - {entity['name']} (EIN {entity['ein']})")
        if "purpose" in entity:
            print(f"    Purpose: {entity['purpose']}")

    print()

    # Display accounts with owner validation
    print("Accounts:")
    for acct in config.get("accounts", []):
        owner = acct['owner']
        owner_valid = owner in valid_owners
        validity_marker = "" if owner_valid else " [INVALID OWNER]"
        print(f"  - {acct['name']} [{acct['platform']}] owned by {owner}{validity_marker}")
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
