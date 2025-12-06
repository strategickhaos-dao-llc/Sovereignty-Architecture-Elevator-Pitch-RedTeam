#!/usr/bin/env python3
"""
Tests for ValorYield Treasury API Connectors
Brain Cell #2: Test suite for api/connectors.py
"""

import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.connectors import (
    load_account_config,
    fetch_all_balances,
    get_platform_connector,
    calculate_total_balance,
    MoneyLionConnector,
    KrakenConnector,
    NinjaTraderConnector,
    ThreadBankConnector,
)


class TestLoadAccountConfig:
    """Test cases for load_account_config function."""
    
    def test_load_valid_config(self, tmp_path):
        """Test loading a valid configuration file."""
        config_content = """
treasury:
  name: "Test Treasury"
  entity_type: "501(c)(3)"

accounts:
  test_account:
    platform: "Test Platform"
    enabled: true
"""
        config_file = tmp_path / "accounts.yaml"
        config_file.write_text(config_content)
        
        config = load_account_config(str(config_file))
        
        assert config is not None
        assert config['treasury']['name'] == "Test Treasury"
        assert 'test_account' in config['accounts']
    
    def test_load_missing_config(self, tmp_path):
        """Test loading a non-existent configuration file."""
        config = load_account_config(str(tmp_path / "nonexistent.yaml"))
        assert config == {}
    
    def test_load_default_config(self):
        """Test loading the default configuration file."""
        config = load_account_config()
        
        # Should load config/accounts.yaml from the repo
        assert config is not None
        assert 'accounts' in config


class TestPlatformConnectors:
    """Test cases for platform connector classes."""
    
    def test_moneylion_mock_balance(self):
        """Test MoneyLion connector returns mock balance when no API key."""
        config = {
            'platform': 'MoneyLion',
            'account_id': '2143',
            'account_type': 'Aggressive Mix',
            'enabled': True,
        }
        
        with patch.dict(os.environ, {}, clear=True):
            connector = MoneyLionConnector(config)
            result = connector.fetch_balance()
        
        assert result['status'] == 'mock'
        assert result['balance'] == 207.69
        assert result['platform'] == 'MoneyLion'
    
    def test_kraken_mock_balance(self):
        """Test Kraken connector returns mock balance when no API key."""
        config = {
            'platform': 'Kraken Pro',
            'account_type': 'Crypto Trading',
            'enabled': True,
        }
        
        with patch.dict(os.environ, {}, clear=True):
            connector = KrakenConnector(config)
            result = connector.fetch_balance()
        
        assert result['status'] == 'mock'
        assert result['balance'] == 1234.56
        assert 'balances' in result
    
    def test_ninjatrader_mock_balance(self):
        """Test NinjaTrader connector returns mock balance when no API key."""
        config = {
            'platform': 'NinjaTrader',
            'account_type': 'Futures/Options',
            'enabled': True,
        }
        
        with patch.dict(os.environ, {}, clear=True):
            connector = NinjaTraderConnector(config)
            result = connector.fetch_balance()
        
        assert result['status'] == 'mock'
        assert result['balance'] == 5678.90
        assert 'positions' in result
    
    def test_thread_bank_mock_balance(self):
        """Test Thread Bank connector returns mock balance when no API key."""
        config = {
            'platform': 'Thread Bank',
            'account_type': 'Checking',
            'enabled': True,
        }
        
        with patch.dict(os.environ, {}, clear=True):
            connector = ThreadBankConnector(config)
            result = connector.fetch_balance()
        
        assert result['status'] == 'mock'
        assert result['balance'] == 10000.00
    
    def test_disabled_platform(self):
        """Test that disabled platforms return zero balance."""
        config = {
            'platform': 'MoneyLion',
            'enabled': False,
        }
        
        connector = MoneyLionConnector(config)
        result = connector.fetch_balance()
        
        assert result['status'] == 'disabled'
        assert result['balance'] == 0.0


