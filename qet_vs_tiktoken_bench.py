#!/usr/bin/env python3
"""
QET vs Tiktoken Bake-Off: Sovereign Tokenizer Wind Tunnel
Strategickhaos DAO LLC - Cyber + LLM Stack

Benchmark script comparing QuantumEvoTokenizer against tiktoken baseline.
Outputs JSON for Obsidian import + DAO log notarization.

Usage:
    python qet_vs_tiktoken_bench.py [--corpora-dir DIR] [--generations N] [--output FILE]
    
Example:
    python qet_vs_tiktoken_bench.py --corpora-dir ./data --generations 100
    
Output:
    - JSON benchmark results file
    - Console summary with compression delta
    - DAO-ready hash for notarization
"""

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


def utc_now() -> datetime:
    """Get current UTC time."""
    return datetime.now(timezone.utc)


def utc_now_iso() -> str:
    """Get current UTC time in ISO format."""
    return utc_now().strftime("%Y-%m-%dT%H:%M:%SZ")

# Check tiktoken availability
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False
    print("[WARN] tiktoken not installed. Install with: pip install tiktoken")

# Import our tokenizer
from quantum_evo_tokenizer_v3 import QuantumEvoTokenizer, QETConfig


def load_corpora(corpora_paths: List[str]) -> List[str]:
    """Load corpus files from provided paths."""
    corpora = []
    
    for path_str in corpora_paths:
        path = Path(path_str)
        
        if path.exists():
            try:
                content = path.read_text(encoding='utf-8', errors='replace')
                if content.strip():
                    corpora.append(content)
                    print(f"  ✓ Loaded: {path.name} ({len(content):,} chars)")
            except Exception as e:
                print(f"  ✗ Failed to load {path}: {e}")
        else:
            print(f"  ✗ File not found: {path}")
    
    return corpora


def get_sample_corpora() -> List[str]:
    """Generate sample corpora for testing when no files provided."""
    return [
        # YAML-heavy content (typical for DAO configs)
        """
version: "3.8"
services:
  refinory:
    image: strategickhaos/refinory:latest
    environment:
      - POSTGRES_HOST=db
      - REDIS_URL=redis://cache:6379
      - LLM_ENDPOINT=http://llm:8080
    volumes:
      - ./data:/app/data
    networks:
      - sovereign_net
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: sovereignty
      POSTGRES_USER: dao_admin
""",
        # Cyber/security content
        """
# MITRE ATT&CK Technique Analysis
T1059.001 - PowerShell Command Execution
Detection: Monitor for unusual PowerShell activity
Mitigation: Enable PowerShell logging, restrict execution policy

CVE-2024-1234: Remote Code Execution in Parsing Module
CVSS: 9.8 (Critical)
Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
Affected: versions < 2.0.1

Incident Response Playbook:
1. Containment: Isolate affected systems
2. Eradication: Remove malicious artifacts
3. Recovery: Restore from known-good backups
4. Lessons Learned: Document timeline and IOCs
""",
        # Technical documentation
        """
# QuantumEvoTokenizer Architecture

The tokenizer uses evolutionary algorithms with quantum-inspired fitness
evaluation to optimize vocabulary for specific corpora.

## Key Components

1. **TokenGenome**: Represents a vocabulary as a genome
2. **QuantumFitnessEvaluator**: Evaluates genome fitness
3. **Evolution Loop**: Selection, crossover, mutation

## Configuration Parameters

- `generations`: Number of evolution cycles (default: 100)
- `population_size`: Size of genome population (default: 32)
- `vocab_size`: Target vocabulary size (default: 8192)
- `backend`: "mock", "qiskit", or "none"

## Safety Features

- Entropy bounds prevent vocabulary poisoning
- Cryptographic hashing for DAO notarization
- Fork logic for yin-yang variants
""",
        # Mixed markdown/code content
        """
## API Reference

### POST /tokenize
```json
{
    "text": "Input text to tokenize",
    "model": "qet-v3",
    "return_offsets": true
}
```

### Response
```json
{
    "tokens": [1234, 5678, 9012],
    "offsets": [[0, 5], [5, 10], [10, 19]],
    "model_hash": "abc123def456"
}
```

### Error Codes
| Code | Message | Description |
|------|---------|-------------|
| 400  | Invalid input | Text is empty or too long |
| 500  | Internal error | Tokenization failed |
"""
    ]


