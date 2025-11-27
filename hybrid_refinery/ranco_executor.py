#!/usr/bin/env python3
"""
Strategickhaos Hybrid Refinery - RANCO Executor
Rebalancing and New Capital Orchestrator.

Features:
- Detects position drift from target weights
- Executes rebalancing when drift exceeds 12%
- Allocates monthly contributions to most underweight positions
- Logs all transactions for audit trail
"""

import csv
import datetime
import json
import logging
import os
from pathlib import Path
from typing import Optional

import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Portfolio holdings as of November 27, 2025
PORTFOLIO = {
    'JPM': {'shares': 0.1555, 'cost_basis': 36.40, 'target_weight': 7.00, 'name': 'JPMorgan Chase'},
    'CB': {'shares': 0.1238, 'cost_basis': 36.40, 'target_weight': 7.01, 'name': 'Chubb Limited'},
    'TD': {'shares': 0.617, 'cost_basis': 36.40, 'target_weight': 7.00, 'name': 'Toronto-Dominion Bank'},
    'PG': {'shares': 0.244, 'cost_basis': 41.60, 'target_weight': 8.00, 'name': 'Procter & Gamble'},
    'KO': {'shares': 0.592, 'cost_basis': 41.60, 'target_weight': 8.00, 'name': 'Coca-Cola'},
    'PEP': {'shares': 0.206, 'cost_basis': 36.40, 'target_weight': 7.00, 'name': 'PepsiCo'},
    'CL': {'shares': 0.305, 'cost_basis': 31.20, 'target_weight': 6.00, 'name': 'Colgate-Palmolive'},
    'NEE': {'shares': 0.428, 'cost_basis': 36.40, 'target_weight': 7.00, 'name': 'NextEra Energy'},
    'O': {'shares': 0.676, 'cost_basis': 41.60, 'target_weight': 8.01, 'name': 'Realty Income'},
    'VICI': {'shares': 1.112, 'cost_basis': 36.40, 'target_weight': 7.01, 'name': 'VICI Properties'},
    'PLD': {'shares': 0.267, 'cost_basis': 31.20, 'target_weight': 5.99, 'name': 'Prologis'},
    'ABBV': {'shares': 0.185, 'cost_basis': 36.40, 'target_weight': 7.00, 'name': 'AbbVie'},
    'JNJ': {'shares': 0.255, 'cost_basis': 41.60, 'target_weight': 8.00, 'name': 'Johnson & Johnson'},
    'XOM': {'shares': 0.255, 'cost_basis': 31.20, 'target_weight': 6.00, 'name': 'Exxon Mobil'},
    'WEC': {'shares': 0.387, 'cost_basis': 36.40, 'target_weight': 7.00, 'name': 'WEC Energy Group'},
}

# Configuration
MONTHLY_CONTRIBUTION = 36.40
DRIFT_THRESHOLD = 12.0  # Percentage drift that triggers rebalancing

# Base directory
BASE_DIR = Path(__file__).parent
LOGS_DIR = BASE_DIR / 'logs'


def ensure_directories():
    """Create necessary directories."""
    LOGS_DIR.mkdir(exist_ok=True)


def get_current_prices() -> dict:
    """
    Fetch current stock prices.
    
    In production, this would use yfinance or broker API.
    For demonstration, returns estimated prices.
    """
    prices = {}
    
    try:
        import yfinance as yf
        
        tickers = list(PORTFOLIO.keys())
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="1d")
                if not hist.empty:
                    prices[ticker] = float(hist['Close'].iloc[-1])
                else:
                    # Fallback to estimated price
                    prices[ticker] = PORTFOLIO[ticker]['cost_basis'] / PORTFOLIO[ticker]['shares']
            except Exception as e:
                logger.warning(f"Could not fetch {ticker}: {e}")
                prices[ticker] = PORTFOLIO[ticker]['cost_basis'] / PORTFOLIO[ticker]['shares']
                
    except ImportError:
        logger.warning("yfinance not installed, using estimated prices")
        for ticker, data in PORTFOLIO.items():
            # Use cost basis to estimate price
            prices[ticker] = data['cost_basis'] / data['shares']
            
    return prices


def calculate_position_drift(prices: dict) -> list:
    """Calculate drift for each position."""
    total_value = 0
    positions = []
    
    # First pass: calculate total value
    for ticker, data in PORTFOLIO.items():
        price = prices.get(ticker, data['cost_basis'] / data['shares'])
        market_value = data['shares'] * price
        total_value += market_value
        
    # Second pass: calculate drift
    for ticker, data in PORTFOLIO.items():
        price = prices.get(ticker, data['cost_basis'] / data['shares'])
        market_value = data['shares'] * price
        actual_weight = (market_value / total_value) * 100
        target_weight = data['target_weight']
        drift = actual_weight - target_weight
        drift_pct = (drift / target_weight) * 100 if target_weight > 0 else 0
        
        positions.append({
            'ticker': ticker,
            'name': data['name'],
            'shares': data['shares'],
            'price': price,
            'market_value': market_value,
            'cost_basis': data['cost_basis'],
            'actual_weight': actual_weight,
            'target_weight': target_weight,
            'drift': drift,
            'drift_pct': drift_pct
        })
        
    return positions, total_value


