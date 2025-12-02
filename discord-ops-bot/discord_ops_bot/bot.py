"""
Discord Ops Bot - Main Entry Point

Strategickhaos Sovereignty Architecture - Discord DevOps Control Plane

This bot provides Discord-based infrastructure management with:
- Slash commands: /status, /logs, /deploy, /scale, /ask
- RBAC-based access control for production operations
- AI agent routing for intelligent assistance
- Comprehensive audit logging

LLM Directive: Extension points are marked with TODO comments.
When extending this bot:
1. Add new commands in the commands/ directory
2. Register them in the setup_commands() function
3. Update RBAC policies in rbac.py
4. Add metrics for observability
"""

import os
import logging
from typing import Optional

import discord
from discord.ext import commands

from .rbac import check_permission, RBACManager
from .ai_router import AIRouter, route_ai_query
from .logging_middleware import setup_logging, AuditLogger

logger = logging.getLogger(__name__)

# Environment configuration
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
PRS_CHANNEL = os.getenv("PRS_CHANNEL")
CONTROL_API_URL = os.getenv("CONTROL_API_URL", "https://control.internal.strategickhaos")
CONTROL_API_TOKEN = os.getenv("CTRL_API_TOKEN")

# Discord intents configuration
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

# Bot instance
bot = commands.Bot(command_prefix="/", intents=intents)

# Global managers
rbac_manager: Optional[RBACManager] = None
ai_router: Optional[AIRouter] = None
audit_logger: Optional[AuditLogger] = None


@bot.event
async def on_ready():
    """Called when the bot is ready and connected to Discord."""
    logger.info("Discord Ops Bot online as %s", bot.user)
    logger.info("Connected to %d guilds", len(bot.guilds))
    
    # Sync slash commands with Discord
    try:
        synced = await bot.tree.sync()
        logger.info("Synced %d slash commands", len(synced))
    except Exception as e:
        logger.error("Failed to sync commands: %s", e)


@bot.tree.command(name="status", description="Report high-level system status")
async def status(interaction: discord.Interaction, service: str):
    """
    Report high-level system status for a service.
    
    LLM Directive: Extend this to query Kubernetes API, Prometheus,
    or other monitoring systems for real status information.
    """
    if audit_logger:
        await audit_logger.log_command(interaction, "status", {"service": service})
    
    # TODO: Query Kubernetes + CI/CD + observability for real status
    # Example: kubectl get deployment {service} -o json
    # Example: prometheus query for service health
    
    embed = discord.Embed(
        title=f"🧭 Status: {service}",
        description="Sovereignty Architecture status check",
        color=0x2f81f7
    )
    embed.add_field(name="State", value="Running (stub)", inline=True)
    embed.add_field(name="Version", value="v0.0.0 (stub)", inline=True)
    embed.add_field(name="Replicas", value="1/1 (stub)", inline=True)
    
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="logs", description="Fetch recent logs from observability stack")
async def logs(interaction: discord.Interaction, target: str = "event-gateway", tail: int = 100):
    """
    Fetch last N logs from Loki / CloudWatch.
    
    LLM Directive: Extend this to query Loki API or CloudWatch Logs
    for actual log data. Implement pagination for large results.
    """
    if audit_logger:
        await audit_logger.log_command(interaction, "logs", {"target": target, "tail": tail})
    
    # TODO: Call Loki API or other log store
    # Example: GET /loki/api/v1/query_range?query={service="{target}"}
    
    await interaction.response.send_message(
        f"📜 Logs for `{target}` (last {tail} lines - stub):\n"
        "```\n"
        "[2024-01-15 10:23:45] INFO: Service started\n"
        "[2024-01-15 10:23:46] INFO: Listening on :8080\n"
        "... (implement real log fetching)\n"
        "```"
    )


