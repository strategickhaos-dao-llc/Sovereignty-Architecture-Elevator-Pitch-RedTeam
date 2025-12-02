"""CLI wrapper for SwarmGate zero-trust executor.

Default: dry-run. `--execute` flips to real mode,
but ONLY if validation passes.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .brokers import BrokerRouter
from .config import FlowConfig, load_flow_config
from .grok_models import GrokPlan
from .math_validator import PortfolioSnapshot, ValidationResult, validate_plan
from .treasury import TreasuryClient


def load_json(path: str | Path) -> Any:
    """Load JSON from a file."""
    with open(path, "r") as f:
        return json.load(f)


def print_validation_result(result: ValidationResult) -> None:
    """Print validation result to stdout."""
    print("=== VALIDATION ===")
    print(f"OK: {result.ok}")

    if result.errors:
        print("\nErrors:")
        for e in result.errors:
            print(f"  ❌ {e}")

    if result.warnings:
        print("\nWarnings:")
        for w in result.warnings:
            print(f"  ⚠️  {w}")


def print_execution_plan(
    plan: GrokPlan, config: FlowConfig, dry_run: bool
) -> None:
    """Print execution plan to stdout."""
    print("\n=== EXECUTION PLAN ===")
    mode = "🔒 DRY-RUN" if dry_run else "🔥 LIVE"
    print(f"Mode: {mode}")
    print(
        f"Treasury transfer: ${plan.treasury_transfer_usd:.2f} "
        f"to {config.settings.treasury_address}"
    )

    if plan.orders:
        print("\nOrders:")
        for o in plan.orders:
            print(f"  - {o.symbol}: ${o.usd:.2f}")
    else:
        print("\nNo orders to execute.")

    print(f"\nTotal invested: ${plan.total_invested:.2f}")
    print(f"New cash buffer: ${plan.new_cash_buffer:.2f}")
    print(f"Expected deviation after: {plan.deviation_after:.4f}")


def main() -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="SwarmGate zero-trust portfolio rebalancer",
        epilog="By default runs in dry-run mode. Use --execute for live trading.",
    )
    parser.add_argument(
        "--flow",
        required=True,
        help="Path to flow.yaml configuration file",
    )
    parser.add_argument(
        "--plan",
        required=True,
        help="Path to Grok output JSON file",
    )
    parser.add_argument(
        "--positions",
        required=True,
        help="Path to positions snapshot JSON file",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually send money/orders (requires validation to pass)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show verbose output",
    )

    args = parser.parse_args()

    # Load configuration
    try:
        config = load_flow_config(args.flow)
        if args.verbose:
            print(f"Loaded config from {args.flow}")
    except FileNotFoundError:
        print(f"Error: Config file not found: {args.flow}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error loading config: {e}", file=sys.stderr)
        return 1

    # Load Grok plan
    try:
        plan_raw = load_json(args.plan)
        plan = GrokPlan.model_validate(plan_raw)
        if args.verbose:
            print(f"Loaded plan from {args.plan}")
    except FileNotFoundError:
        print(f"Error: Plan file not found: {args.plan}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error loading plan: {e}", file=sys.stderr)
        return 1

    # Load snapshot
    try:
        snapshot_raw = load_json(args.positions)
        snapshot = PortfolioSnapshot(
            positions_usd=snapshot_raw["positions_usd"],
            cash_usd=snapshot_raw["cash_usd"],
            paycheck_net_usd=snapshot_raw["paycheck_net_usd"],
        )
        if args.verbose:
            print(f"Loaded snapshot from {args.positions}")
    except FileNotFoundError:
        print(f"Error: Positions file not found: {args.positions}", file=sys.stderr)
        return 1
    except KeyError as e:
        print(f"Error: Missing key in positions file: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error loading positions: {e}", file=sys.stderr)
        return 1

    # Validate the plan
    result = validate_plan(config, snapshot, plan)
    print_validation_result(result)

    if not result.ok:
        print("\n❌ Refusing to execute due to validation errors.")
        return 2

    # Determine execution mode
    dry_run = not args.execute or config.settings.dry_run

    # Print execution plan
    print_execution_plan(plan, config, dry_run)

    # Execute treasury transfer
    treasury_client = TreasuryClient(address=config.settings.treasury_address)

    print("\n=== EXECUTING ===")

    if dry_run:
        tx_hash = f"dry-run-{plan.treasury_transfer_usd:.2f}"
        print(f"Treasury tx (dry-run): {tx_hash}")
    else:
        try:
            tx_hash = treasury_client.send_usdc(
                plan.treasury_transfer_usd, dry_run=False
            )
            print(f"Treasury tx: {tx_hash}")
        except NotImplementedError as e:
            print(f"Treasury transfer not implemented: {e}", file=sys.stderr)
            return 3

    # Execute orders
    broker_router = BrokerRouter()
    exec_results = broker_router.execute_orders(plan.orders, dry_run=dry_run)

    print("\nOrder results:")
    for r in exec_results:
        status_icon = "✅" if r.status in ("dry-run", "submitted") else "❌"
        order_id_str = f"(id={r.order_id})" if r.order_id else ""
        message_str = f"- {r.message}" if r.message else ""
        print(
            f"  {status_icon} {r.symbol}: ${r.usd:.2f} via {r.broker} "
            f"status={r.status} {order_id_str} {message_str}"
        )

    if dry_run:
        print("\n✅ Dry-run complete. Use --execute to send real orders.")
    else:
        print("\n✅ Execution complete.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
