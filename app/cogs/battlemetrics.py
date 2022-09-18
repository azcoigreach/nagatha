from app.config import settings
import discord
from discord import app_commands
from discord.ext import commands, tasks
import logging
import requests
import json
from io import BytesIO
import prettyprint as pp

'''
Reference: https://www.battlemetrics.com/developers/documentation
'''

class Battlemetrics(commands.Cog):
    """battlemetrics.com server info"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.info('battlemetrics cog loaded')

    group = app_commands.Group(name='battlemetrics', description='battlemetrics.com server info', guild_ids=settings.BATTLEMETRICS_GUILD_IDS)

    '''
    Get battalemetrics game list and return a list of games by page with a max of 10 games per page
    use endpoint /games
    list results in a discord embed
    cURL example: 
    $ curl -n https://api.battlemetrics.com/games
      -G \
        -d page[size]=42 \
        -d page[key]=100 \
        -d page[rel]=next \
        -d fields[game]=name
    
    include buttons for PREV and NEXT from data
    {'data: 'links': {'prev': 'https://api.battlemetrics.com/games?page%5Bsize%5D=10&page%5Bkey%5D=7dtd&page%5Brel%5D=prev&fields%5Bgame%5D=name', 
    'next': 'https://api.battlemetrics.com/games?page%5Bsize%5D=10&page%5Bkey%5D=csgo&page%5Brel%5D=next&fields%5Bgame%5D=name'}}
    update list with new data when pressed
    '''
    @group.command(name='list_games')
    async def games(self, interaction: discord.Interaction) -> None:
        """List battlemetrics games and ids"""
        url = "https://api.battlemetrics.com/games"
        params = {'page[size]': 10, 'fields[game]': 'name'}
        logging.info(f"Connecting to {url}")
        response = requests.get(url, params=params)
        data = json.loads(response.text)
        # logging.info(data)
        embed = discord.Embed(title="BattleMetrics.com Game List", color=0x00ff00)
        #add column titles
        embed.add_field(name='Game', value='Name', inline=False)
        for i in range(10):
            embed.add_field(name=data['data'][i]['attributes']['name'], value=data['data'][i]['id'], inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=False)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Battlemetrics(bot))


