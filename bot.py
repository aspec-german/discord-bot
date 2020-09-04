# bot.py
import os
import random
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('DISCORD_LOG_CHANNEL')
INVITE_MEMBER = os.getenv('DISCORD_INVITE_MEMBER')
INVITE_AKTIVISTA = os.getenv('DISCORD_INVITE_AKTIVISTA')
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
    print(f'{bot.user.name} has connected to Discord!')
    guild = discord.utils.get(bot.guilds, name=GUILD)
    invites = await guild.invites()
    dict_invites = {i.code: i.uses for i in invites}

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

@bot.event
async def on_member_join(member):
    # get guild
    guild = discord.utils.get(bot.guilds, name=GUILD)
    # get log channel
    channel = discord.utils.get(guild.channels, name=CHANNEL)
    # build dict_invites_new
    invites_new = await guild.invites()
    dict_invites_new = {i.code: i.uses for i in invites_new}
    # compare uses
    for i in dict_invites:
        if dict_invites_new[i] > dict_invites[i]:
            # update dict_invites
            dict_invites.update({i: dict_invites_new[i]})
            # add role
            await member.add_roles(discord.utils.get(guild.roles, name=dict_roles[i]))
            # send log message to channel
            await channel.send(f'added role "{dict_roles[i]}" to "{member.name}"')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('Command not found. Use `?help` for a command overview.')

bot.run(TOKEN)
