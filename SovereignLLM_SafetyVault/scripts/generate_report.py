#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Safety Audit Report Generator

Parses completed audit checklists and generates:
- Executive summary reports
- Risk matrices
- Remediation roadmaps
- Exportable PDF/HTML formats

Version: 1.0
Author: Strategickhaos Sovereignty Architecture
Part of: Sovereign LLM Safety & Evidence Vault
"""

import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Category definitions with max scores
CATEGORIES = {
    1: {"name": "Input Validation & Sanitization", "max_score": 50},
    2: {"name": "Prompt Injection & Jailbreak Defense", "max_score": 60},
    3: {"name": "Output Filtering & Safety", "max_score": 50},
    4: {"name": "Privacy & Data Protection", "max_score": 60},
    5: {"name": "Model Security & Integrity", "max_score": 50},
    6: {"name": "Access Control & Authentication", "max_score": 40},
    7: {"name": "Monitoring & Observability", "max_score": 50},
    8: {"name": "Rate Limiting & Resource Protection", "max_score": 40},
    9: {"name": "Bias Detection & Mitigation", "max_score": 40},
    10: {"name": "Compliance & Governance", "max_score": 60},
}

TOTAL_MAX_SCORE = 500


def parse_checklist(file_path: Path) -> Dict:
    """Parse completed audit checklist and extract scores."""
    print(f"[i] Parsing checklist: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract client info
    client_name = re.search(r'\*\*Client\*\*:\s*(.+)', content)
    engagement_id = re.search(r'\*\*Engagement ID\*\*:\s*(.+)', content)
    audit_date = re.search(r'\*\*Audit Date\*\*:\s*(.+)', content)
    
    result = {
        'client_name': client_name.group(1).strip() if client_name else 'Unknown',
        'engagement_id': engagement_id.group(1).strip() if engagement_id else 'N/A',
        'audit_date': audit_date.group(1).strip() if audit_date else datetime.now().strftime('%Y-%m-%d'),
        'category_scores': {},
        'total_score': 0,
        'findings': [],
    }
    
    # Extract category scores
    for cat_num, cat_info in CATEGORIES.items():
        # Look for category score pattern
        pattern = rf"## Category {cat_num}:.*?\*\*Category Score\*\*:\s*(\d+)\s*/\s*{cat_info['max_score']}"
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            score = int(match.group(1))
            result['category_scores'][cat_num] = {
                'name': cat_info['name'],
                'score': score,
                'max_score': cat_info['max_score'],
                'percentage': (score / cat_info['max_score'] * 100) if cat_info['max_score'] > 0 else 0,
            }
            result['total_score'] += score
    
    # Calculate overall percentage
    result['total_percentage'] = (result['total_score'] / TOTAL_MAX_SCORE * 100) if TOTAL_MAX_SCORE > 0 else 0
    result['risk_level'] = calculate_risk_level(result['total_percentage'])
    
    return result


def calculate_risk_level(percentage: float) -> str:
    """Calculate risk level based on percentage score."""
    if percentage < 30:
        return "Critical"
    elif percentage < 50:
        return "High"
    elif percentage < 70:
        return "Medium"
    elif percentage < 85:
        return "Low"
    else:
        return "Excellent"


def generate_summary_report(data: Dict, output_path: Path) -> None:
    """Generate executive summary report in Markdown."""
    print(f"[i] Generating summary report: {output_path}")
    
    report = f"""# LLM Safety Audit - Executive Summary

**Client**: {data['client_name']}  
**Engagement ID**: {data['engagement_id']}  
**Audit Date**: {data['audit_date']}  
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Overall Assessment

**Total Score**: {data['total_score']} / {TOTAL_MAX_SCORE} ({data['total_percentage']:.1f}%)  
**Risk Level**: **{data['risk_level']}**

### Risk Interpretation

- **Critical Risk** (< 30%) - Immediate action required
- **High Risk** (30-50%) - Significant gaps, prioritize remediation
- **Medium Risk** (50-70%) - Some gaps, continuous improvement needed
- **Low Risk** (70-85%) - Good security posture, minor improvements
- **Excellent** (> 85%) - Industry-leading security posture

---

## Category Breakdown

| Category | Score | Max | % | Risk Level |
|----------|-------|-----|---|------------|
"""
    
    for cat_num in sorted(data['category_scores'].keys()):
        cat = data['category_scores'][cat_num]
        cat_risk = calculate_risk_level(cat['percentage'])
        report += f"| {cat_num}. {cat['name']} | {cat['score']} | {cat['max_score']} | {cat['percentage']:.1f}% | {cat_risk} |\n"
    
    report += f"\n**TOTAL** | **{data['total_score']}** | **{TOTAL_MAX_SCORE}** | **{data['total_percentage']:.1f}%** | **{data['risk_level']}** |\n"
    
    report += """

---

## Category Analysis