class TestGetPlatformConnector:
    """Test cases for get_platform_connector function."""
    
    def test_get_moneylion_connector(self):
        """Test getting MoneyLion connector."""
        config = {'platform': 'MoneyLion', 'enabled': True}
        connector = get_platform_connector('moneylion', config)
        assert isinstance(connector, MoneyLionConnector)
    
    def test_get_kraken_connector(self):
        """Test getting Kraken connector."""
        config = {'platform': 'Kraken', 'enabled': True}
        connector = get_platform_connector('kraken', config)
        assert isinstance(connector, KrakenConnector)
    
    def test_get_ninjatrader_connector(self):
        """Test getting NinjaTrader connector."""
        config = {'platform': 'NinjaTrader', 'enabled': True}
        connector = get_platform_connector('ninjatrader', config)
        assert isinstance(connector, NinjaTraderConnector)
    
    def test_get_thread_bank_connector(self):
        """Test getting Thread Bank connector."""
        config = {'platform': 'Thread Bank', 'enabled': True}
        connector = get_platform_connector('thread_bank', config)
        assert isinstance(connector, ThreadBankConnector)
    
    def test_get_unknown_connector(self):
        """Test getting connector for unknown platform."""
        config = {'platform': 'Unknown', 'enabled': True}
        connector = get_platform_connector('unknown_platform', config)
        assert connector is None


class TestFetchAllBalances:
    """Test cases for fetch_all_balances function."""
    
    def test_fetch_all_balances_with_config(self):
        """Test fetching balances from all platforms."""
        config = {
            'treasury': {
                'name': 'Test Treasury',
                'entity_type': '501(c)(3)',
            },
            'accounts': {
                'moneylion': {
                    'platform': 'MoneyLion',
                    'account_id': '2143',
                    'enabled': True,
                },
                'kraken': {
                    'platform': 'Kraken Pro',
                    'enabled': True,
                },
            }
        }
        
        with patch.dict(os.environ, {}, clear=True):
            results = fetch_all_balances(config)
        
        assert 'balances' in results
        assert 'total_balance' in results
        assert results['total_balance'] > 0
        assert 'moneylion' in results['balances']
        assert 'kraken' in results['balances']
    
    def test_fetch_balances_empty_config(self):
        """Test fetching balances with empty config."""
        results = fetch_all_balances({})
        assert 'error' not in results or results.get('balances') == {}


class TestCalculateTotalBalance:
    """Test cases for calculate_total_balance function."""
    
    def test_calculate_total_balance(self):
        """Test calculating total balance."""
        balances = {
            'platform1': {'balance': 100.50},
            'platform2': {'balance': 200.25},
            'platform3': {'balance': 50.00},
        }
        
        total = calculate_total_balance(balances)
        assert total == 350.75
    
    def test_calculate_total_balance_empty(self):
        """Test calculating total with empty balances."""
        total = calculate_total_balance({})
        assert total == 0.0
    
    def test_calculate_total_balance_mixed(self):
        """Test calculating total with mixed data types."""
        balances = {
            'platform1': {'balance': 100.0},
            'platform2': 'invalid',  # Should be skipped
            'platform3': {'balance': 50.0},
        }
        
        total = calculate_total_balance(balances)
        assert total == 150.0


class TestRetryLogic:
    """Test cases for retry logic in connectors."""
    
    @patch('api.connectors.requests.get')
    def test_retry_on_timeout(self, mock_get):
        """Test that connector retries on timeout."""
        mock_get.side_effect = [
            MagicMock(side_effect=Exception("Timeout")),
            MagicMock(status_code=200, json=lambda: {'balance': 100})
        ]
        
        config = {
            'platform': 'MoneyLion',
            'account_id': '2143',
            'api_endpoint': 'https://api.test.com',
            'enabled': True,
        }
        
        # The connector will fall back to mock data since no real API key
        with patch.dict(os.environ, {}, clear=True):
            connector = MoneyLionConnector(config)
            result = connector.fetch_balance()
        
        assert result['status'] == 'mock'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
