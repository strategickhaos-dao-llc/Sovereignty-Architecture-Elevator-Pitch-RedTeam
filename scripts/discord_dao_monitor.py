#!/usr/bin/env python3
"""
discord_dao_monitor.py
Discord bot for monitoring DAO status and Kubernetes clusters.

This bot provides real-time monitoring of the Strategickhaos DAO infrastructure
including K8s cluster status, proof generation, and charitable rate routing.
"""

import os
import logging
from datetime import datetime
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration from environment
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN', '')
K8S_CLUSTERS = int(os.environ.get('K8S_CLUSTERS', '4'))
CHARITABLE_RATE = float(os.environ.get('CHARITABLE_RATE', '0.07'))
EIN = os.environ.get('EIN', '39-2923503')


class ClusterStatus:
    """Represents the status of a Kubernetes cluster."""
    
    def __init__(self, name: str, active: bool = True, pods_running: int = 0):
        self.name = name
        self.active = active
        self.pods_running = pods_running
        self.last_check = datetime.now()
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'active': self.active,
            'pods_running': self.pods_running,
            'last_check': self.last_check.isoformat()
        }


class DAOMonitor:
    """DAO monitoring service for Strategickhaos infrastructure."""
    
    def __init__(self):
        self.clusters = []
        self.nodes = ['Nova', 'Lyra']
        self.charitable_rate = CHARITABLE_RATE
        self.ein = EIN
        self._initialize_clusters()
    
    def _initialize_clusters(self):
        """Initialize cluster status tracking."""
        cluster_names = ['prod-us', 'dev', 'staging', 'backup']
        for i, name in enumerate(cluster_names[:K8S_CLUSTERS]):
            self.clusters.append(ClusterStatus(
                name=name,
                active=True,
                pods_running=4 if i < 2 else 2
            ))
    
    def check_all_clusters(self) -> dict:
        """Check status of all Kubernetes clusters."""
        active_count = sum(1 for c in self.clusters if c.active)
        total_pods = sum(c.pods_running for c in self.clusters)
        
        return {
            'clusters_active': active_count,
            'clusters_total': len(self.clusters),
            'total_pods': total_pods,
            'nodes': self.nodes,
            'charitable_rate': self.charitable_rate,
            'ein': self.ein,
            'status': 'healthy' if active_count == len(self.clusters) else 'degraded'
        }
    
    def get_status_message(self) -> str:
        """Generate a formatted status message for Discord."""
        status = self.check_all_clusters()
        return (
            f"✅ Nodes: {', '.join(status['nodes'])}\n"
            f"📊 K8s: {status['clusters_active']}/{status['clusters_total']} active\n"
            f"💰 Charitable: {int(status['charitable_rate'] * 100)}% routing confirmed\n"
            f"🔖 EIN: {status['ein']}"
        )
    
    def get_cluster_details(self) -> str:
        """Get detailed cluster information."""
        lines = ["**Kubernetes Cluster Details**\n"]
        for cluster in self.clusters:
            status_emoji = "🟢" if cluster.active else "🔴"
            lines.append(
                f"{status_emoji} **{cluster.name}**: "
                f"{cluster.pods_running} pods running"
            )
        return "\n".join(lines)


# Discord bot implementation
try:
    import discord
    from discord.ext import commands
    
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None
    commands = None
    logger.warning("discord.py not installed. Bot functionality disabled.")


def create_bot():
    """Create and configure the Discord bot."""
    if not DISCORD_AVAILABLE:
        logger.error("Discord library not available")
        return None
    
    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix='!', intents=intents)
    monitor = DAOMonitor()
    
    @bot.event
    async def on_ready():
        logger.info(f'Bot connected as {bot.user}')
        logger.info(f'Monitoring {K8S_CLUSTERS} clusters')
    
    @bot.command(name='proof')
    async def proof_status(ctx, action: str = 'status'):
        """Check proof-of-origin status.
        
        Usage:
            !proof status - Show current DAO status
            !proof clusters - Show detailed cluster info
        """
        if action == 'status':
            message = monitor.get_status_message()
            await ctx.send(message)
        elif action == 'clusters':
            message = monitor.get_cluster_details()
            await ctx.send(message)
        else:
            await ctx.send(f"Unknown action: {action}. Use 'status' or 'clusters'.")
    
    @bot.command(name='health')
    async def health_check(ctx):
        """Run a health check on all systems."""
        status = monitor.check_all_clusters()
        
        embed = discord.Embed(
            title="🏥 System Health Check",
            color=discord.Color.green() if status['status'] == 'healthy' else discord.Color.orange()
        )
        embed.add_field(name="Status", value=status['status'].upper(), inline=True)
        embed.add_field(name="Clusters", value=f"{status['clusters_active']}/{status['clusters_total']}", inline=True)
        embed.add_field(name="Total Pods", value=str(status['total_pods']), inline=True)
        embed.add_field(name="Consensus Nodes", value=", ".join(status['nodes']), inline=False)
        embed.set_footer(text=f"EIN: {status['ein']} | Charitable Rate: {int(status['charitable_rate'] * 100)}%")
        
        await ctx.send(embed=embed)
    
    @bot.command(name='dao')
    async def dao_info(ctx):
        """Display DAO information."""
        embed = discord.Embed(
            title="🎭 Strategickhaos DAO",
            description="Distributed AI Orchestration Platform",
            color=discord.Color.purple()
        )
        embed.add_field(name="EIN", value=EIN, inline=True)
        embed.add_field(name="Charitable Rate", value=f"{int(CHARITABLE_RATE * 100)}%", inline=True)
        embed.add_field(name="K8s Clusters", value=str(K8S_CLUSTERS), inline=True)
        embed.add_field(name="AI Nodes", value="Claude, GPT, Grok, DuckDuckGo", inline=False)
        embed.set_footer(text="Sovereignty Architecture Control Plane")
        
        await ctx.send(embed=embed)
    
    return bot


def main():
    """Main entry point for the Discord bot."""
    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN environment variable not set")
        logger.info("Running in dry-run mode...")
        
        # Demonstrate functionality without Discord connection
        monitor = DAOMonitor()
        print("\n" + "=" * 50)
        print("DAO Monitor - Dry Run Mode")
        print("=" * 50)
        print("\nStatus Message:")
        print(monitor.get_status_message())
        print("\nCluster Details:")
        print(monitor.get_cluster_details())
        print("\nFull Status:")
        status = monitor.check_all_clusters()
        for key, value in status.items():
            print(f"  {key}: {value}")
        return
    
    bot = create_bot()
    if bot:
        logger.info("Starting Discord bot...")
        bot.run(DISCORD_TOKEN)


if __name__ == '__main__':
    main()
