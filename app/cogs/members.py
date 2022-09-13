import discord
from discord import app_commands
from discord.ext import commands
import logging


class Members(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.info('Members cog loaded')
    
    group = app_commands.Group(name='members', description='Member commands')

    @group.command(name='joined')
    @commands.guild_only()
    async def joined(self, interaction: discord.Interaction,*, member: discord.Member):
        """Says when a member joined."""
        await interaction.response.send_message(f'{member.display_name} joined on {member.joined_at}', ephemeral=True)

    @group.command(name='top_role')
    @commands.guild_only()
    async def show_toprole(self, interaction: discord.Interaction,*, member: discord.Member=None):
        """Simple command which shows the members Top Role."""

        if member is None:
            member = interaction.user

        await interaction.response.send_message(f'The top role for {member.display_name} is {member.top_role.name}', ephemeral=True)
    
    @group.command(name='permissions')
    @commands.guild_only()
    async def check_permissions(self, interaction: discord.Interaction,*, member: discord.Member=None):
        """Checks a members Guild Permissions.
        If member is not provided, the author will be checked."""

        if not member:
            member = interaction.user

        # Here we check if the value of each permission is True.
        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        # And to make it look nice, we wrap it in an Embed.
        embed = discord.Embed(title='Permissions for:', description=member.name, colour=member.colour)
        # embed.set_author(icon_url=member.avatar_url, name=str(member))

        # \uFEFF is a Zero-Width Space, which basically allows us to have an empty field name.
        embed.add_field(name='\uFEFF', value=perms)
        await interaction.response.send_message(content=None, embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Members(bot))