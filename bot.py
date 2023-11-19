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
donair_counts = {}

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
    # initial donair count
    Veggie_Donair = 0 # 0.3x multiplier
    Falafel_Donair = 0 # 0.7x multiplier 
    Chicken_Donair = 0 # 1.2x multiplier
    Beef_Donair = 0 # 2x multiplier

    # checks for donair multiplier items 
    if random.random() <= 0.2:
        Veggie_Donair += 1

    if random.random() <= 0.1:
        Falafel_Donair += 1

    user_id = user.id

    donair_counts.setdefault(user_id, {'Veggie': 0, 'Falafel': 0, 'Chicken': 0, 'Beef': 0})
    donair_counts[user_id]['Veggie'] += Veggie_Donair
    donair_counts[user_id]['Falafel'] += Falafel_Donair
    donair_counts[user_id]['Chicken'] += Chicken_Donair
    donair_counts[user_id]['Beef'] += Beef_Donair

    range_decision = random.random() # generates a new number for the next iteration

    if range_decision <= 0.6:
        # 60% chance of generating number between 2 and 8
        random_points = random.randint(2,8)
    elif range_decision <= 0.9:
        # 30% chance of generating number between 9 and 12
        random_points = random.randint(9,12)
    else:
        # 9% chance of generating random number between 13 and 18
        random_points = random.randint(13,18)

    Veggie_Donair_Points = random_points*(Veggie_Donair)*0.3    
    Falafel_Donair_Points = random_points*(Falafel_Donair)*0.7
    Chicken_Donair_Points = random_points*(Chicken_Donair)*1.2
    Beef_Donair_Points = random_points*(Beef_Donair)*2

    random_points =  random_points + Veggie_Donair_Points + Falafel_Donair_Points + Chicken_Donair_Points + Beef_Donair_Points


    # update user points
    current_points = points_dict.get(user.id, 0)
    new_points = current_points + random_points
    points_dict[user.id] = new_points

    await ctx.send(f'You found {random_points} turkish liras :coin: habibi {user.name}. You now have {new_points} turkish liras.')

@bot.command(name='bank')
async def check_points(ctx, user: discord.User = None):
    ####
    if user is None:
        user = ctx.author

    user_id = user.id
    user_donairs = donair_counts.get(user_id, {'Veggie': 0, 'Falafel': 0, 'Chicken': 0, 'Beef': 0})
    user_points = points_dict.get(ctx.author.id, 0)
    await ctx.send(f'You currently have {user_points} turkish liras\n {user_donairs["Veggie"]} veggie donairs\n {user_donairs["Falafel"]} falafel donairs\n {user_donairs["Chicken"]} chicken donairs\n {user_donairs["Beef"]} beef donairs')

bot.run(TOKEN)
