#!/usr/bin/env python3
"""
Trading Bot Benchmark Runner - Standalone
Runs only the trading bot benchmarks without dependencies on other test modules
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Import trading bot benchmarks
sys.path.append('benchmarks')
from test_trading_bot import TradingBotBenchmarks


def main():
    """Run trading bot benchmark tests."""
    print("🤖 Trading Bot Benchmark Suite - PID-RANCO System")
    print("=" * 70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    benchmarks = TradingBotBenchmarks()
    
    # Run all trading bot tests (31-35)
    print("Running Tests 31-35...")
    test_results = []
    test_results.append(benchmarks.test_31_simple_backtest_validation())
    test_results.append(benchmarks.test_32_advanced_strategy_performance())
    test_results.append(benchmarks.test_33_stress_test_market_conditions())
    test_results.append(benchmarks.test_34_benchmark_comparison())
    test_results.append(benchmarks.test_35_transaction_cost_impact())
    
    # Display results
    print("\n" + "=" * 70)
    print("📊 Test Results Summary")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for result in test_results:
        status_icon = "✅" if result['status'] == 'PASS' else "❌"
        print(f"\n{status_icon} Test {result['test_id']}: {result['name']}")
        print(f"   Status: {result['status']}")
        
        if result['status'] == 'PASS':
            passed += 1
        else:
            failed += 1
            
        if result['status'] == 'FAIL':
            print(f"   Reason: {result.get('reason', result.get('error', 'Unknown'))}")
        
        # Print key metrics if available
        if 'metrics' in result and isinstance(result['metrics'], dict):
            metrics = result['metrics']
            print(f"   Key Metrics:")
            if 'total_return_pct' in metrics:
                print(f"     • Total Return: {metrics['total_return_pct']:.2f}%")
            if 'sharpe_ratio' in metrics:
                print(f"     • Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
            if 'max_drawdown_pct' in metrics:
                print(f"     • Max Drawdown: {metrics['max_drawdown_pct']:.2f}%")
            if 'win_rate' in metrics:
                print(f"     • Win Rate: {metrics['win_rate']:.2f}%")
            if 'profit_factor' in metrics:
                print(f"     • Profit Factor: {metrics['profit_factor']:.2f}")
    
    # Overall summary
    print("\n" + "=" * 70)
    print(f"🎯 Overall Results: {passed}/{len(test_results)} tests passed ({passed/len(test_results)*100:.1f}%)")
    print("=" * 70)
    
    # Save results
    reports_dir = Path("benchmarks/reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = reports_dir / f"trading_bot_results_{timestamp}.json"
    latest_file = reports_dir / "trading_bot_results_latest.json"
    
    # Save with timestamp
    with open(results_file, 'w') as f:
        json.dump(test_results, f, indent=2, default=str)
    
    # Save latest
    with open(latest_file, 'w') as f:
        json.dump(test_results, f, indent=2, default=str)
    
    print(f"\n📁 Results saved to:")
    print(f"   • {results_file}")
    print(f"   • {latest_file}")
    
    # Exit code
    exit_code = 0 if passed == len(test_results) else 1
    print(f"\nExit code: {exit_code}")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
