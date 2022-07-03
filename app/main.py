# Get server data from the battlemetrics.com API and send it in a Discord.
# techstack: Python3, discord.py, requests, battlemetrics.com

from app.config import settings
import requests
import json
import discord
from discord.ext import commands
import random

# This example requires the 'members' and 'message_content' privileged intents to function.

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
# intents.message_content = True

bot = commands.Bot(command_prefix=';', description=description, intents=intents)


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



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def add(ctx):
    """v-rising stats"""
    await ctx.send(get_battlemetrics_data()['data']['attributes']['name'])

# @bot.command()
# async def add(ctx, left: int, right: int):
#     """Adds two numbers together."""
#     await ctx.send(left + right)


# @bot.command()
# async def roll(ctx, dice: str):
#     """Rolls a dice in NdN format."""
#     try:
#         rolls, limit = map(int, dice.split('d'))
#     except Exception:
#         await ctx.send('Format has to be in NdN!')
#         return

#     result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
#     await ctx.send(result)


# @bot.command(description='For when you wanna settle the score some other way')
# async def choose(ctx, *choices: str):
#     """Chooses between multiple choices."""
#     await ctx.send(random.choice(choices))


# @bot.command()
# async def repeat(ctx, times: int, content='repeating...'):
#     """Repeats a message multiple times."""
#     for i in range(times):
#         await ctx.send(content)


# @bot.command()
# async def ping(ctx):
#     """Ping pong"""
#     await ctx.send('Hello Dear.')


# @bot.command()
# async def joined(ctx, member: discord.Member):
#     """Says when a member joined."""
#     await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


# @bot.group()
# async def cool(ctx):
#     """Says if a user is cool.

#     In reality this just checks if a subcommand is being invoked.
#     """
#     if ctx.invoked_subcommand is None:
#         await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


# @cool.command(name='bot')
# async def _bot(ctx):
#     """Is the bot cool?"""
#     await ctx.send('Yes, the bot is cool.')


bot.run(settings.DISCORD_TOKEN)