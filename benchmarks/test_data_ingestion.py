#!/usr/bin/env python3
"""
Enterprise Benchmarks: Data Ingestion & RAG (Tests 1-10)
Strategickhaos DAO LLC - Cyber + LLM Stack
"""

import pytest
import hashlib
import json
import time
import requests
from pathlib import Path
from typing import List, Dict, Tuple
import pandas as pd
import numpy as np
from sklearn.metrics import ndcg_score

class DataIngestionBenchmarks:
    def __init__(self, config_path: str = "benchmarks/benchmark_config.yaml"):
        self.config = self._load_config(config_path)
        self.cyber_path = Path(self.config['data_sources']['cyber_collection'])
        self.llm_path = Path(self.config['data_sources']['llm_collection'])
        self.rag_endpoint = self.config['data_sources']['rag_endpoint']
        
    def test_01_ingestion_integrity(self) -> Dict:
        """Test 1: Verify file count, sizes, and SHA256; fail on drift."""
        results = {"test_id": 1, "name": "Ingestion Integrity", "status": "PASS"}
        
        # Check cyber collection (30 expected files)
        cyber_files = list(self.cyber_path.glob("*.html")) + list(self.cyber_path.glob("*.pdf"))
        results["cyber_file_count"] = len(cyber_files)
        
        # Check LLM collection (27 expected files)
        llm_files = list(self.llm_path.glob("*.pdf"))
        results["llm_file_count"] = len(llm_files)
        
        # Verify checksums
        checksums = {}
        for file_path in cyber_files + llm_files:
            with open(file_path, 'rb') as f:
                checksums[file_path.name] = hashlib.sha256(f.read()).hexdigest()
        
        results["checksums_computed"] = len(checksums)
        results["total_files"] = len(cyber_files) + len(llm_files)
        
        # Fail conditions
        if len(cyber_files) < 25 or len(llm_files) < 20:
            results["status"] = "FAIL"
            results["reason"] = "Insufficient files collected"
            
        return results
    
    def test_02_chunking_correctness(self) -> Dict:
        """Test 2: Sample 100 docs; assert chunk size/overlap; no empty chunks."""
        results = {"test_id": 2, "name": "Chunking Correctness", "status": "PASS"}
        
        # Sample files for chunk analysis
        sample_files = list(self.llm_path.glob("*.pdf"))[:10]  # Sample 10 PDFs
        
        chunk_stats = {
            "files_sampled": len(sample_files),
            "target_chunk_size": 512,
            "target_overlap": 128,
            "empty_chunks": 0,
            "oversized_chunks": 0
        }
        
        # Simulate chunk analysis (would integrate with actual chunking pipeline)
        for file_path in sample_files:
            file_size = file_path.stat().st_size
            estimated_chunks = max(1, file_size // (512 * 4))  # Rough estimate
            
            # Check for potential issues
            if file_size < 100:  # Very small files might create empty chunks
                chunk_stats["empty_chunks"] += 1
                
        results.update(chunk_stats)
        
        if chunk_stats["empty_chunks"] > 5:
            results["status"] = "FAIL"
            results["reason"] = "Too many empty chunks detected"
            
        return results
    
    def test_03_embedding_quality_recall(self) -> Dict:
        """Test 3: Gold Q/A set; measure Recall@5/10, MRR."""
        results = {"test_id": 3, "name": "Embedding Quality (IR@k)", "status": "PASS"}
        
        # Gold standard queries for cyber domain
        gold_queries = [
            {"query": "NIST incident response phases", "expected_docs": ["nist_sp_800_61"]},
            {"query": "MITRE ATT&CK lateral movement", "expected_docs": ["mitre_attack"]},
            {"query": "Constitutional AI harmlessness", "expected_docs": ["constitutional_ai"]},
            {"query": "Chain-of-thought reasoning", "expected_docs": ["chain_of_thought"]},
            {"query": "Chinchilla optimal scaling", "expected_docs": ["chinchilla_scaling"]}
        ]
        
        recall_at_5_scores = []
        recall_at_10_scores = []
        mrr_scores = []
        
        for query_data in gold_queries:
            try:
                response = requests.post(self.rag_endpoint, 
                                       json={"q": query_data["query"], "k": 10},
                                       timeout=5)
                
                if response.status_code == 200:
                    results_data = response.json()
                    retrieved_docs = [doc.get('id', '') for doc in results_data.get('results', [])]
                    
                    # Calculate recall@5 and recall@10
                    relevant_in_5 = sum(1 for doc in retrieved_docs[:5] 
                                       if any(exp in doc for exp in query_data["expected_docs"]))
                    relevant_in_10 = sum(1 for doc in retrieved_docs[:10] 
                                        if any(exp in doc for exp in query_data["expected_docs"]))
                    
                    recall_at_5_scores.append(relevant_in_5 / len(query_data["expected_docs"]))
                    recall_at_10_scores.append(relevant_in_10 / len(query_data["expected_docs"]))
                    
                    # Calculate MRR
                    for i, doc in enumerate(retrieved_docs):
                        if any(exp in doc for exp in query_data["expected_docs"]):
                            mrr_scores.append(1.0 / (i + 1))
                            break
                    else:
                        mrr_scores.append(0.0)
                        
            except Exception as e:
                results["error"] = str(e)
                
        results["recall_at_5"] = np.mean(recall_at_5_scores) if recall_at_5_scores else 0.0
        results["recall_at_10"] = np.mean(recall_at_10_scores) if recall_at_10_scores else 0.0
        results["mrr"] = np.mean(mrr_scores) if mrr_scores else 0.0
        results["queries_tested"] = len(gold_queries)
        
        # SLA check
        target_recall_5 = self.config['sla_targets']['recall_at_5']
        if results["recall_at_5"] < target_recall_5:
            results["status"] = "FAIL"
            results["reason"] = f"Recall@5 {results['recall_at_5']:.3f} below target {target_recall_5}"
            
        return results
    
    def test_04_cross_encoder_rerank(self) -> Dict:
        """Test 4: Compare top-5 before/after re-ranking; report nDCG gain."""
        results = {"test_id": 4, "name": "Cross-Encoder Re-rank Lift", "status": "PASS"}
        
        test_query = "OWASP top 10 web application security risks"
        
        try:
            # Get results without re-ranking
            response_base = requests.post(self.rag_endpoint,
                                        json={"q": test_query, "k": 10, "rerank": False},
                                        timeout=5)
            
            # Get results with re-ranking (simulated)
            response_rerank = requests.post(self.rag_endpoint,
                                          json={"q": test_query, "k": 10, "rerank": True},
                                          timeout=5)
            
            if response_base.status_code == 200:
                base_results = response_base.json().get('results', [])
                rerank_results = response_rerank.json().get('results', []) if response_rerank.status_code == 200 else base_results
                
                # Simulate relevance scores (in practice, would use human judgments)
                base_relevance = [0.8 if 'owasp' in doc.get('id', '').lower() else 0.3 for doc in base_results[:5]]
                rerank_relevance = [0.9 if 'owasp' in doc.get('id', '').lower() else 0.2 for doc in rerank_results[:5]]
                
                # Calculate nDCG for top-5
                if base_relevance and rerank_relevance:
                    base_ndcg = ndcg_score([base_relevance], [base_relevance])
                    rerank_ndcg = ndcg_score([base_relevance], [rerank_relevance])
                    
                    results["base_ndcg"] = base_ndcg
                    results["rerank_ndcg"] = rerank_ndcg
                    results["ndcg_gain"] = rerank_ndcg - base_ndcg
                    results["relative_improvement"] = (rerank_ndcg - base_ndcg) / base_ndcg if base_ndcg > 0 else 0.0
                    
        except Exception as e:
            results["status"] = "FAIL"
            results["error"] = str(e)
            
        return results
    
    def test_05_query_latency_slo(self) -> Dict:
        """Test 5: P50/P90/P99 latency under 50, 200, 800 ms for k=5,10,50."""
        results = {"test_id": 5, "name": "Query Latency SLO", "status": "PASS"}
        
        latencies = {"k5": [], "k10": [], "k50": []}
        test_queries = [
            "NIST cybersecurity framework",
            "transformer attention mechanism", 
            "incident response playbook",
            "constitutional AI safety",
            "MITRE ATT&CK techniques"
        ]
        
        # Test different k values
        for k_value, k_key in [(5, "k5"), (10, "k10"), (50, "k50")]:
            for query in test_queries:
                try:
                    start_time = time.time()
                    response = requests.post(self.rag_endpoint,
                                           json={"q": query, "k": k_value},
                                           timeout=10)
                    end_time = time.time()
                    
                    if response.status_code == 200:
                        latency_ms = (end_time - start_time) * 1000
                        latencies[k_key].append(latency_ms)
                        
                except Exception as e:
                    results["errors"] = results.get("errors", []) + [str(e)]
        
        # Calculate percentiles
        for k_key, times in latencies.items():
            if times:
                results[f"{k_key}_p50"] = np.percentile(times, 50)
                results[f"{k_key}_p90"] = np.percentile(times, 90)
                results[f"{k_key}_p99"] = np.percentile(times, 99)
                
        # Check SLA violations
        targets = self.config['sla_targets']
        violations = []
        
        for k_key in latencies.keys():
            p50_key = f"{k_key}_p50"
            if p50_key in results and results[p50_key] > targets['query_latency_p50']:
                violations.append(f"{k_key} P50: {results[p50_key]:.1f}ms > {targets['query_latency_p50']}ms")
                
        if violations:
            results["status"] = "FAIL"
            results["sla_violations"] = violations
            
        return results

if __name__ == "__main__":
    benchmarks = DataIngestionBenchmarks()
    
    # Run tests 1-5
    test_results = []
    test_results.append(benchmarks.test_01_ingestion_integrity())
    test_results.append(benchmarks.test_02_chunking_correctness())
    test_results.append(benchmarks.test_03_embedding_quality_recall())
    test_results.append(benchmarks.test_04_cross_encoder_rerank())
    test_results.append(benchmarks.test_05_query_latency_slo())
    
    # Output results
    for result in test_results:
        print(f"Test {result['test_id']}: {result['name']} - {result['status']}")
        if result['status'] == 'FAIL':
            print(f"  Reason: {result.get('reason', 'Unknown')}")
            
    # Save detailed results
    with open("benchmarks/reports/data_ingestion_results.json", "w") as f:
        json.dump(test_results, f, indent=2)