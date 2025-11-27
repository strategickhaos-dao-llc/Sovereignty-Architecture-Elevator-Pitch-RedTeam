#!/usr/bin/env python3
"""
nightly_refinery.py
Nightly portfolio equity and drift check for the Live Hybrid Refinery
"""

import datetime
from pathlib import Path

import pandas as pd
import yaml
import yfinance as yf


def load_config() -> list:
    """Load flow.yaml configuration"""
    config_path = Path(__file__).parent / "flow.yaml"
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)["core_tickers"]


def main() -> None:
    """Run nightly equity and drift check"""
    config = load_config()

    tickers = [x["ticker"] for x in config]
    data = yf.download(tickers, period="2d", progress=False)["Adj Close"]
    prices = data.iloc[-1]

    total = 0.0
    for pos in config:
        value = pos["shares"] * prices[pos["ticker"]]
        pos["value"] = round(value, 2)
        total += value

    for pos in config:
        pos["weight"] = pos["value"] / total

    max_drift = max(abs(p["weight"] - p["target"]) for p in config)

    print(
        f"{datetime.date.today()} | Equity: ${total:.2f} | Drift max: {max_drift:.1%}"
    )
    # → add your email alert here if you want


if __name__ == "__main__":
    main()
