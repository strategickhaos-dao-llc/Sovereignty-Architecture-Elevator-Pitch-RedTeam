#!/usr/bin/env python3
"""
Chess Council Agent Health Check
Verifies agent is operational and ready for games.
"""

import os
import sys
import subprocess


def check_processes():
    """Check required processes are running."""
    required = ['python3']  # API server
    for proc in required:
        try:
            subprocess.run(
                ['pgrep', '-f', proc],
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError:
            return False, f"Process {proc} not running"
    return True, "All processes running"


def check_api():
    """Check API endpoint is responding."""
    import urllib.request
    try:
        with urllib.request.urlopen('http://localhost:8080/health', timeout=5) as resp:
            if resp.status == 200:
                return True, "API healthy"
    except Exception as e:
        return False, f"API check failed: {e}"
    return False, "API unhealthy"


def check_workspace():
    """Check workspace directories exist."""
    dirs = ['/workspace', '/config', '/cache']
    for d in dirs:
        if not os.path.isdir(d):
            return False, f"Directory {d} missing"
    return True, "Workspace ready"


def main():
    """Run all health checks."""
    checks = [
        ('processes', check_processes),
        ('workspace', check_workspace),
    ]
    
    all_healthy = True
    for name, check in checks:
        healthy, msg = check()
        if not healthy:
            print(f"UNHEALTHY: {name} - {msg}")
            all_healthy = False
        else:
            print(f"OK: {name} - {msg}")
    
    sys.exit(0 if all_healthy else 1)


if __name__ == '__main__':
    main()
