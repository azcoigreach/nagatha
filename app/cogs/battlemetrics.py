from app.config import settings
import discord
from discord.ext import commands, tasks
import requests
import json
from io import BytesIO
import prettyprint as pp

class ServerInfo(commands.Cog):
    """battlemetrics.com server info"""
    def __init__(self, bot):
        self.bot = bot

    # battlemetrics.com/servers/15443201
    def get_server_info(self):
        url = "https://api.battlemetrics.com/servers/{}".format(settings.SERVER_ID)
        headers = {
            'Authorization': 'Bearer {}'.format(settings.API_KEY),
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        server_info = json.loads(response.text)
        return server_info

    # battlemetrics.com/servers/15443201/relationships/leaderboards/time
    def get_server_leaderboard(self):
        url = "https://api.battlemetrics.com/servers/{}/relationships/leaderboards/time".format(settings.SERVER_ID)
        headers = {
            'Authorization': 'Bearer {}'.format(settings.API_KEY),
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        server_leaderboard = json.loads(response.text)
        return server_leaderboard

    @commands.group()
    async def server(self, ctx):
        """battlemetrics server info"""
        server_info = self.get_server_info()
        ctx.server_name = server_info['data']['attributes']['name']
        ctx.server_id = server_info['data']['id']
        ctx.server_players = server_info['data']['attributes']['players']
        ctx.server_maxPlayers = server_info['data']['attributes']['maxPlayers']
        ctx.server_rank = server_info['data']['attributes']['rank']
        ctx.server_status = server_info['data']['attributes']['status']
        ctx.server_settings = server_info['data']['attributes']['details']['vrising_settings']

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

    @server.command(name='settings')
    async def _settings(self, ctx):
        """server settings"""
        pprint_data = pp(ctx.server_settings).encode('utf-8')
        await ctx.send(file=discord.File(BytesIO(pprint_data), filename='settings.json'))

    @server.command(name='leaderboard')
    async def _players(self, ctx):
        """server leaderboard"""
        url = "https://api.battlemetrics.com/servers/{}/relationships/leaderboards/time".format(settings.SERVER_ID)
        headers = {
            'Authorization': 'Bearer {}'.format(settings.API_KEY),
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        server_info = json.loads(response.text)
        embed = discord.Embed(title=ctx.server_name,
        description="Game server leaderboard", 
        color=0x00ff00,
        url="https://battlemetrics.com/servers/vrising/15443201")
        for player in server_info['data']:
            embed.add_field(name=player['attributes']['name'], value=player['attributes']['score'], inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ServerInfo(bot))


