from app.config import settings
import requests
import json
import discord
from discord import app_commands
from discord.ext import commands
import logging

#discord.py cog that gets YouTube channel information

class YouTube(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger(__name__)
    
    # YouTube commands.  Music. Videos. Channel notifications.
    group = app_commands.Group(name='youtube', description='YouTube music and video', guild_ids=settings.YOUTUBE_GUILD_IDS)

    # Bot joins voice channel and plays playlist
    @group.command(name='play', description='Play YouTube playlist')
    async def play(self, interaction: discord.Interaction, playlist: str) -> None:
        logging.info(f'Play playlist: {playlist}')
        await interaction.response.send_message(f'Play playlist: {playlist}', ephemeral=True)

    # Bot searches for video and plays it
    @group.command(name='search', description='Search for YouTube video')
    async def search(self, interaction: discord.Interaction, video: str) -> None:
        logging.info(f'Search video: {video}')
        await interaction.response.send_message(f'Search video: {video}', ephemeral=True)



# add commands to cog
async def setup(bot: commands.Bot) -> None:
    for guild_id in settings.YOUTUBE_GUILD_IDS:
        logging.info(f'Adding YouTube to {guild_id}')
        await bot.add_cog(YouTube(bot), override=True, guild=discord.Object(id=guild_id))