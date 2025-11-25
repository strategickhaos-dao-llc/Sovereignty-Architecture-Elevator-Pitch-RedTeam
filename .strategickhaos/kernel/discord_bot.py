"""
Strategickhaos Legion Discord Bot - Human Interface

Provides Discord slash commands for proposal submission,
status tracking, and administrative override capabilities.

Run separately from the main kernel: python discord_bot.py
"""

import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('legion_discord')

# Optional imports
try:
    import discord
    from discord.ext import commands
    HAS_DISCORD = True
except ImportError:
    HAS_DISCORD = False
    logger.warning("discord.py not installed - bot functionality disabled")

# Import kernel (handle if not available)
try:
    from connect import LegionKernel
except ImportError:
    LegionKernel = None
    logger.warning("LegionKernel not available")


def create_bot():
    """Create and configure the Discord bot"""
    if not HAS_DISCORD:
        logger.error("Cannot create bot - discord.py not installed")
        return None

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        """Bot startup handler"""
        logger.info(f'Legion Bot connected as {bot.user}')
        print(f'✅ Legion Bot online: {bot.user}')

    @bot.command()
    async def propose(ctx, *, proposal_text: str):
        """
        !propose <description>

        Submit a proposal to the Legion for voting.
        """
        if LegionKernel is None:
            await ctx.send("❌ Kernel not available")
            return

        try:
            kernel = LegionKernel(workspace_id='discord_interface')

            proposal = {
                'title': proposal_text[:50],
                'description': proposal_text,
                'author': str(ctx.author),
                'author_id': str(ctx.author.id),
                'channel': str(ctx.channel),
                'actions': []  # Actions specified in full proposal format
            }

            proposal_id = kernel.propose_change(proposal)

            await ctx.send(
                f"✅ **Proposal submitted:** `{proposal_id}`\n"
                f"📋 Title: {proposal['title']}\n"
                f"🗳️ Departments are now voting...\n"
                f"📊 Track status: `!status {proposal_id}`"
            )

        except Exception as e:
            logger.error(f"Proposal submission failed: {e}")
            await ctx.send(f"❌ Failed to submit proposal: {e}")

    @bot.command()
    async def status(ctx, proposal_id: str):
        """
        !status <proposal_id>

        Check voting status on a proposal.
        """
        if LegionKernel is None:
            await ctx.send("❌ Kernel not available")
            return

        try:
            kernel = LegionKernel(workspace_id='discord_interface')
            result = kernel.check_proposal_status(proposal_id)

            status_emoji = {
                'pending': '⏳',
                'approved': '✅',
                'rejected': '❌',
                'blocked': '🚫'
            }

            emoji = status_emoji.get(result['status'], '❓')
            message = f"{emoji} **Proposal {proposal_id}**\n"
            message += f"Status: `{result['status']}`\n"

            if 'approval_rate' in result:
                message += f"Approval rate: {result['approval_rate']:.1%}\n"

            if 'reason' in result:
                message += f"Reason: {result['reason']}\n"

            if 'votes' in result:
                message += f"Votes received: {result['votes']}\n"

            await ctx.send(message)

        except Exception as e:
            logger.error(f"Status check failed: {e}")
            await ctx.send(f"❌ Failed to check status: {e}")

    @bot.command()
    async def execute(ctx, proposal_id: str):
        """
        !execute <proposal_id>

        Execute an approved proposal. Requires admin permissions.
        """
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("❌ Only administrators can execute proposals")
            return

        if LegionKernel is None:
            await ctx.send("❌ Kernel not available")
            return

        try:
            kernel = LegionKernel(workspace_id='discord_interface')
            result = kernel.execute_approved(proposal_id)

            if result['executed']:
                await ctx.send(
                    f"✅ **Proposal {proposal_id} EXECUTED**\n"
                    f"Approval rate: {result['status']['approval_rate']:.1%}"
                )
            else:
                await ctx.send(
                    f"❌ Cannot execute proposal {proposal_id}\n"
                    f"Status: {result['status']['status']}\n"
                    f"Reason: {result['status'].get('reason', 'Not approved')}"
                )

        except Exception as e:
            logger.error(f"Execution failed: {e}")
            await ctx.send(f"❌ Failed to execute: {e}")

    @bot.command()
    async def override(ctx, proposal_id: str, action: str):
        """
        !override <proposal_id> <approve|reject>

        Dom's manual override (requires admin role).
        WARNING: This bypasses the voting process.
        """
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("❌ Only Dom can override")
            return

        if action.lower() not in ['approve', 'reject']:
            await ctx.send("❌ Action must be 'approve' or 'reject'")
            return

        # Log the override for audit trail
        logger.warning(f"MANUAL OVERRIDE by {ctx.author}: {action} on {proposal_id}")

        await ctx.send(
            f"⚠️ **Manual override initiated**\n"
            f"Proposal: `{proposal_id}`\n"
            f"Action: `{action.upper()}`\n"
            f"Override by: {ctx.author.mention}\n"
            f"⚠️ This bypasses normal voting procedures"
        )

        # TODO: Implement actual override logic
        # This would update the proposal status directly

    @bot.command()
    async def departments(ctx):
        """
        !departments

        List all voting departments and their status.
        """
        if LegionKernel is None:
            await ctx.send("❌ Kernel not available")
            return

        try:
            kernel = LegionKernel(workspace_id='discord_interface')
            deps = kernel.kernel_config.get('legion_os', {}).get('departments', [])

            message = "🏛️ **Legion Departments**\n\n"
            for dept in deps:
                veto = "🛡️" if dept.get('veto_power') else ""
                agent = dept.get('agent') or ', '.join(dept.get('agents', []))
                message += f"**{dept['name'].upper()}** {veto}\n"
                message += f"  Weight: {dept.get('weight', 1)} | Agent: `{agent}`\n"

            rules = kernel.kernel_config.get('legion_os', {}).get('voting_rules', {})
            message += f"\n📋 **Voting Rules**\n"
            message += f"  Quorum: {rules.get('quorum', 3)} departments\n"
            message += f"  Threshold: {rules.get('threshold', 0.6):.0%}\n"
            message += f"  Timeout: {rules.get('timeout', 300)}s\n"

            await ctx.send(message)

        except Exception as e:
            logger.error(f"Department listing failed: {e}")
            await ctx.send(f"❌ Failed to list departments: {e}")

    @bot.command()
    async def help_legion(ctx):
        """
        !help_legion

        Show all Legion governance commands.
        """
        help_text = """
🏛️ **Strategickhaos Legion Commands**

**Proposals**
`!propose <description>` - Submit a new proposal
`!status <proposal_id>` - Check proposal status
`!execute <proposal_id>` - Execute approved proposal (admin)

**Administration**
`!override <id> <approve|reject>` - Manual override (admin)
`!departments` - List voting departments

**Info**
`!help_legion` - Show this help message
"""
        await ctx.send(help_text)

    return bot


def main():
    """Main entry point"""
    if not HAS_DISCORD:
        print("❌ discord.py not installed. Install with: pip install discord.py")
        return

    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("❌ DISCORD_BOT_TOKEN environment variable not set")
        print("   Set it with: export DISCORD_BOT_TOKEN='your_token'")
        return

    bot = create_bot()
    if bot:
        bot.run(token)


if __name__ == '__main__':
    main()
