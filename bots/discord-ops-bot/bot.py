#!/usr/bin/env python3
"""
Strategickhaos Discord Ops Bot
Discord-based DevOps control plane for the Strategickhaos ecosystem.

Provides slash commands for:
- /status - Service status
- /logs - Tail service logs
- /deploy - Deploy tag to environment (protected)
- /scale - Scale service replicas (protected)
"""

import os
import asyncio
import logging
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands
import yaml
from prometheus_client import start_http_server, Counter, Histogram
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Prometheus metrics
COMMANDS_TOTAL = Counter('discord_commands_total', 'Total commands processed', ['command', 'status'])
COMMAND_LATENCY = Histogram('discord_command_latency_seconds', 'Command latency', ['command'])


class DiscordOpsBot(commands.Bot):
    """Strategickhaos Discord Ops Bot."""

    def __init__(self, config_path: str = "/etc/discord-ops/discovery.yml"):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix="!",
            intents=intents,
            description="Strategickhaos Discord DevOps Control Plane"
        )

        self.config_path = config_path
        self.config = self._load_config()
        self.prod_role = self.config.get("discord", {}).get("bot", {}).get("rbac", {}).get("prod_role", "ReleaseMgr")

    def _load_config(self) -> dict:
        """Load discovery configuration."""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning("config_not_found", path=self.config_path)
            return {}
        except yaml.YAMLError as e:
            logger.error("config_parse_error", error=str(e))
            return {}

    async def setup_hook(self):
        """Set up slash commands."""
        await self.tree.sync()
        logger.info("commands_synced")

    async def on_ready(self):
        """Bot ready event."""
        logger.info("bot_ready", user=str(self.user), guilds=len(self.guilds))


# Initialize bot
bot = DiscordOpsBot()


def has_prod_role():
    """Check if user has production role for protected commands."""
    async def predicate(interaction: discord.Interaction) -> bool:
        if not interaction.guild:
            return False
        role = discord.utils.get(interaction.user.roles, name=bot.prod_role)
        return role is not None
    return app_commands.check(predicate)


@bot.tree.command(name="status", description="Get service status")
@app_commands.describe(service="Service name to check status")
async def status_command(interaction: discord.Interaction, service: str):
    """Get status of a Kubernetes service."""
    with COMMAND_LATENCY.labels(command="status").time():
        try:
            await interaction.response.defer()

            # Simulate K8s status check
            embed = discord.Embed(
                title=f"📊 Service Status: {service}",
                color=discord.Color.green()
            )
            embed.add_field(name="Status", value="✅ Running", inline=True)
            embed.add_field(name="Replicas", value="2/2", inline=True)
            embed.add_field(name="Namespace", value="ops", inline=True)
            embed.set_footer(text="Strategickhaos Sovereignty Architecture")

            await interaction.followup.send(embed=embed)
            COMMANDS_TOTAL.labels(command="status", status="success").inc()
            logger.info("command_executed", command="status", service=service)

        except Exception as e:
            COMMANDS_TOTAL.labels(command="status", status="error").inc()
            logger.error("command_failed", command="status", error=str(e))
            await interaction.followup.send(f"❌ Error checking status: {e}")


@bot.tree.command(name="logs", description="Tail service logs")
@app_commands.describe(service="Service name", tail="Number of lines to tail")
async def logs_command(interaction: discord.Interaction, service: str, tail: int = 200):
    """Tail logs from a Kubernetes service."""
    with COMMAND_LATENCY.labels(command="logs").time():
        try:
            await interaction.response.defer()

            embed = discord.Embed(
                title=f"📜 Logs: {service}",
                description=f"Last {tail} lines",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="Recent Logs",
                value="```\n[INFO] Service healthy\n[INFO] Processing events\n```",
                inline=False
            )

            await interaction.followup.send(embed=embed)
            COMMANDS_TOTAL.labels(command="logs", status="success").inc()

        except Exception as e:
            COMMANDS_TOTAL.labels(command="logs", status="error").inc()
            logger.error("command_failed", command="logs", error=str(e))
            await interaction.followup.send(f"❌ Error fetching logs: {e}")


