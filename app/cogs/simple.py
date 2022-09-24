from app.config import settings
import discord
from discord import app_commands
from discord.ext import commands
import logging

class Simple(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    group = app_commands.Group(name='simple', description='Simple command examples', guild_ids=settings.SYSTEM_ADMIN_GUILD_IDS)

    @group.command(name='repeat')
    async def do_repeat(self, interaction: discord.Interaction, *, our_input: str) -> None:
        """A simple command which repeats our input.
        In rewrite Context is automatically passed to our commands as the first argument after self."""

        await interaction.response.send_message(our_input)

    @group.command(name='add')
    @commands.guild_only()
    async def do_addition(self, interaction: discord.Interaction, first: int, second: int) -> None:
        """A simple command which does addition on two integer values."""

        total = first + second
        await interaction.response.send_message(f'The sum of **{first}** and **{second}**  is  **{total}**')

    @group.command(name='me')
    @commands.is_owner()
    async def only_me(self, interaction: discord.Interaction) -> None:
        """A simple command which only responds to the owner of the bot."""


        await interaction.response.send_message(f'Hello {interaction.user.name}#{interaction.user.discriminator}. This command can only be used by you!!')

    @group.command(name='embeds')
    @commands.guild_only()
    async def example_embed(self, interaction: discord.Interaction) -> None:
        """A simple command which showcases the use of embeds.

        Have a play around and visit the Visualizer."""

        embed = discord.Embed(title='Example Embed',
                              description='Showcasing the use of Embeds...\nSee the visualizer for more info.',
                              colour=0x98FB98)
        embed.set_author(name='MysterialPy',
                         url='https://gist.github.com/MysterialPy/public',
                         icon_url='http://i.imgur.com/ko5A30P.png')
        embed.set_image(url='https://cdn.discordapp.com/attachments/84319995256905728/252292324967710721/embed.png')

        embed.add_field(name='Embed Visualizer', value='[Click Here!](https://leovoel.github.io/embed-visualizer/)')
        embed.add_field(name='Command Invoker', value=interaction.user.mention)
        embed.set_footer(text='Made in Python with discord.py@rewrite', icon_url='http://i.imgur.com/5BFecvA.png')

        await interaction.response.send_message(content='**A simple Embed for discord.py@rewrite in cogs.**', embed=embed)
    
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user) -> None:
        """Event Listener which is called when a user is banned from the guild.
        For this example I will keep things simple and just print some info.
        Notice how because we are in a cog class we do not need to use @bot.event

        For more information:
        http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_member_ban

        Check above for a list of events.
        """

        logging.warning(f'{user.name}-{user.id} was banned from {guild.name}-{guild.id}')

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.
async def setup(bot: commands.Bot) -> None:
    for guild_id in settings.SYSTEM_ADMIN_GUILD_IDS:
        logging.info(f'Adding Simple to {guild_id}')
        await bot.add_cog(Simple(bot), override=True, guild=discord.Object(id=guild_id))