#!/usr/bin/env python3
"""
Sovereignty Repository Verification - Full Refinery-Style Check

Scans all repositories in a specified directory for:
- LICENSE file presence and validity
- artifacts/ folder or external_discussions.md
- Git commit history for license additions
- Generates comprehensive audit report
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg: str):
    print(f"{Colors.GREEN}✓ {msg}{Colors.RESET}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.RESET}")

def print_error(msg: str):
    print(f"{Colors.RED}✗ {msg}{Colors.RESET}")

def print_info(msg: str):
    print(f"{Colors.CYAN}ℹ {msg}{Colors.RESET}")

# MIT License template
MIT_TEMPLATE = """MIT License

Copyright (c) {year} [Your Name / Sovereign Heir]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

def find_git_repos(root_path: Path, max_depth: int = 3) -> List[Path]:
    """Find all directories containing .git folders."""
    repos = []
    
    def scan_dir(path: Path, depth: int = 0):
        if depth > max_depth:
            return
        
        try:
            for item in path.iterdir():
                if not item.is_dir():
                    continue
                
                # Check if this directory is a git repo
                if (item / '.git').exists():
                    repos.append(item)
                else:
                    # Recurse into subdirectories
                    scan_dir(item, depth + 1)
        except PermissionError:
            # Skip directories we can't access
            pass
    
    scan_dir(root_path)
    return repos

def detect_license_type(content: str) -> str:
    """Detect license type from file content."""
    content_lower = content.lower()
    
    if 'mit license' in content_lower:
        return 'MIT'
    elif 'apache license' in content_lower:
        return 'Apache-2.0'
    elif 'gnu general public license' in content_lower or 'gpl' in content_lower:
        if 'version 3' in content_lower or 'v3' in content_lower:
            return 'GPL-3.0'
        elif 'version 2' in content_lower or 'v2' in content_lower:
            return 'GPL-2.0'
        else:
            return 'GPL'
    elif 'bsd' in content_lower:
        return 'BSD'
    elif 'mozilla public license' in content_lower:
        return 'MPL'
    else:
        return 'Custom/Other'

