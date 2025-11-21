#!/usr/bin/env python3
"""
Sovereignty Architecture Verification Engine

Verifies and auto-fixes LICENSE and artifacts across all repositories.

This Refinery-style script scans all repositories and ensures:
1. Each repo has a LICENSE file (auto-generates MIT if missing)
2. Each repo has an artifacts/ directory for external AI discussions
3. Generates a sovereignty report showing compliance status
4. Can optionally append to verification_ledger.jsonl for audit trail

Full sovereignty: You own this script, you own the repos, one rm -rf resets everything.
No cloud dependencies, zero internet required after first run.
"""

import os
import sys
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import json
import hashlib


MIT_LICENSE_TEMPLATE = """MIT License

Copyright (c) {year} {copyright_holder}

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

APACHE2_LICENSE_TEMPLATE = """Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

Copyright {year} {copyright_holder}

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

ARTIFACTS_README = """# External AI Artifacts

This directory contains archived external AI discussion links and artifacts used in the development and evolution of this repository.

## Purpose

- Audit trail for design decisions
- Agent training references
- Meta-evolution documentation
- Immutable proof of external contributions

## Adding Artifacts

To add a new artifact:

1. Create a markdown file with date: `artifact_name_YYYY-MM-DD.md`
2. Include source URL and JSON metadata block
3. Add to git: `git add artifacts/ && git commit -m "Archive artifact"`

## Verification

All artifacts are under version control and can be verified with:

```bash
sha256sum artifacts/*.md
```

## Sovereignty Guarantee

- ✅ Fully local and under your control
- ✅ No cloud dependencies
- ✅ Can be deleted or modified at any time
- ✅ Immutable once committed to git
"""


class Colors:
    """ANSI color codes for terminal output"""
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_colored(text: str, color: str = Colors.WHITE):
    """Print colored text to terminal"""
    print(f"{color}{text}{Colors.RESET}")


def get_license_template(license_type: str, copyright_holder: str) -> Optional[str]:
    """Get license template by type"""
    year = datetime.now().year
    
    templates = {
        "MIT": MIT_LICENSE_TEMPLATE,
        "Apache-2.0": APACHE2_LICENSE_TEMPLATE,
    }
    
    template = templates.get(license_type)
    if template:
        return template.format(year=year, copyright_holder=copyright_holder)
    
    return None


def is_git_repository(path: Path) -> bool:
    """Check if path is a git repository"""
    return (path / ".git").exists()


def find_git_repositories(root_path: Path) -> List[Path]:
    """Find all git repositories under root path"""
    repos = []
    
    # Check if root itself is a git repo
    if is_git_repository(root_path):
        repos.append(root_path)
    
    # Search for .git directories
    try:
        for git_dir in root_path.rglob(".git"):
            if git_dir.is_dir():
                repo_path = git_dir.parent
                if repo_path not in repos:
                    repos.append(repo_path)
    except PermissionError:
        pass
    
    return repos


def add_license_file(repo_path: Path, license_type: str, copyright_holder: str) -> bool:
    """Add LICENSE file to repository"""
    license_path = repo_path / "LICENSE"
    license_content = get_license_template(license_type, copyright_holder)
    
    if not license_content:
        print_colored(f"  ⚠️  Unknown license type: {license_type}", Colors.YELLOW)
        return False
    
    try:
        license_path.write_text(license_content, encoding='utf-8')
        print_colored(f"  ✅ Created LICENSE ({license_type}) in: {repo_path.name}", Colors.GREEN)
        
        # Commit to git if possible
        try:
            subprocess.run(
                ["git", "add", "LICENSE"],
                cwd=repo_path,
                capture_output=True,
                check=False
            )
            subprocess.run(
                ["git", "commit", "-m", f"Add {license_type} license — full sovereign control retained"],
                cwd=repo_path,
                capture_output=True,
                check=False
            )
        except Exception:
            pass
        
        return True
    except Exception as e:
        print_colored(f"  ❌ Failed to create LICENSE: {e}", Colors.RED)
        return False


