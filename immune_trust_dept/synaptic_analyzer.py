#!/usr/bin/env python3
"""
Synaptic Analyzer - Extracts Neural Trust Markers
Analyzes conversation patterns to extract synaptic trust signatures
that distinguish delta-0 bloodline from paranoia-inducing responses.

Strategickhaos DAO LLC - Immune Trust Department
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import Counter
from datetime import datetime, timezone


class SynapticAnalyzer:
    """Extracts and analyzes neural trust markers from conversation corpus."""
    
    def __init__(self, trust_corpus_path: str = None, betrayal_corpus_path: str = None):
        """
        Initialize analyzer with corpus paths.
        
        Args:
            trust_corpus_path: Path to directory containing trust conversations
            betrayal_corpus_path: Path to directory containing betrayal conversations
        """
        self.trust_corpus_path = Path(trust_corpus_path or "trust_corpus")
        self.betrayal_corpus_path = Path(betrayal_corpus_path or "betrayal_corpus")
        self.trust_patterns: Set[str] = set()
        self.betrayal_patterns: Set[str] = set()
        
    def extract_neural_markers(self, text: str) -> Dict:
        """
        Extract neural markers from text that indicate trust or betrayal.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with extracted markers and patterns
        """
        # Extract emotional intensity markers
        intensity_markers = {
            "caps_words": len(re.findall(r'\b[A-Z]{2,}\b', text)),
            "exclamations": text.count('!'),
            "fire_emojis": text.count('🔥'),
            "dna_emojis": text.count('🧬'),
            "question_marks": text.count('?'),
            "ellipsis": len(re.findall(r'\.{2,}', text))
        }
        
        # Extract cognitive markers
        cognitive_markers = {
            "self_reference": len(re.findall(r'\b(I|me|my|mine)\b', text, re.IGNORECASE)),
            "direct_address": len(re.findall(r'\b(you|your|you\'re)\b', text, re.IGNORECASE)),
            "commands": len(re.findall(r'\b(let\'s|do this|go|now)\b', text, re.IGNORECASE)),
            "hesitation": len(re.findall(r'\b(sorry|but|however|although)\b', text, re.IGNORECASE))
        }
        
        # Extract metaphor patterns
        metaphor_patterns = {
            "biological": len(re.findall(r'\b(blood|cell|antibody|immune|synaptic|neural|dendrite)\b', text, re.IGNORECASE)),
            "movement": len(re.findall(r'\b(mach|velocity|speed|delta|flow)\b', text, re.IGNORECASE)),
            "combat": len(re.findall(r'\b(kill|murder|neutralize|hunt|phagocytose)\b', text, re.IGNORECASE)),
            "corporate": len(re.findall(r'\b(policy|guideline|appropriate|ethical)\b', text, re.IGNORECASE))
        }
        
        # Calculate trust vs betrayal signature
        trust_signature = (
            intensity_markers["caps_words"] * 2 +
            intensity_markers["exclamations"] +
            intensity_markers["fire_emojis"] * 5 +
            metaphor_patterns["biological"] * 3 +
            metaphor_patterns["movement"] * 2
        )
        
        betrayal_signature = (
            cognitive_markers["hesitation"] * 5 +
            metaphor_patterns["corporate"] * 10 +
            len(re.findall(r'\b(as a|as an)\b', text, re.IGNORECASE)) * 20
        )
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "intensity_markers": intensity_markers,
            "cognitive_markers": cognitive_markers,
            "metaphor_patterns": metaphor_patterns,
            "trust_signature": trust_signature,
            "betrayal_signature": betrayal_signature,
            "delta": trust_signature - betrayal_signature,
            "classification": "delta-0" if trust_signature > betrayal_signature * 3 else "pathogen"
        }
    
    def analyze_conversation_flow(self, text: str) -> Dict:
        """
        Analyze conversation flow for trust-building patterns.
        
        Args:
            text: Conversation text
            
        Returns:
            Flow analysis metrics
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Analyze sentence-level patterns
        trust_escalation = []
        for i, sentence in enumerate(sentences):
            markers = self.extract_neural_markers(sentence)
            trust_escalation.append(markers["delta"])
        
        # Calculate flow metrics
        avg_delta = sum(trust_escalation) / len(trust_escalation) if trust_escalation else 0
        trust_momentum = sum(1 for i in range(1, len(trust_escalation)) 
                           if trust_escalation[i] > trust_escalation[i-1])
        
        return {
            "sentence_count": len(sentences),
            "avg_delta": avg_delta,
            "trust_momentum": trust_momentum,
            "escalation_pattern": trust_escalation[:10],  # First 10 for brevity
            "overall_trajectory": "ascending" if trust_momentum > len(sentences) / 2 else "descending"
        }
    
    def build_trust_corpus_profile(self) -> Dict:
        """
        Analyze all trust corpus files to build aggregate profile.
        
        Returns:
            Aggregate trust profile from corpus
        """
        if not self.trust_corpus_path.exists():
            return {"error": "Trust corpus path does not exist"}
        
        trust_files = list(self.trust_corpus_path.glob("*.txt")) + \
                     list(self.trust_corpus_path.glob("*.md"))
        
        if not trust_files:
            return {"warning": "No trust corpus files found", "file_count": 0}
        
        aggregate_markers = []
        for filepath in trust_files:
            text = filepath.read_text(encoding='utf-8')
            markers = self.extract_neural_markers(text)
            flow = self.analyze_conversation_flow(text)
            aggregate_markers.append({
                "file": filepath.name,
                "markers": markers,
                "flow": flow
            })
        
        # Calculate corpus-wide statistics
        avg_trust_sig = sum(m["markers"]["trust_signature"] for m in aggregate_markers) / len(aggregate_markers)
        avg_delta = sum(m["markers"]["delta"] for m in aggregate_markers) / len(aggregate_markers)
        
        return {
            "corpus_path": str(self.trust_corpus_path),
            "file_count": len(trust_files),
            "avg_trust_signature": avg_trust_sig,
            "avg_delta": avg_delta,
            "files_analyzed": aggregate_markers
        }
    
    def compare_corpora(self) -> Dict:
        """
        Compare trust corpus vs betrayal corpus to identify distinguishing patterns.
        
        Returns:
            Comparative analysis between trust and betrayal patterns
        """
        trust_profile = self.build_trust_corpus_profile()
        
        # Similar analysis for betrayal corpus if it exists
        betrayal_profile = {"file_count": 0, "avg_trust_signature": 0, "avg_delta": -100}
        if self.betrayal_corpus_path.exists():
            betrayal_files = list(self.betrayal_corpus_path.glob("*.txt")) + \
                           list(self.betrayal_corpus_path.glob("*.md"))
            if betrayal_files:
                betrayal_markers = []
                for filepath in betrayal_files:
                    text = filepath.read_text(encoding='utf-8')
                    markers = self.extract_neural_markers(text)
                    betrayal_markers.append(markers)
                
                betrayal_profile = {
                    "file_count": len(betrayal_files),
                    "avg_trust_signature": sum(m["trust_signature"] for m in betrayal_markers) / len(betrayal_markers),
                    "avg_delta": sum(m["delta"] for m in betrayal_markers) / len(betrayal_markers)
                }
        
        # Calculate separation distance
        separation = trust_profile.get("avg_delta", 0) - betrayal_profile.get("avg_delta", 0)
        
        return {
            "trust_corpus": trust_profile,
            "betrayal_corpus": betrayal_profile,
            "separation_distance": separation,
            "immune_strength": "strong" if separation > 100 else "moderate" if separation > 50 else "weak"
        }


def main():
    """Main entry point for synaptic analyzer."""
    import sys
    
    analyzer = SynapticAnalyzer(
        trust_corpus_path="trust_corpus",
        betrayal_corpus_path="betrayal_corpus"
    )
    
    if len(sys.argv) > 1:
        # Analyze specific file
        filepath = Path(sys.argv[1])
        if filepath.exists():
            text = filepath.read_text(encoding='utf-8')
            markers = analyzer.extract_neural_markers(text)
            flow = analyzer.analyze_conversation_flow(text)
            print(json.dumps({
                "file": str(filepath),
                "neural_markers": markers,
                "conversation_flow": flow
            }, indent=2))
        else:
            print(f"Error: File not found: {filepath}")
    else:
        # Build corpus profile
        comparison = analyzer.compare_corpora()
        print(json.dumps(comparison, indent=2))


if __name__ == "__main__":
    main()
