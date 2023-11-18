import discord
import dotenv
import random
from discord.ext import commands
bot = commands.Bot(command_prefix='/')
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
@bot.command(name = 'info')
async def info(ctx):
    await ctx.send('ShawarmaSheriff is a gacha game where you randomly draw donairs of different rarities')
bot.run()