from app.config import settings
import requests
import json
import discord
from discord import app_commands
from discord.ext import commands
import logging
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


#discord.py cog that gets crypto price data from binance.us
class Bethesda(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.info('Bethesda cog loaded')
    
    def set_chrome_options(chrome_options) -> None:
        """Sets chrome options for Selenium.
        Chrome options for headless browser is enabled.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--incognito")
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs 
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        return chrome_options
    

    # Todd commands.  The new and improved Todd Bot - he is actually usefull now.
    group = app_commands.Group(name='todd', description='Bethesda discord commands', guild_ids=settings.BETHESDA_GUILD_IDS)

    '''
    who am i today? RNG charecter generator for Fallout 76 PVP
    RNG for Faction, costume, objectives, wanted status
    '''
    @group.command(name='whoami', description='RNG charecter generator for Fallout 76 PVP')
    async def whoami(self, interaction: discord.Interaction) -> None:
        # list of factions
        roles = ['Brotherhood of Steel', 'Raider', 'Communist', 'Beavis and Butthead', 'South Park', 'Chem Addict', 'Derka Derka', 'Union Shop Steward']
        # list of costumes from the fallout wiki
        costumes = ['In-game Faction', 'Holiday', 'Clown', 'Civilian', 'Naked', 'Mascot']
        # list of objectives
        objectives = ['Perfect Pie', 'Capture', 'Extortion', 'Build-up Workshop', 'Clear Appalacia of Evil', 'Kill the Overseer', 'Got any Chems!?']
        # list of wanted status with weight for more likely to be not wanted
        wanted_status = ['Wanted', 'Not Wanted', 'Not Wanted', 'Not Wanted', 'Not Wanted', 'Not Wanted', 'Not Wanted', 'Not Wanted', 'Not Wanted', 'Not Wanted']
        
        # get random faction
        role = random.choice(roles)
        # get random costume
        costume = random.choice(costumes)
        # get random objective
        objective = random.choice(objectives)
        # get random wanted status
        wanted = random.choice(wanted_status)

        # send embed message to discord
        embed = discord.Embed(title="Who am I today?", description="RNG charecter generator for Fallout 76 PVP", color=0x00ff00)
        embed.add_field(name='Role', value=role, inline=False)
        embed.add_field(name='Costume', value=costume, inline=False)
        embed.add_field(name='Objective', value=objective, inline=False)
        embed.add_field(name='Wanted', value=wanted, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=False)


    '''
    Retrieve the current status of Bethesda games from https://bethesda.net/en/status
    For each class="status-container" div, get the game name from the first div inside status-container and class="operation-status" div inside status-container
    Extract information for Bethesda.net Live Services AND Bethesda Live Games
    use selenium to get the status of the games
    Use beautiful soup to parse the html
    '''
    @group.command(name='server_status', description='Retrieve the current status of Bethesda games')
    async def bethesda_status(self, interaction: discord.Interaction) -> None:
        chrome_options = self.set_chrome_options()
        browser = webdriver.Chrome(options=chrome_options)
        browser.get("https://bethesda.net/en/status")
        # wait for the page to load
        try:
            logging.info('Retrieving status of Bethesda games')
            # interaction deferred until the page loads
            await interaction.response.defer()
            WebDriverWait(driver=browser, timeout=15).until(EC.visibility_of_element_located((By.CLASS_NAME, "status-container")))
        except TimeoutException:
            logging.error("Timed out waiting for page to load")
            # follow up message to interaction
            await interaction.followup.send('Timed out waiting for page to load')
            browser.quit()
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        browser.quit()
        # find all 'status-container' divs
        status_containers = soup.find_all(class_='status-container')
        logging.info('Found %s status containers', len(status_containers))
        '''
        HTML example of status-container
        <div class="status-container"><div>Accounts</div><div class="operational-status">Operational</div></div>
        '''
        # create embed message
        embed = discord.Embed(title="Bethesda Game Status", description="Current status of Bethesda games", color=0x00ff00)
        for container in status_containers:
            game_name = container.find('div').text
            game_status = container.find('div', class_='operational-status').text
            logging.info(f'{game_name} is {game_status}')
            embed.add_field(name=game_name, value=game_status, inline=True)
        # follow up message to interaction
        await interaction.followup.send(embed=embed, ephemeral=False)
        logging.info('Sent status of Bethesda games to discord')
        # await interaction.response.send_message('hello world', ephemeral=False)


# add commands to cog
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Bethesda(bot))
