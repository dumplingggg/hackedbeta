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

money = {}    
donair_counts = {}
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

@bot.command(name='register')
async def register(ctx, user: discord.User = None):
    ####
    if user is None:
        user = ctx.author

    user_id = user.id
    initializeinfo(user_id)
    embed=discord.Embed(
            colour=discord.Colour.dark_gold(),
            title="User Registered",
            description=f"{ctx.author.display_name} joined the hunt!"
        )
    await ctx.send(embed=embed)
    
@bot.command(name='stats') #show user save data
async def user_stats(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author
    user_id = user.id
    stats = readinfo(user_id)
    embed=discord.Embed(
            colour=discord.Colour.dark_teal(),
            title=f"{ctx.author.display_name}'s Donair Stats",
            description=f' Liras:{stats[0]}\nVeggie:{stats[1]}\nFalafel:{stats[2]}\nChicken:{stats[3]}\nBeef:{stats[4]}'
    )
    await ctx.send(embed=embed)

@bot.command(name="rob")
@commands.cooldown(1,5, commands.BucketType.user)
async def rob(ctx, id2: discord.Member = None):
   
    if not id2:
        await ctx.send("Aint no user in this part of town!")
        embed=discord.Embed(
            colour=discord.Colour.pink(),
            title="*Aint no user in this part of town!*",
        )
        return
    id= ctx.author.id
    robbed = id2.id
    robchance=random.randint(1,10)
    if robchance > 8:
        
        embed=discord.Embed(
            colour=discord.Colour.green(),
            title="**Aint no robberies allowed in this town!**",
            
        )
        embed.set_footer(text=f"{ctx.author.display_name} lost 30000 to the Sheriff.")
        await ctx.send(embed=embed)
        money[id] = money.get(id,0) - 30000
        update_entry(id, 'liras', readinfo(id)[0]-30000)
        return
    else:
        money[id] = money.get(id,0) +5000
        update_entry(id, 'liras', readinfo(id)[0]+5000)
        money[robbed] = money.get(robbed,0) -5000
        update_entry(robbed, 'liras', readinfo(robbed)[0]-5000)
        embed=discord.Embed(
            colour=discord.Colour.red(),
            title="**Theft Successful!**",
        )
        embed.set_footer(text=f"{ctx.author.display_name} robbed 5000 from {id2.display_name}!")
        await ctx.send(embed=embed)
@rob.error
async def rob(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("**STOP YAH ROBBIN'!**\n*(Please wait 5 secounds between rob attempts)*")

@bot.command(name="heist")
async def heist(ctx, coop: discord.Member=None, targ: discord.Member=None):
    if (not targ or not coop) :
         await ctx.send("**That aint gonna work Chief!**")
         return
    if targ.id==coop.id or coop.id==targ.id :
         await ctx.send("**That aint gonna work Chief!**")
         return
    coop_msg = await coop.send(f"{coop.mention}, {ctx.author.display_name} wants to go on a heist! Are you in? (react)")

    await coop_msg.add_reaction('💸')


    def coopck(reaction, user):
        return user == coop and str(reaction.emoji) =='💸'
   
    try:
        response = await bot.wait_for('reaction_add', check=coopck, timeout=500)
    except asyncio.TimeoutError:
        await coop_msg.edit(content="Heist Timed-Out")
        return
    await coop_msg.edit(content=f"The Heist is on!, {targ.mention} is now your target")

    
    embed=discord.Embed(
        colour=discord.Colour.dark_grey(),
        title="**A HEIST IS ON ITS WAY**",
        description=f"{targ.mention} is the target...")
            
    await ctx.send(embed=embed)
    await asyncio.sleep(10)

    outcome = random.randint(1,100)
    if outcome > 75:
        embed=discord.Embed(
                colour=discord.Colour.green(),
                title="**HEIST SUCCESS**",
                description=f"{targ.mention}has been robbed, the robbers both earned 20000"
            )
        await ctx.send(embed=embed)
        money[coop.id] +=20000
        update_entry(coop.id, 'liras', readinfo(coop.id)[0]+20000)
        money[targ.id] -=40000
        update_entry(targ.id, 'liras', readinfo(targ.id)[0]-20000)
        money[ctx.author.id] +=20000
        update_entry(ctx.author.id, 'liras', readinfo(ctx.author.id)[0]+20000)

    else:
        embed=discord.Embed(
                colour=discord.Colour.green(),
                title="**HEIST FAILED**",
                description=f"{targ.mention}has defended from the robbers {ctx.author.mention},{coop.mention}, they both lost 40000."
            )
        await ctx.send(embed=embed)
        money[coop.id] -=40000
        money[ctx.author.id] -=40000


@bot.command(name="flex")
async def gift(ctx, id2: discord.Member = None):
   
    if not id2:
        await ctx.send("That aint no playa!")
        embed=discord.Embed(
            colour=discord.Colour.pink(),
            title="*Aint no user in this part of town!*",
        )
        return
    id= ctx.author.id
    robbed = id2.id
    money.setdefault(robbed, 0)
        
    if money[id] > money[robbed]:
        embed=discord.Embed(
            colour=discord.Colour.dark_orange(),
            title="**YOU'RE BROKE!**",
            description=f"{ctx.author.display_name} flexed on {id2.display_name}!"
        )
        
        await ctx.send(embed=embed)
   
        return
    else:
        embed=discord.Embed(
            colour=discord.Colour.purple(),
            title="**awkward...**",
            description=f"{ctx.author.display_name} thought they were richer {id2.display_name}!"
        )
        await ctx.send(embed=embed)
        return  

@bot.command(name='rummage')
async def give_points(ctx, user: discord.User):
    # initial donair count
    Veggie_Donair = 0 # 0.3x multiplier
    Falafel_Donair = 0 # 0.7x multiplier 
    Chicken_Donair = 0 # 1.2x multiplier
    Beef_Donair = 0 # 2x multiplier

    # checks for donair multiplier items 
    if random.random() <= 0.02:
        Veggie_Donair += 1

    if random.random() <= 0.01:
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
    current_points = money.get(user.id, 0)
    new_points = current_points + random_points
    money[user.id] = new_points
    update_entry(user_id, 'liras', new_points)

    await ctx.send(f'You found {random_points} turkish liras :coin: habibi {user.name}. You now have {new_points} turkish liras.')

@bot.command(name='bank')
async def check_points(ctx, user: discord.User = None):
    ####
    if user is None:
        user = ctx.author

    user_id = user.id
    user_donairs = donair_counts.get(user_id, {'Veggie': 0, 'Falafel': 0, 'Chicken': 0, 'Beef': 0})
    user_points = money.get(ctx.author.id, 0)
    await ctx.send(f'You currently have {user_points} turkish liras\n {user_donairs["Veggie"]} veggie donairs\n {user_donairs["Falafel"]} falafel donairs\n {user_donairs["Chicken"]} chicken donairs\n {user_donairs["Beef"]} beef donairs')

@bot.command(name="info")
async def info(ctx):
    embed = discord.Embed(
    colour=discord.Colour.orange(),
    title="Welcome to Shawarma Sheriff!",
    description=("\nYou are a fiend for donair, your sole purpose in life is to eat as many delicious donairs as possible. \n\nThis game can be played using the following commands:\n \n/register: to join the game (required to save progress)\n/rummage: search for loot\n/roll: trade your money to find new Donair\n/rob: steal money from our players, but risk getting caught and losing money\n/heist: call on another player to help you rob someone for even more money, but with a bigger risk\n/stats: display your current donair stats\n/flex: compare your wealth to other players\n")

    )
    await ctx.send(embed=embed)
    
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
            update_entry(id,'Veggie',readinfo(id)[1]+1)

        if 350 <= rollval <820: 
            flav1="Still insubstantial; Think of it as a precursor to donair."
            embed.set_image(url="attachment://Falafel.png")
            dfile=discord.File("Falafel.png")
            donair = "Falafel"
            update_entry(id,'Falafel',readinfo(id)[2]+1)

        if 820<= rollval <950: 
            flav1="A staple of donair. Juicy, seasoned chicken"
            embed.set_image(url="attachment://Shawarma (1).png")
            dfile=discord.File("Shawarma (1).png")
            donair = "Chicken"
            update_entry(id,'Chicken',readinfo(id)[3]+1)
        if 950 <= rollval <1001: 
            flav1="Now you know what’s in it, and it turns out the perfect donair all along was just Beef."
            embed.set_image(url="attachment://Beef.png")
            dfile=discord.File("Beef.png")
            donair = "Beef"
            update_entry(id,'Beef',readinfo(id)[4]+1)
           
        if  1001 <= rollval: 
            flav1="Now you know what’s in it, and it turns out the perfect donair all along was just Beef."
            embed.set_image(url="attachment://Beef.png")
            dfile=discord.File("Beef.png")
            
            donair = "Beef"
            update_entry(id,'Beef',readinfo(id)[4]+1)

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
