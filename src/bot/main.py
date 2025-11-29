import os
import sys
import discord
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"[{datetime.now()}] {client.user} is online - PONG-001 alive")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!ping'):
        await message.reply(f"pong @ {datetime.now().isoformat()}")


token = os.getenv("DISCORD_TOKEN")
if not token:
    print("Error: DISCORD_TOKEN environment variable is not set")
    sys.exit(1)

client.run(token)