def find_most_underweight(positions: list) -> dict:
    """Find the most underweight position for contribution allocation."""
    underweight = [p for p in positions if p['drift_pct'] < 0]
    
    if not underweight:
        # All positions at or above target, choose smallest actual weight
        return min(positions, key=lambda x: x['actual_weight'])
        
    return min(underweight, key=lambda x: x['drift_pct'])


def find_positions_to_rebalance(positions: list, threshold: float) -> tuple:
    """Find positions that exceed drift threshold."""
    overweight = [p for p in positions if p['drift_pct'] > threshold]
    underweight = [p for p in positions if p['drift_pct'] < -threshold]
    
    return overweight, underweight


def calculate_rebalance_trades(positions: list, total_value: float) -> list:
    """Calculate trades needed to rebalance portfolio."""
    trades = []
    
    for pos in positions:
        target_value = total_value * (pos['target_weight'] / 100)
        current_value = pos['market_value']
        diff = target_value - current_value
        
        if abs(diff) > 5:  # Minimum trade size $5
            shares_to_trade = diff / pos['price']
            trades.append({
                'ticker': pos['ticker'],
                'name': pos['name'],
                'action': 'BUY' if diff > 0 else 'SELL',
                'shares': abs(shares_to_trade),
                'estimated_value': abs(diff),
                'current_weight': pos['actual_weight'],
                'target_weight': pos['target_weight'],
                'drift_pct': pos['drift_pct']
            })
            
    return trades


def allocate_contribution(amount: float, target_position: dict, prices: dict) -> dict:
    """Allocate contribution to target position."""
    ticker = target_position['ticker']
    price = prices.get(ticker, target_position['price'])
    shares_to_buy = amount / price
    
    return {
        'ticker': ticker,
        'name': target_position['name'],
        'action': 'BUY',
        'amount': amount,
        'price': price,
        'shares': shares_to_buy,
        'reason': f"Most underweight position ({target_position['drift_pct']:.1f}% drift)"
    }


def log_transaction(transaction: dict):
    """Log transaction to CSV."""
    csv_path = LOGS_DIR / 'transactions.csv'
    today = datetime.datetime.now().isoformat()
    
    file_exists = csv_path.exists()
    
    with open(csv_path, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['timestamp', 'ticker', 'action', 'shares', 
                           'price', 'amount', 'reason', 'executed'])
        writer.writerow([
            today,
            transaction['ticker'],
            transaction['action'],
            f"{transaction['shares']:.4f}",
            f"{transaction.get('price', 0):.2f}",
            f"{transaction.get('amount', transaction.get('estimated_value', 0)):.2f}",
            transaction.get('reason', ''),
            'DRY_RUN'  # In production, this would be 'EXECUTED' after broker confirmation
        ])
        
    logger.info(f"Transaction logged: {transaction['action']} {transaction['shares']:.4f} {transaction['ticker']}")


def execute_monthly_contribution(dry_run: bool = True, contribution: float = None):
    """Execute monthly contribution allocation."""
    amount = contribution if contribution is not None else MONTHLY_CONTRIBUTION
    
    logger.info("=" * 50)
    logger.info("RANCO Executor - Monthly Contribution")
    logger.info("=" * 50)
    
    ensure_directories()
    
    # Get current prices
    prices = get_current_prices()
    
    # Calculate position drift
    positions, total_value = calculate_position_drift(prices)
    
    # Find most underweight position
    target = find_most_underweight(positions)
    
    logger.info(f"Current portfolio value: ${total_value:.2f}")
    logger.info(f"Monthly contribution: ${amount:.2f}")
    logger.info(f"Target position: {target['ticker']} ({target['name']})")
    logger.info(f"Target drift: {target['drift_pct']:.2f}%")
    
    # Calculate allocation
    allocation = allocate_contribution(amount, target, prices)
    
    print(f"\n💰 Monthly Contribution Allocation")
    print(f"   Amount: ${allocation['amount']:.2f}")
    print(f"   Target: {allocation['ticker']} ({allocation['name']})")
    print(f"   Price: ${allocation['price']:.2f}")
    print(f"   Shares: {allocation['shares']:.4f}")
    print(f"   Reason: {allocation['reason']}")
    
    if dry_run:
        print(f"\n⚠️  DRY RUN - No actual trade executed")
        allocation['executed'] = False
    else:
        # In production, would execute via broker API
        print(f"\n✅ Trade would be executed via broker API")
        allocation['executed'] = True
        
    # Log the transaction
    log_transaction(allocation)
    
    return allocation


