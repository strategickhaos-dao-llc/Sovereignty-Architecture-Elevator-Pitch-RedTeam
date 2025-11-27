#!/usr/bin/env python3
"""
nightly_refinery.py - Nightly Equity and Drift Check

Performs daily monitoring of portfolio equity and drift levels.
Add email alert integration as needed.
"""

import datetime
import sys
import yaml
import yfinance as yf


def main():
    """Run nightly equity and drift check."""
    with open('flow.yaml', encoding='utf-8') as f:
        config = yaml.safe_load(f)['core_tickers']

    tickers = [x['ticker'] for x in config]
    data = yf.download(tickers, period='2d', progress=False)

    # Handle case where download returns no data
    if data.empty:
        print(f"{datetime.date.today()} | ERROR: Could not fetch market data")
        sys.exit(1)

    # Handle multi-ticker format (Adj Close is a DataFrame) vs single ticker
    if 'Adj Close' in data.columns or len(tickers) == 1:
        adj_close = data['Adj Close'] if 'Adj Close' in data.columns else data
    else:
        adj_close = data['Adj Close']

    prices = adj_close.iloc[-1]

    total = 0
    for pos in config:
        try:
            price = prices[pos['ticker']] if len(tickers) > 1 else prices
            value = pos['shares'] * float(price)
            pos['value'] = round(value, 2)
            total += value
        except (KeyError, TypeError) as e:
            print(f"Warning: Could not get price for {pos['ticker']}: {e}")
            pos['value'] = 0

    if total == 0:
        print(f"{datetime.date.today()} | ERROR: Total equity is zero")
        sys.exit(1)

    # Calculate weights and drift
    for pos in config:
        pos['weight'] = pos['value'] / total

    max_drift = max(abs(p['weight'] - p['target']) for p in config)

    print(f"{datetime.date.today()} | Equity: ${total:.2f} | Drift max: {max_drift:.1%}")

    # Optional: Add email alert here if drift exceeds threshold
    # if max_drift > 0.12:
    #     send_alert_email(total, max_drift)


if __name__ == '__main__':
    main()
