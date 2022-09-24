from app.config import settings
import requests
import json
import discord
from discord import app_commands
from discord.ext import commands
import logging
from typing import List

'''
Reference: https://github.com/Rapptz/discord.py/tree/master/examples/views
Docs: https://discordpy.readthedocs.io/en/latest/interactions/api.html?highlight=button#discord.ui.Button
'''

class Buttons(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger(__name__)
    
    # YouTube commands.  Music. Videos. Channel notifications.
    group = app_commands.Group(name='buttons', description='Dev button examples', guild_ids=settings.SYSTEM_ADMIN_GUILD_IDS)

    '''
    Confirm Button Example: https://github.com/Rapptz/discord.py/blob/master/examples/views/confirm.py
    '''
    class Confirm(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=60.0)
            self.value = None

        # When the confirm button is pressed, set the inner value to `True` and
        # stop the View from listening to more input.
        # We also send the user an ephemeral message that we're confirming their choice.
        @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
        async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message('Confirming')
            self.value = True
            self.stop()

        # This one is similar to the confirmation button except sets the inner value to `False`
        @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message('Cancelling')
            self.value = False
            self.stop()


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


    # Define a simple View that gives us a counter button
    class Counter(discord.ui.View):
        # Define the actual button
        # When pressed, this increments the number displayed until it hits 5.
        # When it hits 5, the counter button is disabled and it turns green.
        # note: The name of the function does not matter to the library
        @discord.ui.button(label='0', style=discord.ButtonStyle.red)
        async def count(self, interaction: discord.Interaction, button: discord.ui.Button):
            number = int(button.label) if button.label else 0
            if number + 1 >= 5:
                button.style = discord.ButtonStyle.green
                button.disabled = True
            button.label = str(number + 1)

            # Make sure to update the message with our updated selves
            await interaction.response.edit_message(view=self)

    @group.command(name='counter', description='Counter button example')
    async def counter(self, interaction: discord.Interaction) -> None:
        '''Counter button example'''
        view = self.Counter()
        await interaction.response.send_message("Counter example", view=view)



# add commands to cog
async def setup(bot: commands.Bot) -> None:
    for guild_id in settings.SYSTEM_ADMIN_GUILD_IDS:
        logging.info(f'Adding Buttons to {guild_id}')
        await bot.add_cog(Buttons(bot), override=True, guild=discord.Object(id=guild_id))