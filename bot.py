import os
import discord
import math
import random
from dotenv import load_dotenv
from discord.ext import commands
import random
import asyncio
from info import initializeinfo, update_entry, readinfo
from typing import Optional

load_dotenv()
TOKEN = os.getenv('token')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)
points_dict = {}    
donair_counts = {}
zone= [] #PLAYER EATERY
modifier = {} ## TEMP MODIFIER
donairstrg = {} ## USER INVENTORIES

class reroll(discord.ui.Button):
    def __init__(self, user):
        super().__init__(style=discord.ButtonStyle.success, label="Roll Again?")
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        ctx = await bot.get_context(interaction.message)
        ctx.author = self.user
        await ctx.invoke(bot.get_command("roll"), user=self.user)

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
async def register(ctx, user: discord.User):
    initializeinfo(discord.User)
    await ctx.send(f'Save data initialized for {discord.User}!')

@bot.command(name='stats') #show user save data
async def user_stats(ctx, user: discord.User):
    stats = readinfo(discord.User)
    await ctx.send(f'You have {stats[0]} Liras, \n{stats[1]} Veggie Donairs, \n{stats[2]} Falafel Donairs, \n{stats[3]} Chicken Donairs, \n{stats[4]} Beef Donairs, \
    \n{stats[5]} Day-old Donairs, \n{stats[6]} Kids Sized Donairs, \n{stats[7]} Standard Donairs, \n{stats[8]} Jumbo Donairs, \n{stats[9]} Bronze Donairs, \
    \n{stats[10]} Silver Donairs, \n{stats[11]} Gold Donairs, \n{stats[12]} Platinum Donairs, \n{stats[13]} Donner Donairs')

    
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
async def roll(ctx, user: Optional[discord.User] = None):
    money=0
    if money >= 0:
        #Loading of user ID
        id = user.id if user else ctx.author.id
        modval = int(modifier.get(id,1))
        
        #cosmetic
        embed=discord.Embed(
            colour=discord.Colour.green(),
            title="**Donair Capsule Opened!**",
        )

        #Rolling probability

        #rolling rarity
        
        rarval2 = random.randint(0,10000) # range to pick for rarity
        rarval = modval*rarval2 #modval scales rarity to higher number

        if rarval < 4000:
            rarity = "Day-old"
        if 4000<= rarval < 7000:
            rarity = "Kids Sized"
        if 7000<= rarval < 9000:
            rarity = "Standard"
        if 9000<= rarval < 9500:
            rarity = "Jumbo"
        if 9500<= rarval < 9700:
            rarity = "Bronze"
        if 9700<= rarval < 9800:
            rarity = "Silver"
        if 9800<= rarval < 9900:
            rarity = "Gold"
        if 9900<= rarval < 9980:
            rarity = "Platinum"
        if 9980<= rarval < 10000:
            rarity = "Donner"
        if rarval >=10000: #defaults to bronze if surpasses limit  -- should this go to donner?
            rarity = "Bronze" 

        #donair type
        
        roll= random.randint(0,1000)
        rollval = roll*(modval)
        
        if rollval < 350:
            flav1="Is it really donair?"
            embed.set_image(url="attachment://Veggie.png")
            dfile=discord.File("Veggie.png")
            donair = "Veggie"
        if 350 <= rollval <820: 
            flav1="Still insubstantial; Think of it as a precursor to donair."
            embed.set_image(url="attachment://Falafel.png")
            dfile=discord.File("Falafel.png")
           
            donair = "Falafel"
        if 820<= rollval <950: 
            flav1="A staple of donair. Juicy, seasoned chicken"
            embed.set_image(url="attachment://Shawarma (1).png")
            dfile=discord.File("Shawarma (1).png")
     
            donair = "Chicken"
        if 950 <= rollval <1001: 
            flav1="Now you know what’s in it, and it turns out the perfect donair all along was just Beef."
            embed.set_image(url="attachment://Beef.png")
            dfile=discord.File("Beef.png")
         
            donair = "Beef"
           
        if  1001 <= rollval: 
            flav1="Now you know what’s in it, and it turns out the perfect donair all along was just Beef."
            embed.set_image(url="attachment://Beef.png")
            dfile=discord.File("Beef.png")
            
            donair = "Beef"

        embed=discord.Embed(
            colour=discord.Colour.green(),
            title="**Donair Capsule Opened!**",
            description=f"You found a *{rarity}* **{donair} Donair** \n ``{flav1}``"


        )
        
        embed.set_footer(text=f"found by {ctx.author.display_name}")
        await ctx.send(embed=embed, file=dfile)

        if id not in donairstrg: 
            donairstrg[id] = []
        donairstrg[id].append(rarity+" "+donair)


        butn = discord.ui.View()
        butn.add_item(reroll(ctx.author))
        await ctx.send(view=butn)
         
@roll.error
async def roll(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("**Whoa there buckeroo, slow down yer rolling!**\n*(Please wait 5 secounds between rolls)*")
   
@bot.command(name="inv")
async def inv(ctx):
    id = ctx.author.id
    inv_id=donairstrg.get(id,[])
    await ctx.send(inv_id)

bot.run(TOKEN)
