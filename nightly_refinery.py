# nightly_refinery.py — FINAL
import yfinance as yf, yaml
from datetime import datetime

with open("flow.yaml") as f:
    config = yaml.safe_load(f)

positions = config["core_positions"]
tickers = [p["ticker"] for p in positions]
data = yf.download(tickers, period="1d")["Adj Close"]
prices = data.iloc[-1]
equity = sum(p["shares"] * prices[p["ticker"]] for p in positions)

print(f"Hybrid Refinery Nightly — {datetime.now():%Y-%m-%d}")
print(f"Total Equity ≈ ${equity + config['swarmgate_monthly']:.2f}\n")
for p in positions:
    value = p["shares"] * prices[p["ticker"]]
    weight = value / (equity + config["swarmgate_monthly"])
    drift = weight - p["target_weight"]
    print(f"{p['ticker']:6} {p['shares']:8.4f} × ${prices[p['ticker']]:6.2f} = ${value:7.2f}  ({weight:.1%}) drift {drift:+.1%}")
