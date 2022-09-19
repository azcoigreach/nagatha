from app.config import settings
import discord
from discord import app_commands
from discord.ext import commands
import logging

class System(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.info('System cog loaded')
    
    def is_system_admin():
        def predicate(interaction: discord.Interaction) -> bool:
            if interaction.user.id in settings.SYSTEM_ADMIN_IDS:
                logging.info(f'is_system_admin check passed by user_id:{interaction.user.id}')
                return True
            else:
                logging.error(f'is_system_admin check failed by user_id:{interaction.user.id}')
                raise app_commands.CheckFailure("I'm sorry Dear. You are not a system admin.")
        return app_commands.check(predicate)


    group = app_commands.Group(name='module', description='System module commands', guild_ids=settings.SYSTEM_ADMIN_GUILD_IDS)

    # Hidden commands - not visible in HELP.
    @group.command(name='load')
    @is_system_admin()
    async def load(self, interaction: discord.Interaction, *, cog: str):
        """Command which Loads a Module."""
        logging.info(f'Attempting to load cog:{cog}')
        try:
            await self.bot.load_extension(cog)
        except Exception as e:
            await interaction.response.send_message(f'**`ERROR:`** {type(e).__name__} - {e}', ephemeral=True)
        else:
            await interaction.response.send_message(f'**`SUCCESS`**: Loaded {cog}', ephemeral=True)
            

    @group.command(name='unload')
    @is_system_admin()
    async def unload(self, interaction: discord.Interaction, *, cog: str):
        """Command which Unloads a Module."""
        logging.info(f'Attempting to unload cog: {cog}')
        try:
           await self.bot.unload_extension(cog)
        except Exception as e:
            await interaction.response.send_message(f'**`ERROR:`** {type(e).__name__} - {e}', ephemeral=True)
        else:
            await interaction.response.send_message(f'**`SUCCESS`**: Unloaded {cog}', ephemeral=True)
            
    '''
    reload command
    check if user is system admin
    '''
    @group.command(name='reload', description='Reloads a Module.')
    @is_system_admin()
    async def reload(self, interaction: discord.Interaction, *, cog: str):
        """Command which Reloads a Module."""
        logging.info(f'Attempting to reload cog: {cog}')
        try:
            await self.bot.reload_extension(cog)
        except Exception as e:
            await interaction.response.send_message(f'**`ERROR:`** {type(e).__name__} - {e}', ephemeral=True)
        else:
            await interaction.response.send_message(f'**`SUCCESS`**: Reloaded {cog}', ephemeral=True)
            

    
    @group.command(name='sync')
    @is_system_admin()
    async def sync_commands(self, interaction: discord.Interaction):
        """Sync bot commands to discord"""
        logging.info(f'Connected to {len(self.bot.guilds)} guilds:')
        # bot.tree.copy_global_to(guild=NAGATHA_GUILD)
        for guild in self.bot.guilds:
            await self.bot.tree.sync(guild=discord.Object(id=guild.id))
            logging.info(f'Synced - {guild.name} - {guild.id}')
        await interaction.response.send_message(f'**`SUCCESS`**: Synced commands to {len(self.bot.guilds)} guilds', ephemeral=True)

        logging.info('Commands synced')


async def setup(bot):
    await bot.add_cog(System(bot))