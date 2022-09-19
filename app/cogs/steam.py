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
        self.logger.info('Steam cog loaded')
    
    # YouTube commands.  Music. Videos. Channel notifications.
    group = app_commands.Group(name='steam', description='Steam information', guild_ids=settings.STEAM_GUILD_IDS)


# add commands to cog
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Steam(bot))
