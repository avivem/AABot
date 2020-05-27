import os
import discord
import json
import shutil
import string
from dotenv import load_dotenv

#Load environment variables from .env
load_dotenv()
TOK = os.getenv('DISCORD_TOKEN')
GLD = os.getenv('DISCORD_GUILD')

#Load config
if not os.path.exists('config.json'):
    shutil.copyfile('default_config.json', 'config.json')
    print('\nCONFIG.JSON NOT FOUND.\nCONFIG.JSON HAS BEEN CREATED FROM DEFAULTS.\nPLEASE CUSTOMIZE CONFIG.JSON')
with open('config.json') as f:
    config = json.load(f)

client = discord.Client()

#On bot startup
@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GLD)

    print(
        f'{client.user} is connected to the following server:\n'
        f'{guild.name}(id: {guild.id})'

    )

    users = '\n - '.join([user.name if not user.bot else 'BOT  ' + user.name for user in client.users])
    print(f'Guild users:\n - {users}')

#On member join server, send message in welcome channel
@client.event
async def on_member_join(member: discord.Member):
    welcome_channel = client.get_channel(config["welcome_channel"])
    temp = string.Template(config["welcome_message"])
    welcome = temp.substitute(name=member.mention)
    await welcome_channel.send(welcome)

client.run(TOK)