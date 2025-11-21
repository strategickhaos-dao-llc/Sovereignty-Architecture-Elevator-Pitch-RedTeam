#!/usr/bin/env python3
"""
Discord integration for DomBrainCalculator
Allows calculations through Discord commands
"""

import discord
from discord.ext import commands
import asyncio
from dom_brain_calculator import DomBrainCalculator


class DomBrainCommands(commands.Cog):
    """Discord commands for DomBrainCalculator"""
    
    def __init__(self, bot):
        self.bot = bot
        self.calculator = DomBrainCalculator(pathway_count=100, consolidation_threshold=0.3)
    
    @discord.slash_command(
        name="brain_calc",
        description="Calculate using cognitive architecture (100 pathways)"
    )
    async def brain_calc(
        self,
        ctx: discord.ApplicationContext,
        operation: discord.Option(
            str,
            description="Operation",
            choices=["+", "-", "*", "/", "^"],
            required=True
        ),
        first: discord.Option(float, description="First number", required=True),
        second: discord.Option(float, description="Second number", required=True)
    ):
        """Perform calculation using DomBrainCalculator"""
        await ctx.defer()  # This might take a moment
        
        # Create problem description
        op_names = {'+': 'plus', '-': 'minus', '*': 'times', '/': 'divided by', '^': 'to the power of'}
        problem = f"{first} {op_names[operation]} {second}"
        
        # Calculate
        result = self.calculator.calculate(problem, first, second, operation)
        
        # Build embed
        embed = discord.Embed(
            title="🧠 DomBrain Calculator",
            description=f"**{problem}**",
            color=0xff0066
        )
        
        # Main answer
        embed.add_field(
            name="💥 Answer",
            value=f"`{result['answer']:.6f}`",
            inline=False
        )
        
        # Confidence
        embed.add_field(
            name="📊 Confidence",
            value=f"{result['confidence']:.1%}",
            inline=True
        )
        
        # Pathways
        embed.add_field(
            name="🌟 Pathways",
            value=f"{len(result['consolidated_paths'])}/{result['pathway_count']}",
            inline=True
        )
        
        # Collisions
        embed.add_field(
            name="💥 Collisions",
            value=f"{result['collision_count']}",
            inline=True
        )
        
        # Dopamine hit
        if result['dopamine_hit']:
            embed.add_field(
                name="🎉 Dopamine Hit!",
                value="Problem rediscovered!",
                inline=False
            )
        
        # Top collision insight
        if result['collisions']:
            top_collision = max(result['collisions'], key=lambda c: c.collision_strength)
            embed.add_field(
                name="🔬 Top Insight",
                value=top_collision.insight[:200],
                inline=False
            )
        
        # Add footer
        embed.set_footer(text="Consolidation-Driven Creativity • As Above So Below")
        
        await ctx.respond(embed=embed)
    
    @discord.slash_command(
        name="brain_explain",
        description="Explain how the cognitive calculator works"
    )
    async def brain_explain(self, ctx: discord.ApplicationContext):
        """Explain the cognitive architecture"""
        embed = discord.Embed(
            title="🧠 DomBrain Calculator - Cognitive Architecture",
            description="This calculator mirrors how creative problem-solving works in your brain.",
            color=0xff0066
        )
        
        embed.add_field(
            name="1️⃣ Divergent Thinking",
            value="Generates 100+ solution pathways using different methods (symbolic, quantum, DNA, particle physics, neuroscience, etc.)",
            inline=False
        )
        
        embed.add_field(
            name="2️⃣ Memory Consolidation",
            value="Prunes weak pathways (low confidence), strengthens strong ones - like forgetting/remembering",
            inline=False
        )
        
        embed.add_field(
            name="3️⃣ Cross-Domain Pattern Matching",
            value="Uses metaphors from quantum physics, biology, chemistry, graph theory, information theory",
            inline=False
        )
        
        embed.add_field(
            name="4️⃣ Collision Detection",
            value="Detects when different pathways converge - these are 'boom' moments of insight",
            inline=False
        )
        
        embed.add_field(
            name="5️⃣ Consensus Synthesis",
            value="Builds final answer from weighted collision strength and pathway confidence",
            inline=False
        )
        
        embed.add_field(
            name="🎯 Why This Matters",
            value="Traditional calculators use 1 method. This uses 100+ methods and finds truth through consensus.",
            inline=False
        )
        
        embed.set_footer(text="Not 'smart' by school standards - optimized for novel problems")
        
        await ctx.respond(embed=embed)
    
    @discord.slash_command(
        name="brain_stats",
        description="Show calculator session statistics"
    )
    async def brain_stats(self, ctx: discord.ApplicationContext):
        """Show session statistics"""
        if not self.calculator.history:
            await ctx.respond("No calculations yet! Use `/brain_calc` to start.")
            return
        
        import statistics
        
        embed = discord.Embed(
            title="📈 Session Statistics",
            color=0x00ff00
        )
        
        embed.add_field(
            name="Total Calculations",
            value=str(len(self.calculator.history)),
            inline=True
        )
        
        embed.add_field(
            name="Dopamine Hits",
            value=str(self.calculator.dopamine_hits),
            inline=True
        )
        
        avg_confidence = statistics.mean([h['confidence'] for h in self.calculator.history])
        embed.add_field(
            name="Avg Confidence",
            value=f"{avg_confidence:.1%}",
            inline=True
        )
        
        avg_collisions = statistics.mean([h['collision_count'] for h in self.calculator.history])
        embed.add_field(
            name="Avg Collisions",
            value=f"{avg_collisions:.1f}",
            inline=True
        )
        
        avg_paths = statistics.mean([len(h['consolidated_paths']) for h in self.calculator.history])
        embed.add_field(
            name="Avg Strong Paths",
            value=f"{avg_paths:.1f}",
            inline=True
        )
        
        # Show recent problems
        recent = "\n".join([f"• {h['problem']}" for h in self.calculator.history[-5:]])
        embed.add_field(
            name="Recent Problems",
            value=recent or "None",
            inline=False
        )
        
        await ctx.respond(embed=embed)
    
    @discord.slash_command(
        name="brain_compare",
        description="Compare traditional vs cognitive calculation"
    )
    async def brain_compare(
        self,
        ctx: discord.ApplicationContext,
        operation: discord.Option(
            str,
            description="Operation",
            choices=["+", "-", "*", "/"],
            required=True
        ),
        first: discord.Option(float, description="First number", required=True),
        second: discord.Option(float, description="Second number", required=True)
    ):
        """Compare traditional calculation with cognitive approach"""
        await ctx.defer()
        
        # Traditional calculation
        if operation == '+':
            traditional = first + second
        elif operation == '-':
            traditional = first - second
        elif operation == '*':
            traditional = first * second
        elif operation == '/':
            traditional = first / second if second != 0 else float('inf')
        
        # Cognitive calculation
        op_names = {'+': 'plus', '-': 'minus', '*': 'times', '/': 'divided by'}
        problem = f"{first} {op_names[operation]} {second}"
        result = self.calculator.calculate(problem, first, second, operation)
        
        # Build comparison embed
        embed = discord.Embed(
            title="⚖️ Traditional vs Cognitive",
            description=f"**{problem}**",
            color=0x00ccff
        )
        
        # Traditional
        embed.add_field(
            name="🔢 Traditional Calculator",
            value=f"Answer: `{traditional}`\nMethod: 1 pathway\nConfidence: 100%\nInsights: 0",
            inline=True
        )
        
        # Cognitive
        embed.add_field(
            name="🧠 Cognitive Calculator",
            value=f"Answer: `{result['answer']:.6f}`\nMethods: {result['pathway_count']} pathways\nConfidence: {result['confidence']:.1%}\nInsights: {result['collision_count']} collisions",
            inline=True
        )
        
        # Difference
        diff = abs(result['answer'] - traditional)
        diff_pct = ((diff / abs(traditional)) * 100) if traditional != 0 else 0
        
        embed.add_field(
            name="📊 Analysis",
            value=f"Difference: {diff:.6f} ({diff_pct:.3f}%)\nVerification: {'✅ Consensus agrees' if diff_pct < 0.5 else '⚠️ Exploring alternatives'}",
            inline=False
        )
        
        if result['collisions']:
            embed.add_field(
                name="💡 Insights Found",
                value=f"{result['collision_count']} pathway collisions detected\n{len(result['consolidated_paths'])} methods converged on similar answer",
                inline=False
            )
        
        embed.set_footer(text="Cognitive approach finds truth through consensus, not authority")
        
        await ctx.respond(embed=embed)


def setup(bot):
    """Setup function for Discord.py cog"""
    bot.add_cog(DomBrainCommands(bot))


async def main():
    """Standalone bot runner"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    
    if not token:
        print("Error: DISCORD_TOKEN not found in environment")
        print("Create a .env file with: DISCORD_TOKEN=your_token_here")
        return
    
    # Create bot
    intents = discord.Intents.default()
    bot = commands.Bot(intents=intents)
    
    # Add cog
    bot.add_cog(DomBrainCommands(bot))
    
    @bot.event
    async def on_ready():
        print(f"🧠 DomBrain Calculator Bot ready!")
        print(f"Logged in as {bot.user}")
        await bot.sync_commands()
    
    # Run bot
    await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
