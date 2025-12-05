#!/usr/bin/env python3
"""
Hybrid Refinery Nightly Monitor
Run every night at 3 AM to monitor portfolio drift and performance.
Strategickhaos Empire Investment System
"""

import yaml
import yfinance as yf
from datetime import datetime
from pathlib import Path


def load_config(config_path: str = "flow.yaml") -> dict:
    """Load portfolio configuration from YAML file."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def get_current_prices(tickers: list) -> dict:
    """Fetch current adjusted close prices for all tickers."""
    data = yf.download(tickers, period="1d", progress=False)["Adj Close"]
    if len(tickers) == 1:
        return {tickers[0]: float(data.iloc[-1])}
    return {ticker: float(data[ticker].iloc[-1]) for ticker in tickers}


def calculate_portfolio_metrics(config: dict, prices: dict) -> tuple:
    """Calculate portfolio values, weights, and drift for all positions."""
    lines = []
    total_equity = 0.0

    # First pass: calculate total equity
    for pos in config["core_positions"]:
        ticker = pos["ticker"]
        value = pos["shares"] * prices[ticker]
        total_equity += value

    # Add swarmgate allocation to total
    total_equity += config["swarmgate_monthly"]

    # Second pass: calculate weights and drift
    for pos in config["core_positions"]:
        ticker = pos["ticker"]
        price = prices[ticker]
        value = pos["shares"] * price
        weight = value / total_equity if total_equity > 0 else 0
        drift = weight - pos["target_weight"]

        lines.append(
            f"{ticker:6} {pos['shares']:8.4f} × ${price:6.2f} = "
            f"${value:7.2f} ({weight:.1%}) drift {drift:+.1%}"
        )

    return lines, total_equity


def run_nightly_refinery():
    """Execute nightly portfolio monitoring."""
    # Load configuration
    script_dir = Path(__file__).parent
    config_path = script_dir / "flow.yaml"
    config = load_config(str(config_path))

    # Get tickers
    tickers = [pos["ticker"] for pos in config["core_positions"]]

    # Fetch current prices
    prices = get_current_prices(tickers)

    # Calculate metrics
    lines, total_equity = calculate_portfolio_metrics(config, prices)

    # Build output
    output = [f"Hybrid Refinery Nightly — {datetime.now():%Y-%m-%d}\n"]
    output.extend(lines)
    output.append(f"\nTotal Equity ≈ ${total_equity:.2f}")

    # Print results
    result = "\n".join(output)
    print(result)

    # Optionally save to log file
    log_path = script_dir / "refinery_log.txt"
    with open(log_path, "a") as f:
        f.write(result + "\n\n" + "=" * 60 + "\n\n")

    return result


if __name__ == "__main__":
    run_nightly_refinery()
