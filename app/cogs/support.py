from app.config import settings
import discord
from discord import app_commands
from discord.ext import commands
import logging

class Support(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    group = app_commands.Group(name='support', description='Support and information for Nagatha', guild_ids=settings.REGISTERED_GUILD_IDS)

    @group.command(name='visit_nagatha', description='Visit Nagtha\'s Discord server for support')
    async def visit_nagatha(self, interaction: discord.Interaction) -> None:
        '''Visit Nagtha's Discord server for support'''
        self.support_link = "https://discord.gg/pM4Z8jjG2y"
        await interaction.response.send_message(f'Nagatha is a custom Bot and constantly under development.\nJoin the support server: {self.support_link}\nPlease report any bugs or issues to @azcoigreach#0001')

    # Ping Nagatha to make sure she's awake
    @group.command(name='ping', description='Ping Nagatha to make sure she\'s awake')
    async def ping(self, interaction: discord.Interaction) -> None:
        """Ping Nagatha"""
        # log guild and channel name ping was sent from
        logging.info(f"Ping from {interaction.guild.name} in {interaction.channel.name}")
        await interaction.response.send_message('Hello Dear.')

async def setup(bot: commands.Bot) -> None:
    for guild_id in settings.REGISTERED_GUILD_IDS:
        logging.info(f'Adding Support to {guild_id}')
        await bot.add_cog(Support(bot), override=True, guild=discord.Object(id=guild_id))