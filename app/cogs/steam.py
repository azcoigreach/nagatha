from app.config import settings
import requests
import json
import discord
from discord import app_commands
from discord.ext import commands
import logging

# https://developer.valvesoftware.com/wiki/Steam_Web_API

class Steam(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger(__name__)
    
    # YouTube commands.  Music. Videos. Channel notifications.
    group = app_commands.Group(name='steam', description='Steam information', guild_ids=settings.STEAM_GUILD_IDS)


    # Steam games subcommand to list all games
    @group.command(name='list', description='List all Steam games')
    async def list(self, interaction: discord.Interaction) -> None:
        logging.info(f'List all Steam games')
        await interaction.response.send_message(f'List all Steam games', ephemeral=True)
    
    # Steam games subcommand to show game stats
    @group.command(name='stats', description='Show Steam game stats')
    async def stats(self, interaction: discord.Interaction, game: str) -> None:
        logging.info(f'Show Steam game stats: {game}')
        await interaction.response.send_message(f'Show Steam game stats: {game}', ephemeral=True)




# add commands to cog
async def setup(bot: commands.Bot) -> None:
    for guild_id in settings.STEAM_GUILD_IDS:
        logging.info(f'Adding Steam to {guild_id}')
        await bot.add_cog(Steam(bot), override=True, guild=discord.Object(id=guild_id))