def benchmark_tiktoken(corpora: List[str], model: str = "gpt-4") -> Dict[str, Any]:
    """Benchmark tiktoken on provided corpora."""
    if not TIKTOKEN_AVAILABLE:
        return {
            "error": "tiktoken not installed",
            "avg_tokens": 0,
            "avg_compression": 0,
            "total_vocab_used": 0
        }
    
    try:
        enc = tiktoken.encoding_for_model(model)
    except KeyError:
        try:
            enc = tiktoken.get_encoding("cl100k_base")
        except Exception as e:
            return {
                "error": f"tiktoken encoding not available: {e}",
                "avg_tokens": 0,
                "avg_compression": 0,
                "total_vocab_used": 0
            }
    except Exception as e:
        # Network error or other issue loading tiktoken
        return {
            "error": f"tiktoken unavailable (network?): {str(e)[:100]}",
            "avg_tokens": 0,
            "avg_compression": 0,
            "total_vocab_used": 0
        }
    
    results = []
    all_tokens = []
    
    for corpus in corpora:
        tokens = enc.encode(corpus)
        all_tokens.extend(tokens)
        
        results.append({
            "token_count": len(tokens),
            "chars_per_token": len(corpus) / len(tokens) if tokens else 0,
            "vocab_used": len(set(tokens))
        })
    
    return {
        "avg_tokens": sum(r["token_count"] for r in results) / len(corpora),
        "avg_compression": sum(r["chars_per_token"] for r in results) / len(corpora),
        "total_vocab_used": len(set(all_tokens)),
        "total_chars": sum(len(c) for c in corpora),
        "total_tokens": sum(r["token_count"] for r in results),
        "per_corpus": results
    }


def benchmark_qet(
    corpora: List[str], 
    config: QETConfig
) -> Dict[str, Any]:
    """Benchmark QuantumEvoTokenizer on provided corpora."""
    
    # Force mock backend for speed in benchmarking
    config.backend = "mock"
    
    # Initialize and evolve
    qet = QuantumEvoTokenizer(config, corpora)
    evo_result = qet.evolve()
    
    vocab = evo_result["vocab"]
    results = []
    all_tokens = []
    
    for corpus in corpora:
        tokens = qet._temp_encode(corpus.encode('utf-8'), vocab)
        all_tokens.extend(tokens)
        
        results.append({
            "token_count": len(tokens),
            "chars_per_token": len(corpus) / len(tokens) if tokens else 0,
            "vocab_used": len(set(tokens))
        })
    
    return {
        "avg_tokens": sum(r["token_count"] for r in results) / len(corpora),
        "avg_compression": sum(r["chars_per_token"] for r in results) / len(corpora),
        "total_vocab_used": len(set(all_tokens)),
        "total_chars": sum(len(c) for c in corpora),
        "total_tokens": sum(r["token_count"] for r in results),
        "per_corpus": results,
        "evo_metrics": evo_result["metrics"],
        "vocab_hash": evo_result["final_hash"],
        "notarization": qet.notarize()
    }