def add_artifacts_directory(repo_path: Path) -> bool:
    """Add artifacts/ directory to repository"""
    artifacts_path = repo_path / "artifacts"
    
    if artifacts_path.exists():
        return False
    
    try:
        artifacts_path.mkdir(exist_ok=True)
        
        # Create README in artifacts directory
        readme_path = artifacts_path / "README.md"
        readme_path.write_text(ARTIFACTS_README, encoding='utf-8')
        
        print_colored(f"  ✅ Created artifacts/ directory with README in: {repo_path.name}", Colors.GREEN)
        
        # Commit to git if possible
        try:
            subprocess.run(
                ["git", "add", "artifacts/"],
                cwd=repo_path,
                capture_output=True,
                check=False
            )
            subprocess.run(
                ["git", "commit", "-m", "Add artifacts directory for external AI discussion archiving"],
                cwd=repo_path,
                capture_output=True,
                check=False
            )
        except Exception:
            pass
        
        return True
    except Exception as e:
        print_colored(f"  ❌ Failed to create artifacts/: {e}", Colors.RED)
        return False


def generate_report(results: List[Dict], scan_path: str, auto_fix: bool, output_file: str):
    """Generate sovereignty verification report"""
    total = len(results)
    with_license = sum(1 for r in results if r['has_license'])
    with_artifacts = sum(1 for r in results if r['has_artifacts'])
    fixed = sum(1 for r in results if r['fixed'])
    
    report_lines = [
        "Sovereignty Architecture Verification Report",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Scan Path: {scan_path}",
        f"Auto-fix: {auto_fix}",
        "",
        "Summary:",
        "=" * 60,
        f"Total Repositories Scanned: {total}",
        f"Repositories with LICENSE: {with_license} ({round(with_license/total*100, 1) if total > 0 else 0}%)",
        f"Repositories with artifacts/: {with_artifacts} ({round(with_artifacts/total*100, 1) if total > 0 else 0}%)",
        f"Repositories Fixed: {fixed}",
        "",
        "Details:",
        "=" * 60,
    ]
    
    for result in results:
        report_lines.extend([
            "",
            result['repository'],
            f"  Path: {result['path']}",
            f"  LICENSE: {result['has_license']}",
            f"  artifacts/: {result['has_artifacts']}",
        ])
        if result['fixed']:
            report_lines.append("  Status: FIXED ✅")
    
    report = "\n".join(report_lines)
    
    Path(output_file).write_text(report, encoding='utf-8')
    print_colored(f"\n📄 Report saved to: {output_file}", Colors.CYAN)
    
    return {
        'total': total,
        'with_license': with_license,
        'with_artifacts': with_artifacts,
        'fixed': fixed
    }


