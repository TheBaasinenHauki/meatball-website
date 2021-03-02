import json
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import time as t
import string
import random

with open ("token.txt", "r") as tokenFile:
    discordToken = tokenFile.read()

###################################################################################################################################
#------------------------------------------------------------BOT------------------------------------------------------------------#
###################################################################################################################################

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('meatballbot.me'))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Hoom")
    await discord.Member.add_roles(member, role)
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)

@client.event
async def on_member_remove(member):
    linkCH = client.get_channel(496299897365200908)
    link = await linkCH.create_invite(max_age = 600)
    await member.send(link)
    print(f"kicked {member}")

@client.command(aliases = ['kick'])
@commands.has_permissions(administrator = True)
async def _kick(ctx, member: discord.Member):
    await ctx.send(f"Kicked {member}")
    await member.kick(reason = None)

@client.command(aliases = ['ban'])
@commands.has_permissions(administrator = True)
async def _ban(ctx, member: discord.Member):
    await ctx.send(f"Banned {member}")
    await member.ban(reason = None)



###############################################################################################
#-------------------------------------------Level on_message----------------------------------#
###############################################################################################

@client.event
async def on_message(message):
    if message.author.bot == False:
        with open('users.json', 'r') as f:
            users = json.load(f)

        await update_data(users, message.author)
        await add_message_count(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)

        with open('users.json', 'w') as f:
            json.dump(users, f)

        await get_user_names()

    await client.process_commands(message)

#---------------------------------------------Level Functions--------------------------------------------#

async def get_user_names():
    user_id_file = {}
    with open('users_id.json', 'w') as f:
        pass

    with open('users.json', 'r') as p:
        users = json.load(p)

    for user in users:
        user_int = int(user)
        user_object = client.get_user(user_int)
        user_if_name = user_object.name
        user_id_file[f"{user_if_name}"] = {}
        user_id_file[f"{user_if_name}"]['experience'] = users[f"{user}"]['experience']
        user_id_file[f"{user_if_name}"]['level'] = users[f"{user}"]['level']
        user_id_file[f"{user_if_name}"]['messages'] = users[f"{user}"]['messages']

    with open('users_id.json', 'w') as f:
        json.dump(user_id_file, f)

async def add_message_count(users, user):
    message_count = users[f'{user.id}']['messages']
    users[f'{user.id}']['messages'] = message_count + 1

async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1
        users[f'{user.id}']['messages'] = 0

async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp

async def level_up(users, user, message):
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (4/10))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}')
        users[f'{user.id}']['level'] = lvl_end
        
@client.command()
async def stats(ctx, member: discord.Member = None):
    if not member:
        id = ctx.message.author.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        usr_xp = users[str(id)]['experience']
        usr_msg = users[str(id)]['messages']
        await ctx.send(f' Level: {lvl} \n XP: {usr_xp} \n Messages: {usr_msg}')
    else:
        id = member.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'{member} is at level {lvl}!')

#Token#

client.run("Nz" + discordToken)
