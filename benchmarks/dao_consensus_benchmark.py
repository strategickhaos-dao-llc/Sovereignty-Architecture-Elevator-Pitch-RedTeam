#!/usr/bin/env python3
"""
DAO Consensus Benchmark Suite
Strategickhaos DAO LLC - Performance Evaluation Framework

This script measures key performance metrics for the Git-native
multi-agent consensus protocol as defined in EVALUATION_METRICS.md.
"""

import argparse
import json
import random
import statistics
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.dao.kernel import DAOKernel, VoteDecision, ProposalStatus


@dataclass
class BenchmarkResult:
    """Result of a single benchmark run"""
    metric_name: str
    value: float
    unit: str
    timestamp: str
    metadata: dict


@dataclass
class BenchmarkSuite:
    """Complete benchmark suite results"""
    suite_name: str
    run_id: str
    timestamp: str
    duration_seconds: float
    results: list
    summary: dict
    environment: dict


class DAOConsensusBenchmark:
    """
    Benchmark suite for DAO consensus performance evaluation.
    
    Metrics measured:
    - Consensus time (voting duration)
    - Throughput (proposals per hour)
    - Scalability (time vs agent count)
    - Decision quality (simulated)
    """
    
    def __init__(self, output_dir: str = "benchmarks/reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results: list[BenchmarkResult] = []
        self.start_time = None
        self.run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
    def _record_result(self, name: str, value: float, unit: str, metadata: dict = None):
        """Record a benchmark result"""
        result = BenchmarkResult(
            metric_name=name,
            value=value,
            unit=unit,
            timestamp=datetime.utcnow().isoformat() + 'Z',
            metadata=metadata or {}
        )
        self.results.append(result)
        print(f"  📊 {name}: {value:.2f} {unit}")
        
    def _simulate_agent_vote(self, kernel: DAOKernel, proposal_id: str,
                             agent_id: str, delay: float = 0.0):
        """Simulate an agent casting a vote"""
        # Simulate processing time
        if delay > 0:
            time.sleep(delay)
            
        # Random decision weighted towards approval (70%)
        rand = random.random()
        if rand < 0.70:
            decision = VoteDecision.APPROVE
        elif rand < 0.90:
            decision = VoteDecision.REJECT
        else:
            decision = VoteDecision.ABSTAIN
            
        confidence = 0.5 + random.random() * 0.5  # 0.5 to 1.0
        reasoning = f"Automated benchmark vote from {agent_id}"
        
        kernel.submit_vote(proposal_id, agent_id, decision, confidence, reasoning)
        
    def benchmark_consensus_time(self, agent_counts: list[int] = None,
                                  iterations: int = 5) -> dict:
        """
        Benchmark: Measure consensus time for different agent counts.
        
        This measures how long it takes to reach consensus with varying
        numbers of voting agents.
        """
        print("\n⏱️  Benchmark: Consensus Time")
        print("=" * 50)
        
        if agent_counts is None:
            agent_counts = [3, 5, 10, 25]  # Smaller counts for benchmark
            
        results_by_count = {}
        
        for num_agents in agent_counts:
            print(f"\n  Testing with {num_agents} agents...")
            times = []
            
            for i in range(iterations):
                # Create fresh kernel for each test (using temp dir)
                import tempfile
                with tempfile.TemporaryDirectory() as tmpdir:
                    kernel = DAOKernel(repo_path=tmpdir, data_dir="proposals")
                    
                    # Create proposal
                    proposal = kernel.create_proposal(
                        title=f"Benchmark Proposal {i+1}",
                        description="Performance benchmark test proposal",
                        author="benchmark-runner",
                        quorum_threshold=0.66
                    )
                    
                    # Time the voting process
                    start = time.perf_counter()
                    
                    for j in range(num_agents):
                        agent_id = f"agent-{j:03d}"
                        self._simulate_agent_vote(kernel, proposal.proposal_id, agent_id)
                        
                    # Finalize and record consensus
                    kernel.finalize_proposal(proposal.proposal_id)
                    
                    end = time.perf_counter()
                    elapsed = end - start
                    times.append(elapsed)
                    
            # Calculate statistics
            avg_time = statistics.mean(times)
            std_time = statistics.stdev(times) if len(times) > 1 else 0
            p90_time = sorted(times)[int(len(times) * 0.9)] if len(times) >= 10 else max(times)
            
            results_by_count[num_agents] = {
                'mean': avg_time,
                'std': std_time,
                'p90': p90_time,
                'min': min(times),
                'max': max(times),
                'samples': len(times)
            }
            
            self._record_result(
                f"voting_time_{num_agents}_agents",
                avg_time,
                "seconds",
                {'agent_count': num_agents, 'iterations': iterations}
            )
            
        return results_by_count
        
    def benchmark_throughput(self, duration_seconds: int = 30,
                             num_agents: int = 5) -> dict:
        """
        Benchmark: Measure proposal throughput.
        
        This measures how many proposals can be processed per hour.
        """
        print("\n📈 Benchmark: Throughput")
        print("=" * 50)
        
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            kernel = DAOKernel(repo_path=tmpdir, data_dir="proposals")
            
            proposals_completed = 0
            start = time.perf_counter()
            
            while time.perf_counter() - start < duration_seconds:
                # Create and complete a proposal
                proposal = kernel.create_proposal(
                    title=f"Throughput Test {proposals_completed + 1}",
                    description="Throughput benchmark proposal",
                    author="benchmark-runner"
                )
                
                for i in range(num_agents):
                    agent_id = f"agent-{i:03d}"
                    self._simulate_agent_vote(kernel, proposal.proposal_id, agent_id)
                    
                kernel.finalize_proposal(proposal.proposal_id)
                proposals_completed += 1
                
            elapsed = time.perf_counter() - start
            
        # Calculate throughput
        throughput_per_second = proposals_completed / elapsed
        throughput_per_hour = throughput_per_second * 3600
        
        result = {
            'proposals_completed': proposals_completed,
            'duration_seconds': elapsed,
            'throughput_per_second': throughput_per_second,
            'throughput_per_hour': throughput_per_hour
        }
        
        self._record_result(
            "throughput_proposals_per_hour",
            throughput_per_hour,
            "proposals/hour",
            {'duration_seconds': duration_seconds, 'agents': num_agents}
        )
        
        return result
        
    def benchmark_scalability(self, max_agents: int = 50,
                               step: int = 10) -> dict:
        """
        Benchmark: Measure scalability with increasing agent counts.
        
        This measures how voting time scales with agent count.
        """
        print("\n📐 Benchmark: Scalability")
        print("=" * 50)
        
        agent_counts = list(range(step, max_agents + 1, step))
        if 3 not in agent_counts:
            agent_counts = [3] + agent_counts
            
        scaling_data = []
        
        for num_agents in agent_counts:
            print(f"\n  Testing scalability with {num_agents} agents...")
            
            import tempfile
            with tempfile.TemporaryDirectory() as tmpdir:
                kernel = DAOKernel(repo_path=tmpdir, data_dir="proposals")
                
                # Create proposal
                proposal = kernel.create_proposal(
                    title=f"Scalability Test",
                    description="Scalability benchmark proposal",
                    author="benchmark-runner"
                )
                
                # Time voting with this agent count
                start = time.perf_counter()
                
                for i in range(num_agents):
                    agent_id = f"agent-{i:03d}"
                    self._simulate_agent_vote(kernel, proposal.proposal_id, agent_id)
                    
                kernel.finalize_proposal(proposal.proposal_id)
                
                elapsed = time.perf_counter() - start
                
                scaling_data.append({
                    'agents': num_agents,
                    'time': elapsed,
                    'time_per_agent': elapsed / num_agents
                })
                
        # Analyze scaling behavior
        times = [d['time'] for d in scaling_data]
        agents = [d['agents'] for d in scaling_data]
        
        # Simple linear regression for scaling factor
        if len(agents) > 1:
            n = len(agents)
            sum_x = sum(agents)
            sum_y = sum(times)
            sum_xy = sum(a * t for a, t in zip(agents, times))
            sum_xx = sum(a * a for a in agents)
            
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x)
            scaling_factor = slope
        else:
            scaling_factor = 0
            
        result = {
            'scaling_data': scaling_data,
            'scaling_factor': scaling_factor,
            'max_agents_tested': max_agents
        }
        
        self._record_result(
            "scaling_factor",
            scaling_factor,
            "seconds/agent",
            {'max_agents': max_agents}
        )
        
        return result
        
    def benchmark_decision_quality(self, num_proposals: int = 20) -> dict:
        """
        Benchmark: Simulate decision quality metrics.
        
        In production, this would compare against human expert decisions.
        For benchmarking, we simulate agreement rates.
        """
        print("\n🎯 Benchmark: Decision Quality")
        print("=" * 50)
        
        import tempfile
        
        agreements = 0
        false_positives = 0
        false_negatives = 0
        confidences = []
        
        with tempfile.TemporaryDirectory() as tmpdir:
            kernel = DAOKernel(repo_path=tmpdir, data_dir="proposals")
            
            for i in range(num_proposals):
                # Create proposal with known "ground truth"
                should_approve = random.random() < 0.7  # 70% should be approved
                
                proposal = kernel.create_proposal(
                    title=f"Quality Test {i+1}",
                    description="Decision quality benchmark",
                    author="benchmark-runner"
                )
                
                # Have agents vote
                num_agents = random.randint(5, 10)
                for j in range(num_agents):
                    agent_id = f"agent-{j:03d}"
                    self._simulate_agent_vote(kernel, proposal.proposal_id, agent_id)
                    
                # Get result
                result = kernel.finalize_proposal(proposal.proposal_id)
                
                # Compare to "ground truth"
                if result.approved == should_approve:
                    agreements += 1
                elif result.approved and not should_approve:
                    false_positives += 1
                else:
                    false_negatives += 1
                    
                # Track confidences
                proposal = kernel.get_proposal(proposal.proposal_id)
                for vote in proposal.votes:
                    confidences.append(vote.confidence)
                    
        # Calculate metrics
        agreement_rate = agreements / num_proposals
        fp_rate = false_positives / num_proposals
        fn_rate = false_negatives / num_proposals
        avg_confidence = statistics.mean(confidences) if confidences else 0
        
        result = {
            'agreement_rate': agreement_rate,
            'false_positive_rate': fp_rate,
            'false_negative_rate': fn_rate,
            'average_confidence': avg_confidence,
            'proposals_tested': num_proposals
        }
        
        self._record_result(
            "human_agreement_simulated",
            agreement_rate * 100,
            "percent",
            {'proposals': num_proposals}
        )
        
        self._record_result(
            "false_positive_rate",
            fp_rate * 100,
            "percent",
            {}
        )
        
        self._record_result(
            "average_confidence",
            avg_confidence * 100,
            "percent",
            {}
        )
        
        return result
        
    def run_full_benchmark(self) -> BenchmarkSuite:
        """Run all benchmarks and generate comprehensive report"""
        print("\n" + "=" * 60)
        print("🚀 DAO CONSENSUS BENCHMARK SUITE")
        print("   Strategickhaos DAO LLC - Performance Evaluation")
        print("=" * 60)
        
        self.start_time = time.perf_counter()
        
        # Run all benchmarks
        consensus_results = self.benchmark_consensus_time()
        throughput_results = self.benchmark_throughput()
        scalability_results = self.benchmark_scalability()
        quality_results = self.benchmark_decision_quality()
        
        duration = time.perf_counter() - self.start_time
        
        # Generate summary
        summary = {
            'consensus_time_3_agents': consensus_results.get(3, {}).get('mean', 0),
            'consensus_time_10_agents': consensus_results.get(10, {}).get('mean', 0),
            'throughput_per_hour': throughput_results['throughput_per_hour'],
            'scaling_factor': scalability_results['scaling_factor'],
            'simulated_agreement': quality_results['agreement_rate']
        }
        
        # Environment info
        import platform
        environment = {
            'python_version': platform.python_version(),
            'platform': platform.platform(),
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        suite = BenchmarkSuite(
            suite_name="DAO Consensus Benchmark",
            run_id=self.run_id,
            timestamp=datetime.utcnow().isoformat() + 'Z',
            duration_seconds=duration,
            results=[asdict(r) for r in self.results],
            summary=summary,
            environment=environment
        )
        
        # Save results
        self._save_results(suite)
        
        # Print summary
        self._print_summary(suite)
        
        return suite
        
    def _save_results(self, suite: BenchmarkSuite):
        """Save benchmark results to JSON"""
        results_file = self.output_dir / f"dao_benchmark_{self.run_id}.json"
        with open(results_file, 'w') as f:
            json.dump(asdict(suite), f, indent=2)
            
        # Also save latest
        latest_file = self.output_dir / "dao_benchmark_latest.json"
        with open(latest_file, 'w') as f:
            json.dump(asdict(suite), f, indent=2)
            
        print(f"\n📁 Results saved to: {results_file}")
        
    def _print_summary(self, suite: BenchmarkSuite):
        """Print benchmark summary"""
        print("\n" + "=" * 60)
        print("📊 BENCHMARK SUMMARY")
        print("=" * 60)
        
        print(f"\n  Run ID: {suite.run_id}")
        print(f"  Duration: {suite.duration_seconds:.1f} seconds")
        print(f"  Metrics collected: {len(suite.results)}")
        
        print("\n  Key Metrics:")
        for key, value in suite.summary.items():
            if isinstance(value, float):
                print(f"    • {key}: {value:.4f}")
            else:
                print(f"    • {key}: {value}")
                
        print("\n" + "=" * 60)
        

def main():
    parser = argparse.ArgumentParser(
        description="DAO Consensus Benchmark Suite"
    )
    parser.add_argument(
        '--mode',
        choices=['full', 'consensus', 'throughput', 'scalability', 'quality'],
        default='full',
        help='Benchmark mode to run'
    )
    parser.add_argument(
        '--output',
        default='benchmarks/reports',
        help='Output directory for results'
    )
    parser.add_argument(
        '--agents',
        type=int,
        default=25,
        help='Maximum number of agents to test'
    )
    
    args = parser.parse_args()
    
    benchmark = DAOConsensusBenchmark(output_dir=args.output)
    
    if args.mode == 'full':
        benchmark.run_full_benchmark()
    elif args.mode == 'consensus':
        benchmark.benchmark_consensus_time()
    elif args.mode == 'throughput':
        benchmark.benchmark_throughput()
    elif args.mode == 'scalability':
        benchmark.benchmark_scalability(max_agents=args.agents)
    elif args.mode == 'quality':
        benchmark.benchmark_decision_quality()
        
    print("\n✅ Benchmark complete!")
    

if __name__ == '__main__':
    main()