def main():
    parser = argparse.ArgumentParser(
        description='Verify and auto-fix LICENSE and artifacts across repositories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --repos-path ~/repos --auto-fix
  %(prog)s --auto-fix --license-type Apache-2.0
  %(prog)s --repos-path . --output-report my_report.txt
        """
    )
    
    parser.add_argument(
        '--repos-path',
        default='.',
        help='Root directory containing repositories to scan (default: current directory)'
    )
    parser.add_argument(
        '--auto-fix',
        action='store_true',
        help='Automatically create missing LICENSE files and artifacts directories'
    )
    parser.add_argument(
        '--license-type',
        choices=['MIT', 'Apache-2.0'],
        default='MIT',
        help='License type to use when auto-generating (default: MIT)'
    )
    parser.add_argument(
        '--copyright-holder',
        default='Sovereign Heir',
        help='Copyright holder name for auto-generated licenses (default: "Sovereign Heir")'
    )
    parser.add_argument(
        '--output-report',
        default='sovereignty_report.txt',
        help='Path to save the sovereignty report (default: sovereignty_report.txt)'
    )
    parser.add_argument(
        '--append-ledger',
        action='store_true',
        help='Append results to verification_ledger.jsonl'
    )
    
    args = parser.parse_args()
    
    # Print header
    print()
    print_colored("🔍 Sovereignty Architecture Verification Engine", Colors.CYAN + Colors.BOLD)
    print_colored("=" * 60, Colors.CYAN)
    print_colored(f"Scanning: {args.repos_path}", Colors.YELLOW)
    print_colored(f"Auto-fix: {args.auto_fix}", Colors.YELLOW)
    print_colored("=" * 60, Colors.CYAN)
    print()
    
    # Find repositories
    root_path = Path(args.repos_path).resolve()
    if not root_path.exists():
        print_colored(f"❌ Path not found: {args.repos_path}", Colors.RED)
        return 1
    
    git_repos = find_git_repositories(root_path)
    
    if not git_repos:
        print_colored(f"⚠️  No git repositories found in: {args.repos_path}", Colors.YELLOW)
        return 0
    
    print_colored(f"Found {len(git_repos)} git repositories\n", Colors.CYAN)
    
    # Scan repositories
    results = []
    repos_scanned = 0
    repos_with_license = 0
    repos_with_artifacts = 0
    repos_fixed = 0
    
    for repo_path in git_repos:
        repos_scanned += 1
        repo_name = repo_path.name
        
        print_colored(f"📦 Checking: {repo_name}", Colors.WHITE)
        
        has_license = (repo_path / "LICENSE").exists()
        has_artifacts = (repo_path / "artifacts").exists()
        fixed = False
        
        # Check LICENSE
        if has_license:
            print_colored("  ✅ LICENSE exists", Colors.GREEN)
            repos_with_license += 1
        else:
            print_colored("  ❌ LICENSE missing", Colors.RED)
            
            if args.auto_fix:
                if add_license_file(repo_path, args.license_type, args.copyright_holder):
                    has_license = True
                    fixed = True
                    repos_fixed += 1
                    repos_with_license += 1
        
        # Check artifacts/
        if has_artifacts:
            print_colored("  ✅ artifacts/ exists", Colors.GREEN)
            repos_with_artifacts += 1
        else:
            print_colored("  ❌ artifacts/ missing", Colors.RED)
            
            if args.auto_fix:
                if add_artifacts_directory(repo_path):
                    has_artifacts = True
                    fixed = True
                    repos_fixed += 1
                    repos_with_artifacts += 1
        
        results.append({
            'repository': repo_name,
            'path': str(repo_path),
            'has_license': has_license,
            'has_artifacts': has_artifacts,
            'fixed': fixed
        })
        
        print()
    
    # Generate report
    summary = generate_report(results, args.repos_path, args.auto_fix, args.output_report)
    
    # Append to ledger if requested
    if args.append_ledger:
        ledger_entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'type': 'sovereignty_verification',
            'repos_scanned': summary['total'],
            'repos_with_license': summary['with_license'],
            'repos_with_artifacts': summary['with_artifacts'],
            'repos_fixed': summary['fixed'],
            'auto_fix': args.auto_fix,
            'actor': 'sovereignty-verification-system'
        }
        
        try:
            with open('verification_ledger.jsonl', 'a') as f:
                f.write(json.dumps(ledger_entry) + '\n')
            print_colored("📝 Appended to verification_ledger.jsonl", Colors.CYAN)
        except Exception as e:
            print_colored(f"⚠️  Could not append to ledger: {e}", Colors.YELLOW)
    
    # Display summary
    print()
    print_colored("=" * 60, Colors.CYAN)
    print_colored("Summary:", Colors.CYAN + Colors.BOLD)
    print_colored("=" * 60, Colors.CYAN)
    print_colored(f"Total Repositories: {summary['total']}", Colors.WHITE)
    
    license_pct = round(summary['with_license']/summary['total']*100, 1) if summary['total'] > 0 else 0
    license_color = Colors.GREEN if summary['with_license'] == summary['total'] else Colors.YELLOW
    print_colored(f"With LICENSE: {summary['with_license']}/{summary['total']} ({license_pct}%)", license_color)
    
    artifacts_pct = round(summary['with_artifacts']/summary['total']*100, 1) if summary['total'] > 0 else 0
    artifacts_color = Colors.GREEN if summary['with_artifacts'] == summary['total'] else Colors.YELLOW
    print_colored(f"With artifacts/: {summary['with_artifacts']}/{summary['total']} ({artifacts_pct}%)", artifacts_color)
    
    if args.auto_fix and summary['fixed'] > 0:
        print_colored(f"Repositories Fixed: {summary['fixed']}", Colors.GREEN)
    
    print()
    print_colored("✨ Sovereignty verification complete!", Colors.GREEN)
    print_colored("Full control retained. Zero cloud dependencies. 100% auditable.\n", Colors.GRAY)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
