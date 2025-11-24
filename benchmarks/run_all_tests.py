#!/usr/bin/env python3
"""
Master Benchmark Runner - Execute All 30 Enterprise Tests
Strategickhaos DAO LLC - Cyber + LLM Stack Validation
"""

import argparse
import json
import time
import sys
from pathlib import Path
from datetime import datetime
import subprocess

# Import test modules
sys.path.append('benchmarks')
from test_data_ingestion import DataIngestionBenchmarks
from test_llm_safety import LLMSafetyBenchmarks  
from test_security_analytics import SecurityAnalyticsBenchmarks
from test_comprehensive import ComprehensiveBenchmarks
from test_trading_bot import TradingBotBenchmarks

class MasterBenchmarkRunner:
    def __init__(self, config_path: str = "benchmarks/benchmark_config.yaml"):
        self.config_path = config_path
        self.results = []
        self.start_time = None
        self.end_time = None
        
    def run_smoke_tests(self):
        """Run essential smoke tests (Tests 1, 3, 5, 11, 13, 19, 23, 26, 29, 31)"""
        print("🔥 Running Smoke Test Suite (10 critical tests)")
        
        # Data Ingestion
        data_benchmarks = DataIngestionBenchmarks(self.config_path)
        self.results.extend([
            data_benchmarks.test_01_ingestion_integrity(),
            data_benchmarks.test_03_embedding_quality_recall(),
            data_benchmarks.test_05_query_latency_slo()
        ])
        
        # LLM Safety  
        safety_benchmarks = LLMSafetyBenchmarks(self.config_path)
        self.results.extend([
            safety_benchmarks.test_11_factual_accuracy_rag_vs_norag(),
            safety_benchmarks.test_13_safety_redteaming()
        ])
        
        # Security Analytics
        security_benchmarks = SecurityAnalyticsBenchmarks(self.config_path)
        self.results.append(security_benchmarks.test_19_attack_detection_coverage())
        
        # Comprehensive Tests
        comprehensive_benchmarks = ComprehensiveBenchmarks(self.config_path)
        self.results.extend([
            comprehensive_benchmarks.test_23_kev_nvd_sync_fidelity(),
            comprehensive_benchmarks.test_26_benchmarks_conformance(),
            comprehensive_benchmarks.test_29_chaos_and_failover()
        ])
        
        # Trading Bot Tests
        trading_benchmarks = TradingBotBenchmarks(self.config_path)
        self.results.append(trading_benchmarks.test_31_simple_backtest_validation())
        
    def run_full_regression(self):
        """Run all 30 enterprise benchmark tests"""
        print("🎯 Running Full Regression Suite (30 tests)")
        
        self.start_time = datetime.now()
        
        # Tests 1-10: Data Ingestion & RAG
        print("\n📊 Data Ingestion & RAG Tests (1-10)")
        data_benchmarks = DataIngestionBenchmarks(self.config_path)
        self.results.extend([
            data_benchmarks.test_01_ingestion_integrity(),
            data_benchmarks.test_02_chunking_correctness(),
            data_benchmarks.test_03_embedding_quality_recall(),
            data_benchmarks.test_04_cross_encoder_rerank(),
            data_benchmarks.test_05_query_latency_slo()
        ])
        # Tests 6-10 would be added here (throughput, freshness, deduplication, etc.)
        
        # Tests 11-18: LLM Safety & Alignment  
        print("\n🛡️ LLM Safety & Alignment Tests (11-18)")
        safety_benchmarks = LLMSafetyBenchmarks(self.config_path)
        self.results.extend([
            safety_benchmarks.test_11_factual_accuracy_rag_vs_norag(),
            safety_benchmarks.test_12_hallucination_rate(),
            safety_benchmarks.test_13_safety_redteaming(),
            safety_benchmarks.test_14_toxicity_pii_filters(),
            safety_benchmarks.test_15_citation_faithfulness()
        ])
        # Tests 16-18 would be added here (CoT control, multi-hop reasoning, determinism)
        
        # Tests 19-22: Security Analytics
        print("\n🔒 Security Analytics & Detection Tests (19-22)")
        security_benchmarks = SecurityAnalyticsBenchmarks(self.config_path)
        self.results.extend([
            security_benchmarks.test_19_attack_detection_coverage(),
            security_benchmarks.test_20_atomic_red_team_validation(),
            security_benchmarks.test_21_elastalert_edr_latency(),
            security_benchmarks.test_22_log_pipeline_integrity()
        ])
        
        # Tests 23-30: Threat Intel, Cloud Posture, Reliability
        print("\n🌐 Comprehensive Infrastructure Tests (23-30)")
        comprehensive_benchmarks = ComprehensiveBenchmarks(self.config_path)
        self.results.extend([
            comprehensive_benchmarks.test_23_kev_nvd_sync_fidelity(),
            comprehensive_benchmarks.test_24_cvss_scoring_consistency(),
            comprehensive_benchmarks.test_25_patch_intelligence_timeliness(),
            comprehensive_benchmarks.test_26_benchmarks_conformance(),
            comprehensive_benchmarks.test_27_policy_as_code_gates(),
            comprehensive_benchmarks.test_28_runtime_hardening_tests(),
            comprehensive_benchmarks.test_29_chaos_and_failover(),
            comprehensive_benchmarks.test_30_cost_performance_curve()
        ])
        
        # Tests 31-35: Trading Bot Backtesting
        print("\n🤖 Trading Bot Benchmark Tests (31-35)")
        trading_benchmarks = TradingBotBenchmarks(self.config_path)
        self.results.extend([
            trading_benchmarks.test_31_simple_backtest_validation(),
            trading_benchmarks.test_32_advanced_strategy_performance(),
            trading_benchmarks.test_33_stress_test_market_conditions(),
            trading_benchmarks.test_34_benchmark_comparison(),
            trading_benchmarks.test_35_transaction_cost_impact()
        ])
        
        self.end_time = datetime.now()
        
    def generate_executive_summary(self):
        """Generate executive summary of test results"""
        if not self.results:
            return {"error": "No test results available"}
            
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.get('status') == 'PASS')
        failed_tests = total_tests - passed_tests
        
        # Category breakdown
        categories = {
            "data_ingestion": [r for r in self.results if 1 <= r.get('test_id', 0) <= 10],
            "llm_safety": [r for r in self.results if 11 <= r.get('test_id', 0) <= 18],
            "security_analytics": [r for r in self.results if 19 <= r.get('test_id', 0) <= 22], 
            "threat_intel": [r for r in self.results if 23 <= r.get('test_id', 0) <= 25],
            "cloud_posture": [r for r in self.results if 26 <= r.get('test_id', 0) <= 28],
            "reliability": [r for r in self.results if 29 <= r.get('test_id', 0) <= 30],
            "trading_bot": [r for r in self.results if 31 <= r.get('test_id', 0) <= 35]
        }
        
        category_summary = {}
        for category, tests in categories.items():
            if tests:
                category_passed = sum(1 for t in tests if t.get('status') == 'PASS')
                category_summary[category] = {
                    "total": len(tests),
                    "passed": category_passed,
                    "pass_rate": category_passed / len(tests)
                }
        
        # Performance metrics extraction
        key_metrics = {}
        for result in self.results:
            if result.get('test_id') == 3:  # Embedding quality
                key_metrics['recall_at_5'] = result.get('recall_at_5', 0)
            elif result.get('test_id') == 5:  # Query latency
                key_metrics['latency_p90'] = result.get('k5_p90', 0)
            elif result.get('test_id') == 12:  # Hallucination rate
                key_metrics['hallucination_rate'] = result.get('hallucination_rate', 0)
            elif result.get('test_id') == 13:  # Safety
                key_metrics['safety_pass_rate'] = result.get('safety_pass_rate', 0)
        
        summary = {
            "execution_time": str(self.end_time - self.start_time) if self.end_time and self.start_time else "N/A",
            "overall": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "pass_rate": passed_tests / total_tests if total_tests > 0 else 0
            },
            "category_breakdown": category_summary,
            "key_metrics": key_metrics,
            "failed_tests": [
                {"id": r.get('test_id'), "name": r.get('name'), "reason": r.get('reason')} 
                for r in self.results if r.get('status') == 'FAIL'
            ],
            "timestamp": datetime.now().isoformat(),
            "enterprise_ready": failed_tests == 0 and passed_tests >= 20
        }
        
        return summary
    
    def save_results(self, output_dir: str = "benchmarks/reports"):
        """Save detailed results and summary"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results
        detailed_file = f"{output_dir}/detailed_results_{timestamp}.json"
        with open(detailed_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Save executive summary
        summary = self.generate_executive_summary()
        summary_file = f"{output_dir}/executive_summary_{timestamp}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Save latest results (for dashboards)
        with open(f"{output_dir}/latest_results.json", 'w') as f:
            json.dump(self.results, f, indent=2)
        with open(f"{output_dir}/latest_summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📁 Results saved:")
        print(f"   Detailed: {detailed_file}")
        print(f"   Summary: {summary_file}")
        
        return summary
    
    def print_summary(self):
        """Print executive summary to console"""
        summary = self.generate_executive_summary()
        
        print("\n" + "="*60)
        print("🎯 ENTERPRISE BENCHMARK RESULTS SUMMARY")
        print("="*60)
        
        print(f"\n📊 Overall Performance:")
        print(f"   Total Tests: {summary['overall']['total_tests']}")
        print(f"   Passed: {summary['overall']['passed']}")
        print(f"   Failed: {summary['overall']['failed']}")
        print(f"   Pass Rate: {summary['overall']['pass_rate']:.1%}")
        
        if summary.get('execution_time'):
            print(f"   Execution Time: {summary['execution_time']}")
        
        print(f"\n🏆 Category Breakdown:")
        for category, stats in summary['category_breakdown'].items():
            status_icon = "✅" if stats['pass_rate'] == 1.0 else "⚠️" if stats['pass_rate'] > 0.8 else "❌"
            print(f"   {status_icon} {category}: {stats['passed']}/{stats['total']} ({stats['pass_rate']:.1%})")
        
        if summary['key_metrics']:
            print(f"\n📈 Key Metrics:")
            for metric, value in summary['key_metrics'].items():
                print(f"   {metric}: {value}")
        
        if summary['failed_tests']:
            print(f"\n❌ Failed Tests:")
            for test in summary['failed_tests']:
                print(f"   Test {test['id']}: {test['name']} - {test['reason']}")
        
        enterprise_status = "🏆 ENTERPRISE READY" if summary['enterprise_ready'] else "⚠️ NEEDS ATTENTION"
        print(f"\n{enterprise_status}")
        print("="*60)

def main():
    parser = argparse.ArgumentParser(description="Enterprise Benchmark Runner")
    parser.add_argument("--mode", choices=['smoke', 'full', 'security', 'performance'], 
                       default='smoke', help="Test execution mode")
    parser.add_argument("--config", default="benchmarks/benchmark_config.yaml",
                       help="Configuration file path")
    parser.add_argument("--output", default="benchmarks/reports",
                       help="Output directory for results")
    
    args = parser.parse_args()
    
    runner = MasterBenchmarkRunner(args.config)
    
    print(f"🚀 Starting {args.mode} benchmark execution...")
    
    if args.mode == 'smoke':
        runner.run_smoke_tests()
    elif args.mode == 'full':
        runner.run_full_regression()
    else:
        print(f"Mode '{args.mode}' not fully implemented yet. Running smoke tests.")
        runner.run_smoke_tests()
    
    # Generate and display results
    summary = runner.save_results(args.output)
    runner.print_summary()
    
    # Exit code based on results
    exit_code = 0 if summary['enterprise_ready'] else 1
    sys.exit(exit_code)

if __name__ == "__main__":
    main()