@bot.tree.command(name="deploy", description="Trigger a deployment to environment")
@check_permission("deploy")
async def deploy(interaction: discord.Interaction, env: str, ref: str = "main"):
    """
    Trigger a deployment to the given environment.
    
    Protected command - requires 'deploy' permission (ReleaseMgr role).
    
    LLM Directive: Extend this to invoke CI/CD workflow via:
    - GitHub Actions dispatch API
    - ArgoCD sync
    - Kubernetes deployment rollout
    """
    if audit_logger:
        await audit_logger.log_command(interaction, "deploy", {"env": env, "ref": ref})
    
    # TODO: Invoke CI/CD workflow
    # Example: POST /repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches
    # Example: ArgoCD app sync
    
    embed = discord.Embed(
        title="🚀 Deployment Triggered",
        description=f"Deploying `{ref}` to `{env}`",
        color=0x28a745
    )
    embed.add_field(name="Environment", value=env, inline=True)
    embed.add_field(name="Reference", value=ref, inline=True)
    embed.add_field(name="Status", value="Pending (stub)", inline=True)
    embed.set_footer(text="Monitor at: https://github.com/org/repo/actions (stub)")
    
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="scale", description="Scale a service to specified replicas")
@check_permission("scale")
async def scale(interaction: discord.Interaction, service: str, replicas: int):
    """
    Scale a service to the specified replica count.
    
    Protected command - requires 'scale' permission (ReleaseMgr role).
    
    LLM Directive: Extend this to call Kubernetes API for actual scaling:
    PATCH /apis/apps/v1/namespaces/{ns}/deployments/{name}/scale
    """
    if audit_logger:
        await audit_logger.log_command(interaction, "scale", {"service": service, "replicas": replicas})
    
    # TODO: Call Kubernetes API to scale deployment
    # Example: kubectl scale deployment/{service} --replicas={replicas}
    
    embed = discord.Embed(
        title="📈 Scaling Service",
        description=f"Scaling `{service}` to {replicas} replicas",
        color=0x17a2b8
    )
    embed.add_field(name="Service", value=service, inline=True)
    embed.add_field(name="Target Replicas", value=str(replicas), inline=True)
    embed.add_field(name="Status", value="Pending (stub)", inline=True)
    
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="ask", description="Ask an AI agent for assistance")
async def ask(interaction: discord.Interaction, query: str):
    """
    Route a question to the appropriate AI agent.
    
    AI agent is selected based on channel configuration in discovery.yml.
    
    LLM Directive: The ai_router.py module handles model selection
    and context retrieval. Extend there to add new model providers
    or vector store integrations.
    """
    if audit_logger:
        await audit_logger.log_command(interaction, "ask", {"query": query[:100]})
    
    # Defer response since AI queries may take time
    await interaction.response.defer()
    
    try:
        response = await route_ai_query(interaction.channel.name, query)
        model = ai_router.get_model_for_channel(interaction.channel.name) if ai_router else "unknown"
        
        await interaction.followup.send(f"🤖 [{model}] {response}")
    except Exception as e:
        logger.error("AI query failed: %s", e)
        await interaction.followup.send(f"❌ AI query failed: {e}")


@bot.event
async def on_command_error(ctx, error):
    """Handle command errors with appropriate responses."""
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument: {error.param.name}")
    else:
        logger.error("Command error: %s", error)
        await ctx.send(f"❌ An error occurred: {error}")


def setup_managers():
    """Initialize global manager instances."""
    global rbac_manager, ai_router, audit_logger
    
    rbac_manager = RBACManager()
    ai_router = AIRouter()
    audit_logger = AuditLogger()


def main():
    """Main entry point for the Discord Ops Bot."""
    if not DISCORD_TOKEN:
        raise RuntimeError("DISCORD_BOT_TOKEN environment variable not set")
    
    # Setup logging
    setup_logging()
    
    # Initialize managers
    setup_managers()
    
    logger.info("Starting Discord Ops Bot...")
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
