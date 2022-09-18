from app.config import settings
import requests
import json
import discord
from discord import app_commands
from discord.ext import commands
import logging
import random

#discord.py cog that gets crypto price data from binance.us
class Bethesda(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.info('Bethesda cog loaded')
    
    # YouTube commands.  Music. Videos. Channel notifications.
    group = app_commands.Group(name='todd', description='Bethesda discord commands', guild_ids=settings.YOUTUBE_GUILD_IDS)

    '''
    who am i today? RNG charecter generator for Fallout 76 PVP
    RNG for Faction, costume, objectives, wanted status
    '''
    @group.command(name='whoami', description='RNG charecter generator for Fallout 76 PVP')
    async def whoami(self, interaction: discord.Interaction):
        # list of factions
        factions = ['Enclave', 'Brotherhood of Steel', 'Raider', 'Communist', 'Beavis and Butthead', 'South Park']
        # list of costumes from the fallout wiki
        costumes = ['In-game Faction', 'Holiday', 'Clown', 'Civilian', 'Naked', 'Mascot']
        # list of objectives
        objectives = ['Perfect Pie', 'Capture', 'Extortion', 'Build-up Workshop']
        # list of wanted status with weight for more likely to be not wanted
        wanted_status = ['Wanted', 'Not Wanted', 'Not Wanted', 'Not Wanted', 'Not Wanted', 'Not Wanted', 'Not Wanted', 'Not Wanted', 'Not Wanted', 'Not Wanted']
        
        # get random faction
        faction = random.choice(factions)
        # get random costume
        costume = random.choice(costumes)
        # get random objective
        objective = random.choice(objectives)
        # get random wanted status
        wanted = random.choice(wanted_status)

        # send embed message to discord
        embed = discord.Embed(title="Who am I today?", description="RNG charecter generator for Fallout 76 PVP", color=0x00ff00)
        embed.add_field(name='Faction', value=faction, inline=False)
        embed.add_field(name='Costume', value=costume, inline=False)
        embed.add_field(name='Objective', value=objective, inline=False)
        embed.add_field(name='Wanted', value=wanted, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=False)




# add commands to cog
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Bethesda(bot))
