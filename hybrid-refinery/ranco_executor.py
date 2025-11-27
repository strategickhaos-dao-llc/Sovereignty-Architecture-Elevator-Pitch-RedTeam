#!/usr/bin/env python3
"""
ranco_executor.py - Monthly Rebalance Executor

Runs on the 1st of each month with new SwarmGate cash injection.
Calculates which positions to buy based on target allocation drift.
"""

import yaml
import yfinance as yf


def main():
    """Execute monthly rebalance calculation."""
    cash = 36.40  # SwarmGate injection

    with open('flow.yaml', encoding='utf-8') as f:
        positions = yaml.safe_load(f)['core_tickers']

    # Get current prices for all tickers
    tickers_str = ' '.join(p['ticker'] for p in positions)
    prices = yf.Tickers(tickers_str).tickers

    # Calculate total equity including new cash
    total_equity = cash
    for p in positions:
        current_price = prices[p['ticker']].info['regularMarketPrice']
        total_equity += p['shares'] * current_price

    print(f"Total Equity (with cash): ${total_equity:.2f}")
    print(f"New Cash: ${cash:.2f}")
    print("-" * 50)

    # Calculate buys needed
    buy_orders = []
    for p in positions:
        current_price = prices[p['ticker']].info['regularMarketPrice']
        target_value = total_equity * p['target']
        current_value = p['shares'] * current_price
        underweight = target_value - current_value

        if underweight > 3:  # only buy if >$3 underweight
            buy_shares = underweight / current_price
            buy_orders.append({
                'ticker': p['ticker'],
                'shares': buy_shares,
                'price': current_price,
                'amount': underweight
            })
            print(f"BUY {buy_shares:.4f} {p['ticker']} @ ${current_price:.2f}")

    if not buy_orders:
        print("No positions underweight by >$3 - portfolio balanced")

    print("-" * 50)
    print("SwarmGate 7% routed: $20.80 SGOV | $10.40 AI-Fuel | $5.20 BTC/ETH")


if __name__ == '__main__':
    main()
