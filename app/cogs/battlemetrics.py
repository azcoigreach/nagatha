from asyncio import wait_for
from app.config import settings
import discord
from discord import app_commands
from discord.ext import commands
import logging
import requests
import json

'''
Reference: https://www.battlemetrics.com/developers/documentation
'''

class BattleMetrics(commands.Cog):
    """battlemetrics.com server info"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    group = app_commands.Group(name='battlemetrics', description='battlemetrics.com server info', guild_ids=settings.BATTLEMETRICS_GUILD_IDS)

    class ListGamesView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=15.0)
            self.value = None
        
        @discord.ui.button(label="Previous", style=discord.ButtonStyle.grey, disabled=False)
        async def prev(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
            self.value = 'prev'
            self.stop()
            await interaction.response.defer()

        @discord.ui.button(label="Next", style=discord.ButtonStyle.grey, disabled=False)
        async def next(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
            self.value = 'next'
            self.stop()
            await interaction.response.defer()

    async def list_games_proc(self, interaction: discord.Interaction, url) -> None:
        try:
            logging.info(f"Connecting to {url}")
            game_list = requests.get(url)
            data = json.loads(game_list.text)
            embed = discord.Embed(title="Battlemetrics Games", description="List of games and ids", color=0x00ff00)
            for game in data['data']:
                embed.add_field(name=game['attributes']['name'], value=game['id'], inline=True)
                
            if 'prev' in data['links'] and 'next' in data['links']:
                view = self.ListGamesView()
            elif 'prev' not in data['links'] and 'next' in data['links']:
                view = self.ListGamesView()
                view = view.remove_item(view.children[0])   
            elif 'prev' in data['links'] and 'next' not in data['links']:
                view = self.ListGamesView()
                view = view.remove_item(view.children[1])
            else:
                logging.error('No links in data')

            await interaction.edit_original_response(embed=embed, view=view)
            await view.wait()

            if view.value is not None:
                await interaction.edit_original_response(view=None)
                if view.value == 'prev':
                    await self.list_games_proc(interaction, data['links']['prev'])
                elif view.value == 'next':
                    await self.list_games_proc(interaction, data['links']['next'])
            else:
                await interaction.edit_original_response(view=None)
                view.stop()

        except Exception as e:
            logging.error(f"list_games_proc() Error: {e}")
            await interaction.followup.send(f"Oops, something went wrong. Please try again later.")

    @group.command(name='list_games')
    async def list_games(self, interaction: discord.Interaction) -> None:
        """List battlemetrics games and ids"""
        logging.info(f'Attempting to list battlemetrics games')
        page_size = 9
        url = f"https://api.battlemetrics.com/games?page[size]={page_size}&fields[game]=name"
        await interaction.response.defer(ephemeral=False)
        await self.list_games_proc(interaction, url)

    async def list_servers_proc(self, interaction: discord.Interaction, url) -> None:
        try:
            logging.info(f"Connecting to {url}")
            server_list = requests.get(url)
            data = json.loads(server_list.text)
            embed = discord.Embed(title="Battlemetrics Servers", description="List of servers", color=0x00ff00)
            logging.info(data)
            for server in data['data']:
                embed.add_field(name=server['attributes']['name'], value=f"IP: {server['attributes']['ip']}:{server['attributes']['port']}\nSERVER ID: {server['id']}", inline=True)
                
            if 'prev' in data['links'] and 'next' in data['links']:
                view = self.ListGamesView()
            elif 'prev' not in data['links'] and 'next' in data['links']:
                view = self.ListGamesView()
                view = view.remove_item(view.children[0])   
            elif 'prev' in data['links'] and 'next' not in data['links']:
                view = self.ListGamesView()
                view = view.remove_item(view.children[1])
            else:
                view = self.ListGamesView()
                view = view.clear_items()

            if len(data['data']) == 0:
                embed.add_field(name="No servers found", value= "No servers found", inline=True)
                view = self.ListGamesView()
                view = view.clear_items()

            await interaction.edit_original_response(embed=embed, view=view)
            await view.wait()

            if view.value is not None:
                await interaction.edit_original_response(view=None)
                if view.value == 'prev':
                    await self.list_servers_proc(interaction, data['links']['prev'])
                elif view.value == 'next':
                    await self.list_servers_proc(interaction, data['links']['next'])
            else:
                await interaction.edit_original_response(view=None)
                view.stop()

        except Exception as e:
            logging.error(f"list_servers_proc() Error: {e}")
            await interaction.followup.send(f"Oops, something went wrong. Please try again later.")
    
    
    # TODO: Add pagination
    # TODO: Add search
    # TODO: Add additional filters
    #Reference: https://www.battlemetrics.com/developers/documentation#link-GET-server-/servers
    '''
    CURL example: $ curl -n https://api.battlemetrics.com/servers
        -G \
        -d location=47.6140999%2C-122.1966574 \
        -d include=serverGroup \
        -d filter[search]=PVE \
        -d filter[game]=ark \
        -d filter[status]=online \
        -d filter[countries][]=US \
        -d filter[countries][]=CA \
        -d filter[maxDistance]=5000 \
        -d filter[players][min]=42 \
        -d filter[players][max]=42 \
        -d filter[features][469a1706-c8be-11e7-9d7a-e3ed64915530]=true \
        -d filter[features][11bc8572-ca45-11e7-bad6-2f023a014d57][or][]=1a7c6614-ca45-11e7-84a2-8b4c8bd3712b \
        -d filter[features][11bc8572-ca45-11e7-bad6-2f023a014d57][or][]=1abb5fb8-ca45-11e7-858b-affed11cb7fd \
        -d filter[rcon]=true \
        -d filter[favorites]=true \
        -d filter[groups]=example \
        -d filter[groupLeader]=true \
        -d filter[ids][whitelist]=123 \
        -d filter[ids][blacklist]=123 \
        -d filter[organizations]=123 \
        -d page[size]=42 \
        -d page[key]=100 \
        -d page[offset]=50 \
        -d page[rel]=next \
        -d sort=example \
        -d fields[server]=name%2Cip%2Cport \
        -d relations[server]=a%2Cb%2Cc \
    '''
    @group.command(name='list_servers')
    async def list_servers(self, interaction: discord.Interaction, game: str, search: str, ) -> None: # search is optional
        
        """List battlemetrics servers"""
        logging.info(f'Attempting to list battlemetrics servers')
        page_size = 9
        url = f"https://api.battlemetrics.com/servers?filter[game]={game}&filter[search]={search}&page[size]={page_size}&fields[server]=name,ip,port"
        await interaction.response.defer(ephemeral=False)
        await self.list_servers_proc(interaction, url)
    
        
    # Reference: https://www.battlemetrics.com/developers/documentation#link-GET-server-/servers/{(%23%2Fdefinitions%2Fserver%2Fdefinitions%2Fidentity)}
    ''' CURL EXAMPLE: 
    $ curl -n https://api.battlemetrics.com/servers/$SERVER_ID
        -G \
        -d include=player%2Cidentifier \
        -d fields[player]=updatedAt%2Cname \
        -d fields[server]=name%2Cip%2Cport \
        -d fields[identifier]=type%2Cidentifier \
        -d fields[session]=start%2Cstop \
        -d fields[serverUptime]=value \
        -d fields[serverEvent]=value \
        -d fields[serverGroup]=rank \
        -d fields[serverDescription]=description%2Clinks \
        -d fields[organization]=tz%2CbanTemplate \
        -d fields[orgDescription]=description%2Clinks \
        -d fields[orgGroupDescription]=description%2Clinks \
        -d relations[server]=a%2Cb \
        -d relations[player]=a%2Cb \
        -d relations[identifier]=a%2Cb \
        -d relations[session]=a%2Cb \
        -d relations[serverUptime]=a%2Cb \
        -d relations[serverEvent]=a%2Cb \
        -d relations[serverGroup]=a%2Cb \
        -d relations[serverDescription]=a%2Cb \
        -d relations[organization]=a%2Cb \
        -d relations[orgDescription]=a%2Cb \
        -d relations[orgGroupDescription]=a%2Cb \
    '''
    ''' Example response:
    {
  "data": {
    "type": "server",
    "id": "42",
    "attributes": {
      "id": "42",
      "name": "Server Name",
      "address": "play.example.com",
      "ip": "127.0.0.1",
      "port": 2302,
      "portQuery": 2303,
      "players": 42,
      "maxPlayers": 42,
      "rank": 42,
      "createdAt": "2015-01-01T12:00:00Z",
      "updatedAt": "2015-01-01T12:00:00Z",
      "location": [
        47.6140999,
        -122.1966574
      ],
      "country": "US",
      "status": "online",
      "details": null,
      "metadata": {
      },
      "rconActive": true,
      "queryStatus": null,
      "rconStatus": null,
      "rconLastConnected": "2015-01-01T12:00:00Z",
      "rconDisconnected": "2015-01-01T12:00:00Z",
      "private": false
    },
    "relationships": {
      "game": {
        "data": {
          "type": "game",
          "id": "ark"
        }
      }
    }
  },
  "included": [
    null
  ]
}
    '''

    @group.command(name='server_info')
    async def server_info(self, interaction: discord.Interaction, server_id: str) -> None:
        """Get server info"""
        try:
            await interaction.response.defer(ephemeral=False)
            url = f"https://api.battlemetrics.com/servers/{server_id}"
            logging.info(f'Attempting to get server info from {url}')
            server_info = requests.get(url)
            data = json.loads(server_info.text)
            logging.info(f'Server info: {data}')
            # embed include server name, id, description, address, ip, port, rank, players, maxPlayers, status, createdAt, updatedAt, location, country
            
            embed = discord.Embed(title=data['data']['attributes']['name'], url=f"https://battlemetrics.com/servers/{data['data']['relationships']['game']['data']['id']}/{data['data']['id']}" ,color=0x00ff00)
            embed.add_field(name="Server ID", value=data['data']['attributes']['id'], inline=True)
            embed.add_field(name="Address", value=data['data']['attributes']['address'], inline=True)
            embed.add_field(name="IP", value=data['data']['attributes']['ip'], inline=True)
            embed.add_field(name="Port", value=data['data']['attributes']['port'], inline=True)
            embed.add_field(name="Rank", value=data['data']['attributes']['rank'], inline=True)
            embed.add_field(name="Players", value=data['data']['attributes']['players'], inline=True)
            embed.add_field(name="Max Players", value=data['data']['attributes']['maxPlayers'], inline=True)
            embed.add_field(name="Status", value=data['data']['attributes']['status'], inline=True)
            embed.add_field(name="Created At", value=data['data']['attributes']['createdAt'], inline=True)
            embed.add_field(name="Updated At", value=data['data']['attributes']['updatedAt'], inline=True)
            embed.add_field(name="Location", value=data['data']['attributes']['location'], inline=True)
            embed.add_field(name="Country", value=data['data']['attributes']['country'], inline=True)
            

            await interaction.edit_original_response(embed=embed)

        

        except Exception as e:
            logging.error(f"server_info() Error: {e}")
            await interaction.followup.send(f"Oops, something went wrong. Please try again later.")

async def setup(bot: commands.Bot) -> None:
    # logging.info("Loading battlemetrics cog")
    for guild_id in settings.BATTLEMETRICS_GUILD_IDS:
        logging.info(f'Adding BattleMetrics to {guild_id}')
        await bot.add_cog(BattleMetrics(bot), override=True, guild=discord.Object(id=guild_id))