def get_license_commit_date(repo_path: Path) -> Optional[str]:
    """Get the commit date when LICENSE was first added."""
    try:
        result = subprocess.run(
            ['git', 'log', '--follow', '--format=%ai', '--', 'LICENSE'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().split('\n')
            return lines[-1] if lines else None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    return None

def scan_repository(repo_path: Path, auto_fix: bool = False) -> Dict:
    """Scan a single repository for sovereignty compliance."""
    repo_name = repo_path.name
    license_path = repo_path / 'LICENSE'
    artifacts_path = repo_path / 'artifacts'
    ext_discussions_path = repo_path / 'external_discussions.md'
    
    print(f"{Colors.WHITE}Scanning: {repo_name}{Colors.RESET}")
    
    result = {
        'name': repo_name,
        'path': str(repo_path),
        'has_license': False,
        'license_type': None,
        'license_commit_date': None,
        'has_artifacts': False,
        'artifact_location': None,
        'status': 'unknown',
        'issues': []
    }
    
    # Check for LICENSE file
    if license_path.exists():
        result['has_license'] = True
        
        # Detect license type
        try:
            with open(license_path, 'r', encoding='utf-8') as f:
                content = f.read()
                result['license_type'] = detect_license_type(content)
        except (IOError, UnicodeDecodeError) as e:
            result['license_type'] = 'Error reading'
            result['issues'].append(f'Failed to read LICENSE: {type(e).__name__}')
        
        # Get commit date
        result['license_commit_date'] = get_license_commit_date(repo_path)
        
        print_success(f"  LICENSE found: {result['license_type']}")
    else:
        result['issues'].append('Missing LICENSE file')
        print_warning("  LICENSE file not found")
        
        # Auto-fix if requested
        if auto_fix:
            print_info("  Adding MIT LICENSE...")
            # Check if running in interactive terminal
            if sys.stdin.isatty():
                response = input(f"  Add MIT license to {repo_name}? (y/N): ")
                if response.lower() == 'y':
                    try:
                        with open(license_path, 'w', encoding='utf-8') as f:
                            f.write(MIT_TEMPLATE.format(year=datetime.now().year))
                        print_success("  LICENSE created")
                        result['has_license'] = True
                        result['license_type'] = 'MIT'
                        result['issues'].remove('Missing LICENSE file')
                    except (IOError, ValueError) as e:
                        print_error(f"  Failed to create LICENSE: {e}")
            else:
                print_warning("  Non-interactive mode, skipping confirmation")
    
    # Check for artifacts
    if artifacts_path.exists() and artifacts_path.is_dir():
        result['has_artifacts'] = True
        result['artifact_location'] = 'artifacts/'
        artifact_count = sum(1 for _ in artifacts_path.glob('*'))
        print_success(f"  artifacts/ folder found ({artifact_count} files)")
    elif ext_discussions_path.exists():
        result['has_artifacts'] = True
        result['artifact_location'] = 'external_discussions.md'
        print_success("  external_discussions.md found")
    else:
        result['issues'].append('No artifact archive found')
        print_warning("  No artifacts/ folder or external_discussions.md")
    
    # Determine overall status
    if result['has_license'] and result['has_artifacts']:
        result['status'] = 'fully_sovereign'
        print_success("  Status: Fully Sovereign ✓")
    elif result['has_license']:
        result['status'] = 'needs_artifacts'
        print_warning("  Status: Licensed (needs artifacts)")
    else:
        result['status'] = 'needs_attention'
        print_error("  Status: Needs Attention")
    
    print()
    return result

def generate_reports(results: List[Dict], stats: Dict, output_path: Path, repo_root: Path):
    """Generate JSON and Markdown reports."""
    # JSON report
    report = {
        'timestamp': datetime.now().isoformat(),
        'scan_root': str(repo_root),
        'statistics': stats,
        'repositories': results
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print_success(f"Report generated: {output_path}")
    
    # Markdown report
    md_path = output_path.with_suffix('.md')
    
    total = stats['total']
    licensed_pct = round((stats['licensed'] / total) * 100, 1) if total > 0 else 0
    artifacts_pct = round((stats['has_artifacts'] / total) * 100, 1) if total > 0 else 0
    sovereign_pct = round((stats['fully_sovereign'] / total) * 100, 1) if total > 0 else 0
    attention_pct = round((stats['needs_attention'] / total) * 100, 1) if total > 0 else 0
    
    md_content = f"""# Sovereignty Verification Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Scan Root: {repo_root}

## Summary Statistics

| Metric | Count | Percentage |
|--------|-------|------------|
| Total Repositories | {stats['total']} | 100% |
| Licensed | {stats['licensed']} | {licensed_pct}% |
| Has Artifacts | {stats['has_artifacts']} | {artifacts_pct}% |
| Fully Sovereign | {stats['fully_sovereign']} | {sovereign_pct}% |
| Needs Attention | {stats['needs_attention']} | {attention_pct}% |

## Repository Details

"""
    
    for result in results:
        license_str = result['license_type'] if result['has_license'] else '❌ None'
        artifacts_str = f"✓ {result['artifact_location']}" if result['has_artifacts'] else '❌ None'
        issues_str = f"\n- **Issues**: {', '.join(result['issues'])}" if result['issues'] else ''
        
        md_content += f"""
### {result['name']}

- **Status**: {result['status']}
- **License**: {license_str}
- **Artifacts**: {artifacts_str}
- **Path**: `{result['path']}`{issues_str}

"""
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print_success(f"Markdown report generated: {md_path}")

def main():
    parser = argparse.ArgumentParser(
        description='Sovereignty Repository Verification - Full Refinery-Style Check'
    )
    parser.add_argument(
        '--repo-root',
        type=Path,
        default=Path.home() / 'repos',
        help='Root directory containing repositories to scan'
    )
    parser.add_argument(
        '--auto-fix',
        action='store_true',
        help='Automatically add missing LICENSE files (with confirmation)'
    )
    parser.add_argument(
        '--generate-report',
        action='store_true',
        help='Generate detailed report in JSON/Markdown format'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('./sovereignty_verification_report.json'),
        help='Output path for the report'
    )
    
    args = parser.parse_args()
    
    # Check if repo root exists
    if not args.repo_root.exists():
        print_error(f"Repository root directory not found: {args.repo_root}")
        print_info("Please specify a valid directory with --repo-root parameter")
        sys.exit(1)
    
    print_info(f"Scanning repositories in: {args.repo_root}")
    print_info("━" * 40)
    
    # Find all git repositories
    repos = find_git_repos(args.repo_root)
    
    if not repos:
        print_warning(f"No git repositories found in {args.repo_root}")
        sys.exit(0)
    
    print_info(f"Found {len(repos)} repositories to scan")
    print()
    
    # Statistics
    stats = {
        'total': len(repos),
        'licensed': 0,
        'has_artifacts': 0,
        'fully_sovereign': 0,
        'needs_attention': 0
    }
    
    # Scan all repositories
    results = []
    for repo in repos:
        result = scan_repository(repo, args.auto_fix)
        results.append(result)
        
        if result['has_license']:
            stats['licensed'] += 1
        if result['has_artifacts']:
            stats['has_artifacts'] += 1
        if result['status'] == 'fully_sovereign':
            stats['fully_sovereign'] += 1
        if result['status'] in ('needs_attention', 'needs_artifacts'):
            stats['needs_attention'] += 1
    
    # Print summary
    print(f"{Colors.CYAN}{'━' * 40}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}SOVEREIGNTY VERIFICATION SUMMARY{Colors.RESET}")
    print(f"{Colors.CYAN}{'━' * 40}{Colors.RESET}")
    print()
    print(f"{Colors.WHITE}Total Repositories:    {stats['total']}{Colors.RESET}")
    
    licensed_color = Colors.GREEN if stats['licensed'] == stats['total'] else Colors.YELLOW
    print(f"{licensed_color}Licensed:              {stats['licensed']}/{stats['total']}{Colors.RESET}")
    
    artifacts_color = Colors.GREEN if stats['has_artifacts'] == stats['total'] else Colors.YELLOW
    print(f"{artifacts_color}Has Artifacts:         {stats['has_artifacts']}/{stats['total']}{Colors.RESET}")
    
    sovereign_color = Colors.GREEN if stats['fully_sovereign'] == stats['total'] else Colors.YELLOW
    print(f"{sovereign_color}Fully Sovereign:       {stats['fully_sovereign']}/{stats['total']}{Colors.RESET}")
    
    attention_color = Colors.GREEN if stats['needs_attention'] == 0 else Colors.RED
    print(f"{attention_color}Needs Attention:       {stats['needs_attention']}{Colors.RESET}")
    print()
    
    # Generate report if requested
    if args.generate_report:
        generate_reports(results, stats, args.output, args.repo_root)
    
    print()
    print(f"{Colors.GREEN}Verification complete! 🎉{Colors.RESET}")
    
    # Exit with appropriate code
    sys.exit(1 if stats['needs_attention'] > 0 else 0)

if __name__ == '__main__':
    main()
