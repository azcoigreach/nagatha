from app.config import settings
import requests
import json
import discord
from discord import app_commands
from discord.ext import commands
import logging

'''
Reference: https://github.com/Rapptz/discord.py/tree/master/examples/views
Docs: https://discordpy.readthedocs.io/en/latest/interactions/api.html?highlight=button#discord.ui.Button
'''

class Buttons(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.info('Buttons cog loaded')
    
    # YouTube commands.  Music. Videos. Channel notifications.
    group = app_commands.Group(name='buttons', description='Dev button examples', guild_ids=settings.BUTTONS_GUILD_IDS)

    class Confirm(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=60.0)

        @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
        async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
            # edit the original message to show a green tick or whatever
            await interaction.response.edit_message(content="Confirmed!", view=None)
            await interaction.response.send_message("Confirmed", ephemeral=True)

        @discord.ui.button(label="Deny", style=discord.ButtonStyle.red)
        async def deny(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message("Denied", ephemeral=True)

    @group.command(name='confirm', description='Confirm button example')
    async def confirm(self, interaction: discord.Interaction) -> None:
        '''Confirm button example'''
        view = self.Confirm()
        await interaction.response.send_message("Are you sure?", view=view)
        await view.wait()
        if view.value is None:
            await interaction.followup.send("Timed out", ephemeral=True)
        elif view.value:
            await interaction.followup.send("Confirmed", ephemeral=True)
        else:
            await interaction.followup.send("Denied", ephemeral=True)

# add commands to cog
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Buttons(bot))