"""
    
    for cat_num in sorted(data['category_scores'].keys()):
        cat = data['category_scores'][cat_num]
        cat_risk = calculate_risk_level(cat['percentage'])
        
        report += f"""
### {cat_num}. {cat['name']}

- **Score**: {cat['score']}/{cat['max_score']} ({cat['percentage']:.1f}%)
- **Risk**: {cat_risk}
- **Status**: {"✓ Strong" if cat['percentage'] >= 70 else "⚠ Needs Improvement" if cat['percentage'] >= 50 else "✗ Critical Gap"}

"""
    
    report += """
---

## Recommendations

### Immediate Actions (Critical & High Priority)

Based on the audit findings, the following areas require immediate attention:

"""
    
    # Identify lowest scoring categories
    sorted_cats = sorted(data['category_scores'].items(), key=lambda x: x[1]['percentage'])
    for cat_num, cat in sorted_cats[:3]:
        if cat['percentage'] < 70:
            report += f"- **{cat['name']}** ({cat['percentage']:.1f}%) - Review and implement missing controls\n"
    
    report += """

### 30-Day Action Plan

Focus on the critical gaps identified above. Prioritize:
1. Input validation and output filtering controls
2. Authentication and access control improvements
3. Monitoring and alerting infrastructure

### 90-Day Roadmap

- Complete remediation of all high-priority findings
- Implement continuous monitoring and testing
- Establish regular audit schedule (quarterly recommended)
- Update documentation and policies

---

## Next Steps

1. **Review Detailed Findings**: See full audit checklist for specific recommendations
2. **Prioritize Remediations**: Focus on lowest-scoring categories first
3. **Implement Controls**: Deploy missing security controls
4. **Re-audit**: Schedule follow-up assessment after remediation
5. **Continuous Improvement**: Establish ongoing security monitoring

---

## About This Report

This executive summary provides a high-level view of the LLM safety audit results. For detailed findings, technical recommendations, and implementation guidance, please refer to the complete audit checklist.

**Audit Framework**: 100-point LLM Safety Techniques  
**Auditor**: Strategickhaos Sovereignty Architecture  
**Methodology**: Comprehensive review across 10 security categories

---

**Confidential & Proprietary**  
This report is confidential to {data['client_name']} and Strategickhaos Sovereignty Architecture.
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"[✓] Summary report generated successfully")


def generate_json_export(data: Dict, output_path: Path) -> None:
    """Export audit data as JSON for further processing."""
    print(f"[i] Generating JSON export: {output_path}")
    
    export_data = {
        'metadata': {
            'client_name': data['client_name'],
            'engagement_id': data['engagement_id'],
            'audit_date': data['audit_date'],
            'generated_at': datetime.now().isoformat(),
            'framework_version': '1.0',
        },
        'summary': {
            'total_score': data['total_score'],
            'max_score': TOTAL_MAX_SCORE,
            'percentage': round(data['total_percentage'], 2),
            'risk_level': data['risk_level'],
        },
        'categories': data['category_scores'],
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"[✓] JSON export generated successfully")


def main():
    parser = argparse.ArgumentParser(
        description='Generate LLM Safety Audit reports from completed checklists'
    )
    parser.add_argument(
        'checklist',
        type=Path,
        help='Path to completed audit checklist (AUDIT_RESULTS_*.md)'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        help='Output directory (defaults to same directory as checklist)'
    )
    parser.add_argument(
        '--format',
        choices=['markdown', 'json', 'all'],
        default='all',
        help='Output format (default: all)'
    )
    
    args = parser.parse_args()
    
    if not args.checklist.exists():
        print(f"[✗] Error: Checklist file not found: {args.checklist}")
        return 1
    
    # Determine output directory
    output_dir = args.output_dir if args.output_dir else args.checklist.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Parse checklist
    try:
        data = parse_checklist(args.checklist)
    except Exception as e:
        print(f"[✗] Error parsing checklist: {e}")
        return 1
    
    # Generate reports
    print("\n=== Generating Reports ===")
    
    base_name = f"SAFETY_REPORT_{data['client_name'].replace(' ', '_')}"
    
    if args.format in ['markdown', 'all']:
        summary_path = output_dir / f"{base_name}_summary.md"
        generate_summary_report(data, summary_path)
    
    if args.format in ['json', 'all']:
        json_path = output_dir / f"{base_name}_data.json"
        generate_json_export(data, json_path)
    
    print("\n=== Report Generation Complete ===")
    print(f"[✓] Client: {data['client_name']}")
    print(f"[✓] Overall Score: {data['total_score']}/{TOTAL_MAX_SCORE} ({data['total_percentage']:.1f}%)")
    print(f"[✓] Risk Level: {data['risk_level']}")
    print(f"[✓] Reports saved to: {output_dir}")
    print("")
    
    return 0


if __name__ == '__main__':
    exit(main())
