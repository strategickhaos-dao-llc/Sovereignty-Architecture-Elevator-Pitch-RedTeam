#!/usr/bin/env python3
"""
Obsidian Neural Mesh Discord Bot
Real-time brain graph sync + board receipt generation

Genesis Lock: Increment 3449 | Architect: 1067614449693569044
"""
import discord
from discord.ext import commands
import os
import yaml
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('obsidian-mesh')

# Genesis constants
ARCHITECT_SNOWFLAKE = 1067614449693569044
GENESIS_INCREMENT = 3449

# Default vault path (configurable via environment)
DEFAULT_VAULT_PATH = "/vault/legions-of-minds"


def get_vault_path() -> Path:
    """Get vault path from environment or use default."""
    return Path(os.getenv('OBSIDIAN_VAULT_PATH', DEFAULT_VAULT_PATH))


def load_config(config_path: str = None) -> dict:
    """Load configuration from YAML file."""
    if config_path is None:
        # Try multiple locations
        search_paths = [
            Path("obsidian-mesh-config.yaml"),
            Path(__file__).parent.parent / "obsidian-mesh-config.yaml",
            Path.cwd() / "obsidian-mesh-config.yaml",
        ]
        for path in search_paths:
            if path.exists():
                config_path = str(path)
                break
        else:
            raise FileNotFoundError(
                "Could not find obsidian-mesh-config.yaml. "
                "Please ensure it exists in the repository root."
            )
    
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def generate_genesis_hash(department: str, timestamp: str) -> str:
    """Generate a genesis verification hash."""
    data = f"{GENESIS_INCREMENT}:{ARCHITECT_SNOWFLAKE}:{department}:{timestamp}"
    return hashlib.sha256(data.encode()).hexdigest()[:16]


def get_department_config(config: dict, dept_name: str) -> dict:
    """Get department configuration by name."""
    dept_lower = dept_name.lower()
    for dept in config.get('departments', []):
        if dept['name'].lower() == dept_lower:
            return dept
    return None


def validate_path_within_vault(path: Path, vault_path: Path) -> bool:
    """Validate that a path is within the vault directory (prevents path traversal)."""
    try:
        # Resolve both paths to absolute paths
        resolved_path = path.resolve()
        resolved_vault = vault_path.resolve()
        # Check if the path is within the vault
        resolved_path.relative_to(resolved_vault)
        return True
    except ValueError:
        return False


class ObsidianMeshBot(commands.Bot):
    """Discord bot for Obsidian Neural Mesh management."""
    
    def __init__(self, config: dict):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        self.mesh_config = config
        self.vault_path = get_vault_path()
    
    async def on_ready(self):
        """Called when the bot is ready."""
        logger.info(f'🟠 Obsidian Neural Mesh Bot Online: {self.user}')
        logger.info(f'⚡ Watching vault: {self.vault_path}')
        logger.info(f'🔒 Genesis Lock: Increment {GENESIS_INCREMENT}')
        logger.info(f'📊 Departments: {len(self.mesh_config.get("departments", []))}')


