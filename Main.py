import os

# Discord import
import discord
from discord.ext import commands
# For env
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intent = (discord.Intents.all())
client = discord.Client(intents=intent)
bot = commands.Bot(command_prefix='::', intents=intent)

options = (
    "Usage:\n"
+   "::help     |   Brings up this menu any time\n"
+   "::add      |   To add an event\n"
+   "::remove   |   To remove an event"
)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for guild in client.guilds:
        print(guild.name)
        print(guild.id)

@bot.command()
async def add(ctx, message:str):
    await ctx.send(message)

@bot.listen('on_message')
async def send(message):
    if message.author == bot.user:
        return
    
    if message.content == ('::'):
        await message.channel.send(options)

bot.run(TOKEN)