def benchmark(
    corpora: List[str], 
    config: QETConfig,
    tiktoken_model: str = "gpt-4"
) -> Dict[str, Any]:
    """
    Run full benchmark comparison between QET and tiktoken.
    
    Args:
        corpora: List of text strings to benchmark
        config: QETConfig for QET tokenizer
        tiktoken_model: Model name for tiktoken encoding
    
    Returns:
        Dict with comparison results, deltas, and DAO hash
    """
    print("\n🔬 Running Tokenizer Bake-Off...")
    print("=" * 50)
    
    # Tiktoken baseline
    print("\n📊 Benchmarking tiktoken...")
    start = time.time()
    tik_results = benchmark_tiktoken(corpora, tiktoken_model)
    tik_time = time.time() - start
    
    tiktoken_available = "error" not in tik_results
    if tiktoken_available:
        print(f"   Completed in {tik_time:.2f}s")
    else:
        print(f"   ⚠️ Unavailable: {tik_results.get('error', 'unknown error')[:80]}")
    
    # QET evolution
    print("\n🧬 Evolving QET vocabulary...")
    start = time.time()
    qet_results = benchmark_qet(corpora, config)
    qet_time = time.time() - start
    print(f"   Completed in {qet_time:.2f}s")
    
    # Calculate deltas (only if tiktoken available)
    delta = {}
    
    if tiktoken_available and tik_results.get("avg_compression", 0) > 0:
        delta["compression_improvement"] = (
            (qet_results["avg_compression"] - tik_results["avg_compression"]) 
            / tik_results["avg_compression"]
        ) * 100
    else:
        delta["compression_improvement"] = 0
        delta["tiktoken_unavailable"] = True
    
    if tiktoken_available and tik_results.get("avg_tokens", 0) > 0:
        delta["token_reduction_pct"] = (
            (tik_results["avg_tokens"] - qet_results["avg_tokens"]) 
            / tik_results["avg_tokens"]
        ) * 100
    else:
        delta["token_reduction_pct"] = 0
    
    delta["vocab_efficiency"] = (
        qet_results["total_vocab_used"] / tik_results["total_vocab_used"]
    ) if tik_results.get("total_vocab_used", 0) > 0 else 1.0
    
    # Build result
    result = {
        "timestamp": utc_now_iso(),
        "benchmark_id": f"QET-BENCH-{utc_now().strftime('%Y%m%d-%H%M%S')}",
        "corpora_stats": {
            "num_documents": len(corpora),
            "total_chars": sum(len(c) for c in corpora),
            "avg_doc_length": sum(len(c) for c in corpora) / len(corpora)
        },
        "tiktoken": {
            "model": tiktoken_model,
            "available": tiktoken_available,
            "benchmark_time_s": tik_time,
            **{k: v for k, v in tik_results.items() if k != "per_corpus"}
        },
        "qet": {
            "config": {
                "generations": config.generations,
                "population_size": config.population_size,
                "vocab_size": config.vocab_size,
                "backend": config.backend,
                "safety_mode": config.safety_mode
            },
            "benchmark_time_s": qet_time,
            **{k: v for k, v in qet_results.items() if k != "per_corpus"}
        },
        "delta": delta,
        "verdict": "QET_STANDALONE" if delta.get("tiktoken_unavailable") else ("QET_WINS" if delta["compression_improvement"] > 0 else "TIKTOKEN_WINS"),
        "hash": qet_results.get("vocab_hash", ""),
        "dao_notarization": qet_results.get("notarization", {})
    }
    
    return result


def print_summary(results: Dict[str, Any]):
    """Print human-readable benchmark summary."""
    print("\n" + "=" * 60)
    print("🏆 TOKENIZER BAKE-OFF RESULTS")
    print("=" * 60)
    
    print(f"\n📁 Corpora: {results['corpora_stats']['num_documents']} documents")
    print(f"   Total chars: {results['corpora_stats']['total_chars']:,}")
    
    print(f"\n📊 Tiktoken ({results['tiktoken']['model']}):")
    if results['tiktoken'].get('available', False):
        print(f"   Avg tokens/doc: {results['tiktoken']['avg_tokens']:.1f}")
        print(f"   Avg chars/token: {results['tiktoken']['avg_compression']:.2f}")
        print(f"   Vocab used: {results['tiktoken']['total_vocab_used']:,}")
    else:
        print(f"   ⚠️ Unavailable: {results['tiktoken'].get('error', 'network/import error')[:60]}")
    
    print(f"\n🧬 QET (gen={results['qet']['config']['generations']}):")
    print(f"   Avg tokens/doc: {results['qet']['avg_tokens']:.1f}")
    print(f"   Avg chars/token: {results['qet']['avg_compression']:.2f}")
    print(f"   Vocab used: {results['qet']['total_vocab_used']:,}")
    print(f"   Fitness: {results['qet']['evo_metrics']['fitness']:.4f}")
    
    print(f"\n📈 Delta:")
    delta = results['delta']
    
    if delta.get('tiktoken_unavailable'):
        print("   ⚠️ Comparison unavailable (tiktoken not loaded)")
    else:
        compression_icon = "✅" if delta['compression_improvement'] > 0 else "❌"
        print(f"   {compression_icon} Compression improvement: {delta['compression_improvement']:+.1f}%")
        
        token_icon = "✅" if delta['token_reduction_pct'] > 0 else "❌"
        print(f"   {token_icon} Token reduction: {delta['token_reduction_pct']:+.1f}%")
    
    print(f"\n🏁 Verdict: {results['verdict']}")
    print(f"🔏 QET Hash: {results['hash']}")
    print(f"⏱️  Timestamp: {results['timestamp']}")
    
    if delta.get('tiktoken_unavailable'):
        print("\n📝 QET standalone results (no comparison available)")
        print("   → Run with network access to compare against tiktoken")
    elif delta['compression_improvement'] > 0:
        print("\n🎉 QET outperforms tiktoken on this corpus!")
        print("   → DAO artifact ready for notarization")
    else:
        print("\n📝 tiktoken performs better on this corpus")
        print("   → Consider more generations or corpus-specific tuning")
    
    print("=" * 60)


