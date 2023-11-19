import os
import discord
import math
import random
from dotenv import load_dotenv
from discord.ext import commands
import random
import asyncio
from info import initializeinfo, update_entry, readinfo

load_dotenv()
TOKEN = os.getenv('token')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)
points_dict = {}    
donair_counts = {}
zone= [] #PLAYER EATERY
modifier = {} ## TEMP MODIFIER
donairstrg = {} ## USER INVENTORIES

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

@bot.command(name='register') #initialize user save data
async def server_info(ctx):
    guild = ctx.guild
    initializeinfo(discord.User)
    await ctx.send(f'Save data initialized for {discord.User}!')

@bot.command(name='stats') #show user save data
async def server_info(ctx):
    guild = ctx.guild
    stats = readinfo(discord.User)
    await ctx.send(f'You have {stats[0]} Liras, \n{stats[1]} Veggie Donairs, \n{stats[2]} Falafel Donairs, \n{stats[3]} Chicken Donairs, \n{stats[4]} Beef Donairs')
    
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


    update_entry(user_id,'Veggie', Veggie_Donair)
    update_entry(user_id,'Falafel', Falafel_Donair)
    update_entry(user_id,'Chicken', Chicken_Donair)
    update_entry(user_id,'Beef', Beef_Donair)

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
    update_entry(user_id, liras, new_points)

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

@bot.command(name="info")
async def info(ctx):
    await ctx.send("Welcome to Shawarma Sheriff! \nYou are a fiend for donair, your sole purpose in life is to eat as many delicious donairs as possible. \nThis game can be played using the following commands:")

@bot.command(name="modifierset")
async def modifierset(ctx, value="int"):
    id = ctx.author.id
    modifier[id] = value
    await ctx.send(f"{ctx.author.mention} modifier is now {value}")
    
@bot.command(name="roll")
@commands.cooldown(1,5, commands.BucketType.user)
async def roll(ctx):
    #Loading of user ID
    id = ctx.author.id
    modval = modifier.get(id,1)
        
    #cosmetic
    await ctx.send("**Donair Capsule Opened!** \n-----------------------------------------------------------------")
    #Rolling probability

    #rolling rarity
    rarity = "day-old"
    rarval = random.randint(0,10000)
    
    #donair type
    
    roll= random.randint(0,1000)
    rollval = roll*modval

    if rollval < 350:
        await ctx.send(f"You found a *{rarity}* **Veggie Donair**\n-----------------------------------------------------------------")
        veg="Veggie.png"
        await ctx.send(file=discord.File(veg))
        donair = "Veggie"
    if 350 <= rollval <820: 
        await ctx.send(f"You found a *{rarity}* **Falafel Donair**\n-----------------------------------------------------------------")
        falafel="Falafel.png"
        await ctx.send(file=discord.File(falafel))
        donair = "Falafel"
    if 820<= rollval <950: 
        await ctx.send(f"You found a *{rarity}* **Chicken Donair**\n-----------------------------------------------------------------")
        shawarma="Shawarma_1.png"
        await ctx.send(file=discord.File(shawarma))
        donair = "Chicken"
    if 950 <= rollval <1001: 
        await ctx.send(f"You found a *{rarity}* **Beef Donair**\n-----------------------------------------------------------------")
        beef="Beef.png"
        await ctx.send(file=discord.File(beef))
        donair = "Beef"
    await ctx.send("-----------------------------------------------------------------")
    if  1001 <= rollval: 
        await ctx.send(f"You found a *{rarity}* **Beef Donair**\n-----------------------------------------------------------------")
        beef="Beef.png"
        await ctx.send(file=discord.File(beef))
        await ctx.send("-----------------------------------------------------------------")
        donair = "Beef"
    if id not in donairstrg: 
        donairstrg[id] = []
    donairstrg[id].append(donair)
    
@roll.error
async def roll(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("**Wallahi fam slow down. You must appreciate the donair.**\n*(Please wait 5 seconds between rolls)*")
   
@bot.command(name="inv")
async def inv(ctx):
    id = ctx.author.id
    inv_id=donairstrg.get(id,[])
    await ctx.send(inv_id)

bot.run(TOKEN)
