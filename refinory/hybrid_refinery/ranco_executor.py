#!/usr/bin/env python3
"""
ranco_executor.py
Monthly capital injection allocation for the Live Hybrid Refinery
(only runs on the 1st with new cash)
"""

from pathlib import Path

import yaml
import yfinance as yf


def load_config() -> list:
    """Load flow.yaml configuration"""
    config_path = Path(__file__).parent / "flow.yaml"
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)["core_tickers"]


def main() -> None:
    """Execute monthly SwarmGate capital injection"""
    cash = 36.40  # SwarmGate injection
    positions = load_config()

    tickers = " ".join(p["ticker"] for p in positions)
    ticker_info = yf.Tickers(tickers).tickers

    total_equity = cash
    for p in positions:
        price = ticker_info[p["ticker"]].info["regularMarketPrice"]
        total_equity += p["shares"] * price

    for p in positions:
        current_price = ticker_info[p["ticker"]].info["regularMarketPrice"]
        target_value = total_equity * p["target"]
        current_value = p["shares"] * current_price
        if target_value - current_value > 3:  # only buy if >$3 underweight
            buy_shares = (target_value - current_value) / current_price
            print(f"BUY {buy_shares:.4f} {p['ticker']} @ ${current_price:.2f}")

    print("SwarmGate 7% routed: $20.80 SGOV | $10.40 AI-Fuel | $5.20 BTC/ETH")


if __name__ == "__main__":
    main()
