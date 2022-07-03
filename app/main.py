# Get server data from the battlemetrics.com API and send it in a Discord.
# techstack: Python3, discord.py, requests, battlemetrics.com, io, pydantic, json
import sys, traceback
from app.config import settings
import discord
from discord.ext import commands

# This example requires the 'members' and 'message_content' privileged intents to function.

description = '''Nagatha is a multi-function discord bot.
 - Retrieve server data from battlemetrics.com
 - Retrieve crypto currency data from binance.us'''

def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ['>?', 'nagatha ', 'nag ', '!?']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return '?'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)

# list of folders our cogs are in
initial_extensions = [
    'app.cogs.owner',
    'app.cogs.members',
    'app.cogs.simple',
    'app.cogs.server',
    'app.cogs.crypto'
    ]

bot = commands.Bot(command_prefix=get_prefix, description=description)


# discord invite: https://discord.gg/pM4Z8jjG2y
# bot invite link: https://discord.com/api/oauth2/authorize?client_id=992074795854352504&permissions=534723947584&scope=bot
@bot.command()
async def invite(ctx):
    """Invite and support links"""
    bot_link = "https://discord.com/api/oauth2/authorize?client_id=992074795854352504&permissions=534723947584&scope=bot"
    support_link = "https://discord.gg/pM4Z8jjG2y"
    await ctx.send(f"Invite Nagatha to your Discord: {bot_link}\nJoin the support server: {support_link}")

@bot.command()
async def ping(ctx):
    """Ping pong"""
    await ctx.send('Hello Dear.')

# random cat photo from tenor to discord
@bot.command()
async def cat(ctx):
    """Random cat photo"""
    url = "https://api.tenor.com/v1/random?key=LIVDSRZULELA&q=cats&limit=1"
    response = requests.get(url)
    data = json.loads(response.text)
    embed = discord.Embed(title="Random cat photo", color=0x00ff00)
    embed.set_image(url=data['results'][0]['media'][0]['gif']['url'])
    await ctx.send(embed=embed)

# load cogs from initial_extensions
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})\nVersion: {discord.__version__}\n')
    print('------')
    # change discord presence
    await bot.change_presence(activity=discord.Game(name="nagatha help"))
    print(f'Successfully logged in and booted...!')

bot.run(settings.DISCORD_TOKEN)


