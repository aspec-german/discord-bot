# bot.py
import os
import random
import logging
import discord
import datetime as dt
import humanize
from discord.ext import commands
from dotenv import load_dotenv, set_key
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')

load_dotenv(dotenv_path, verbose=True)
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('DISCORD_CHANNEL')
BOTS_CHANNEL = os.getenv('DISCORD_BOTS_CHANNEL')
JOIN_LEAVE_LOG_CHANNEL = os.getenv('DISCORD_JOIN_LEAVE_LOG_CHANNEL')
MEMBER_LOG_CHANNEL = os.getenv('DISCORD_MEMBER_LOG_CHANNEL')
SERVER_LOG_CHANNEL = os.getenv('DISCORD_SERVER_LOG_CHANNEL')
GREETING = os.getenv('DISCORD_GREETING')
INVITE_MEMBER = os.getenv('DISCORD_INVITE_MEMBER')
INVITE_AKTIVISTA = os.getenv('DISCORD_INVITE_AKTIVISTA')
ROLE_ADMIN = os.getenv('DISCORD_ROLE_ADMIN')
ROLE_MEMBER = os.getenv('DISCORD_ROLE_MEMBER')
ROLE_AKTIVISTA = os.getenv('DISCORD_ROLE_AKTIVISTA')
DEBUG_LEVEL = os.getenv('DISCORD_DEBUG_LEVEL')
DEBUG_FILE = os.getenv('DISCORD_DEBUG_FILE')

bot = commands.Bot(command_prefix='?')

# https://discordpy.readthedocs.io/en/latest/logging.html
logger = logging.getLogger('discord')
logger.setLevel(DEBUG_LEVEL)
handler = logging.FileHandler(filename=DEBUG_FILE, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# if ready, create dict_invites and dict_roles
dict_invites = {}
dict_roles = {
    INVITE_MEMBER: ROLE_MEMBER,
    INVITE_AKTIVISTA: ROLE_AKTIVISTA,
}
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord and is connected to the following guilds:')
    print(bot.guilds)
    # fill dict_invites
    guild = discord.utils.get(bot.guilds, name=GUILD)
    bots_channel = discord.utils.get(guild.channels, name=BOTS_CHANNEL)
    invites = await guild.invites()
    for i in invites:
        dict_invites[i.code] = i.uses
    await bots_channel.send(':robot:')

# commands
@bot.command(name='dice', help='Simulates rolling dice(s), e.g. `?dice 2 4`')
async def dice(ctx, number_of_dices: int = 1, number_of_sides: int = 6):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dices)
    ]
    await ctx.send(', '.join(dice))

@bot.command(name='ping', help='Are you still alive?\nhttps://www.youtube.com/watch?v=nfRlrV8awo0')
async def ping(ctx):
    await ctx.send('pong? :ping_pong:')

# events
@bot.event
async def on_member_join(member):
    f = 'on_member_join'
    # get guild
    guild = discord.utils.get(bot.guilds, name=GUILD)
    if not guild:
        print(f'{f}: no such guild {guild}, abort')
    # get log channels
    join_leave_channel = discord.utils.get(guild.channels, name=JOIN_LEAVE_LOG_CHANNEL)
    if not join_leave_channel:
        print(f'{f}: no such channel {join_leave_channel}, abort')
    member_channel = discord.utils.get(guild.channels, name=MEMBER_LOG_CHANNEL)
    if not member_channel:
        print(f'{f}: no such channel {member_channel}, abort')
    print(f'{f}: "{member.name}" joined')
    # embed
    users = len(guild.members)
    since_created = humanize.precisedelta(dt.datetime.utcnow() - member.created_at)
    embed = discord.Embed(
        title='Member joined',
        description="{} {}. to join\ncreated {} ago".format(member.mention, users, since_created),
        timestamp=member.joined_at if member.joined_at else dt.datetime.utcnow(),
    )
    embed.set_footer(text="User ID: " + str(member.id))
    embed.set_author(name=member, icon_url=member.avatar_url)
    # build dict_invites_new
    invites_new = await guild.invites()
    if not invites_new:
        print(f'{f}: no invites found, abort')
    dict_invites_new = {i.code: i.uses for i in invites_new}
    # compare uses
    for i in dict_invites:
        if dict_invites_new[i] > dict_invites[i]:
            embed.add_field(name="Invite Link", value=i)
            embed.add_field(name="Roles", value=dict_roles[i])
            await join_leave_channel.send(embed=embed)
            # update dict_invites
            dict_invites.update({i: dict_invites_new[i]})
            # add role(s)
            for r in dict_roles[i].split(','):
                await member.add_roles(discord.utils.get(guild.roles, name=r))
                # send log message to channel
                print(f'{f}: added role "{r}" to "{member.name}"')
                # TODO use embed
                await member_channel.send(f'added role "{r}" to "{member.name}"')
    # TODO greet
    # get welcome channel
    #channel = discord.utils.get(guild.channels, name=CHANNEL)
    # send welcome message to channel
    #await channel.send(GREETING.replace('$member', member.mention).replace('$channel', channel.mention))

@bot.event
async def on_member_remove(member):
    f = 'on_member_remove'
    # get guild
    guild = discord.utils.get(bot.guilds, name=GUILD)
    if not guild:
        print(f'{f}: no such guild {guild}, abort')
    # get log channel
    join_leave_channel = discord.utils.get(guild.channels, name=JOIN_LEAVE_LOG_CHANNEL)
    if not join_leave_channel:
        print(f'{f}: no such channel {join_leave_channel}, abort')
    print(f'{f}: "{member.name}" left')
    embed = discord.Embed(
        title='Member left',
        description="{} joined {} ago".format(member.mention, humanize.precisedelta(dt.datetime.utcnow() - member.joined_at)),
        timestamp=dt.datetime.utcnow(),
    )
    embed.set_footer(text="User ID: " + str(member.id))
    embed.set_author(name=member, icon_url=member.avatar_url)
    roles = [ r.mention for r in member.roles ]
    embed.add_field(name="Roles", value=', '.join(roles))
    await join_leave_channel.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('Command not found. Use `?help` for a command overview.')

bot.run(TOKEN)
