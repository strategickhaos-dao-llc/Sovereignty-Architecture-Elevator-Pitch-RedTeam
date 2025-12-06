"""
Token Boundary Visualization Tool
Implements improvement #27: Visualization tool for token boundaries
"""

import html
from typing import Dict, List, Optional, Set, Tuple
import math


def compute_local_entropy(text: str, position: int, window_size: int = 4) -> float:
    """Compute Shannon entropy in a window around position."""
    start = max(0, position - window_size)
    end = min(len(text), position + window_size + 1)
    window = text[start:end]
    
    if not window:
        return 0.0
    
    char_counts: Dict[str, int] = {}
    for c in window:
        char_counts[c] = char_counts.get(c, 0) + 1
    
    total = len(window)
    entropy = 0.0
    for count in char_counts.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)
    
    return entropy


def entropy_to_color(entropy: float, max_entropy: float = 4.0) -> str:
    """Convert entropy value to CSS color (blue=low, red=high)."""
    normalized = min(entropy / max_entropy, 1.0)
    
    # Blue (low entropy) to Red (high entropy)
    r = int(255 * normalized)
    b = int(255 * (1 - normalized))
    g = int(100 * (1 - abs(normalized - 0.5) * 2))  # Green peaks at middle
    
    return f"rgb({r},{g},{b})"


def generate_html_visualization(
    text: str,
    token_boundaries: List[int],
    vocab: Optional[Set[bytes]] = None,
    title: str = "QET Token Visualization"
) -> str:
    """
    Generate HTML visualization of token boundaries and entropy.
    
    Args:
        text: The text to visualize
        token_boundaries: Positions where token boundaries occur
        vocab: Optional vocabulary for labeling
        title: Page title
    
    Returns:
        HTML string
    """
    # Compute entropy for each position
    entropies = [compute_local_entropy(text, i) for i in range(len(text))]
    max_entropy = max(entropies) if entropies else 1.0
    
    # Build HTML spans for each character
    spans = []
    boundary_set = set(token_boundaries)
    
    for i, char in enumerate(text):
        entropy = entropies[i] if i < len(entropies) else 0
        color = entropy_to_color(entropy, max_entropy)
        
        # Escape HTML characters
        escaped_char = html.escape(char)
        if char == ' ':
            escaped_char = '&nbsp;'
        elif char == '\n':
            escaped_char = '<br>'
        elif char == '\t':
            escaped_char = '&nbsp;&nbsp;&nbsp;&nbsp;'
        
        # Add boundary marker
        if i in boundary_set:
            spans.append('<span class="boundary">|</span>')
        
        spans.append(
            f'<span class="char" style="background-color: {color};" '
            f'title="pos={i}, entropy={entropy:.2f}">{escaped_char}</span>'
        )
    
    # Add final boundary if present
    if len(text) in boundary_set:
        spans.append('<span class="boundary">|</span>')
    
    content = ''.join(spans)
    
    # Generate token summary if vocab provided
    token_summary = ""
    if vocab:
        token_summary = generate_token_summary(text, token_boundaries, vocab)
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Consolas', 'Monaco', monospace;
            margin: 20px;
            background-color: #1a1a2e;
            color: #eee;
        }}
        h1 {{
            color: #00d9ff;
            border-bottom: 2px solid #00d9ff;
            padding-bottom: 10px;
        }}
        .visualization {{
            background-color: #16213e;
            padding: 20px;
            border-radius: 8px;
            font-size: 16px;
            line-height: 2;
            word-wrap: break-word;
            white-space: pre-wrap;
        }}
        .char {{
            padding: 2px 1px;
            border-radius: 2px;
            margin: 0 1px;
        }}
        .boundary {{
            color: #00ff00;
            font-weight: bold;
            margin: 0 2px;
        }}
        .legend {{
            margin-top: 20px;
            padding: 15px;
            background-color: #16213e;
            border-radius: 8px;
        }}
        .legend h3 {{
            margin-top: 0;
            color: #00d9ff;
        }}
        .color-scale {{
            display: flex;
            height: 30px;
            margin: 10px 0;
            border-radius: 4px;
            overflow: hidden;
        }}
        .color-scale div {{
            flex: 1;
        }}
        .scale-labels {{
            display: flex;
            justify-content: space-between;
            color: #888;
        }}
        .summary {{
            margin-top: 20px;
            padding: 15px;
            background-color: #16213e;
            border-radius: 8px;
        }}
        .summary h3 {{
            margin-top: 0;
            color: #00d9ff;
        }}
        .token {{
            display: inline-block;
            background-color: #2a2a4a;
            padding: 4px 8px;
            margin: 4px;
            border-radius: 4px;
            border: 1px solid #444;
        }}
        .token:hover {{
            background-color: #3a3a5a;
            border-color: #00d9ff;
        }}
        .stats {{
            margin-top: 20px;
            padding: 15px;
            background-color: #16213e;
            border-radius: 8px;
        }}
        .stats h3 {{
            margin-top: 0;
            color: #00d9ff;
        }}
        .stat-row {{
            display: flex;
            justify-content: space-between;
            padding: 5px 0;
            border-bottom: 1px solid #333;
        }}
    </style>
