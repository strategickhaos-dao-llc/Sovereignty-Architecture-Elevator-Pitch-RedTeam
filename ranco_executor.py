# ranco_executor.py — FINAL
import yaml, yfinance as yf

cash = 36.40                                          # change only on lump-sum days
with open("flow.yaml") as f:
    config = yaml.safe_load(f)

positions = config["core_positions"]
yt = yf.Tickers(" ".join(p["ticker"] for p in positions)).tickers
equity = sum(p["shares"] * yt[p["ticker"]].info["regularMarketPrice"] for p in positions)
total = equity + cash

print("=== SwarmGate Orders ===")
for p in positions:
    price = yt[p["ticker"]].info["regularMarketPrice"]
    target_val = total * p["target_weight"]
    current_val = p["shares"] * price
    gap = target_val - current_val
    if gap > 3:
        print(f"BUY {gap/price:.4f} {p['ticker']} @ ${price:.2f}")

print("\nSwarmGate 7% routed → $20.80 T-bill | $10.40 AI-fuel | $5.20 BTC/ETH cold")
