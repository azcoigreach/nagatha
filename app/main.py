import sys, traceback, requests, json
from app.config import settings
import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import logging

#inititalize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


# This example requires the 'members' and 'message_content' privileged intents to function.

description = '''Nagatha is a multi-function discord bot.
 - Retrieve server data from battlemetrics.com
 - Retrieve crypto currency data from binance.us'''

def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ['!!', 'nagatha ', 'nag ']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow !! to be used in DMs
        return '!!'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)

# list of folders our cogs are in
initial_extensions = [
    'app.cogs.system',
    'app.cogs.members',
    'app.cogs.simple',
    'app.cogs.battlemetrics',
    'app.cogs.crypto'
    ]

# declare intents
intents = discord.Intents.default()
intents.message_content = True
# intents.members = True


NAGATHA_GUILD = discord.Object(id=settings.GUILD_ID)

class NagathaClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(intents=intents, *args, **kwargs)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=NAGATHA_GUILD)
        await self.tree.sync(guild=NAGATHA_GUILD)
        logging.info('Global commands synced')

bot = NagathaClient(description=description)
bot = commands.Bot(command_prefix=get_prefix, description=description, intents=intents)

# discord invite: https://discord.gg/pM4Z8jjG2y
# bot invite link: https://discord.com/api/oauth2/authorize?client_id=992074795854352504&permissions=534723947584&scope=bot
# @bot.tree.command()
# async def invite(interaction: discord.Interaction):
#     """Invite and support links"""
#     bot_link = "https://discord.com/api/oauth2/authorize?client_id=992074795854352504&permissions=534723947584&scope=bot"
#     support_link = "https://discord.gg/pM4Z8jjG2y"
#     await interaction.response.send_message(f"Invite Nagatha to your Discord: {bot_link}\nJoin the support server: {support_link}")

# Ping Nagatha to make sure she's awake
@bot.tree.command()
async def ping(interaction: discord.Interaction):
    """Ping Nagatha"""
    # log guild and channel name ping was sent from
    logging.info(f"Ping from {interaction.guild.name} in {interaction.channel.name}")
    await interaction.response.send_message('Hello Dear.')

# random cat photo from tenor to discord
@bot.tree.command()
async def cat(interaction: discord.Interaction):
    """Random cat photo"""
    url = "https://api.tenor.com/v1/random?key=LIVDSRZULELA&q=cats&limit=1"
    response = requests.get(url)
    data = json.loads(response.text)
    embed = discord.Embed(title="Random cat photo", color=0x00ff00)
    embed.set_image(url=data['results'][0]['media'][0]['gif']['url'])
    await interaction.response.send_message(embed=embed)

# Sync bot commands to discord
# only works in guild with id = settings.GUILD_ID
# @bot.tree.command()
# @app_commands.guilds(discord.Object(id=settings.GUILD_ID))
# async def sync_commands(interaction: discord.Interaction):
#     """Sync bot commands to discord"""
#     await bot.tree.sync(guild=None)
#     await interaction.response.send_message('Commands synced')
#     logging.info('Commands synced')

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user} (ID: {bot.user.id})\nVersion: {discord.__version__}\n')
    # print('------')
    # change discord presence
    await bot.change_presence(activity=discord.Game(name="How may I help you?"))
    # sync commands to discord
    await bot.tree.sync(guild=None)
    logging.info(f'Successfully logged in and booted...!')

async def load_extentions():
    logging.info("Loading extensions...") # make bright red
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
        except Exception as e:
            logging.error(f'Failed to load extension {extension}.', exc_info=e)
            traceback.print_exc()

async def main():
    async with bot:
        await load_extentions()
        await bot.start(settings.DISCORD_TOKEN)
        

asyncio.run(main())