def create_receipt_embed(dept_config: dict, receipt_filename: str) -> discord.Embed:
    """Create a Discord embed for a board receipt."""
    embed = discord.Embed(
        title=f"📋 Board Receipt: {dept_config['name']}",
        description=f"Quadrant: {dept_config['quadrant']} | Branch: `{dept_config['git_branch']}`",
        color=0xFF4500,
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(
        name="🔒 Genesis Lock",
        value=f"Increment {GENESIS_INCREMENT}",
        inline=True
    )
    embed.add_field(
        name="👑 Architect",
        value=f"`{ARCHITECT_SNOWFLAKE}`",
        inline=True
    )
    embed.add_field(
        name="🧠 Brain Path",
        value=f"`{dept_config['brain_path']}`",
        inline=False
    )
    
    # Add licenses
    licenses_str = "\n".join(
        f"✅ {lic}" for lic in dept_config.get('licenses', [])
    ) or "None"
    embed.add_field(name="📜 Licenses", value=licenses_str, inline=True)
    
    # Add APIs
    apis_str = "\n".join(
        f"🔌 {api}" for api in dept_config.get('apis', [])
    ) or "None"
    embed.add_field(name="🔌 APIs", value=apis_str, inline=True)
    
    # Add MCP tools
    tools_str = "\n".join(
        f"🛠️ {tool}" for tool in dept_config.get('mcp_tools', [])
    ) or "None"
    embed.add_field(name="🛠️ MCP Tools", value=tools_str, inline=True)
    
    embed.set_footer(text=f"Receipt file: {receipt_filename}")
    
    return embed


def create_brain_embed(dept_config: dict, methodology: str, 
                       brain_files: list, git_log: str) -> discord.Embed:
    """Create a Discord embed for brain state."""
    embed = discord.Embed(
        title=f"🧠 Brain State: {dept_config['name']}",
        description=f"Quadrant: **{dept_config['quadrant']}**",
        color=0x4ECDC4,
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(
        name="📁 Brain Path",
        value=f"`{dept_config['brain_path']}`",
        inline=False
    )
    embed.add_field(
        name="📄 Files",
        value=f"{len(brain_files)} markdown files",
        inline=True
    )
    embed.add_field(
        name="🌿 Git Branch",
        value=f"`{dept_config['git_branch']}`",
        inline=True
    )
    
    # Truncate methodology for embed
    methodology_preview = methodology[:400] + "..." if len(methodology) > 400 else methodology
    embed.add_field(
        name="📝 Methodology Preview",
        value=f"```{methodology_preview}```",
        inline=False
    )
    
    # Truncate git log
    git_log_preview = git_log[:500] if git_log else "No recent commits"
    embed.add_field(
        name="📜 Recent Commits",
        value=f"```{git_log_preview}```",
        inline=False
    )
    
    return embed


def create_health_embed(config: dict) -> discord.Embed:
    """Create a Discord embed for cluster health."""
    embed = discord.Embed(
        title="🟠 OBSIDIAN NEURAL MESH HEALTH",
        description="Sovereign Knowledge Graph Status",
        color=0xFF4500,
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(
        name="🧠 Vault Status",
        value="✅ Online",
        inline=True
    )
    embed.add_field(
        name="📊 Departments",
        value=f"{len(config.get('departments', []))} active",
        inline=True
    )
    embed.add_field(
        name="🔒 Genesis Lock",
        value=f"Increment {GENESIS_INCREMENT}",
        inline=True
    )
    
    # Add department status
    dept_status = []
    for dept in config.get('departments', []):
        dept_status.append(f"• **{dept['name']}** ({dept['quadrant']})")
    embed.add_field(
        name="🏛️ Department Status",
        value="\n".join(dept_status) or "No departments",
        inline=False
    )
    
    return embed


def setup_commands(bot: ObsidianMeshBot):
    """Set up bot commands."""
    
    @bot.command(name='receipt')
    async def generate_receipt(ctx, department: str = None):
        """Generate board member receipt for a department."""
        if not department:
            await ctx.send(
                "Usage: `!receipt [department]` (athena, lyra, nova, ipower)"
            )
            return
        
        dept_config = get_department_config(bot.mesh_config, department)
        
        if not dept_config:
            await ctx.send(f"❌ Department '{department}' not found")
            return
        
        await ctx.send(
            f"🟠 Generating board receipt for **{dept_config['name']}**..."
        )
        
        # Generate receipt content
        timestamp = datetime.now().isoformat()
        genesis_hash = generate_genesis_hash(dept_config['name'], timestamp)
        
        receipt_content = f"""---
type: board-receipt
department: "{dept_config['name']}"
generated: "{timestamp}"
genesis_increment: {GENESIS_INCREMENT}
tags:
  - "#{dept_config['name'].lower()}"
  - "#board-receipt"
  - "#genesis"
---

# 📋 Board Member Receipt: {dept_config['name']}

## 🔒 Genesis Lock
- **Increment:** {GENESIS_INCREMENT}
- **Architect Snowflake:** {ARCHITECT_SNOWFLAKE}
- **Generated:** {timestamp}
- **Hash:** `{genesis_hash}`

## 🏛️ Department Information
- **Name:** {dept_config['name']}
- **Quadrant:** {dept_config['quadrant']}
- **Brain Path:** `{dept_config['brain_path']}`
- **Sandbox Path:** `{dept_config['sandbox_path']}`
- **Git Branch:** `{dept_config['git_branch']}`

## 📜 Licenses Held
{chr(10).join(f"- {lic}" for lic in dept_config.get('licenses', []))}

## 🔌 API Access
{chr(10).join(f"- {api}" for api in dept_config.get('apis', []))}

## 🛠️ MCP Tools Available
{chr(10).join(f"- {tool}" for tool in dept_config.get('mcp_tools', []))}

---
*Genesis Proof: {genesis_hash}*
*This receipt is sovereign property of Strategickhaos DAO LLC*
"""
        
        # Save receipt with path validation
        receipt_filename = (
            f"receipt-{dept_config['name'].lower()}-"
            f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        )
        receipt_dir = bot.vault_path / "board-receipts"
        receipt_dir.mkdir(parents=True, exist_ok=True)
        receipt_full_path = receipt_dir / receipt_filename
        
        # Validate path is within vault (prevent path traversal)
        if not validate_path_within_vault(receipt_full_path, bot.vault_path):
            logger.error(f"Path validation failed: {receipt_full_path}")
            await ctx.send("❌ Invalid path detected")
            return
        
        try:
            with open(receipt_full_path, "w") as f:
                f.write(receipt_content)
            logger.info(f"Receipt saved: {receipt_full_path}")
        except Exception as e:
            logger.warning(f"Could not save receipt to vault: {e}")
            # Continue even if vault write fails
        
        # Try Git commit (non-blocking) with path validation
        try:
            # Double-check path is still within vault before Git operations
            if validate_path_within_vault(receipt_full_path, bot.vault_path):
                subprocess.run(
                    ['git', 'add', str(receipt_full_path)],
                    cwd=bot.vault_path,
                    check=True,
                    capture_output=True
                )
                subprocess.run(
                    ['git', 'commit', '-m',
                     f'🟠 Board receipt: {dept_config["name"]} | '
                     f'Increment {GENESIS_INCREMENT}'],
                    cwd=bot.vault_path,
                    check=True,
                    capture_output=True
                )
                subprocess.run(
                    ['git', 'push'],
                    cwd=bot.vault_path,
                    check=True,
                    capture_output=True
                )
                logger.info("Receipt committed to Git")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Git operation failed: {e}")
        except FileNotFoundError:
            logger.warning("Git not available or vault not a git repo")
        
        # Create and send embed
        embed = create_receipt_embed(dept_config, receipt_filename)
        
        # Try to send file attachment (use try/except instead of exists check)
        try:
            with open(receipt_full_path, 'rb') as f:
                file = discord.File(f, filename=receipt_filename)
                await ctx.send(embed=embed, file=file)
        except FileNotFoundError:
            await ctx.send(embed=embed)
            logger.warning("Receipt file not found for attachment")
        except Exception as e:
            await ctx.send(embed=embed)
            logger.warning(f"Could not attach file: {e}")
        
        logger.info(f"✅ Receipt generated: {receipt_filename}")
    
    @bot.command(name='brain')
    async def show_brain(ctx, department: str = None):
        """Show current brain state for a department."""
        if not department:
            await ctx.send(
                "Usage: `!brain [department]` (athena, lyra, nova, ipower)"
            )
            return
        
        dept_config = get_department_config(bot.mesh_config, department)
        
        if not dept_config:
            await ctx.send(f"❌ Department '{department}' not found")
            return
        
        brain_path = bot.vault_path / dept_config['brain_path']
        methodology_path = bot.vault_path / dept_config['methodology_file']
        
        # Read methodology
        methodology = "No methodology found"
        if methodology_path.exists():
            try:
                with open(methodology_path, 'r') as f:
                    methodology = f.read()[:500]
            except Exception as e:
                logger.warning(f"Could not read methodology: {e}")
        
        # Count files in brain
        brain_files = []
        if brain_path.exists():
            brain_files = list(brain_path.glob('**/*.md'))
        
        # Get recent Git commits for this brain
        git_log = "No recent commits"
        try:
            result = subprocess.run(
                ['git', 'log', '--oneline', '-n', '5', '--',
                 str(dept_config['brain_path'])],
                cwd=bot.vault_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout:
                git_log = result.stdout
        except Exception as e:
            logger.warning(f"Could not get git log: {e}")
        
        embed = create_brain_embed(dept_config, methodology, brain_files, git_log)
        await ctx.send(embed=embed)
    
    @bot.command(name='sync')
    async def force_sync(ctx):
        """Force sync Obsidian vault to Git and Discord."""
        await ctx.send("🟠 Force syncing Obsidian vault...")
        
        try:
            # Git add all
            subprocess.run(
                ['git', 'add', '.'],
                cwd=bot.vault_path,
                check=True,
                capture_output=True
            )
            
            # Commit
            commit_msg = (
                f"🟠 Manual sync | Increment {GENESIS_INCREMENT} | "
                f"{datetime.now().isoformat()}"
            )
            result = subprocess.run(
                ['git', 'commit', '-m', commit_msg],
                cwd=bot.vault_path,
                capture_output=True,
                text=True
            )
            
            # Push
            if result.returncode == 0:
                subprocess.run(
                    ['git', 'push'],
                    cwd=bot.vault_path,
                    check=True,
                    capture_output=True
                )
                await ctx.send(f"✅ Sync complete: {commit_msg}")
            else:
                await ctx.send("✅ No changes to sync")
        
        except subprocess.CalledProcessError as e:
            await ctx.send(f"❌ Sync failed: {e}")
            logger.error(f"Sync error: {e}")
        except FileNotFoundError:
            await ctx.send("❌ Git not available or vault not initialized")
    
    @bot.command(name='archive')
    async def search_archive(ctx, *, query: str = None):
        """Search archive vault for license/API/tool."""
        if not query:
            await ctx.send(
                "Usage: `!archive [query]` "
                "(e.g., 'unity license', 'discord api')"
            )
            return
        
        query_lower = query.lower()
        results = []
        
        archive = bot.mesh_config.get('archive_vault', {}).get('structure', {})
        
        # Search licenses
        for lic in archive.get('licenses', []):
            if (query_lower in lic.get('name', '').lower() or
                query_lower in str(lic.get('assigned_to', [])).lower()):
                results.append(('License', lic['name'], lic.get('file', 'N/A')))
        
        # Search APIs
        for api in archive.get('apis', []):
            if (query_lower in api.get('name', '').lower() or
                query_lower in str(api.get('used_by', [])).lower()):
                results.append(('API', api['name'], api.get('file', 'N/A')))
        
        # Search MCP tools
        for tool in archive.get('mcp_tools', []):
            if (query_lower in tool.get('name', '').lower() or
                query_lower in tool.get('description', '').lower()):
                results.append(('MCP Tool', tool['name'], tool.get('server', 'N/A')))
        
        if not results:
            await ctx.send(f"❌ No results found for: `{query}`")
            return
        
        embed = discord.Embed(
            title=f"🗄️ Archive Search: {query}",
            description=f"Found {len(results)} results",
            color=0xFFD700
        )
        
        for result_type, name, path in results[:10]:
            embed.add_field(
                name=f"{result_type}: {name}",
                value=f"`{path}`",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @bot.command(name='health')
    async def cluster_health(ctx):
        """Show Obsidian Neural Mesh health status."""
        embed = create_health_embed(bot.mesh_config)
        await ctx.send(embed=embed)
    
    @bot.command(name='departments')
    async def list_departments(ctx):
        """List all available departments."""
        embed = discord.Embed(
            title="🏛️ Available Departments",
            description="Obsidian Neural Mesh Brain Registry",
            color=0xFF4500,
            timestamp=datetime.utcnow()
        )
        
        for dept in bot.mesh_config.get('departments', []):
            embed.add_field(
                name=f"{dept['name']} ({dept['quadrant']})",
                value=(
                    f"Branch: `{dept['git_branch']}`\n"
                    f"Tag: `{dept.get('tag', 'N/A')}`"
                ),
                inline=True
            )
        
        embed.set_footer(
            text=f"Genesis Lock: Increment {GENESIS_INCREMENT}"
        )
        await ctx.send(embed=embed)


def validate_config(config: dict) -> list:
    """Validate configuration and return list of warnings."""
    warnings = []
    
    # Check departments
    departments = config.get('departments', [])
    if not departments:
        warnings.append("No departments configured")
    
    for dept in departments:
        dept_name = dept.get('name', 'Unknown')
        
        # Check for null channel IDs
        if dept.get('discord_channel_id') is None:
            warnings.append(
                f"Department '{dept_name}' has no Discord channel ID configured"
            )
    
    # Check sync pipeline discord channels
    sync_discord = config.get('sync_pipeline', {}).get('discord', {})
    channels = sync_discord.get('channels', {})
    for channel_name, channel_id in channels.items():
        if channel_id is None:
            warnings.append(
                f"Sync pipeline channel '{channel_name}' is not configured"
            )
    
    return warnings


def main():
    """Main entry point for the bot."""
    # Load configuration
    try:
        config = load_config()
        logger.info("Configuration loaded successfully")
    except FileNotFoundError as e:
        logger.error(f"Configuration error: {e}")
        exit(1)
    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML configuration: {e}")
        exit(1)
    
    # Validate configuration and log warnings
    warnings = validate_config(config)
    for warning in warnings:
        logger.warning(f"Config: {warning}")
    
    if warnings:
        logger.info(
            "Some configuration values are not set. "
            "The bot will work but some features may be limited."
        )
    
    # Get Discord token
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logger.error("❌ DISCORD_TOKEN environment variable not set")
        exit(1)
    
    # Create and configure bot
    bot = ObsidianMeshBot(config)
    setup_commands(bot)
    
    # Run bot
    logger.info("Starting Obsidian Neural Mesh Discord Bot...")
    bot.run(token)


if __name__ == "__main__":
    main()
