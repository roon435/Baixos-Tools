import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)
tree = client.tree

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("Slash commands synced.")

@tree.command(name="workingdm", description="DM a user a message multiple times")
@app_commands.describe(user_id="The user ID", message="Message to send", amount="How many times to send")
async def workingdm(interaction: discord.Interaction, user_id: str, message: str, amount: int):
    try:
        user = await client.fetch_user(int(user_id))
        await interaction.response.send_message(f"Sending {amount} DMs to <@{user_id}>...", ephemeral=True)
        for _ in range(amount):
            await user.send(message)
            await asyncio.sleep(1)
    except Exception as e:
        await interaction.followup.send(f"Error: {e}", ephemeral=True)

@tree.command(name="workingecho", description="Echo a message in this channel")
@app_commands.describe(message="Message to echo", amount="How many times to echo")
async def workingecho(interaction: discord.Interaction, message: str, amount: int):
    await interaction.response.send_message("Echoing...", ephemeral=True)
    for _ in range(min(amount, 10)):
        await interaction.channel.send(message)
        await asyncio.sleep(1)

client.run(TOKEN)
