# import modules
from app.config import settings
import discord
from discord.ext import commands, tasks
import requests
import json
from io import BytesIO
import prettyprint as pp

class ServerInfo(commands.Cog):
    """v-rising server info"""
    def __init__(self, bot):
        self.bot = bot

    # battlemetrics.com/servers/vrising/15443201
    def get_battlemetrics_data(self):
        url = "https://api.battlemetrics.com/servers/{}".format(settings.SERVER_ID)
        headers = {
            'Authorization': 'Bearer {}'.format(settings.API_KEY),
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        server_data = json.loads(response.text)
        return server_data

    @commands.group()
    async def vrising(self, ctx):
        """v-rising server info"""
        server_data = self.get_battlemetrics_data()
        ctx.server_name = server_data['data']['attributes']['name']
        ctx.server_id = server_data['data']['id']
        ctx.server_players = server_data['data']['attributes']['players']
        ctx.server_maxPlayers = server_data['data']['attributes']['maxPlayers']
        ctx.server_rank = server_data['data']['attributes']['rank']
        ctx.server_status = server_data['data']['attributes']['status']
        ctx.server_settings = server_data['data']['attributes']['details']['vrising_settings']

        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title=ctx.server_name,
            description="Game server status", 
            color=0x00ff00,
            url="https://battlemetrics.com/servers/vrising/15443201")
            embed.add_field(name="Status", value=ctx.server_status, inline=True)
            embed.add_field(name="Server ID", value=ctx.server_id, inline=True)
            embed.add_field(name="Players", value=f"{ctx.server_players} of {ctx.server_maxPlayers}", inline=True)
            embed.add_field(name="Rank", value=ctx.server_rank, inline=True)
            await ctx.send(embed=embed)

    @vrising.command(name='settings')
    async def _settings(self, ctx):
        """server settings"""
        pprint_data = pp(ctx.server_settings).encode('utf-8')
        await ctx.send(file=discord.File(BytesIO(pprint_data), filename='settings.json'))

def setup(bot):
    bot.add_cog(ServerInfo(bot))



# # vrising group command shows server information in discord embed format
# @bot.group()
# async def vrising(ctx):
#     """v-rising server info"""
#     server_data = get_battlemetrics_data()
#     ctx.server_name = server_data['data']['attributes']['name']
#     ctx.server_id = server_data['data']['id']
#     ctx.server_players = server_data['data']['attributes']['players']
#     ctx.server_maxPlayers = server_data['data']['attributes']['maxPlayers']
#     ctx.server_rank = server_data['data']['attributes']['rank']
#     ctx.server_status = server_data['data']['attributes']['status']
#     ctx.server_settings = server_data['data']['attributes']['details']['vrising_settings']


#     if ctx.invoked_subcommand is None:
#         embed = discord.Embed(title=ctx.server_name,
#         description="Game server status", 
#         color=0x00ff00,
#         url="https://battlemetrics.com/servers/vrising/15443201")
#         embed.add_field(name="Status", value=ctx.server_status, inline=True)
#         embed.add_field(name="Server ID", value=ctx.server_id, inline=True)
#         embed.add_field(name="Players", value=f"{ctx.server_players} of {ctx.server_maxPlayers}", inline=True)
#         embed.add_field(name="Rank", value=ctx.server_rank, inline=True)
#         await ctx.send(embed=embed)

# # retrieve vrising_settings from battlemetrics.com
# # send json string with BytesIO as file to discord
# @vrising.command(name='settings')
# async def _settings(ctx):
#     """server settings"""
#     pprint_data = pp(ctx.server_settings).encode('utf-8')
#     await ctx.send(file=discord.File(BytesIO(pprint_data), filename='settings.json'))



