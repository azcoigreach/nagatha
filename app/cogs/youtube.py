from app.config import settings
import requests
import json
import discord
from discord import app_commands
from discord.ext import commands
import logging

#discord.py cog that gets crypto price data from binance.us
class YouTube(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.info('YouTube cog loaded')
    
    # YouTube commands.  Music. Videos. Channel notifications.
    group = app_commands.Group(name='youtube', description='YouTube music and video', guild_ids=settings.YOUTUBE_GUILD_IDS)


# add commands to cog
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(YouTube(bot))
