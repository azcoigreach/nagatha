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
        # self.bot.tree.copy_global_to(guild=None)
        # defer response
        await interaction.response.defer(ephemeral=True)
        # self.bot.tree.clear_commands(guild=None)
        for guild in self.bot.guilds:
            self.bot.tree.clear_commands(guild=discord.Object(id=guild.id))
            await self.bot.tree.sync(guild=discord.Object(id=guild.id))
            logging.info(f'Synced - {guild.name} - {guild.id}')
        
        await interaction.followup.send(f'**`SUCCESS`**: Synced commands to {len(self.bot.guilds)} guilds', ephemeral=True)
        logging.info('Commands synced')

    # get command tree list
    @group.command(name='get_tree')
    @is_system_admin()
    async def get_tree(self, interaction: discord.Interaction):
        """Get bot command tree"""
        logging.info(f'Connected to {len(self.bot.guilds)} guilds:')
        for guild in self.bot.guilds:
            logging.info(f'Guild: {guild.name} - {guild.id}')
            command_list = self.bot.tree.get_commands(guild=discord.Object(id=guild.id))
            for command in command_list:
                # display List[Union[ContextMenu, Command, Group]]
                logging.info(f'Command: {command.name} - {command.description}')
                if isinstance(command, discord.app_commands.Group):
                    for subcommand in command.commands:
                        logging.info(f'  Subcommand: {subcommand.name} - {subcommand.description}')
        await interaction.response.send_message(f'**`SUCCESS`**: Got command tree for {len(self.bot.guilds)} guilds', ephemeral=True)

    @group.command(name='clear_tree')
    @is_system_admin()
    async def clear_tree(self, interaction: discord.Interaction):
        """Clear command tree from discord"""
        logging.info(f'Connected to {len(self.bot.guilds)} guilds:')
        # self.bot.tree.copy_global_to(guild=None)
        # defer response
        await interaction.response.defer(ephemeral=True)
        # self.bot.tree.clear_commands(guild=None)
        for guild in self.bot.guilds:
            self.bot.tree.clear_commands(guild=discord.Object(id=guild.id))
            logging.info(f'Cleared - {guild.name} - {guild.id}')
        
        await interaction.followup.send(f'**`SUCCESS`**: Cleared commands from {len(self.bot.guilds)} guilds', ephemeral=True)

    # fetch_commands
    @group.command(name='fetch_global_commands')
    @is_system_admin()
    async def fetch_global_commands(self, interaction: discord.Interaction):
        """Fetch global commands"""
        logging.info(f'Connected to {len(self.bot.guilds)} guilds:')
        # self.bot.tree.copy_global_to(guild=None)
        # defer response
        await interaction.response.defer(ephemeral=True)
        command_list = await self.bot.tree.fetch_commands(guild=None)
        for command in command_list:
            # display List[Union[ContextMenu, Command, Group]]
            logging.info(f'Command: {command.name} - {command.description}')
            if isinstance(command, discord.app_commands.Group):
                for subcommand in command.commands:
                    logging.info(f'  Subcommand: {subcommand.name} - {subcommand.description}')
        await interaction.followup.send(f'**`SUCCESS`**: Retrieved global command tree', ephemeral=True)

    # scrub global commands
    @group.command(name='scrub_and_resync')
    @is_system_admin()
    async def scrub_and_resync(self, interaction: discord.Interaction, discord_id: str):
        """Scrub commands and resync"""
        logging.info(f'Scrubbing commands for {discord_id}')
        # defer response
        await interaction.response.defer(ephemeral=True)
        command_list = await self.bot.tree.fetch_commands(guild=discord.Object(id=discord_id))
        for command in command_list:
            self.bot.tree.remove_command(command=command.name, guild=discord.Object(id=discord_id))
            # display List[Union[ContextMenu, Command, Group]]
            # logging.info(f'Command: {command.name} - {command.description} - {command.type}')
            # if isinstance(command, discord.app_commands.Group):
            #     for subcommand in command.commands:
            #         #remove subcommand
            #         self.bot.tree.remove_command(command=subcommand.name, guild=discord.Object(id=discord_id))
            logging.info(f'Removed command: {command.name} - {command.description} - {command.type}')
        # sync
        await self.bot.tree.sync(guild=discord.Object(id=discord_id))
        await interaction.followup.send(f'**`SUCCESS`**: Scrubbed command tree', ephemeral=True)


async def setup(bot):
    await bot.add_cog(System(bot))