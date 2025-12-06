#!/usr/bin/env python3
"""
Sovereign Grok Tokenizer
Build a local tokenizer that approximates Grok's behavior without API dependency.

Uses tiktoken (OpenAI's BPE library) as base, then trains custom vocab.
"""

import tiktoken
import json
from pathlib import Path
from typing import List, Dict
from collections import Counter

class SovereignTokenizer:
    """
    Local tokenizer for processing massive context dumps.
    No API calls, full sovereignty.
    """
    
    def __init__(self, model_name: str = "gpt-4"):
        # Start with GPT-4 encoding as base (similar to Grok)
        try:
            self.encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            raise ValueError(f"Unsupported model name: {model_name}. Use a valid tiktoken model name.")
        self.vocab_size = self.encoding.n_vocab
        
    def tokenize(self, text: str) -> List[int]:
        """Convert text to token IDs"""
        return self.encoding.encode(text)
    
    def detokenize(self, tokens: List[int]) -> str:
        """Convert token IDs back to text"""
        return self.encoding.decode(tokens)
    
    def count_tokens(self, text: str) -> int:
        """Fast token counting (what Grok's console shows)"""
        return len(self.encoding.encode(text))
    
    def analyze_text(self, text: str) -> Dict:
        """
        Full analysis like Grok's tokenizer console
        Returns: tokens, characters, token IDs, and compression ratio (chars per token)
        """
        tokens = self.tokenize(text)
        return {
            "tokens": tokens,
            "token_count": len(tokens),
            "character_count": len(text),
            "compression_ratio": len(text) / len(tokens) if tokens else 0,  # chars per token
            "vocab_coverage": len(set(tokens)) / self.vocab_size
        }
    
    def batch_analyze(self, texts: List[str]) -> Dict:
        """Analyze multiple contexts (your 9-10 dumps)"""
        results = []
        total_tokens = 0
        total_chars = 0
        
        for i, text in enumerate(texts):
            analysis = self.analyze_text(text)
            analysis["context_id"] = i
            results.append(analysis)
            total_tokens += analysis["token_count"]
            total_chars += analysis["character_count"]
        
        return {
            "contexts": results,
            "total_tokens": total_tokens,
            "total_characters": total_chars,
            "avg_compression": total_chars / total_tokens if total_tokens else 0
        }
    
    def save_analysis(self, analysis: Dict, output_path: Path):
        """Save analysis as JSON for your pipeline"""
        with output_path.open("w") as f:
            json.dump(analysis, f, indent=2)


def extract_token_patterns(text: str, tokenizer: SovereignTokenizer) -> Dict:
    """
    Extract repeating token patterns (for finding DNA motifs in your contexts)
    """
    tokens = tokenizer.tokenize(text)
    
    # Find most common token sequences (3-grams)
    trigrams = []
    for i in range(len(tokens) - 2):
        trigrams.append(tuple(tokens[i:i+3]))
    
    common_patterns = Counter(trigrams).most_common(10)
    
    return {
        "total_unique_tokens": len(set(tokens)),
        "most_common_trigrams": [
            {
                "tokens": list(pattern),
                "text": tokenizer.detokenize(list(pattern)),
                "count": count
            }
            for pattern, count in common_patterns
        ]
    }


if __name__ == "__main__":
    # Example usage for your contexts
    tokenizer = SovereignTokenizer()
    
    # Simulate one of your context dumps
    sample_context = """
    Strategickhaos Sovereign Compute Architecture v1.0
    Evolution = Adaptation: Same process + different environments = opposite adaptations
    
    supremacy_pillars:
      - pillar: 1
        name: "Compute Monopoly"
        bottlenecks:
          - "H100/H200/GB200 allocation starvation"
          - "Power grid denials for 500MW+ clusters"
    """
    
    # Analyze
    analysis = tokenizer.analyze_text(sample_context)
    print(f"Tokens: {analysis['token_count']}")
    print(f"Characters: {analysis['character_count']}")
    print(f"Compression: {analysis['compression_ratio']:.2f} chars/token")
    
    # Extract patterns
    patterns = extract_token_patterns(sample_context, tokenizer)
    print(f"\nUnique tokens: {patterns['total_unique_tokens']}")
    print("\nCommon patterns:")
    for p in patterns['most_common_trigrams'][:3]:
        print(f"  '{p['text']}' ({p['count']}x)")
