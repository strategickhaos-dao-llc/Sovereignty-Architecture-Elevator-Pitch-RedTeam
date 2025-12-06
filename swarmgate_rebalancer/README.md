# SwarmGate Zero-Trust Portfolio Rebalancer

A zero-trust execution wrapper that validates Grok's JSON output, independently verifies all math, and only executes trades after validation passes.

## Features

- **Zero-trust validation**: Independently recomputes all math from Grok's output
- **Dry-run by default**: Requires explicit `--execute` flag for live trading
- **Treasury-first**: Signs and broadcasts treasury transfer before placing orders
- **Locked schemas**: Pydantic models for `flow.yaml` and Grok JSON output
- **Multi-broker support**: Routes orders to Fidelity, Coinbase, Kraken based on symbol

## Installation

```bash
cd swarmgate_rebalancer
pip install -e ".[dev]"
```

## Usage

### Dry Run (Default)

```bash
python -m swarmgate_rebalancer.cli \
  --flow flow.yaml \
  --plan examples/grok_plan.json \
  --positions examples/snapshot.json
```

### Live Execution

```bash
python -m swarmgate_rebalancer.cli \
  --flow flow.yaml \
  --plan examples/grok_plan.json \
  --positions examples/snapshot.json \
  --execute
```

If validation fails, the script exits without touching funds.

## File Formats

### flow.yaml (Configuration)

```yaml
version: 1

portfolio:
  target:
    QQQ:   0.25    # Target allocation weights must sum to 1.0
    TQQQ:  0.20
    BTC:   0.20
    ETH:   0.15
    SOL:   0.10
    SWARM: 0.07    # Treasury cut
    CASH:  0.03    # Emergency buffer
  current: {}      # Populated by your data fetch step

settings:
  paycheck_net: 10666.67      # Net paycheck amount
  treasury_pct: 0.07          # 7% to treasury
  rebalance_threshold: 0.015  # 1.5% deviation trigger
  dry_run: true               # Default to dry-run
  treasury_address: "0x..."
  max_single_order_usd: 5000
```

### grok_plan.json (Grok Output)

```json
{
  "treasury_transfer_usd": 746.67,
  "treasury_tx": "send $746.67 USDC to 0x...",
  "orders": [
    {"symbol": "TQQQ", "usd": 842.12},
    {"symbol": "SOL", "usd": 312.44}
  ],
  "total_invested": 1154.56,
  "new_cash_buffer": 0.00,
  "deviation_after": 0.0031
}
```

### snapshot.json (Portfolio State)

```json
{
  "positions_usd": {
    "QQQ": 12345.67,
    "TQQQ": 8000.00,
    "BTC": 9500.00,
    "ETH": 6800.00,
    "SOL": 4200.00
  },
  "cash_usd": 1500.00,
  "paycheck_net_usd": 10666.67
}
```

## Validation Rules

The validator checks:

1. **Treasury math**: `treasury_transfer_usd == paycheck_net * treasury_pct`
2. **Order totals**: `total_invested == sum(order.usd for each order)`
3. **Order limits**: Each order must be ≤ `max_single_order_usd`
4. **SWARM protection**: SWARM cannot appear in market orders (treasury only)
5. **Authorized symbols**: All order symbols must exist in target allocations
6. **Cash availability**: Orders cannot exceed available cash
7. **Correct direction**: Orders must move underweight assets toward targets

## Development

### Run Tests

```bash
cd swarmgate_rebalancer
pytest tests/ -v
```

### Run Type Checks

```bash
mypy swarmgate_rebalancer/
```

## Architecture

```
swarmgate_rebalancer/
├── __init__.py          # Package init
├── config.py            # Pydantic models for flow.yaml
├── grok_models.py       # Pydantic models for Grok JSON
├── math_validator.py    # Zero-trust math validation
├── treasury.py          # Treasury transfer client (stub)
├── brokers.py           # Multi-broker order routing (stubs)
├── cli.py               # CLI entry point
├── flow.yaml            # Sample configuration
├── pyproject.toml       # Package configuration
├── examples/            # Sample data files
│   ├── grok_plan.json
│   └── snapshot.json
└── tests/               # Unit tests
    ├── test_config.py
    ├── test_grok_models.py
    └── test_math_validator.py
```

## Next Steps

1. **Wire broker APIs**: Implement actual Fidelity/Coinbase/Kraken clients in `brokers.py`
2. **Treasury signing**: Implement real USDC transfer in `treasury.py` using your key management
3. **Automate data fetching**: Build the upstream script that produces `snapshot.json`
4. **Dashboard**: Add monitoring/visualization after core execution is bulletproof

## License

MIT
