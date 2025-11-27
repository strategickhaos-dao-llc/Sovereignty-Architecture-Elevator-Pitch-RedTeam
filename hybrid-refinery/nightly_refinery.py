#!/usr/bin/env python3
"""
nightly_refinery.py - Nightly Equity and Drift Check

Performs daily monitoring of portfolio equity and drift levels.
Add email alert integration as needed.
"""

import datetime
import yaml
import yfinance as yf


def main():
    """Run nightly equity and drift check."""
    with open('flow.yaml', encoding='utf-8') as f:
        config = yaml.safe_load(f)['core_tickers']

    tickers = [x['ticker'] for x in config]
    data = yf.download(tickers, period='2d')['Adj Close']
    prices = data.iloc[-1]

    total = 0
    for pos in config:
        value = pos['shares'] * prices[pos['ticker']]
        pos['value'] = round(value, 2)
        total += value

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
