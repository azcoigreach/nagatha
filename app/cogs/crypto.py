import requests
import json
import discord
from discord.ext import commands

#discord.py cog that gets crypto price data from binance.us
class Crypto(commands.Cog):
    '''Crypto prices from binance.us'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def crypto(self, ctx, *, crypto):
        """Get crypto price data from binance.us"""
        url = "https://api.binance.us/api/v3/ticker/price"
        params = {'symbol': crypto}
        response = requests.get(url, params=params)
        data = json.loads(response.text)
        print(data)
        embed = discord.Embed(title=f"{data['symbol']}", description=f"{data['price']}", color=0x00ff00)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Crypto(bot))