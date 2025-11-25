# Evaluation Metrics Framework

## Overview

This document defines the quantitative metrics required to validate the Git-native multi-agent consensus protocol for academic publication. All metrics should be collected using the benchmark scripts in `benchmarks/`.

---

## 1. Consensus Performance Metrics

### 1.1 Voting Time

**Definition**: Time from proposal creation to consensus decision.

| Metric | Description | Target | Measurement Method |
|--------|-------------|--------|-------------------|
| `voting_time_10` | Consensus time with 10 agents | < 30s | `dao_consensus_benchmark.py --agents 10` |
| `voting_time_50` | Consensus time with 50 agents | < 120s | `dao_consensus_benchmark.py --agents 50` |
| `voting_time_105` | Consensus time with 105 agents | < 300s | `dao_consensus_benchmark.py --agents 105` |
| `voting_time_p50` | Median voting time | Report | Percentile analysis |
| `voting_time_p90` | 90th percentile voting time | Report | Percentile analysis |
| `voting_time_p99` | 99th percentile voting time | Report | Percentile analysis |

### 1.2 Throughput

**Definition**: Number of proposals processed per unit time.

| Metric | Description | Target | Measurement Method |
|--------|-------------|--------|-------------------|
| `proposals_per_hour` | Sustained throughput | > 10 | Load test |
| `peak_throughput` | Maximum burst capacity | Report | Stress test |
| `concurrent_proposals` | Parallel processing | > 5 | Concurrent test |

### 1.3 Git Operations

**Definition**: Latency of underlying Git operations.

| Metric | Description | Target | Measurement Method |
|--------|-------------|--------|-------------------|
| `commit_latency` | Time to create commit | < 1s | Instrumentation |
| `push_latency` | Time to push to remote | < 5s | Network test |
| `branch_create_latency` | Time to create branch | < 1s | Instrumentation |
| `merge_latency` | Time to merge PR | < 2s | Instrumentation |

---

## 2. Decision Quality Metrics

### 2.1 Accuracy

**Definition**: Alignment of AI decisions with ground truth.

| Metric | Description | Target | Measurement Method |
|--------|-------------|--------|-------------------|
| `human_agreement` | Agreement with human experts | > 85% | Expert panel review |
| `consensus_accuracy` | Correct consensus decisions | > 90% | Ground truth comparison |
| `inter_agent_agreement` | Agreement among agents | Report | Cohen's Kappa |

### 2.2 Error Rates

**Definition**: Types of incorrect decisions.

| Metric | Description | Target | Measurement Method |
|--------|-------------|--------|-------------------|
| `false_positive_rate` | Incorrectly approved proposals | < 10% | Historical analysis |
| `false_negative_rate` | Incorrectly rejected proposals | < 10% | Historical analysis |
| `abstention_rate` | Agents that did not vote | < 5% | Vote records |

### 2.3 Confidence Metrics

**Definition**: Self-reported confidence of agent decisions.

| Metric | Description | Target | Measurement Method |
|--------|-------------|--------|-------------------|
| `avg_confidence` | Average agent confidence score | > 0.8 | Vote metadata |
| `confidence_calibration` | Confidence vs. actual accuracy | Report | Calibration curve |
| `low_confidence_rate` | Votes with confidence < 0.5 | < 10% | Vote metadata |

---

## 3. Scalability Metrics

### 3.1 Agent Scaling

**Definition**: Performance as agent count increases.

| Metric | Description | Target | Measurement Method |
|--------|-------------|--------|-------------------|
| `scaling_factor` | Time increase per agent | Sublinear | Regression analysis |
| `max_agents` | Maximum supported agents | > 100 | Stress test |
| `agent_overhead` | Resource per agent | Report | Resource monitoring |

### 3.2 Resource Utilization

**Definition**: Infrastructure resource consumption.

| Metric | Description | Target | Measurement Method |
|--------|-------------|--------|-------------------|
| `cpu_utilization` | CPU usage during consensus | < 80% | K8s metrics |
| `memory_utilization` | Memory usage during consensus | < 80% | K8s metrics |
| `network_bandwidth` | Network usage | Report | K8s metrics |
| `git_storage` | Repository size growth | Report | Git stats |

### 3.3 Cost Metrics

**Definition**: Operational costs compared to alternatives.

| Metric | Description | Target | Measurement Method |
|--------|-------------|--------|-------------------|
| `cost_per_proposal` | Infrastructure cost per decision | < $0.10 | Cloud billing |
| `cost_vs_blockchain` | Comparison to Ethereum gas | > 90% savings | Published data |
| `agent_api_cost` | LLM API costs per vote | Report | API billing |

---

## 4. Reliability Metrics

### 4.1 Fault Tolerance

**Definition**: System behavior under failure conditions.

