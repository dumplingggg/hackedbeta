import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('token')

intents = discord.Intents(8)
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user}) has connected to Discord!')

client.run('token')