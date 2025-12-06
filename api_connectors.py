#!/usr/bin/env python3
"""
ValorYield Sovereign Treasury OS - API Connectors
Brain Cell #2: Transforms the static accounts registry into a dynamic system.

This module:
- Loads the accounts.yaml registry
- Defines functions to fetch balances for each platform using mock data
- Updates balance fields in a copy of the YAML data structure
- Prints the final updated structure

Usage:
    python api_connectors.py

Security Notes:
- In production, credentials should be fetched from environment variables
  or a secret manager (e.g., HashiCorp Vault)
- Never hardcode API keys or sensitive credentials
"""

import copy
import os
import sys
from decimal import Decimal

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required but not installed.")
    print("Please install it with: pip install pyyaml")
    sys.exit(1)


# Mock data for platform balances (simulating API responses)
# NOTE: These are example values only for demonstration purposes.
# In production, these would be replaced by actual API calls.
# Real balances will differ from these mock values.
MOCK_BALANCES = {
    "MoneyLion": {
        "mlion-2143": Decimal("207.69"),
    },
    "Kraken": {
        "kraken-primary": Decimal("1523.45"),
    },
    "NinjaTrader": {
        "ninjatrader-main": Decimal("5847.32"),
    },
    "Kalshi": {
        "kalshi-events": Decimal("312.50"),
    },
    "Bank": {
        "biz-checking": Decimal("8942.18"),
    },
}


def get_api_key_from_env(platform: str) -> str:
    """
    Retrieve API key from environment variables.
    Returns empty string if not found (mock mode).
    """
    env_var = f"{platform.upper()}_API_KEY"
    return os.environ.get(env_var, "")


def fetch_moneylion_balance(account_id: str) -> Decimal:
    """
    Fetch balance from MoneyLion API.
    Currently returns mock data.
    """
    # In production: Use requests library to call MoneyLion API
    # api_key = get_api_key_from_env("MoneyLion")
    return MOCK_BALANCES.get("MoneyLion", {}).get(account_id, Decimal("0"))


def fetch_kraken_balance(account_id: str) -> Decimal:
    """
    Fetch balance from Kraken API.
    Currently returns mock data.
    """
    # In production: Use requests library with Kraken API
    # api_key = get_api_key_from_env("Kraken")
    # api_secret = os.environ.get("KRAKEN_API_SECRET", "")
    return MOCK_BALANCES.get("Kraken", {}).get(account_id, Decimal("0"))


def fetch_ninjatrader_balance(account_id: str) -> Decimal:
    """
    Fetch balance from NinjaTrader API.
    Currently returns mock data.
    """
    # In production: Use NinjaTrader API client
    # api_key = get_api_key_from_env("NinjaTrader")
    return MOCK_BALANCES.get("NinjaTrader", {}).get(account_id, Decimal("0"))


def fetch_kalshi_balance(account_id: str) -> Decimal:
    """
    Fetch balance from Kalshi API.
    Currently returns mock data.
    """
    # In production: Use Kalshi API client
    # api_key = get_api_key_from_env("Kalshi")
    return MOCK_BALANCES.get("Kalshi", {}).get(account_id, Decimal("0"))


def fetch_bank_balance(account_id: str) -> Decimal:
    """
    Fetch balance from Bank API (via Plaid or similar).
    Currently returns mock data.
    """
    # In production: Use Plaid or bank-specific API
    # access_token = os.environ.get("PLAID_ACCESS_TOKEN", "")
    return MOCK_BALANCES.get("Bank", {}).get(account_id, Decimal("0"))


# Platform-specific fetch function mapping
PLATFORM_FETCHERS = {
    "MoneyLion": fetch_moneylion_balance,
    "Kraken": fetch_kraken_balance,
    "NinjaTrader": fetch_ninjatrader_balance,
    "Kalshi": fetch_kalshi_balance,
    "Bank": fetch_bank_balance,
}


def fetch_balance(platform: str, account_id: str) -> Decimal:
    """
    Fetch balance for any platform using the appropriate connector.
    Returns Decimal(0) for unknown platforms.
    """
    fetcher = PLATFORM_FETCHERS.get(platform)
    if fetcher:
        return fetcher(account_id)
    print(f"Warning: No connector available for platform '{platform}'")
    return Decimal("0")


def load_accounts_config() -> dict:
    """Load the accounts configuration from YAML file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config", "accounts.yaml")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {config_path}")
        print("Please ensure config/accounts.yaml exists.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML format in {config_path}")
        print(f"Details: {e}")
        sys.exit(1)


def update_balances(config: dict) -> dict:
    """
    Create a copy of the config and update all account balances.
    Returns the updated configuration.
    """
    updated_config = copy.deepcopy(config)

    for account in updated_config.get("accounts", []):
        platform = account.get("platform", "")
        account_id = account.get("id", "")
        balance = fetch_balance(platform, account_id)
        # Store balance as string for YAML serialization
        account["balance"] = str(balance)

    return updated_config


def print_updated_config(config: dict) -> None:
    """Print the updated configuration with balances."""
    treasury = config.get("treasury_os", {})
    print(f"=== {treasury.get('name', 'Treasury OS')} - Live Balances ===")
    print()

    # Display entities
    entities = config.get("entities", {})
    print("Entities:")
    for key, entity in entities.items():
        print(f"  - {entity['name']} (EIN {entity['ein']})")

    print()

    # Calculate totals per owner
    owner_totals = {}
    total_all = Decimal("0")

    print("Accounts with Balances:")
    for acct in config.get("accounts", []):
        owner = acct.get("owner", "unknown")
        balance = Decimal(acct.get("balance", "0"))
        total_all += balance

        if owner not in owner_totals:
            owner_totals[owner] = Decimal("0")
        owner_totals[owner] += balance

        print(f"  - {acct['name']} [{acct['platform']}]")
        print(f"    Owner: {owner}")
        print(f"    Balance: ${balance:,.2f}")
        if "notes" in acct:
            print(f"    Notes: {acct['notes']}")

    print()
    print("Summary by Owner:")
    for owner, total in owner_totals.items():
        entity_name = entities.get(owner, {}).get("name", owner)
        print(f"  {entity_name}: ${total:,.2f}")

    print()
    print(f"Total Treasury Value: ${total_all:,.2f}")
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


def main():
    """Main entry point for the API connectors."""
    print("Loading accounts configuration...")
    config = load_accounts_config()

    print("Fetching balances from platforms (mock data)...")
    print()

    updated_config = update_balances(config)
    print_updated_config(updated_config)

    print()
    print("---")
    print("Updated YAML Structure:")
    print("---")
    print(yaml.dump(updated_config, default_flow_style=False, sort_keys=False))


if __name__ == "__main__":
    main()
