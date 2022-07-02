# Get server data from the battlemetrics.com API and send it in a Discord.
# techstack: Python3, discord.py, requests, battlemetrics.com

from app.config import settings
import requests
import json
import discord
from discord.ext import commands


description = '''Nagath is a bot that send you battlemetrics.com server data in Discord.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=';', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


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

@bot.command(name = "ping", description = "Pong!"):
async def ping(self, ctx):
    await ctx.send("Pong!")

bot.run(settings.DISCORD_TOKEN)