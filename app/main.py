import sys, traceback, requests, json
from app.config import settings
import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import logging

#inititalize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

description = '''
Nagatha is a work in progressand currently in development by @azcoigreach#0001
Use the (/) slash command to see a list of commands.
If you would like to have your own module writen for Nagatha, please contact @azcoigreach#0001
Current modules include:
 - /battlemetrics - Retrieve server data from battlemetrics.com
 - /crypto - Retrieve crypto currency data from binance.us
 - /help - Get help using Nagatha
 '''

def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ['!!']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow !! to be used in DMs
        return '!!'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)

# list of folders our cogs are in
initial_extensions = [
    'app.cogs.support',
    'app.cogs.system',
    'app.cogs.battlemetrics',
    'app.cogs.crypto',
    'app.cogs.bethesda',
    # 'app.cogs.youtube',
    # 'app.cogs.steam',
    # 'app.cogs.buttons',
    # 'app.cogs.members',
    # 'app.cogs.simple',
    ]

# declare intents
intents = discord.Intents.default()
intents.message_content = True

# checks
def is_system_admin():
        def predicate(interaction: discord.Interaction) -> bool:
            if interaction.user.id in settings.SYSTEM_ADMIN_IDS:
                logging.info(f'is_system_admin check passed by user_id:{interaction.user.id}')
                return True
            else:
                logging.error(f'is_system_admin check failed by user_id:{interaction.user.id}')
                raise app_commands.CheckFailure("I'm sorry Dear. You are not a system admin.")

                # return False
        return app_commands.check(predicate)


class NagathaClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(intents=intents, *args, **kwargs)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        pass
        
# init bot
bot = NagathaClient(description=description)
bot = commands.Bot(command_prefix=get_prefix, description=description, intents=intents)

# ON READY
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="How may I help you?"))
    logging.info(f'Bot Ready - Version: {discord.__version__}')
    logging.info(f'Logged in as: {bot.user.name} - {bot.user.id}')
    logging.info(f'Connected to {len(bot.guilds)} guilds:')
    for guild in bot.guilds:
        await bot.tree.sync(guild=discord.Object(id=guild.id))
        logging.info(f'Synced - {guild.name} - {guild.id}')
    logging.info('--OK--')

# load cogs
async def load_extentions():
    logging.info("Loading extensions...")
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
        except Exception as e:
            logging.error(f'Failed to load extension {extension}.', exc_info=e)
            # traceback.print_exc()

# MAIN
async def main():
    async with bot:
        logging.info("Starting bot...")
        await load_extentions()
        await bot.start(settings.DISCORD_TOKEN)

asyncio.run(main())


