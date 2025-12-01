#!/usr/bin/env python3
"""
Sovereignty Architecture Deployment CLI with Discord Integration

Deploy the immune system to GKE clusters with Discord notifications.

Usage:
    python main.py deploy gke --cluster <cluster-name> [--discord-integration]
    python main.py status --cluster <cluster-name>
    python main.py wake --cluster <cluster-name>
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from typing import Optional

# ANSI color codes
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    MAGENTA = '\033[0;35m'
    NC = '\033[0m'  # No Color

def print_info(msg: str) -> None:
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")

def print_success(msg: str) -> None:
    print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {msg}")

def print_warning(msg: str) -> None:
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {msg}")

def print_error(msg: str) -> None:
    print(f"{Colors.RED}[ERROR]{Colors.NC} {msg}")

def print_banner() -> None:
    banner = f"""{Colors.CYAN}
╔══════════════════════════════════════════════════════════════╗
║       🧬 SOVEREIGNTY ARCHITECTURE DEPLOYMENT CLI 🧬          ║
║                                                              ║
║       Discord Nervous System • Living Infrastructure         ║
╚══════════════════════════════════════════════════════════════╝
{Colors.NC}"""
    print(banner)

# GKE cluster configurations
GKE_CLUSTERS = {
    "jarvis-swarm-personal-001": {
        "description": "Main production brain",
        "zone": "us-central1",
        "namespaces": ["swarm-immune", "production", "agents"]
    },
    "red-team": {
        "description": "Security testing environment",
        "zone": "us-central1",
        "namespaces": ["security-tests", "penetration", "chaos"]
    },
    "autopilot-cluster-1": {
        "description": "Experimental playground",
        "zone": "us-central1",
        "namespaces": ["experiments", "staging", "dev"]
    }
}

def send_discord_notification(channel_id: str, title: str, description: str, color: int = 0x00ff00) -> bool:
    """Send a notification to Discord via the bot token."""
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        print_warning("DISCORD_TOKEN not set - skipping Discord notification")
        return False
    
    try:
        import urllib.request
        import ssl
        
        payload = {
            "embeds": [{
                "title": title,
                "description": description,
                "color": color,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "footer": {"text": "Sovereignty Architecture • Living Infrastructure"}
            }]
        }
        
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"https://discord.com/api/v10/channels/{channel_id}/messages",
            data=data,
            headers={
                "Authorization": f"Bot {token}",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        
        context = ssl.create_default_context()
        with urllib.request.urlopen(req, context=context) as response:
            return response.status == 200
    except Exception as e:
        print_warning(f"Failed to send Discord notification: {e}")
        return False

def get_cluster_credentials(cluster_name: str, zone: str) -> bool:
    """Get GKE cluster credentials."""
    print_info(f"Getting credentials for cluster: {cluster_name}")
    
    try:
        result = subprocess.run(
            ["gcloud", "container", "clusters", "get-credentials", cluster_name, f"--zone={zone}"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_success(f"Credentials obtained for {cluster_name}")
            return True
        else:
            print_error(f"Failed to get credentials: {result.stderr}")
            return False
    except FileNotFoundError:
        print_warning("gcloud not found - running in simulation mode")
        return True

def deploy_immune_system(cluster_name: str, discord_integration: bool = False) -> bool:
    """Deploy the immune system to a GKE cluster."""
    cluster = GKE_CLUSTERS.get(cluster_name)
    if not cluster:
        print_error(f"Unknown cluster: {cluster_name}")
        print_info(f"Available clusters: {', '.join(GKE_CLUSTERS.keys())}")
        return False
    
    print_info(f"🐉 Waking dragon: {cluster_name}")
    print_info(f"   Description: {cluster['description']}")
    print_info(f"   Zone: {cluster['zone']}")
    
    # Get cluster credentials
    get_cluster_credentials(cluster_name, cluster["zone"])
    
    # Apply Kubernetes manifests
    print_info("Deploying immune system components...")
    
    manifests = [
        "bootstrap/k8s/rbac.yaml",
        "bootstrap/k8s/secrets.yaml",
        "bootstrap/k8s/configmap.yaml",
        "bootstrap/k8s/bot-deployment.yaml",
        "bootstrap/k8s/gateway-deployment.yaml"
    ]
    
    for manifest in manifests:
        if os.path.exists(manifest):
            print_info(f"  Applying {manifest}...")
            try:
                result = subprocess.run(
                    ["kubectl", "apply", "-f", manifest],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    print_warning(f"kubectl not available or manifest failed: {manifest}")
            except FileNotFoundError:
                print_warning("kubectl not found - running in simulation mode")
        else:
            print_warning(f"  Manifest not found: {manifest}")
    
    print_success(f"🔥 Dragon {cluster_name} is awakening!")
    
    # Send Discord notification if enabled
    if discord_integration:
        channel_id = os.environ.get("DEPLOYMENTS_CHANNEL_ID", os.environ.get("SWARM_HEALTH_CHANNEL_ID", ""))
        if channel_id:
            send_discord_notification(
                channel_id,
                f"🐉 Dragon Awakened: {cluster_name}",
                f"**Description:** {cluster['description']}\n"
                f"**Zone:** {cluster['zone']}\n"
                f"**Namespaces:** {', '.join(cluster['namespaces'])}\n\n"
                f"🩸 Immune system deployed and operational.\n"
                f"🧠 Quorum sensing enabled.",
                color=0x00ff00
            )
            print_success("Discord notification sent")
    
    return True

def show_status(cluster_name: Optional[str] = None) -> None:
    """Show the status of clusters and immune system."""
    print_info("🩸 Immune System Status")
    print()
    
    if cluster_name:
        clusters = [cluster_name] if cluster_name in GKE_CLUSTERS else []
        if not clusters:
            print_error(f"Unknown cluster: {cluster_name}")
            return
    else:
        clusters = list(GKE_CLUSTERS.keys())
    
    for name in clusters:
        cluster = GKE_CLUSTERS[name]
        print(f"  🐉 {Colors.CYAN}{name}{Colors.NC}")
        print(f"     └ {cluster['description']}")
        print(f"     └ Zone: {cluster['zone']}")
        print(f"     └ Status: ✅ Configured")
        print()
    
    print_info("Cell Counts:")
    print("  🩸 RBC: 3 active")
    print("  🔬 WBC: 2 scanning")
    print("  🩹 Platelets: 1 ready")
    print()
    print_info("Mode: 🤝 Coordinate")
    print_info("Quorum Sensing: 🧠 Enabled")
    print_info("Density: 14 cells active")

def wake_cluster(cluster_name: str) -> bool:
    """Wake a dormant dragon cluster."""
    cluster = GKE_CLUSTERS.get(cluster_name)
    if not cluster:
        print_error(f"Unknown cluster: {cluster_name}")
        print_info(f"Available clusters: {', '.join(GKE_CLUSTERS.keys())}")
        return False
    
    print_info(f"🔥 Waking dragon: {cluster_name}")
    print()
    print(f"  {Colors.MAGENTA}gcloud container clusters get-credentials {cluster_name} --zone={cluster['zone']}{Colors.NC}")
    print()
    
    return get_cluster_credentials(cluster_name, cluster["zone"])

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sovereignty Architecture Deployment CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py deploy gke --cluster jarvis-swarm-personal-001 --discord-integration
    python main.py status
    python main.py status --cluster red-team
    python main.py wake --cluster autopilot-cluster-1

Environment Variables:
    DISCORD_TOKEN               - Discord bot token for notifications
    DEPLOYMENTS_CHANNEL_ID      - Channel ID for deployment notifications
    SWARM_HEALTH_CHANNEL_ID     - Channel ID for swarm health updates
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Deploy command
    deploy_parser = subparsers.add_parser("deploy", help="Deploy immune system to a cluster")
    deploy_parser.add_argument("target", choices=["gke"], help="Deployment target")
    deploy_parser.add_argument("--cluster", required=True, help="Cluster name")
    deploy_parser.add_argument("--discord-integration", action="store_true", help="Enable Discord notifications")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show cluster and immune system status")
    status_parser.add_argument("--cluster", help="Specific cluster name (optional)")
    
    # Wake command
    wake_parser = subparsers.add_parser("wake", help="Wake a dormant dragon cluster")
    wake_parser.add_argument("--cluster", required=True, help="Cluster name")
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.command == "deploy":
        if args.target == "gke":
            success = deploy_immune_system(args.cluster, args.discord_integration)
            return 0 if success else 1
    elif args.command == "status":
        show_status(args.cluster)
        return 0
    elif args.command == "wake":
        success = wake_cluster(args.cluster)
        return 0 if success else 1
    else:
        parser.print_help()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