</head>
<body>
    <h1>🔬 {title}</h1>
    
    <div class="visualization">
        {content}
    </div>
    
    <div class="legend">
        <h3>Entropy Color Scale</h3>
        <div class="color-scale">
            <div style="background: rgb(0,100,255);"></div>
            <div style="background: rgb(64,100,191);"></div>
            <div style="background: rgb(128,100,128);"></div>
            <div style="background: rgb(191,100,64);"></div>
            <div style="background: rgb(255,100,0);"></div>
        </div>
        <div class="scale-labels">
            <span>Low Entropy (0.0)</span>
            <span>High Entropy ({max_entropy:.2f})</span>
        </div>
        <p><span class="boundary">|</span> = Token boundary</p>
    </div>
    
    {token_summary}
    
    <div class="stats">
        <h3>Statistics</h3>
        <div class="stat-row">
            <span>Total Characters:</span>
            <span>{len(text)}</span>
        </div>
        <div class="stat-row">
            <span>Token Boundaries:</span>
            <span>{len(token_boundaries)}</span>
        </div>
        <div class="stat-row">
            <span>Avg Entropy:</span>
            <span>{sum(entropies) / max(len(entropies), 1):.3f}</span>
        </div>
        <div class="stat-row">
            <span>Max Entropy:</span>
            <span>{max_entropy:.3f}</span>
        </div>
    </div>
    
    <footer style="margin-top: 30px; color: #666; text-align: center;">
        Generated by QuantumEvoTokenizer | Strategickhaos DAO LLC
    </footer>
</body>
</html>"""
    
    return html_template


def generate_token_summary(
    text: str,
    boundaries: List[int],
    vocab: Set[bytes]
) -> str:
    """Generate HTML summary of tokens."""
    # Extract tokens based on boundaries
    sorted_boundaries = sorted(set([0] + boundaries + [len(text)]))
    tokens = []
    
    for i in range(len(sorted_boundaries) - 1):
        start = sorted_boundaries[i]
        end = sorted_boundaries[i + 1]
        if start < end:
            token_text = text[start:end]
            token_bytes = token_text.encode("utf-8", errors="replace")
            in_vocab = token_bytes in vocab
            tokens.append({
                "text": token_text,
                "bytes": token_bytes.hex(),
                "length": len(token_bytes),
                "in_vocab": in_vocab
            })
    
    token_spans = []
    for t in tokens:
        status = "✓" if t["in_vocab"] else "✗"
        escaped = html.escape(t["text"]).replace(" ", "&nbsp;")
        token_spans.append(
            f'<span class="token" title="hex: {t["bytes"]}, len: {t["length"]}">'
            f'{escaped} <small>({status})</small></span>'
        )
    
    return f"""
    <div class="summary">
        <h3>Tokens ({len(tokens)})</h3>
        <div>{"".join(token_spans)}</div>
    </div>
    """


def save_visualization(
    text: str,
    token_boundaries: List[int],
    output_path: str,
    vocab: Optional[Set[bytes]] = None,
    title: str = "QET Token Visualization"
) -> str:
    """
    Generate and save HTML visualization.
    
    Returns:
        Path to saved file
    """
    html_content = generate_html_visualization(text, token_boundaries, vocab, title)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return output_path


def visualize_tokenizer_output(
    tokenizer,
    text: str,
    output_path: str
) -> str:
    """
    Convenience function to visualize tokenizer output.
    
    Args:
        tokenizer: QuantumEvoTokenizer instance
        text: Text to tokenize and visualize
        output_path: Where to save HTML
    
    Returns:
        Path to saved file
    """
    # Get tokens and find boundaries
    text_bytes = text.encode("utf-8")
    token_ids = tokenizer.encode(text_bytes)
    
    # Reconstruct boundaries from tokens
    boundaries = []
    position = 0
    
    if tokenizer._encoder:
        id_to_token = {v: k for k, v in tokenizer._encoder.mergeable_ranks.items()}
        
        for token_id in token_ids:
            if token_id in id_to_token:
                token = id_to_token[token_id]
                position += len(token)
                boundaries.append(position)
    
    return save_visualization(
        text,
        boundaries,
        output_path,
        vocab=tokenizer.vocab,
        title="QET Token Visualization"
    )


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Visualize token boundaries")
    parser.add_argument("--text", type=str, required=True, help="Text to visualize")
    parser.add_argument("--boundaries", type=str, help="Comma-separated boundary positions")
    parser.add_argument("--output", type=str, default="token_viz.html", help="Output HTML file")
    
    args = parser.parse_args()
    
    boundaries = []
    if args.boundaries:
        boundaries = [int(x) for x in args.boundaries.split(",")]
    
    output = save_visualization(args.text, boundaries, args.output)
    print(f"Visualization saved to: {output}")
