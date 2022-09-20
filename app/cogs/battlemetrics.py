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

    class BattleMetricsView(discord.ui.View):
        def __init__(self, data: dict):
            super().__init__(timeout=60.0)

            self.data = data

        @discord.ui.button(label="Previous", custom_id="bm:prev", style=discord.ButtonStyle.grey)
        async def prev(self, button: discord.ui.Button, interaction: discord.Interaction):

            updated_data = await self.get_game_list(self, self.data['links']['prev'])
            updated_embed = await self.game_list_embed(updated_data)
            await interaction.response.edit_message(embed=updated_embed ,view=self)


        @discord.ui.button(label="Next", custom_id="bm:next", style=discord.ButtonStyle.grey)
        async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
            updated_data = await self.get_game_list(self, self.data['links']['next'])
            updated_embed = await self.game_list_embed(updated_data)
            await interaction.response.edit_message(embed=updated_embed ,view=self)
            # await interaction.response.edit_message('Next')


            # if 'prev' not in self.data['links']:
            #     self.add_item(discord.ui.Button(label='Previous', custom_id='prev', disabled=True))
            # else:
            #     self.add_item(discord.ui.Button(label='Previous', custom_id='prev'))

            # if 'next' not in self.data['links']:
            #     self.add_item(discord.ui.Button(label='Next', custom_id='next', disabled=True))
            # else:
            #     self.add_item(discord.ui.Button(label='Next', custom_id='next'))

            # if 'next' not in self.data['links']:
            #     @discord.ui.button(label="Next", custom_id="bm:next", disabled=True)
            #     async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
            #         pass

            # else:
            #     @discord.ui.button(label="Next", custom_id="bm:next")
            #     async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
            #         updated_data = await self.update_data(self.data['links']['next'])
            #         await interaction.response.edit_message(embed=Battlemetrics.game_list_embed(updated_data) ,view=self)



            # # if self.data is not None:
            # logging.info(f"BattleMetricsView data: {self.data}")
            # if 'prev' not in self.view.data['links']:
            #     # self.add_item(discord.ui.Button(label="Prev", disabled=True))
            #     @discord.ui.button(label="Previous", custom_id="bm:prev" ,disabled=True)
            #     async def prev(self, button: discord.ui.Button, interaction: discord.Interaction):
            #         pass
                
            # else:
            #     @discord.ui.button(label="Previous", custom_id="bm:prev")
            #     async def prev(self, button: discord.ui.Button, interaction: discord.Interaction):
            #         updated_data = await Battlemetrics.get_game_list(self, self.data['links']['prev'])
            #         updated_embed = await Battlemetrics.game_list_embed(updated_data)
            #         await interaction.response.edit_message(embed=updated_embed ,view=self)

            # if 'next' not in self.data['links']:
            #     @discord.ui.button(label="Next", custom_id="bm:next", disabled=True)
            #     async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
            #         pass

            # else:
            #     @discord.ui.button(label="Next", custom_id="bm:next")
            #     async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
            #         updated_data = await self.update_data(self.data['links']['next'])
            #         await interaction.response.edit_message(embed=Battlemetrics.game_list_embed(updated_data) ,view=self)


    async def get_game_list(self, url, interaction: discord.Interaction) -> None:
        try:
            await interaction.response.defer()
            logging.info(f"Connecting to {url}")
            game_list = requests.get(url)
            data = json.loads(game_list.text)

            return data
        except Exception as e:
            logging.error(e)
            await interaction.followup.send(f"Error: {e}", ephemeral=True)

    async def game_list_embed(self, data: dict) -> discord.Embed:
        embed = discord.Embed(title="Battlemetrics Games", description="List of games and ids", color=0x00ff00)
        for game in data['data']:
            embed.add_field(name=game['attributes']['name'], value=game['id'], inline=True)
        logging.info(f"Embed created")
        return embed

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
    async def list_games(self, interaction: discord.Interaction) -> None:
        """List battlemetrics games and ids"""
        logging.info(f'Attempting to list battlemetrics games')
        try:
            page_size = 24
            url = f"https://api.battlemetrics.com/games?page[size]={page_size}&fields[game]=name"
            data = await self.get_game_list(url, interaction)
            embed = await self.game_list_embed(data)
            view = Battlemetrics.BattleMetricsView(data)
            logging.info(f"Sending embed to {interaction.user} in {interaction.channel}")
            await interaction.followup.send(embed=embed, view=view ,ephemeral=True)
            # await view.wait()
        except Exception as e:
            logging.error(e)
            await interaction.followup.send(f"Ooops. Something went wrong.", ephemeral=True)



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Battlemetrics(bot))


