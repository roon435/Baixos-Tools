import discord
from discord import app_commands
import os
import asyncio

MY_GUILD_ID = 1397768752023470100

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        guild = discord.Object(id=MY_GUILD_ID)
        self.tree.clear_commands(guild=guild)
        await self.tree.sync(guild=guild)
        print(f"Commands synced to guild {MY_GUILD_ID}")

client = MyBot()

@client.tree.command(name="workingdm", description="DM a user multiple times by user ID")
@app_commands.guilds(discord.Object(id=MY_GUILD_ID))
@app_commands.describe(
    user_id="User ID to DM",
    message="Message to send",
    amount="How many times",
    speed_ms="Delay between messages (in milliseconds)"
)
async def workingdm(
    interaction: discord.Interaction,
    user_id: str,
    message: str,
    amount: int,
    speed_ms: int = 500  # Default 500ms
):
    await interaction.response.defer(ephemeral=True)
    try:
        user = await client.fetch_user(int(user_id))
        for _ in range(amount):
            await user.send(message)
            await asyncio.sleep(speed_ms / 1000)  # convert ms to seconds
        await interaction.followup.send(
            f"Sent {amount} messages to {user.name} with {speed_ms}ms delay.",
            ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(f"Failed to DM user: {e}", ephemeral=True)

@client.tree.command(name="workingecho", description="Echo a message multiple times in channel")
@app_commands.guilds(discord.Object(id=MY_GUILD_ID))
@app_commands.describe(
    message="Message to echo",
    amount="How many times",
    speed_ms="Delay between messages (in milliseconds)"
)
async def workingecho(
    interaction: discord.Interaction,
    message: str,
    amount: int,
    speed_ms: int = 300  # Default 300ms
):
    await interaction.response.defer()
    for _ in range(amount):
        await interaction.channel.send(message)
        await asyncio.sleep(speed_ms / 1000)  # convert ms to seconds
    await interaction.followup.send(
        f"Echoed {amount} messages with {speed_ms}ms delay.",
        ephemeral=True
    )

client.run(os.getenv("DISCORD_TOKEN"))
