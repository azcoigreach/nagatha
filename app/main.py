# Get server data from the battlemetrics.com API and send it in a Discord.
# techstack: Python3, discord.py, requests, battlemetrics.com

from app.config import settings
import requests
import json
import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='>', intents=intents)

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

@bot.command()
async def ping(ctx):
    await ctx.send('Hello dear.')

@bot.listen
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(settings.DISCORD_TOKEN)