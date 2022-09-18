from app.config import settings
import requests
import json
import discord
from discord import app_commands
from discord.ext import commands
import logging

#discord.py cog that gets crypto price data from binance.us
class Crypto(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.info('Crypto cog loaded')

    group = app_commands.Group(name='crypto', description='Crypto currency data', guild_ids=settings.CRYPTO_GUILD_IDS)

    @group.command(name='top')
    async def markets(self, interaction: discord.Interaction):
        """Top 10 crypto coins markets"""
        url = "https://api.binance.us/api/v3/ticker/24hr"
        logging.info(f"Connecting to {url}")
        response = requests.get(url)
        data = json.loads(response.text)
        embed = discord.Embed(title="Top 10 coins by volume", color=0x00ff00)
        for i in range(10):
            embed.add_field(name=data[i]['symbol'], value=data[i]['lastPrice'], inline=True)
        await interaction.response.send_message(embed=embed)

    @group.command(name='price')
    async def crypto_price(self, interaction: discord.Interaction, crypto_pair: str) -> None:
        """Get crypto price ex: /crypto price BTCUSDT"""
        url = "https://api.binance.us/api/v3/ticker/24hr?symbol={}".format(crypto_pair)
        # params = {'symbol': crypto_pair}
        logging.info(f"Connecting to {url}")
        response = requests.get(url)
        data = json.loads(response.text)
        logging.info(data)
        embed = discord.Embed(title=f"{data['symbol']}", description=f"{data['lastPrice']}", color=0x00ff00)
        embed.add_field(name='Volume', value=data['volume'])
        embed.add_field(name='24hr change', value=data['priceChange'])
        embed.add_field(name='24hr % change', value=data['priceChangePercent'])
        embed.add_field(name='24hr high', value=data['highPrice'])
        embed.add_field(name='24hr low', value=data['lowPrice'])
        # add footer to embed
        # example: "Exchange data provided by Binance.us" with link to https://www.binance.us/en/markets
        embed.set_footer(text="Exchange data provided by Binance.us", icon_url="https://docs.binance.us/images/logo-961a0eb7.png")
        await interaction.response.send_message(embed=embed, ephemeral=False)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Crypto(bot))