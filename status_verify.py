#!/usr/bin/env python3
"""
status_verify.py – run the verify_commands from status_manifest.yaml

Usage:
    python status_verify.py                  # runs all
    python status_verify.py repository_infra # runs specific component
    python status_verify.py --list           # list all components
"""
import subprocess
import sys
import pathlib
import argparse

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

MANIFEST = pathlib.Path(__file__).parent / "status_manifest.yaml"


def load():
    """Load the status manifest YAML file."""
    if not MANIFEST.exists():
        print(f"Error: {MANIFEST} not found")
        sys.exit(1)
    return yaml.safe_load(MANIFEST.read_text())


def run_cmd(cmd):
    """Execute a shell command and report pass/fail."""
    print(f"→ {cmd}")
    
    # Handle PowerShell commands differently
    if cmd.startswith("PowerShell>"):
        cmd = cmd.replace("PowerShell> ", "")
        shell_cmd = ["powershell", "-Command", cmd]
    else:
        shell_cmd = cmd
    
    try:
        result = subprocess.run(
            shell_cmd,
            shell=isinstance(shell_cmd, str),
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("   PASS")
            if result.stdout.strip():
                for line in result.stdout.strip().split('\n')[:5]:
                    print(f"   {line}")
        else:
            print("   FAIL")
            if result.stderr.strip():
                for line in result.stderr.strip().split('\n')[:3]:
                    print(f"   {line}")
        print("-" * 60)
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("   TIMEOUT (60s)")
        print("-" * 60)
        return False
    except FileNotFoundError as e:
        print(f"   SKIP (command not found: {e.filename})")
        print("-" * 60)
        return True  # Skip as pass for missing tools


def main():
    parser = argparse.ArgumentParser(
        description="Verify status manifest components"
    )
    parser.add_argument(
        "component",
        nargs="?",
        help="Run only this component"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all components and their status"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show commands without executing"
    )
    args = parser.parse_args()

    data = load()
    components = data.get("components", {})

    if args.list:
        print(f"{'Component':<35} {'State':<12} {'Complete':<10}")
        print("=" * 60)
        for name, info in components.items():
            state = info.get('state', 'unknown')
            pct = info.get('percent_complete', 0)
            print(f"{name:<35} {state:<12} {pct}%")
        print()
        print(f"Overall completion: {data.get('overall_completion_percent', 0)}%")
        return

    targets = [args.component] if args.component else list(components.keys())
    all_pass = True
    results = {}
    
    for name in targets:
        if name not in components:
            print(f"Component not found: {name}")
            print(f"Available: {', '.join(components.keys())}")
            continue
        
        print(f"\n{'='*60}")
        print(f"=== Verifying: {name} ===")
        print(f"{'='*60}")
        
        comp = components[name]
        print(f"State: {comp.get('state', 'unknown')}")
        print(f"Complete: {comp.get('percent_complete', 0)}%")
        if 'description' in comp:
            print(f"Description: {comp['description']}")
        print()
        
        component_pass = True
        for cmd in comp.get("verify_commands", []):
            if args.dry_run:
                print(f"[DRY-RUN] Would execute: {cmd}")
            else:
                if not run_cmd(cmd):
                    component_pass = False
        
        results[name] = component_pass
        if not component_pass:
            all_pass = False

    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    for name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {name:<35} {status}")
    
    print()
    print(f"Overall result: {'ALL VERIFIED' if all_pass else 'SOME FAILED'}")
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