| Metric | Description | Target | Measurement Method |
|--------|-------------|--------|-------------------|
| `agent_failure_recovery` | Recovery from agent crash | < 10s | Chaos test |
| `network_partition_handling` | Behavior during partition | Correct | Network test |
| `consensus_with_failures` | Consensus with 20% agent loss | Success | Fault injection |

### 4.2 Availability

**Definition**: System uptime and reliability.

| Metric | Description | Target | Measurement Method |
|--------|-------------|--------|-------------------|
| `uptime` | System availability | > 99.9% | Monitoring |
| `mttr` | Mean time to recovery | < 5 min | Incident logs |
| `mtbf` | Mean time between failures | > 7 days | Incident logs |

### 4.3 Consistency

**Definition**: Data consistency guarantees.

| Metric | Description | Target | Measurement Method |
|--------|-------------|--------|-------------------|
| `consensus_consistency` | Same result on replay | 100% | Determinism test |
| `state_divergence` | Branch divergence rate | 0% | Git analysis |
| `vote_integrity` | Votes match recorded | 100% | Audit |

---

## 5. Comparison Baselines

### 5.1 Traditional PR Flow (GitHub)

| Metric | Our System | GitHub PRs |
|--------|------------|------------|
| Review Time | X min | 24-48 hours |
| Reviewers | 105 agents | 2-3 humans |
| Cost | $Y | $0 (human time) |
| Automation | 100% | Manual |

### 5.2 Blockchain DAOs (Aragon)

| Metric | Our System | Aragon |
|--------|------------|--------|
| Voting Time | X min | 3-7 days |
| Cost per Vote | $Y | $5-50 gas |
| Throughput | Z/hour | Limited |
| Legal Integration | Wyoming DAO | Smart contract |

### 5.3 Multi-Agent Systems (AutoGPT)

| Metric | Our System | AutoGPT |
|--------|------------|---------|
| Consensus Mechanism | Git-native | None |
| Agent Count | 105 | 1 |
| State Persistence | Git history | Session |
| Reproducibility | Commits | Logs |

---

## 6. Data Collection Protocol

### 6.1 Benchmark Execution

```bash
# Run full benchmark suite
python benchmarks/dao_consensus_benchmark.py --mode full

# Run specific metric categories
python benchmarks/dao_consensus_benchmark.py --mode consensus
python benchmarks/dao_consensus_benchmark.py --mode scalability
python benchmarks/dao_consensus_benchmark.py --mode reliability
```

### 6.2 Data Storage

All metrics should be stored in:
- `benchmarks/reports/` - JSON results files
- `benchmarks/data/` - Raw measurement data
- Git history - Version controlled metrics

### 6.3 Reproducibility Requirements

For each metric:
1. **Timestamp**: When measurement was taken
2. **Environment**: K8s cluster, agent versions
3. **Methodology**: Exact steps to reproduce
4. **Raw Data**: Underlying measurements
5. **Statistical Analysis**: Mean, std, percentiles

---

## 7. Visualization Templates

### 7.1 Performance Charts

```python
# Example: Voting time vs. agent count
import matplotlib.pyplot as plt

agents = [10, 25, 50, 75, 105]
times = [28, 45, 89, 156, 267]  # seconds

plt.figure(figsize=(10, 6))
plt.plot(agents, times, 'b-o', linewidth=2)
plt.xlabel('Number of Agents')
plt.ylabel('Consensus Time (seconds)')
plt.title('Scalability: Voting Time vs. Agent Count')
plt.grid(True)
plt.savefig('figures/scalability.png', dpi=300)
```

### 7.2 Comparison Tables

| System | Voting Time | Cost/Vote | Throughput | Legal |
|--------|-------------|-----------|------------|-------|
| **Ours** | 5 min | $0.05 | 12/hr | ✓ |
| Aragon | 3 days | $25 | 1/day | ✗ |
| GitHub | 24 hrs | $0 | 10/day | ✗ |

---

## 8. Statistical Requirements

### 8.1 Sample Sizes
- Minimum 30 runs per configuration
- Report mean, standard deviation, confidence intervals
- Use appropriate statistical tests (t-test, ANOVA)

### 8.2 Significance Levels
- α = 0.05 for statistical comparisons
- Report p-values for all claims
- Use Bonferroni correction for multiple comparisons

### 8.3 Effect Sizes
- Report Cohen's d for comparisons
- Use practical significance thresholds
- Contextualize improvements

---

## References

- [PAPER_STRUCTURE.md](./PAPER_STRUCTURE.md) - Where metrics appear in paper
- [PUBLICATION_TIMELINE.md](./PUBLICATION_TIMELINE.md) - When to collect metrics
- `benchmarks/dao_consensus_benchmark.py` - Benchmark implementation
- `src/dao/kernel.py` - System under test

---

*"Reviewers want quantifiable metrics that make your claims defensible academically."*