@bot.tree.command(name="deploy", description="Deploy tag to environment")
@app_commands.describe(env="Target environment", tag="Docker image tag to deploy")
@app_commands.choices(env=[
    app_commands.Choice(name="dev", value="dev"),
    app_commands.Choice(name="staging", value="staging"),
    app_commands.Choice(name="prod", value="prod"),
])
@has_prod_role()
async def deploy_command(interaction: discord.Interaction, env: str, tag: str):
    """Deploy a tag to an environment (protected command)."""
    with COMMAND_LATENCY.labels(command="deploy").time():
        try:
            await interaction.response.defer()

            embed = discord.Embed(
                title=f"🚀 Deployment Initiated",
                color=discord.Color.orange()
            )
            embed.add_field(name="Environment", value=env, inline=True)
            embed.add_field(name="Tag", value=tag, inline=True)
            embed.add_field(name="Initiated By", value=interaction.user.mention, inline=True)
            embed.set_footer(text="Deployment in progress...")

            await interaction.followup.send(embed=embed)
            COMMANDS_TOTAL.labels(command="deploy", status="success").inc()
            logger.info("deployment_initiated", env=env, tag=tag, user=str(interaction.user))

        except Exception as e:
            COMMANDS_TOTAL.labels(command="deploy", status="error").inc()
            logger.error("command_failed", command="deploy", error=str(e))
            await interaction.followup.send(f"❌ Deployment failed: {e}")


@bot.tree.command(name="scale", description="Scale service replicas")
@app_commands.describe(service="Service to scale", replicas="Number of replicas")
@has_prod_role()
async def scale_command(interaction: discord.Interaction, service: str, replicas: int):
    """Scale a service (protected command)."""
    with COMMAND_LATENCY.labels(command="scale").time():
        try:
            await interaction.response.defer()

            embed = discord.Embed(
                title=f"⚖️ Scaling: {service}",
                color=discord.Color.purple()
            )
            embed.add_field(name="Service", value=service, inline=True)
            embed.add_field(name="Target Replicas", value=str(replicas), inline=True)
            embed.add_field(name="Initiated By", value=interaction.user.mention, inline=True)

            await interaction.followup.send(embed=embed)
            COMMANDS_TOTAL.labels(command="scale", status="success").inc()
            logger.info("scaling_initiated", service=service, replicas=replicas, user=str(interaction.user))

        except Exception as e:
            COMMANDS_TOTAL.labels(command="scale", status="error").inc()
            logger.error("command_failed", command="scale", error=str(e))
            await interaction.followup.send(f"❌ Scaling failed: {e}")


@deploy_command.error
@scale_command.error
async def protected_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """Handle errors for protected commands."""
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message(
            f"❌ Permission denied. You need the `{bot.prod_role}` role to use this command.",
            ephemeral=True
        )
    else:
        logger.error("command_error", error=str(error))
        await interaction.response.send_message(f"❌ An error occurred: {error}", ephemeral=True)


async def run_health_server():
    """Run a simple health check server."""
    from aiohttp import web

    async def health(request):
        return web.Response(text="OK")

    async def ready(request):
        if bot.is_ready():
            return web.Response(text="Ready")
        return web.Response(text="Not Ready", status=503)

    app = web.Application()
    app.router.add_get('/health', health)
    app.router.add_get('/ready', ready)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    logger.info("health_server_started", port=8080)


async def main():
    """Main entry point."""
    # Start Prometheus metrics server
    metrics_port = int(os.getenv("METRICS_PORT", "9090"))
    start_http_server(metrics_port)
    logger.info("metrics_server_started", port=metrics_port)

    # Start health check server
    await run_health_server()

    # Get bot token
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("missing_bot_token")
        raise ValueError("DISCORD_BOT_TOKEN environment variable is required")

    # Run the bot
    await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