def check_rebalancing_needed(dry_run: bool = True):
    """Check if rebalancing is needed and calculate trades."""
    logger.info("=" * 50)
    logger.info("RANCO Executor - Drift Check")
    logger.info("=" * 50)
    
    ensure_directories()
    
    # Get current prices
    prices = get_current_prices()
    
    # Calculate position drift
    positions, total_value = calculate_position_drift(prices)
    
    logger.info(f"Current portfolio value: ${total_value:.2f}")
    logger.info(f"Drift threshold: {DRIFT_THRESHOLD}%")
    
    # Find positions exceeding threshold
    overweight, underweight = find_positions_to_rebalance(positions, DRIFT_THRESHOLD)
    
    print(f"\n📊 Drift Analysis")
    print(f"   Portfolio Value: ${total_value:.2f}")
    print(f"   Threshold: {DRIFT_THRESHOLD}%")
    print(f"   Overweight positions: {len(overweight)}")
    print(f"   Underweight positions: {len(underweight)}")
    
    if not overweight and not underweight:
        print(f"\n✅ All positions within {DRIFT_THRESHOLD}% drift tolerance")
        print("   No rebalancing needed")
        return None
        
    # Display drift details
    print(f"\n⚠️  Positions exceeding {DRIFT_THRESHOLD}% drift:")
    for pos in overweight:
        print(f"   🔴 {pos['ticker']:5} +{pos['drift_pct']:.1f}% (overweight)")
    for pos in underweight:
        print(f"   🔵 {pos['ticker']:5} {pos['drift_pct']:.1f}% (underweight)")
        
    # Calculate rebalancing trades
    trades = calculate_rebalance_trades(positions, total_value)
    
    if trades:
        print(f"\n📋 Suggested Rebalancing Trades:")
        for trade in trades:
            symbol = "🟢" if trade['action'] == 'BUY' else "🔴"
            print(f"   {symbol} {trade['action']:4} {trade['shares']:.4f} {trade['ticker']:5} "
                  f"(${trade['estimated_value']:.2f}) - drift: {trade['drift_pct']:.1f}%")
                  
        if dry_run:
            print(f"\n⚠️  DRY RUN - No actual trades executed")
        else:
            print(f"\n✅ Trades would be executed via broker API")
            
        # Log trades
        for trade in trades:
            trade['reason'] = f"Rebalancing - drift {trade['drift_pct']:.1f}%"
            log_transaction(trade)
            
    return trades


def print_portfolio_status():
    """Print current portfolio status."""
    ensure_directories()
    
    prices = get_current_prices()
    positions, total_value = calculate_position_drift(prices)
    
    print("\n" + "=" * 70)
    print("STRATEGICKHAOS HYBRID REFINERY - PORTFOLIO STATUS")
    print("=" * 70)
    print(f"\nDate: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Value: ${total_value:.2f}")
    print(f"Total Cost Basis: ${sum(p['cost_basis'] for p in positions):.2f}")
    print(f"Unrealized G/L: ${total_value - sum(p['cost_basis'] for p in positions):.2f}")
    print("\n" + "-" * 70)
    print(f"{'Ticker':<6} {'Name':<20} {'Shares':>8} {'Value':>10} {'Weight':>8} {'Target':>8} {'Drift':>8}")
    print("-" * 70)
    
    for pos in sorted(positions, key=lambda x: x['drift_pct']):
        drift_indicator = "🔴" if pos['drift_pct'] > 10 else "🔵" if pos['drift_pct'] < -10 else "🟢"
        print(f"{pos['ticker']:<6} {pos['name'][:20]:<20} {pos['shares']:>8.4f} "
              f"${pos['market_value']:>8.2f} {pos['actual_weight']:>7.1f}% "
              f"{pos['target_weight']:>7.1f}% {drift_indicator}{pos['drift_pct']:>6.1f}%")
              
    print("-" * 70)
    print(f"\n{'Legend:':<10} 🔴 >10% overweight | 🔵 >10% underweight | 🟢 on target")
    print("=" * 70)


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='RANCO Executor - Rebalancing and New Capital Orchestrator')
    parser.add_argument('--action', choices=['status', 'contribute', 'rebalance'], 
                       default='status', help='Action to perform')
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Simulate trades without executing (default: True)')
    parser.add_argument('--execute', action='store_true',
                       help='Execute trades (requires broker integration)')
    parser.add_argument('--contribution', type=float, default=MONTHLY_CONTRIBUTION,
                       help=f'Contribution amount (default: ${MONTHLY_CONTRIBUTION})')
    
    args = parser.parse_args()
    dry_run = not args.execute
    contribution_amount = args.contribution
    
    if args.action == 'status':
        print_portfolio_status()
    elif args.action == 'contribute':
        execute_monthly_contribution(dry_run=dry_run, contribution=contribution_amount)
    elif args.action == 'rebalance':
        check_rebalancing_needed(dry_run=dry_run)
        
    return 0


if __name__ == '__main__':
    exit(main())
