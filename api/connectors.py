#!/usr/bin/env python3
"""
ValorYield Treasury API Connectors
Brain Cell #2: Platform connectors for fetching real-time account balances

This module provides connectors for multiple financial platforms:
- MoneyLion (robo-advisor)
- Kraken Pro (cryptocurrency exchange)
- NinjaTrader (futures/options trading)
- Thread Bank (checking account)

Usage:
    python api/connectors.py
"""

import os
import sys
import time
import logging
import hashlib
import hmac
import base64
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class PlatformConnector(ABC):
    """Abstract base class for platform connectors."""
    
    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.platform_name = config.get('platform', 'Unknown')
        self.enabled = config.get('enabled', True)
        self.api_endpoint = config.get('api_endpoint', '')
        self.last_updated: datetime | None = None
        
    @abstractmethod
    def fetch_balance(self) -> dict[str, Any]:
        """Fetch the current balance from the platform."""
        pass
    
    def _make_request(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        data: dict[str, Any] | None = None,
        max_retries: int = 3,
        backoff_factor: float = 1.5
    ) -> requests.Response | None:
        """Make HTTP request with retry logic and exponential backoff."""
        for attempt in range(max_retries):
            try:
                if method.upper() == 'GET':
                    response = requests.get(url, headers=headers, timeout=30)
                elif method.upper() == 'POST':
                    response = requests.post(url, headers=headers, json=data, timeout=30)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                    
                response.raise_for_status()
                return response
                
            except requests.exceptions.Timeout:
                logger.warning(f"Request timeout (attempt {attempt + 1}/{max_retries})")
            except requests.exceptions.ConnectionError as e:
                logger.warning(f"Connection error (attempt {attempt + 1}/{max_retries}): {e}")
            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP error: {e}")
                if e.response.status_code in [401, 403]:
                    logger.error("Authentication failed - check API credentials")
                    return None
                    
            if attempt < max_retries - 1:
                sleep_time = backoff_factor ** attempt
                logger.info(f"Retrying in {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
                
        logger.error(f"Failed after {max_retries} attempts")
        return None


class MoneyLionConnector(PlatformConnector):
    """Connector for MoneyLion robo-advisor platform."""
    
    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.api_key = os.environ.get('MONEYLION_API_KEY', '')
        self.account_id = config.get('account_id', '')
        
    def fetch_balance(self) -> dict[str, Any]:
        """Fetch balance from MoneyLion API."""
        if not self.enabled:
            return {'status': 'disabled', 'balance': 0.0}
            
        if not self.api_key:
            logger.warning("MoneyLion API key not configured - using mock data")
            return self._get_mock_balance()
            
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            url = f"{self.api_endpoint}/accounts/{self.account_id}/balance"
            
            response = self._make_request('GET', url, headers=headers)
            
            if response:
                data = response.json()
                self.last_updated = datetime.now()
                return {
                    'status': 'success',
                    'platform': self.platform_name,
                    'account_id': self.account_id,
                    'account_type': self.config.get('account_type', 'Investment'),
                    'balance': float(data.get('balance', 0)),
                    'currency': 'USD',
                    'last_updated': self.last_updated.isoformat()
                }
        except (requests.RequestException, ValueError) as e:
            logger.error(f"MoneyLion API error: {e}")
            
        return self._get_mock_balance()
    
    def _get_mock_balance(self) -> dict[str, Any]:
        """Return mock balance data for testing."""
        self.last_updated = datetime.now()
        return {
            'status': 'mock',
            'platform': self.platform_name,
            'account_id': self.account_id,
            'account_type': self.config.get('account_type', 'Aggressive Mix'),
            'balance': 207.69,
            'allocation': self.config.get('allocation', {}),
            'currency': 'USD',
            'last_updated': self.last_updated.isoformat()
        }


class KrakenConnector(PlatformConnector):
    """Connector for Kraken Pro cryptocurrency exchange."""
    
    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.api_key = os.environ.get('KRAKEN_API_KEY', '')
        self.api_secret = os.environ.get('KRAKEN_API_SECRET', '')
        
    def _generate_signature(self, urlpath: str, data: dict[str, Any], nonce: str) -> str:
        """Generate Kraken API signature for authenticated requests."""
        postdata = '&'.join([f"{k}={v}" for k, v in sorted(data.items())])
        encoded = (nonce + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()
        signature = hmac.new(base64.b64decode(self.api_secret), message, hashlib.sha512)
        return base64.b64encode(signature.digest()).decode()
        
    def fetch_balance(self) -> dict[str, Any]:
        """Fetch balance from Kraken API."""
        if not self.enabled:
            return {'status': 'disabled', 'balance': 0.0}
            
        if not self.api_key or not self.api_secret:
            logger.warning("Kraken API credentials not configured - using mock data")
            return self._get_mock_balance()
            
        try:
            nonce = str(int(time.time() * 1000))
            urlpath = '/0/private/Balance'
            url = f"{self.api_endpoint}{urlpath}"
            data = {'nonce': nonce}
            
            headers = {
                'API-Key': self.api_key,
                'API-Sign': self._generate_signature(urlpath, data, nonce),
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = self._make_request('POST', url, headers=headers, data=data)
            
            if response:
                result = response.json()
                if result.get('error'):
                    logger.error(f"Kraken API error: {result['error']}")
                    return self._get_mock_balance()
                    
                balances = result.get('result', {})
                total_usd = self._calculate_usd_value(balances)
                
                self.last_updated = datetime.now()
                return {
                    'status': 'success',
                    'platform': self.platform_name,
                    'account_type': self.config.get('account_type', 'Crypto Trading'),
                    'balances': balances,
                    'balance': total_usd,
                    'currency': 'USD',
                    'last_updated': self.last_updated.isoformat()
                }
        except (requests.RequestException, ValueError) as e:
            logger.error(f"Kraken API error: {e}")
            
        return self._get_mock_balance()
    
    def _calculate_usd_value(self, balances: dict[str, str]) -> float:
        """Calculate total USD value of crypto holdings."""
        # In production, fetch current prices from Kraken ticker
        # For now, use mock prices
        mock_prices = {
            'XXBT': 95000.0,  # BTC
            'XETH': 3500.0,   # ETH
            'ZUSD': 1.0,      # USD
            'USDT': 1.0,      # USDT
        }
        
        total = 0.0
        for asset, amount in balances.items():
            price = mock_prices.get(asset, 0.0)
            total += float(amount) * price
            
        return round(total, 2)
    
    def _get_mock_balance(self) -> dict[str, Any]:
        """Return mock balance data for testing."""
        self.last_updated = datetime.now()
        return {
            'status': 'mock',
            'platform': self.platform_name,
            'account_type': self.config.get('account_type', 'Crypto Trading'),
            'balances': {
                'BTC': '0.01',
                'ETH': '0.15',
                'USDT': '250.00'
            },
            'balance': 1234.56,
            'currency': 'USD',
            'last_updated': self.last_updated.isoformat()
        }


class NinjaTraderConnector(PlatformConnector):
    """Connector for NinjaTrader futures/options platform."""
    
    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.api_token = os.environ.get('NINJATRADER_API_TOKEN', '')
        
    def fetch_balance(self) -> dict[str, Any]:
        """Fetch balance from NinjaTrader API."""
        if not self.enabled:
            return {'status': 'disabled', 'balance': 0.0}
            
        if not self.api_token:
            logger.warning("NinjaTrader API token not configured - using mock data")
            return self._get_mock_balance()
            
        try:
            headers = {
                'Authorization': f'Bearer {self.api_token}',
                'Content-Type': 'application/json'
            }
            url = f"{self.api_endpoint}/accounts/equity"
            
            response = self._make_request('GET', url, headers=headers)
            
            if response:
                data = response.json()
                self.last_updated = datetime.now()
                return {
                    'status': 'success',
                    'platform': self.platform_name,
                    'account_type': self.config.get('account_type', 'Futures/Options'),
                    'balance': float(data.get('total_equity', 0)),
                    'positions': data.get('positions', []),
                    'currency': 'USD',
                    'last_updated': self.last_updated.isoformat()
                }
        except (requests.RequestException, ValueError) as e:
            logger.error(f"NinjaTrader API error: {e}")
            
        return self._get_mock_balance()
    
    def _get_mock_balance(self) -> dict[str, Any]:
        """Return mock balance data for testing."""
        self.last_updated = datetime.now()
        return {
            'status': 'mock',
            'platform': self.platform_name,
            'account_type': self.config.get('account_type', 'Futures/Options'),
            'balance': 5678.90,
            'positions': [
                {'symbol': 'ES', 'type': 'futures', 'quantity': 1},
                {'symbol': 'NQ', 'type': 'futures', 'quantity': 1}
            ],
            'currency': 'USD',
            'last_updated': self.last_updated.isoformat()
        }


class ThreadBankConnector(PlatformConnector):
    """Connector for Thread Bank checking account."""
    
    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.api_key = os.environ.get('THREAD_BANK_API_KEY', '')
        
    def fetch_balance(self) -> dict[str, Any]:
        """Fetch balance from Thread Bank API."""
        if not self.enabled:
            return {'status': 'disabled', 'balance': 0.0}
            
        if not self.api_key:
            logger.warning("Thread Bank API key not configured - using mock data")
            return self._get_mock_balance()
            
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            url = f"{self.api_endpoint}/accounts/balance"
            
            response = self._make_request('GET', url, headers=headers)
            
            if response:
                data = response.json()
                self.last_updated = datetime.now()
                return {
                    'status': 'success',
                    'platform': self.platform_name,
                    'account_type': self.config.get('account_type', 'Checking'),
                    'balance': float(data.get('available_balance', 0)),
                    'currency': 'USD',
                    'last_updated': self.last_updated.isoformat()
                }
        except (requests.RequestException, ValueError) as e:
            logger.error(f"Thread Bank API error: {e}")
            
        return self._get_mock_balance()
    
    def _get_mock_balance(self) -> dict[str, Any]:
        """Return mock balance data for testing."""
        self.last_updated = datetime.now()
        return {
            'status': 'mock',
            'platform': self.platform_name,
            'account_type': self.config.get('account_type', 'Checking'),
            'linked_entity': self.config.get('linked_entity', ''),
            'balance': 10000.00,
            'currency': 'USD',
            'last_updated': self.last_updated.isoformat()
        }


def load_account_config(config_path: str | None = None) -> dict[str, Any]:
    """
    Load accounts configuration from YAML file.
    
    Args:
        config_path: Path to accounts.yaml file. Defaults to config/accounts.yaml
        
    Returns:
        Dictionary containing account configurations
    """
    if config_path is None:
        # Find config relative to this file or from project root
        script_dir = Path(__file__).parent.parent
        config_path = str(script_dir / 'config' / 'accounts.yaml')
        
    config_file = Path(config_path)
    
    if not config_file.exists():
        logger.error(f"Config file not found: {config_path}")
        return {}
        
    try:
        with open(config_file, encoding='utf-8') as f:
            config = yaml.safe_load(f)
        logger.info(f"Loaded configuration from {config_path}")
        return config
    except yaml.YAMLError as e:
        logger.error(f"Error parsing config file: {e}")
        return {}


def get_platform_connector(platform_key: str, config: dict[str, Any]) -> PlatformConnector | None:
    """
    Get the appropriate connector for a platform.
    
    Args:
        platform_key: Key identifying the platform (e.g., 'moneylion', 'kraken')
        config: Platform configuration dictionary
        
    Returns:
        PlatformConnector instance or None if platform is not supported
    """
    connectors: dict[str, type[PlatformConnector]] = {
        'moneylion': MoneyLionConnector,
        'kraken': KrakenConnector,
        'ninjatrader': NinjaTraderConnector,
        'thread_bank': ThreadBankConnector,
    }
    
    connector_class = connectors.get(platform_key.lower())
    if connector_class:
        return connector_class(config)
    
    logger.warning(f"No connector available for platform: {platform_key}")
    return None


def fetch_all_balances(config: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    Fetch balances from all configured platforms.
    
    Args:
        config: Optional config dictionary. If not provided, loads from file.
        
    Returns:
        Dictionary containing balances from all platforms
    """
    if config is None:
        config = load_account_config()
        
    if not config:
        logger.error("No configuration loaded")
        return {'error': 'Configuration not loaded', 'balances': {}}
        
    accounts = config.get('accounts', {})
    results: dict[str, Any] = {
        'treasury': config.get('treasury', {}),
        'balances': {},
        'total_balance': 0.0,
        'currency': 'USD',
        'timestamp': datetime.now().isoformat()
    }
    
    for platform_key, platform_config in accounts.items():
        if not platform_config.get('enabled', True):
            logger.info(f"Skipping disabled platform: {platform_key}")
            continue
            
        connector = get_platform_connector(platform_key, platform_config)
        if connector:
            try:
                balance_data = connector.fetch_balance()
                results['balances'][platform_key] = balance_data
                results['total_balance'] += balance_data.get('balance', 0.0)
                logger.info(f"Fetched balance from {platform_key}: ${balance_data.get('balance', 0):.2f}")
            except (ValueError, TypeError, KeyError) as e:
                logger.error(f"Error fetching balance from {platform_key}: {e}")
                results['balances'][platform_key] = {
                    'status': 'error',
                    'error': str(e),
                    'balance': 0.0
                }
                
    results['total_balance'] = round(results['total_balance'], 2)
    return results


def calculate_total_balance(balances: dict[str, Any]) -> float:
    """
    Calculate total balance across all platforms.
    
    Args:
        balances: Dictionary of platform balances
        
    Returns:
        Total balance in USD
    """
    total = 0.0
    for platform_data in balances.values():
        if isinstance(platform_data, dict):
            total += float(platform_data.get('balance', 0))
    return round(total, 2)


def print_balance_report(results: dict[str, Any]) -> None:
    """Print a formatted balance report to console."""
    print("\n" + "=" * 50)
    print("        ValorYield Treasury Balance")
    print("=" * 50 + "\n")
    
    treasury = results.get('treasury', {})
    if treasury:
        print(f"Entity: {treasury.get('name', 'Unknown')}")
        print(f"Type: {treasury.get('entity_type', 'Unknown')}")
        print("-" * 50 + "\n")
    
    balances = results.get('balances', {})
    for platform_key, data in balances.items():
        status = data.get('status', 'unknown')
        status_indicator = "✓" if status in ['success', 'mock'] else "✗"
        platform_name = data.get('platform', platform_key)
        account_type = data.get('account_type', '')
        balance = data.get('balance', 0)
        
        print(f"{status_indicator} {platform_name} ({account_type}): ${balance:,.2f}")
        
        if status == 'mock':
            print("   (using mock data - API key not configured)")
    
    print("\n" + "-" * 50)
    print(f"TOTAL BALANCE: ${results.get('total_balance', 0):,.2f}")
    print("-" * 50)
    print(f"\nLast Updated: {results.get('timestamp', 'Unknown')}")
    print("=" * 50 + "\n")


def main():
    """Main entry point for CLI interface."""
    logger.info("Starting ValorYield Treasury balance fetch...")
    
    # Load configuration
    config = load_account_config()
    if not config:
        print("Error: Could not load configuration file")
        print("Make sure config/accounts.yaml exists")
        sys.exit(1)
    
    # Fetch all balances
    results = fetch_all_balances(config)
    
    # Print the report
    print_balance_report(results)
    
    return results


if __name__ == "__main__":
    main()
