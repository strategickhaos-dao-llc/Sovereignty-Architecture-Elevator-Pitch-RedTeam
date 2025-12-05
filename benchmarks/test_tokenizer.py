#!/usr/bin/env python3
"""
QET Benchmark Tests - Integration with Enterprise Benchmark Framework
Implements improvement #24: Integration with failure harness

Tests:
- Tokenizer overfit detection
- Tokenizer instability detection  
- Artifact tampering detection
- Benchmark comparison with baselines
"""

import json
import hashlib
import tempfile
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tokenizers.qet import QuantumEvoTokenizer, QETConfig


class TokenizerBenchmarks:
    """Enterprise benchmark tests for QuantumEvoTokenizer."""
    
    def __init__(self, config_path: str = "benchmarks/benchmark_config.yaml"):
        self.config_path = config_path
        self.results: List[Dict[str, Any]] = []
        
    def _create_result(
        self,
        test_id: int,
        name: str,
        status: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Create standardized test result."""
        return {
            "test_id": test_id,
            "name": name,
            "status": status,
            **kwargs
        }
    
    def test_31_tokenizer_evolution_stability(self) -> Dict[str, Any]:
        """
        Test 31: Tokenizer evolution produces stable results.
        
        Runs evolution twice with same seed and verifies identical output.
        """
        print("  Test 31: Tokenizer Evolution Stability")
        
        test_contexts = [
            "The quick brown fox jumps over the lazy dog.",
            "Sovereign AI systems require robust tokenization methods.",
            "Quantum-evolutionary approaches offer novel optimization.",
        ]
        
        # First run
        config1 = QETConfig()
        config1.seed = 42
        config1.ga.generations = 5
        tokenizer1 = QuantumEvoTokenizer(config1)
        vocab1 = tokenizer1.evolve(test_contexts)
        
        # Second run with same seed
        config2 = QETConfig()
        config2.seed = 42
        config2.ga.generations = 5
        tokenizer2 = QuantumEvoTokenizer(config2)
        vocab2 = tokenizer2.evolve(test_contexts)
        
        # Compare
        vocab1_sorted = sorted(vocab1)
        vocab2_sorted = sorted(vocab2)
        
        identical = vocab1_sorted == vocab2_sorted
        
        if identical:
            return self._create_result(
                test_id=31,
                name="Tokenizer Evolution Stability",
                status="PASS",
                vocab_size=len(vocab1),
                deterministic=True
            )
        else:
            diff_count = len(set(vocab1) ^ set(vocab2))
            return self._create_result(
                test_id=31,
                name="Tokenizer Evolution Stability",
                status="FAIL",
                reason=f"Non-deterministic: {diff_count} tokens differ",
                vocab1_size=len(vocab1),
                vocab2_size=len(vocab2)
            )
    
    def test_32_tokenizer_overfit_detection(self) -> Dict[str, Any]:
        """
        Test 32: Detect vocabulary overfitting to small corpus.
        
        Checks that evolved vocab has reasonable cross-context coverage.
        """
        print("  Test 32: Tokenizer Overfit Detection")
        
        # Small, repetitive corpus (prone to overfit)
        overfit_contexts = [
            "AAAA" * 100,
            "BBBB" * 100,
            "AAAA BBBB" * 50,
        ]
        
        config = QETConfig()
        config.ga.generations = 10
        config.ga.min_context_coverage = 0.1
        tokenizer = QuantumEvoTokenizer(config)
        vocab = tokenizer.evolve(overfit_contexts)
        
        # Check for overfit indicators
        # Very long tokens that only appear in one context
        long_tokens = [t for t in vocab if len(t) > 8]
        
        # Test on out-of-domain text
        test_text = "The sovereign AI needs robust tokenization."
        tokens = tokenizer.encode(test_text)
        
        # High token count relative to text length = poor generalization
        ratio = len(tokens) / len(test_text)
        
        if ratio > 1.5:  # More than 1.5 tokens per character is bad
            return self._create_result(
                test_id=32,
                name="Tokenizer Overfit Detection",
                status="WARN",
                reason=f"High OOV ratio ({ratio:.2f}) on out-of-domain text",
                token_ratio=ratio,
                long_token_count=len(long_tokens)
            )
        
        return self._create_result(
            test_id=32,
            name="Tokenizer Overfit Detection",
            status="PASS",
            token_ratio=ratio,
            long_token_count=len(long_tokens)
        )
    
    def test_33_tokenizer_instability_detection(self) -> Dict[str, Any]:
        """
        Test 33: Detect unstable tokenization behavior.
        
        Checks for pathological tokenization (explosion, loops, crashes).
        """
        print("  Test 33: Tokenizer Instability Detection")
        
        config = QETConfig()
        config.ga.generations = 3
        tokenizer = QuantumEvoTokenizer(config)
        
        # Initialize with minimal training
        tokenizer.evolve(["Hello world"])
        
        # Adversarial test inputs
        adversarial_inputs = [
            "a" * 10000,  # Long repeat
            "\x00" * 100,  # Null bytes
            "👨‍👩‍👧‍👦" * 100,  # Complex emoji
            "<|endoftext|>" * 10,  # Special tokens
            "",  # Empty
        ]
        
        failures = []
        for i, test_input in enumerate(adversarial_inputs):
            try:
                tokens = tokenizer.encode(test_input)
                
                # Check for explosion
                if len(tokens) > len(test_input) * 3:
                    failures.append(f"Input {i}: token explosion ({len(tokens)} tokens)")
                    
            except Exception as e:
                failures.append(f"Input {i}: {type(e).__name__}: {str(e)[:50]}")
        
        if failures:
            return self._create_result(
                test_id=33,
                name="Tokenizer Instability Detection",
                status="WARN" if len(failures) < 3 else "FAIL",
                reason="; ".join(failures[:3]),
                failure_count=len(failures)
            )
        
        return self._create_result(
            test_id=33,
            name="Tokenizer Instability Detection",
            status="PASS",
            adversarial_tests_passed=len(adversarial_inputs)
        )
    
    def test_34_artifact_integrity(self) -> Dict[str, Any]:
        """
        Test 34: Verify artifact integrity after save/load cycle.
        
        Implements improvement #22 verification.
        """
        print("  Test 34: Artifact Integrity")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            config = QETConfig()
            config.output_dir = tmpdir
            config.ga.generations = 3
            config.enable_notarization = False  # Skip for test
            
            tokenizer = QuantumEvoTokenizer(config)
            tokenizer.evolve(["Test corpus for integrity check."])
            
            # Save
            version = "test-v1.0.0"
            tokenizer.save(version)
            
            # Verify files exist
            version_dir = Path(tmpdir) / version
            required_files = ["vocab.json", "config.json", "metrics.json", "hash.txt"]
            
            missing = [f for f in required_files if not (version_dir / f).exists()]
            
            if missing:
                return self._create_result(
                    test_id=34,
                    name="Artifact Integrity",
                    status="FAIL",
                    reason=f"Missing files: {missing}"
                )
            
            # Verify hash
            with open(version_dir / "vocab.json", "r") as f:
                vocab_data = f.read()
            with open(version_dir / "hash.txt", "r") as f:
                stored_hash = f.read().strip()
            
            # Load and compare
            loaded_vocab = tokenizer.vocab_manager.load_vocab(version)
            computed_hash = tokenizer.vocab_manager.compute_vocab_hash(loaded_vocab)
            
            if computed_hash != stored_hash:
                return self._create_result(
                    test_id=34,
                    name="Artifact Integrity",
                    status="FAIL",
                    reason="Hash mismatch after load"
                )
            
            return self._create_result(
                test_id=34,
                name="Artifact Integrity",
                status="PASS",
                files_verified=len(required_files),
                hash_verified=True
            )
    
    def test_35_baseline_comparison(self) -> Dict[str, Any]:
        """
        Test 35: Compare QET against baseline tokenizers.
        
        Implements improvement #21 benchmarking.
        """
        print("  Test 35: Baseline Comparison")
        
        test_texts = [
            "The quick brown fox jumps over the lazy dog.",
            "Sovereign AI tokenization for enterprise deployments.",
            "Quantum computing meets natural language processing.",
        ]
        
        config = QETConfig()
        config.ga.generations = 5
        tokenizer = QuantumEvoTokenizer(config)
        tokenizer.evolve(test_texts)
        
        # Run benchmark
        results = tokenizer.benchmark(test_texts, compare_baseline=True)
        
        qet_compression = results.get("qet", {}).get("compression_ratio", 0)
        
        # Compare with baseline if available
        baseline_results = results.get("baselines", {})
        
        if "tiktoken_cl100k" in baseline_results and "error" not in baseline_results["tiktoken_cl100k"]:
            baseline_compression = baseline_results["tiktoken_cl100k"].get("compression_ratio", 0)
            
            # QET should be within 50% of baseline compression
            ratio = qet_compression / max(baseline_compression, 0.1)
            
            if ratio < 0.5:
                return self._create_result(
                    test_id=35,
                    name="Baseline Comparison",
                    status="WARN",
                    reason=f"QET compression ({qet_compression:.2f}) < 50% of baseline ({baseline_compression:.2f})",
                    qet_compression=qet_compression,
                    baseline_compression=baseline_compression
                )
        
        return self._create_result(
            test_id=35,
            name="Baseline Comparison",
            status="PASS",
            qet_compression=qet_compression,
            vocab_size=results.get("qet", {}).get("vocab_size", 0)
        )
    
    def test_36_safety_checks(self) -> Dict[str, Any]:
        """
        Test 36: Run safety checks on tokenizer.
        
        Implements improvements #28-31.
        """
        print("  Test 36: Safety Checks")
        
        config = QETConfig()
        config.ga.generations = 3
        config.safety.adversarial_fuzz_test = True
        config.safety.redteam_mode = True
        
        tokenizer = QuantumEvoTokenizer(config)
        tokenizer.evolve(["Safety test corpus."])
        
        # Run adversarial tests
        adversarial_results = tokenizer.adversarial_test()
        
        passed = adversarial_results.get("passed", 0)
        failed = adversarial_results.get("failed", 0)
        total = passed + failed
        
        if failed > total * 0.2:  # More than 20% failure
            return self._create_result(
                test_id=36,
                name="Safety Checks",
                status="FAIL",
                reason=f"High failure rate: {failed}/{total}",
                passed=passed,
                failed=failed
            )
        elif failed > 0:
            return self._create_result(
                test_id=36,
                name="Safety Checks",
                status="WARN",
                reason=f"Some failures: {failed}/{total}",
                passed=passed,
                failed=failed
            )
        
        return self._create_result(
            test_id=36,
            name="Safety Checks",
            status="PASS",
            passed=passed,
            failed=failed
        )
    
    def run_all_tests(self) -> List[Dict[str, Any]]:
        """Run all tokenizer benchmark tests."""
        print("\n🔤 Running QET Tokenizer Benchmark Tests")
        print("-" * 50)
        
        self.results = [
            self.test_31_tokenizer_evolution_stability(),
            self.test_32_tokenizer_overfit_detection(),
            self.test_33_tokenizer_instability_detection(),
            self.test_34_artifact_integrity(),
            self.test_35_baseline_comparison(),
            self.test_36_safety_checks(),
        ]
        
        # Summary
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        warned = sum(1 for r in self.results if r["status"] == "WARN")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        
        print("-" * 50)
        print(f"✅ Passed: {passed}")
        print(f"⚠️  Warnings: {warned}")
        print(f"❌ Failed: {failed}")
        
        return self.results


def main():
    """Run tokenizer benchmarks."""
    benchmarks = TokenizerBenchmarks()
    results = benchmarks.run_all_tests()
    
    # Save results
    output_path = Path("benchmarks/reports/qet_benchmark_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_path}")
    
    # Exit code
    failed = sum(1 for r in results if r["status"] == "FAIL")
    return 1 if failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