def main():
    """Main entry point for benchmark script."""
    parser = argparse.ArgumentParser(
        description="QET vs Tiktoken Tokenizer Benchmark",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Run with default sample corpora
    python qet_vs_tiktoken_bench.py
    
    # Run with custom corpus files
    python qet_vs_tiktoken_bench.py --corpus master.yaml --corpus ai_bottlenecks.txt
    
    # Run with specific evolution parameters
    python qet_vs_tiktoken_bench.py --generations 200 --population 64
    
    # Output to specific file
    python qet_vs_tiktoken_bench.py --output benchmarks/results.json
"""
    )
    
    parser.add_argument(
        "--corpus", "-c",
        action="append",
        dest="corpora",
        help="Path to corpus file (can specify multiple)"
    )
    
    parser.add_argument(
        "--corpora-dir", "-d",
        type=str,
        help="Directory containing corpus files (*.txt, *.yaml, *.md)"
    )
    
    parser.add_argument(
        "--generations", "-g",
        type=int,
        default=100,
        help="Number of evolution generations (default: 100)"
    )
    
    parser.add_argument(
        "--population", "-p",
        type=int,
        default=32,
        help="Population size for evolution (default: 32)"
    )
    
    parser.add_argument(
        "--vocab-size", "-v",
        type=int,
        default=4096,
        help="Target vocabulary size (default: 4096)"
    )
    
    parser.add_argument(
        "--tiktoken-model", "-m",
        type=str,
        default="gpt-4",
        help="Tiktoken model for baseline (default: gpt-4)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="qet_bench_results.json",
        help="Output JSON file path (default: qet_bench_results.json)"
    )
    
    parser.add_argument(
        "--seed", "-s",
        type=int,
        default=None,
        help="Random seed for reproducibility"
    )
    
    parser.add_argument(
        "--safety-mode",
        type=str,
        choices=["daylight", "moonlight"],
        default="daylight",
        help="Safety mode: daylight (conservative) or moonlight (experimental)"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress progress output"
    )
    
    args = parser.parse_args()
    
    # Load corpora
    print("🔄 Loading corpora...")
    corpora = []
    
    if args.corpora:
        corpora = load_corpora(args.corpora)
    
    if args.corpora_dir:
        corpus_dir = Path(args.corpora_dir)
        if corpus_dir.exists():
            files = list(corpus_dir.glob("*.txt")) + \
                    list(corpus_dir.glob("*.yaml")) + \
                    list(corpus_dir.glob("*.yml")) + \
                    list(corpus_dir.glob("*.md"))
            corpora.extend(load_corpora([str(f) for f in files]))
    
    if not corpora:
        print("   No corpus files provided, using sample data...")
        corpora = get_sample_corpora()
    
    print(f"   Loaded {len(corpora)} documents, {sum(len(c) for c in corpora):,} total chars")
    
    # Create config
    config = QETConfig(
        generations=args.generations,
        population_size=args.population,
        vocab_size=args.vocab_size,
        backend="mock",  # Always use mock for benchmarking
        seed=args.seed,
        safety_mode=args.safety_mode
    )
    
    # Run benchmark
    results = benchmark(corpora, config, args.tiktoken_model)
    
    # Print summary
    if not args.quiet:
        print_summary(results)
    
    # Save results
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2))
    
    print(f"\n💾 Results saved to: {output_path}")
    print(f"   DAO Notarization command:")
    print(f"   ./generate_dao_record.sh --topic 'QET v3 Benchmark' --input {output_path}")
    
    # Exit code based on outcome
    if results['delta'].get('tiktoken_unavailable'):
        sys.exit(0)  # Standalone mode - success
    elif results['delta']['compression_improvement'] > 0:
        sys.exit(0)  # QET wins
    else:
        sys.exit(1)  # tiktoken wins (signals need for more evolution)


if __name__ == "__main__":
    main()
