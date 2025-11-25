#!/usr/bin/env python3
"""
DOM Score Visualization Generator
=================================
Generates IEEE-ready figures for sovereignty benchmark results:
- Radar chart comparing DOM Score components
- Latency curves across context lengths

Strategickhaos DAO LLC - Sovereign Infrastructure Benchmarks
Generated: 2025-11-25

Usage:
    python generate_benchmark_figures.py --input results.ndjson --output-dir figs/
    python generate_benchmark_figures.py --demo  # Generate with demo data

Requirements:
    pip install matplotlib numpy

Output:
    - dom_radar_2025.pdf: Composite performance radar chart
    - latency_curves_2025.pdf: End-to-end latency comparison
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend for server environments
    import matplotlib.pyplot as plt
    import numpy as np
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Warning: matplotlib not available. Install with: pip install matplotlib numpy",
          file=sys.stderr)


# Reference benchmark data from IEEE methodology
DEMO_DATA = {
    "models": {
        "Qwen2.5:14b-q6_K": {
            "type": "local",
            "latency_s": 41.2,
            "ci_low": 40.8,
            "ci_high": 41.7,
            "tokens_per_second": 298,
            "dom_score": {
                "speed": 60,      # Normalized: 298/500 * 100
                "freedom": 100,   # No content filtering
                "sovereignty": 100, # Complete data control
                "cost": 100,      # Zero recurring cost
                "total": 100      # Weighted total
            }
        },
        "Gemma3:1b": {
            "type": "local",
            "latency_s": 8.4,
            "ci_low": 8.1,
            "ci_high": 8.8,
            "tokens_per_second": 812,
            "dom_score": {
                "speed": 95,
                "freedom": 100,
                "sovereignty": 100,
                "cost": 100,
                "total": 95
            }
        },
        "GPT-5.1": {
            "type": "cloud",
            "latency_s": 38.6,
            "ci_low": 36.2,
            "ci_high": 41.0,
            "tokens_per_second": 3789,
            "dom_score": {
                "speed": 100,
                "freedom": 50,
                "sovereignty": 0,
                "cost": 20,
                "total": 68
            }
        },
        "Claude Opus 4": {
            "type": "cloud",
            "latency_s": 45.2,
            "ci_low": 42.8,
            "ci_high": 47.6,
            "tokens_per_second": 2156,
            "dom_score": {
                "speed": 75,
                "freedom": 40,
                "sovereignty": 0,
                "cost": 20,
                "total": 59
            }
        },
        "Grok 4": {
            "type": "cloud",
            "latency_s": 36.1,
            "ci_low": 34.0,
            "ci_high": 38.2,
            "tokens_per_second": 4102,
            "dom_score": {
                "speed": 100,
                "freedom": 60,
                "sovereignty": 0,
                "cost": 15,
                "total": 62
            }
        }
    },
    "latency_curves": {
        "context_lengths": [512, 1024, 2048, 4096, 8192, 16384],
        "Qwen2.5:14b-q6_K": [5.2, 10.4, 20.8, 41.2, 82.4, 164.8],
        "Gemma3:1b": [1.1, 2.1, 4.2, 8.4, 16.8, 33.6],
        "GPT-5.1": [4.8, 9.6, 19.3, 38.6, 77.2, 154.4],
        "Claude Opus 4": [5.6, 11.3, 22.6, 45.2, 90.4, 180.8],
        "Grok 4": [4.5, 9.0, 18.0, 36.1, 72.2, 144.4]
    }
}


def create_radar_chart(data: dict, output_path: str):
    """Create DOM Score radar chart comparing models."""
    if not HAS_MATPLOTLIB:
        print("Skipping radar chart: matplotlib not available", file=sys.stderr)
        return False

    models = data["models"]

    # Categories for radar chart
    categories = ["Speed", "Freedom", "Sovereignty", "Cost"]
    num_categories = len(categories)

    # Create angles for radar chart
    angles = np.linspace(0, 2 * np.pi, num_categories, endpoint=False).tolist()
    angles += angles[:1]  # Close the polygon

    # Set up the figure
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

    # Color schemes
    local_colors = ['#2E7D32', '#43A047']  # Green shades for local
    cloud_colors = ['#1565C0', '#1976D2', '#42A5F5']  # Blue shades for cloud

    local_idx = 0
    cloud_idx = 0

    for model_name, model_data in models.items():
        dom = model_data["dom_score"]
        values = [dom["speed"], dom["freedom"], dom["sovereignty"], dom["cost"]]
        values += values[:1]  # Close the polygon

        # Select color based on model type
        if model_data["type"] == "local":
            color = local_colors[local_idx % len(local_colors)]
            linestyle = '-'
            local_idx += 1
        else:
            color = cloud_colors[cloud_idx % len(cloud_colors)]
            linestyle = '--'
            cloud_idx += 1

        # Plot the polygon
        ax.plot(angles, values, marker='o', linewidth=2, label=model_name,
                color=color, linestyle=linestyle, markersize=6)
        ax.fill(angles, values, alpha=0.15, color=color)

    # Customize the chart
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12, fontweight='bold')

    # Set y-axis limits
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=9)

    # Add title and legend
    ax.set_title('DOM Score Comparison: Local Sovereign vs Cloud Inference',
                 fontsize=14, fontweight='bold', pad=20)

    # Position legend outside the chart
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=10)

    # Add grid
    ax.grid(True, linestyle=':', alpha=0.6)

    # Save figure
    plt.tight_layout()
    plt.savefig(output_path, format='pdf', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Radar chart saved to: {output_path}", file=sys.stderr)
    return True


def create_latency_curves(data: dict, output_path: str):
    """Create latency curves across context lengths."""
    if not HAS_MATPLOTLIB:
        print("Skipping latency curves: matplotlib not available", file=sys.stderr)
        return False

    curves = data["latency_curves"]
    context_lengths = curves["context_lengths"]
    models = data["models"]

    # Set up the figure
    fig, ax = plt.subplots(figsize=(12, 7))

    # Color and style schemes
    local_styles = {
        "color": ['#2E7D32', '#43A047'],
        "marker": ['s', '^'],
        "linestyle": ['-', '-']
    }
    cloud_styles = {
        "color": ['#1565C0', '#1976D2', '#42A5F5'],
        "marker": ['o', 'D', 'v'],
        "linestyle": ['--', '--', '--']
    }

    local_idx = 0
    cloud_idx = 0

    for model_name in curves.keys():
        if model_name == "context_lengths":
            continue

        latencies = curves[model_name]
        model_type = models.get(model_name, {}).get("type", "cloud")

        if model_type == "local":
            color = local_styles["color"][local_idx % len(local_styles["color"])]
            marker = local_styles["marker"][local_idx % len(local_styles["marker"])]
            linestyle = local_styles["linestyle"][local_idx % len(local_styles["linestyle"])]
            local_idx += 1
        else:
            color = cloud_styles["color"][cloud_idx % len(cloud_styles["color"])]
            marker = cloud_styles["marker"][cloud_idx % len(cloud_styles["marker"])]
            linestyle = cloud_styles["linestyle"][cloud_idx % len(cloud_styles["linestyle"])]
            cloud_idx += 1

        ax.plot(context_lengths, latencies, marker=marker, linestyle=linestyle,
                linewidth=2, markersize=8, label=model_name, color=color)

    # Customize axes
    ax.set_xlabel('Context Length (tokens)', fontsize=12, fontweight='bold')
    ax.set_ylabel('End-to-End Latency (seconds)', fontsize=12, fontweight='bold')
    ax.set_title('Inference Latency vs Context Length: Local vs Cloud',
                 fontsize=14, fontweight='bold')

    # Use log scale for x-axis
    ax.set_xscale('log', base=2)
    ax.set_xticks(context_lengths)
    ax.set_xticklabels([str(c) for c in context_lengths])

    # Add grid
    ax.grid(True, linestyle=':', alpha=0.6)

    # Legend
    ax.legend(loc='upper left', fontsize=10, framealpha=0.9)

    # Add annotation for key insight
    ax.annotate('Local models: predictable scaling\nCloud models: network-dependent',
                xy=(0.98, 0.02), xycoords='axes fraction',
                fontsize=9, ha='right', va='bottom',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # Save figure
    plt.tight_layout()
    plt.savefig(output_path, format='pdf', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Latency curves saved to: {output_path}", file=sys.stderr)
    return True


def create_benchmark_table(data: dict, output_path: str):
    """Create a summary table figure."""
    if not HAS_MATPLOTLIB:
        print("Skipping table: matplotlib not available", file=sys.stderr)
        return False

    models = data["models"]

    # Prepare table data
    headers = ['Model', 'Type', 'Latency (s)', 'Tokens/s', 'DOM Score', 'Cost']
    rows = []

    for model_name, model_data in models.items():
        cost_symbol = '$0' if model_data['type'] == 'local' else '$$$'
        rows.append([
            model_name,
            model_data['type'].title(),
            f"{model_data['latency_s']:.1f}",
            f"{model_data['tokens_per_second']:,}",
            f"{model_data['dom_score']['total']}/100",
            cost_symbol
        ])

    # Sort by DOM score
    rows.sort(key=lambda x: int(x[4].split('/')[0]), reverse=True)

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis('off')

    # Create table
    table = ax.table(
        cellText=rows,
        colLabels=headers,
        cellLoc='center',
        loc='center',
        colWidths=[0.22, 0.1, 0.14, 0.14, 0.14, 0.1]
    )

    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.8)

    # Header styling
    for i, header in enumerate(headers):
        cell = table[(0, i)]
        cell.set_facecolor('#2E7D32')
        cell.set_text_props(color='white', fontweight='bold')

    # Row styling based on model type
    for row_idx, row in enumerate(rows, 1):
        model_type = row[1].lower()
        for col_idx in range(len(headers)):
            cell = table[(row_idx, col_idx)]
            if model_type == 'local':
                cell.set_facecolor('#E8F5E9')  # Light green
            else:
                cell.set_facecolor('#E3F2FD')  # Light blue

    ax.set_title('Benchmark Results Summary: Local vs Cloud Inference',
                 fontsize=14, fontweight='bold', y=0.95)

    # Save figure
    plt.tight_layout()
    plt.savefig(output_path, format='pdf', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Summary table saved to: {output_path}", file=sys.stderr)
    return True


def load_ndjson_results(filepath: str) -> dict:
    """Load benchmark results from NDJSON file."""
    data = {
        "models": {},
        "latency_curves": {"context_lengths": [512, 1024, 2048, 4096, 8192, 16384]}
    }

    with open(filepath, 'r') as f:
        for line in f:
            record = json.loads(line.strip())
            record_type = record.get("record_type")

            if record_type == "summary":
                model_name = record.get("model")
                summary = record.get("data", {})

                data["models"][model_name] = {
                    "type": summary.get("model", {}).get("type", "unknown"),
                    "latency_s": summary.get("median_latency_s", 0),
                    "ci_low": summary.get("ci_95_low", 0),
                    "ci_high": summary.get("ci_95_high", 0),
                    "tokens_per_second": summary.get("median_tokens_per_second", 0),
                    "dom_score": {
                        "speed": summary.get("dom_score", {}).get("speed_score", 0),
                        "freedom": summary.get("dom_score", {}).get("freedom_score", 0),
                        "sovereignty": summary.get("dom_score", {}).get("sovereignty_score", 0),
                        "cost": summary.get("dom_score", {}).get("cost_score", 0),
                        "total": summary.get("dom_score", {}).get("total_score", 0),
                    }
                }

    return data


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate IEEE-ready benchmark visualization figures",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Generate with demo data
    python generate_benchmark_figures.py --demo --output-dir papers/figs/

    # Generate from benchmark results
    python generate_benchmark_figures.py --input results.ndjson --output-dir figs/

Output Files:
    - dom_radar_2025.pdf: Radar chart comparing DOM Score components
    - latency_curves_2025.pdf: Latency vs context length curves
    - benchmark_table_2025.pdf: Summary table (optional)
        """
    )

    parser.add_argument(
        "--input", "-i",
        help="Input NDJSON file with benchmark results"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="figs",
        help="Output directory for figures (default: figs)"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Generate figures using demo data from IEEE methodology"
    )
    parser.add_argument(
        "--format",
        choices=["pdf", "png", "svg"],
        default="pdf",
        help="Output format (default: pdf)"
    )
    parser.add_argument(
        "--include-table",
        action="store_true",
        help="Generate summary table figure"
    )

    args = parser.parse_args()

    if not HAS_MATPLOTLIB:
        print("Error: matplotlib is required. Install with: pip install matplotlib numpy",
              file=sys.stderr)
        sys.exit(1)

    # Load data
    if args.demo:
        data = DEMO_DATA
        print("Using demo data from IEEE methodology", file=sys.stderr)
    elif args.input:
        data = load_ndjson_results(args.input)
        print(f"Loaded data from: {args.input}", file=sys.stderr)
    else:
        print("Error: Specify --input or --demo", file=sys.stderr)
        sys.exit(1)

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate figures
    ext = args.format
    success = True

    # Radar chart
    radar_path = output_dir / f"dom_radar_2025.{ext}"
    success &= create_radar_chart(data, str(radar_path))

    # Latency curves
    latency_path = output_dir / f"latency_curves_2025.{ext}"
    success &= create_latency_curves(data, str(latency_path))

    # Optional: Summary table
    if args.include_table:
        table_path = output_dir / f"benchmark_table_2025.{ext}"
        success &= create_benchmark_table(data, str(table_path))

    if success:
        print(f"\n✅ All figures generated successfully in: {output_dir}", file=sys.stderr)
    else:
        print(f"\n⚠️ Some figures could not be generated", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
