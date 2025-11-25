#!/usr/bin/env python3
"""
Strategickhaos Legions of Minds OS - Discord Bot

Human interface for the Legion OS. Allows humans to:
- Submit proposals via Discord commands
- Check proposal status
- Monitor voting progress
- Override (admin only) decisions
- Receive real-time notifications

Commands:
  !propose <description>  - Submit a new proposal
  !status <proposal_id>   - Check proposal status
  !list                   - List all proposals
  !vote <id> <dept> <decision> - Manually record a vote (admin)
  !override <id> <action> - Manual override (admin only)
  !execute <id>          - Execute an approved proposal
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Any

# Add kernel directory to path
kernel_path = Path(__file__).parent / "kernel"
sys.path.insert(0, str(kernel_path))

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    print("Warning: discord.py not installed. Install with: pip install discord.py")

_LEGION_KERNEL_IMPORT_ERROR: str | None = None

try:
    from kernel.connect import LegionKernel
except ImportError:
    # Try relative import if running from different directory
    try:
        from connect import LegionKernel
    except ImportError as e:
        _LEGION_KERNEL_IMPORT_ERROR = str(e)
        # Define a placeholder that will fail clearly if used
        class LegionKernel:  # type: ignore[no-redef]
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                raise RuntimeError(
                    f"LegionKernel not available: {_LEGION_KERNEL_IMPORT_ERROR}. "
                    "Ensure connect.py is in the kernel directory."
                )


class LegionDiscordBot:
    """Discord bot for Strategickhaos Legion OS human interface."""
    
    def __init__(self) -> None:
        """Initialize the Discord bot."""
        if not DISCORD_AVAILABLE:
            raise RuntimeError("discord.py is not installed")
        
        intents = discord.Intents.default()
        intents.message_content = True
        
        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self.kernel = LegionKernel(workspace_id="discord_interface")
        
        self._register_commands()
    
    def _register_commands(self) -> None:
        """Register all bot commands."""
        
        @self.bot.event
        async def on_ready() -> None:
            print(f"Legion Bot connected as {self.bot.user}")
            print(f"Connected to {len(self.bot.guilds)} guild(s)")
        
        @self.bot.command(name="propose")
        async def propose(ctx: commands.Context, *, proposal_text: str) -> None:
            """
            !propose <description>
            
            Submit a proposal to the Legion for voting.
            """
            proposal = {
                "title": proposal_text[:50],
                "description": proposal_text,
                "author": str(ctx.author),
                "author_id": str(ctx.author.id),
                "channel": str(ctx.channel),
                "type": "general",
                "actions": []
            }
            
            proposal_id = self.kernel.propose_change(proposal)
            
            embed = discord.Embed(
                title="📋 Proposal Submitted",
                description=f"**ID:** `{proposal_id}`\n\n{proposal_text[:500]}",
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Submitted by {ctx.author.display_name}")
            embed.add_field(
                name="Status",
                value="🔄 Departments are now voting...",
                inline=False
            )
            embed.add_field(
                name="Track Status",
                value=f"`!status {proposal_id}`",
                inline=False
            )
            
            await ctx.send(embed=embed)
        
        @self.bot.command(name="status")
        async def status(ctx: commands.Context, proposal_id: str) -> None:
            """
            !status <proposal_id>
            
            Check voting status on a proposal.
            """
            proposal = self.kernel.get_proposal(proposal_id)
            
            if proposal is None:
                await ctx.send(f"❌ Proposal `{proposal_id}` not found")
                return
            
            status = self.kernel.check_proposal_status(proposal_id)
            
            # Status emoji mapping
            status_emoji = {
                "pending": "🔄",
                "approved": "✅",
                "rejected": "❌",
                "blocked": "🚫",
                "timeout": "⏰",
                "executing": "⚙️",
                "completed": "🎉",
                "failed": "💥"
            }
            
            emoji = status_emoji.get(status.get("status", "pending"), "❓")
            
            embed = discord.Embed(
                title=f"{emoji} Proposal Status: {proposal_id}",
                description=proposal.get("description", "No description")[:500],
                color=self._status_color(status.get("status", "pending"))
            )
            
            embed.add_field(
                name="Status",
                value=status.get("status", "unknown").upper(),
                inline=True
            )
            
            if "approval_rate" in status:
                embed.add_field(
                    name="Approval Rate",
                    value=f"{status['approval_rate']:.1%}",
                    inline=True
                )
            
            # Show votes
            votes = proposal.get("votes", {})
            if votes:
                vote_text = "\n".join([
                    f"• **{dept}**: {v.get('decision', 'N/A')}"
                    for dept, v in votes.items()
                ])
                embed.add_field(
                    name=f"Votes ({len(votes)})",
                    value=vote_text or "No votes yet",
                    inline=False
                )
            
            if "reason" in status:
                embed.add_field(
                    name="Details",
                    value=status["reason"],
                    inline=False
                )
            
            await ctx.send(embed=embed)
        
        @self.bot.command(name="list")
        async def list_proposals(ctx: commands.Context, status_filter: str | None = None) -> None:
            """
            !list [status]
            
            List all proposals, optionally filtered by status.
            """
            proposals = self.kernel.list_proposals(status_filter=status_filter)
            
            if not proposals:
                await ctx.send("📭 No proposals found")
                return
            
            embed = discord.Embed(
                title="📋 Proposals",
                description=f"Showing {len(proposals)} proposal(s)" + 
                           (f" (filter: {status_filter})" if status_filter else ""),
                color=discord.Color.blue()
            )
            
            for prop in proposals[:10]:  # Limit to 10
                status = prop.get("status", "unknown")
                status_emoji = {
                    "pending": "🔄", "approved": "✅", "rejected": "❌",
                    "blocked": "🚫", "completed": "🎉"
                }.get(status, "❓")
                
                embed.add_field(
                    name=f"{status_emoji} {prop.get('id', 'unknown')}",
                    value=f"{prop.get('title', 'Untitled')[:50]}\nStatus: {status}",
                    inline=False
                )
            
            if len(proposals) > 10:
                embed.set_footer(text=f"Showing 10 of {len(proposals)} proposals")
            
            await ctx.send(embed=embed)
        
        @self.bot.command(name="vote")
        @commands.has_permissions(administrator=True)
        async def manual_vote(ctx: commands.Context, proposal_id: str, 
                            department: str, decision: str, *, explanation: str = "") -> None:
            """
            !vote <proposal_id> <department> <APPROVE|REJECT|ABSTAIN> [explanation]
            
            Manually record a vote (admin only).
            """
            if decision.upper() not in ["APPROVE", "REJECT", "ABSTAIN"]:
                await ctx.send("❌ Decision must be APPROVE, REJECT, or ABSTAIN")
                return
            
            success = self.kernel.record_vote(
                proposal_id, department, decision.upper(), explanation
            )
            
            if success:
                emoji = {"APPROVE": "✅", "REJECT": "❌", "ABSTAIN": "⏸️"}[decision.upper()]
                await ctx.send(
                    f"{emoji} Vote recorded: **{department}** → **{decision.upper()}** on `{proposal_id}`"
                )
            else:
                await ctx.send(f"❌ Failed to record vote")
        
        @self.bot.command(name="override")
        @commands.has_permissions(administrator=True)
        async def override(ctx: commands.Context, proposal_id: str, action: str) -> None:
            """
            !override <proposal_id> <approve|reject>
            
            Manual override (admin only). Bypasses voting.
            """
            if action.lower() not in ["approve", "reject"]:
                await ctx.send("❌ Action must be 'approve' or 'reject'")
                return
            
            proposal = self.kernel.get_proposal(proposal_id)
            if proposal is None:
                await ctx.send(f"❌ Proposal `{proposal_id}` not found")
                return
            
            # Update proposal status directly
            proposal_file = self.kernel.proposals_path / f"{proposal_id}.json"
            proposal["status"] = "approved" if action.lower() == "approve" else "rejected"
            proposal["override"] = {
                "by": str(ctx.author),
                "action": action.lower(),
                "timestamp": time.time()
            }
            
            with open(proposal_file, "w") as f:
                json.dump(proposal, f, indent=2)
            
            emoji = "✅" if action.lower() == "approve" else "❌"
            await ctx.send(
                f"⚠️ **MANUAL OVERRIDE**\n"
                f"{emoji} Proposal `{proposal_id}` has been **{action.upper()}D** by {ctx.author.mention}\n"
                f"This bypasses the normal voting process."
            )
        
        @self.bot.command(name="execute")
        @commands.has_permissions(administrator=True)
        async def execute_proposal(ctx: commands.Context, proposal_id: str) -> None:
            """
            !execute <proposal_id>
            
            Execute an approved proposal.
            """
            status = self.kernel.check_proposal_status(proposal_id)
            
            if status.get("status") != "approved":
                await ctx.send(
                    f"❌ Cannot execute proposal `{proposal_id}`: Status is **{status.get('status')}**"
                )
                return
            
            await ctx.send(f"⚙️ Executing proposal `{proposal_id}`...")
            
            result = self.kernel.execute_approved(proposal_id)
            
            if result.get("success"):
                await ctx.send(
                    f"🎉 **Proposal Executed Successfully!**\n"
                    f"ID: `{proposal_id}`\n"
                    f"Actions completed: {len(result.get('execution_results', []))}"
                )
            else:
                await ctx.send(
                    f"💥 **Execution Failed**\n"
                    f"ID: `{proposal_id}`\n"
                    f"Reason: {result.get('reason', 'Unknown error')}"
                )
        
        @self.bot.command(name="departments")
        async def list_departments(ctx: commands.Context) -> None:
            """
            !departments
            
            List all AI departments and their voting power.
            """
            departments = self.kernel.kernel_config.get("legion_os", {}).get("departments", [])
            
            embed = discord.Embed(
                title="🏛️ Legion Departments",
                description="AI agents that vote on proposals",
                color=discord.Color.purple()
            )
            
            for dept in departments:
                veto_emoji = "🛡️" if dept.get("veto_power") else ""
                embed.add_field(
                    name=f"{dept.get('name', 'unknown').upper()} {veto_emoji}",
                    value=(
                        f"**Agent:** {dept.get('agent', dept.get('agents', 'N/A'))}\n"
                        f"**Weight:** {dept.get('weight', 1)}\n"
                        f"**Veto Power:** {'Yes' if dept.get('veto_power') else 'No'}\n"
                        f"{dept.get('description', '')}"
                    ),
                    inline=True
                )
            
            rules = self.kernel.kernel_config.get("legion_os", {}).get("voting_rules", {})
            embed.add_field(
                name="📜 Voting Rules",
                value=(
                    f"**Quorum:** {rules.get('quorum', 1)} departments\n"
                    f"**Threshold:** {rules.get('threshold', 0.5):.0%}\n"
                    f"**Timeout:** {rules.get('timeout', 300)}s\n"
                    f"**Veto Blocks:** {'Yes' if rules.get('veto_blocks') else 'No'}"
                ),
                inline=False
            )
            
            await ctx.send(embed=embed)
    
    def _status_color(self, status: str) -> discord.Color:
        """Get embed color based on status."""
        return {
            "pending": discord.Color.yellow(),
            "approved": discord.Color.green(),
            "rejected": discord.Color.red(),
            "blocked": discord.Color.dark_red(),
            "timeout": discord.Color.orange(),
            "executing": discord.Color.blue(),
            "completed": discord.Color.green(),
            "failed": discord.Color.red()
        }.get(status, discord.Color.greyple())
    
    def run(self, token: str | None = None) -> None:
        """Run the Discord bot."""
        token = token or os.getenv("DISCORD_BOT_TOKEN")
        
        if not token:
            raise ValueError(
                "Discord bot token not provided. "
                "Set DISCORD_BOT_TOKEN environment variable or pass token to run()"
            )
        
        self.bot.run(token)


def main() -> None:
    """Main entry point for the Discord bot."""
    if not DISCORD_AVAILABLE:
        print("Error: discord.py is required but not installed")
        print("Install with: pip install discord.py")
        sys.exit(1)
    
    if LegionKernel is None:
        print("Error: LegionKernel not available")
        sys.exit(1)
    
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   Strategickhaos Legions OS - Discord Bot Starting...     ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    bot = LegionDiscordBot()
    bot.run()


if __name__ == "__main__":
    main()
