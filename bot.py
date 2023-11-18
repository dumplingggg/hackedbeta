import os
import discord
import math
import random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('token')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)
points_dict = {}    

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='serverinfo')
async def server_info(ctx):
    guild = ctx.guild
    embed = discord.Embed(title="Server Information", color=0x00ff00)
    embed.add_field(name="Server Name", value=guild.name, inline=False)
    embed.add_field(name="Server ID", value=guild.id, inline=False)
    embed.add_field(name="Members", value=guild.member_count, inline=False)
    await ctx.send(embed=embed)

@bot.command(name='rummage')
async def give_points(ctx, user: discord.User):
    # generates a randum number to determine the range
    range_decision = random.random() # creates float between 0 and 1

    if range_decision <= 0.6:
        # 60% chance of generating number between 2 and 8
        random_points = random.randint(2,8)
    elif range_decision <= 0.9:
        # 30% chance of generating number between 9 and 12
        random_points = random.randint(9,12)
    elif range_decision <= 0.99: 
        # 10% chance of generating random number between 13 and 18
        random_points = random.randint(13,18)
    # update user points
    current_points = points_dict.get(user.id, 0)
    new_points = current_points + random_points
    points_dict[user.id] = new_points

    await ctx.send(f'You found {random_points} habibi {user.name}. You now have {new_points} turkish liras.')

@bot.command(name='bank')
async def check_points(ctx):
    ####
    user_points = points_dict.get(ctx.author.id, 0)
    await ctx.send(f'You currently have {user_points} turkish liras.')

bot.run(TOKEN)
