#!/usr/bin/env python3
"""
Hybrid Refinery RANCO Executor
Run on the 1st of each month (or when adding lump sum cash).
Calculates and displays rebalancing orders for SwarmGate strategy.
Strategickhaos Empire Investment System
"""

import yaml
import yfinance as yf
from pathlib import Path


def load_config(config_path: str = "flow.yaml") -> dict:
    """Load portfolio configuration from YAML file."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def get_realtime_prices(tickers: list) -> dict:
    """Fetch real-time market prices for all tickers."""
    ticker_objs = yf.Tickers(" ".join(tickers))
    prices = {}
    for ticker in tickers:
        try:
            info = ticker_objs.tickers[ticker].info
            prices[ticker] = info.get(
                "regularMarketPrice", info.get("previousClose", 0)
            )
        except (KeyError, AttributeError):
            # Fallback to historical data if real-time fails
            try:
                data = yf.download(ticker, period="1d", progress=False)
                if not data.empty:
                    prices[ticker] = float(data["Close"].iloc[-1])
                else:
                    print(f"Warning: No data available for {ticker}, using 0")
                    prices[ticker] = 0.0
            except Exception as e:
                print(f"Warning: Failed to fetch price for {ticker}: {e}")
                prices[ticker] = 0.0
    return prices


def calculate_rebalancing_orders(
    config: dict, prices: dict, cash: float, min_order: float = 3.0
) -> list:
    """Calculate buy orders needed to rebalance portfolio."""
    orders = []

    # Calculate total equity including new cash
    total_equity = cash
    for pos in config["core_positions"]:
        ticker = pos["ticker"]
        total_equity += pos["shares"] * prices[ticker]

    # Calculate orders for each position
    for pos in config["core_positions"]:
        ticker = pos["ticker"]
        current_price = prices[ticker]
        target_value = total_equity * pos["target_weight"]
        current_value = pos["shares"] * current_price
        dollar_gap = target_value - current_value

        # Only buy if gap exceeds minimum order threshold
        if dollar_gap > min_order:
            shares_to_buy = dollar_gap / current_price
            orders.append(
                {
                    "action": "BUY",
                    "ticker": ticker,
                    "shares": shares_to_buy,
                    "price": current_price,
                    "dollar_amount": dollar_gap,
                }
            )

    return orders


def run_ranco_executor(cash: float = 36.40):
    """Execute RANCO rebalancing calculation."""
    # Load configuration
    script_dir = Path(__file__).parent
    config_path = script_dir / "flow.yaml"
    config = load_config(str(config_path))

    # Get tickers
    tickers = [pos["ticker"] for pos in config["core_positions"]]

    # Fetch current prices
    prices = get_realtime_prices(tickers)

    # Calculate rebalancing orders
    orders = calculate_rebalancing_orders(config, prices, cash)

    # Display results
    print("=== SwarmGate Orders ===")
    if orders:
        for order in orders:
            print(
                f"{order['action']:4} {order['shares']:.4f} "
                f"{order['ticker']} @ ${order['price']:.2f}"
            )
    else:
        print("No rebalancing orders needed at this time.")

    print(
        "\nSwarmGate 7% routed → "
        "$20.80 SGOV | $10.40 AI-Fuel | $5.20 BTC/ETH cold"
    )


if __name__ == "__main__":
    # Default monthly contribution - change when adding extra lump sums
    MONTHLY_CASH = 36.40
    run_ranco_executor(MONTHLY_CASH)
