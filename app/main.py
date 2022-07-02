# Get server data from the battlemetrics.com API and send it in a Discord.
# techstack: Python3, discord.py, requests, battlemetrics.com

from app.config import settings
import requests
import json
import discord
from discord import app_commands

class client(discord.Client):
    async def startup(self):
        await self.wait_until_ready()
        await tree.sync(guild = discord.Object(id = settings.GUILD_ID))
        print('Ready!')

nagatha = client()
tree = app_commands.CommandTree(name='tree', invoke_without_command=True)


# battlemetrics.com/servers/vrising/15443201
def get_battlemetrics_data():
    url = "https://api.battlemetrics.com/servers/{}".format(settings.SERVER_ID)
    headers = {
        'Authorization': 'Bearer {}'.format(settings.API_KEY),
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    server_data = json.loads(response.text)
    return server_data

@tree.command(guild = settings.GUILD_ID, name = "ping", description = "Pong!"):
async def ping(self, ctx):
    await ctx.send("Pong!")

nagatha.run(settings.DISCORD_TOKEN)