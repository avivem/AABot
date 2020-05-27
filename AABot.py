import os
import discord
from discord.ext import commands
import json
import shutil
import string
from dotenv import load_dotenv

if not os.path.exists('.env'):
    shutil.copyfile('default.env', '.env')
    print('\n.ENV NOT FOUND.\n.ENV HAS BEEN CREATED FROM DEFAULTS.\nPLEASE CUSTOMIZE .ENV AND RESTART THE BOT.')

#Load environment variables from .env
load_dotenv()
TOK = os.getenv('DISCORD_TOKEN')
GLD = os.getenv('DISCORD_GUILD')
PREFIX = os.getenv('PREFIX')

#Load config
if not os.path.exists('config.json'):
    shutil.copyfile('default_config.json', 'config.json')
    print('\nCONFIG.JSON NOT FOUND.\nCONFIG.JSON HAS BEEN CREATED FROM DEFAULTS.\nPLEASE CUSTOMIZE CONFIG.JSON AND RESTART THE BOT.')
with open('config.json') as f:
    config = json.load(f)

bot = commands.Bot(command_prefix=PREFIX)

#On bot startup
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GLD)

    print(
        f'{bot.user} is connected to the following server:\n'
        f'{guild.name}(id: {guild.id})'

    )

    users = '\n - '.join([user.name if not user.bot else 'BOT  ' + user.name for user in bot.users])
    print(f'Guild users:\n - {users}')

#On member join server, send message in welcome channel
@bot.event
async def on_member_join(member: discord.Member):
    welcome_channel = bot.get_channel(config["welcome_channel"])
    temp = string.Template(config["welcome_message"])
    welcome = temp.substitute(name=member.mention)
    await welcome_channel.send(welcome)

#Respond to errors by providing the specific error.
@bot.event
async def on_command_error(context: commands.Context, error):
    role = discord.utils.find(lambda r: r.id == config["manager_role"], context.message.author.roles)
    if role:
        await context.send(str(error))
    else:
        await context.send("Invalid command.")


#Command to create new Echo commands.
#Example: <prefix>create_echo <echo_name> <echo_msg>
@bot.command(name='create_echo')
@commands.has_role(config["manager_role"])
async def create_echo(context: commands.Context):
    msg = context.message.content.split()
    with open('config.json', 'w') as f:
        action = 'updated' if msg[1] in config["echos"] else 'created'
        config["echos"][msg[1]] = ' '.join(msg[2:]).strip('\"')
        f.write(json.dumps(config, indent=4))
        f.truncate()
    
    await context.send(f'Echo {msg[1]} has been {action}.')

#Error when creating echo.
@create_echo.error
async def create_echo_error(context: commands.Context, error):
    await context.send("Create Echo Error. Please check spelling and permissions.")

#Command for listing all echos.
@bot.command(name='list_echos')
async def list_echos(context: commands.Context):
    embed = discord.Embed(title="List of Echos")
    for echo in config["echos"]:
        embed.add_field(name=echo, value=config["echos"][echo])
    await context.send(embed=embed)

#Command for executing echos.
@bot.command(name='e')
async def echo(context: commands.Context):
    msg = context.message.content.split()
    if msg[1] in config["echos"]:
        await context.send(config["echos"][msg[1]])
    else:
        await context.send("Invalid Echo.")

#Give a single role by id from every member except bots and the owner.
@bot.command(name="mass_give_role")
async def mass_give_role(context: commands.Context):
    guild = discord.utils.get(bot.guilds, name=GLD)
    msg = context.message.content.split()
    role = guild.get_role(int(msg[1]))
    for member in guild.members:
        if member.id != guild.owner.id and member.bot == False:
            print(f'{member.name} {member.id}')
            await member.add_roles(role)
    await context.send(f'Added the {role} role to everyone except the Owner and bots.')

#Remove a single role by id from every member except bots and the owner.
@bot.command(name="mass_remove_role")
async def mass_remove_role(context: commands.Context):
    guild = discord.utils.get(bot.guilds, name=GLD)
    msg = context.message.content.split()
    role = guild.get_role(int(msg[1]))
    for member in guild.members:
        if member.id != guild.owner.id and member.bot == False:
            await member.remove_roles(role)
    await context.send(f'Removed the {role} role from everyone except the Owner and bots.')

bot.run(TOK)