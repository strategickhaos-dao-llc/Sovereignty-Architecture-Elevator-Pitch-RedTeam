#!/usr/bin/env python3
"""
ranco_executor.py - Monthly Rebalance Executor

Runs on the 1st of each month with new SwarmGate cash injection.
Calculates which positions to buy based on target allocation drift.
"""

import yaml
import yfinance as yf

# Minimum underweight threshold to trigger a buy order (in dollars)
MIN_BUY_THRESHOLD = 3.0


def main():
    """Execute monthly rebalance calculation."""
    cash = 36.40  # SwarmGate injection

    with open('flow.yaml', encoding='utf-8') as f:
        positions = yaml.safe_load(f)['core_tickers']

    # Get current prices for all tickers
    tickers_list = [p['ticker'] for p in positions]
    tickers_str = ' '.join(tickers_list)
    tickers_obj = yf.Tickers(tickers_str)

    # Fetch current prices
    current_prices = {}
    for ticker in tickers_list:
        try:
            ticker_info = tickers_obj.tickers[ticker].info
            current_prices[ticker] = ticker_info.get('regularMarketPrice') or ticker_info.get('currentPrice', 0)
        except (KeyError, AttributeError):
            print(f"Warning: Could not fetch price for {ticker}")
            current_prices[ticker] = 0

    # Calculate total equity including new cash
    total_equity = cash
    for p in positions:
        total_equity += p['shares'] * current_prices[p['ticker']]

    print(f"Total Equity (with cash): ${total_equity:.2f}")
    print(f"New Cash: ${cash:.2f}")
    print("-" * 50)

    # Calculate buys needed
    buy_orders = []
    for p in positions:
        price = current_prices[p['ticker']]
        if price <= 0:
            continue

        target_value = total_equity * p['target']
        current_value = p['shares'] * price
        underweight = target_value - current_value

        if underweight > MIN_BUY_THRESHOLD:
            buy_shares = underweight / price
            buy_orders.append({
                'ticker': p['ticker'],
                'shares': buy_shares,
                'price': price,
                'amount': underweight
            })
            print(f"BUY {buy_shares:.4f} {p['ticker']} @ ${price:.2f}")

    if not buy_orders:
        print(f"No positions underweight by >${MIN_BUY_THRESHOLD:.0f} - portfolio balanced")

    print("-" * 50)
    print("SwarmGate 7% routed: $20.80 SGOV | $10.40 AI-Fuel | $5.20 BTC/ETH")


if __name__ == '__main__':
    main()
