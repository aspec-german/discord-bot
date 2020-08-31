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
CHANNEL = os.getenv('DISCORD_CHANNEL')
INVITE_MEMBER = os.getenv('DISCORD_INVITE_MEMBER')
INVITE_AKTIVISTA = os.getenv('DISCORD_INVITE_AKTIVISTA')
ROLE_MEMBER = os.getenv('DISCORD_ROLE_MEMBER')
ROLE_AKTIVISTA = os.getenv('DISCORD_ROLE_AKTIVISTA')
DEBUG_LEVEL = os.getenv('DISCORD_DEBUG_LEVEL')
DEBUG_FILE = os.getenv('DISCORD_DEBUG_FILE')

bot = commands.Bot(command_prefix='!')

# https://discordpy.readthedocs.io/en/latest/logging.html
logger = logging.getLogger('discord')
logger.setLevel(DEBUG_LEVEL)
handler = logging.FileHandler(filename=DEBUG_FILE, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# if ready, create dict_invites and dict_roles
dict_invites = {}
dict_roles = {}
dict_roles[INVITE_MEMBER] = ROLE_MEMBER
dict_roles[INVITE_AKTIVISTA] = ROLE_AKTIVISTA
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    guild = discord.utils.get(bot.guilds, name=GUILD)
    invites = await guild.invites()
    for i in invites:
        dict_invites[i.code] = i.uses
    #print(dict_invites)
    #print(dict_roles)

@bot.command(name='dice', help='Simulates rolling dice(s).')
async def dice(ctx, number_of_dice: int = 1, number_of_sides: int = 6):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

#@bot.command(name='create_channel', help='admin: create channel')
#@commands.has_role('admin')
#async def create_channel(ctx, channel_name='test'):
#    guild = ctx.guild
#    existing_channel = discord.utils.get(guild.channels, name=channel_name)
#    if not existing_channel:
#        print(f'Creating a new channel: {channel_name}')
#        await guild.create_text_channel(channel_name)

@bot.command(name='ping', help='Are you still alive?\nhttps://www.youtube.com/watch?v=nfRlrV8awo0')
async def ping(ctx):
    await ctx.send('pong! :ping_pong:')

#@bot.command(name='invites', help='get all invites')
#async def invites(ctx):
#    guild = discord.utils.get(bot.guilds, name=GUILD)
#    invites = await guild.invites()
#    # will print discord box
#    #invites = await bot.fetch_invite('https://discord.gg/pBzMeWc')
#    print(invites)
#    for i in invites:
#        # NOTE i.channel.name not needed
#        dict_invites[i.code] = i.uses
#    print(dict_invites)
#    await ctx.send(dict_invites)
#
#@bot.command(name='roles', help='get all roles')
#async def roles(ctx):
#    guild = discord.utils.get(bot.guilds, name=GUILD)
#    roles = guild.roles
#    print(roles)
#    for r in roles:
#        print(r.name)
#    await ctx.send(roles)

@bot.event
async def on_member_join(member):
    # get guild
    guild = discord.utils.get(bot.guilds, name=GUILD)
    # build dict_invites_new
    invites_new = await guild.invites()
    dict_invites_new = {}
    for i in invites_new:
        dict_invites_new[i.code] = i.uses
    # compare uses
    for i in dict_invites:
        if dict_invites_new[i] > dict_invites[i]:
            # update dict_invites
            dict_invites.update({i: dict_invites_new[i]})
            # add role
            await member.add_roles(discord.utils.get(guild.roles, name=dict_roles[i]))
            print(f'added role "{dict_roles[i]}" to {member.name}')
    # get welcome channel
    channel = discord.utils.get(guild.channels, name=CHANNEL)
    # send welcome message to channel
    await channel.send(f'Hey und herzlich willkommen {member.mention}, schön, dass du den Weg zu unserem Server gefunden hast! Dies ist eine kleine Oase für Aces, Aros, Menschen in den jeweiligen Spektren und natürlich auch für alle Menschen, die questioning sind :palm_tree:. Wir freuen uns sehr, dass du hier bist :cake:. Klicke dich durch die Channel, die sich direkt unter {channel.mention} befinden, für mehr Infos. :sunflower:\nWenn du offene Fragen hast, schreibe einfach in diesen Channel oder wende dich jederzeit an eine Person des Server-Teams (in orange). :cherry_blossom:')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('Command not found. Use `!help` for a command overview.')

bot.run(TOKEN)
