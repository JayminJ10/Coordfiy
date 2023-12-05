# For env
from dotenv import load_dotenv
import os
# Discord import
import discord
from discord.ext import commands
# Datetime
import datetime
from datetime import datetime
# sqlite3
import sqlite3
# For pattern matching
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intent = (discord.Intents.all())
client = discord.Client(intents=intent)
bot = commands.Bot(command_prefix='::', intents=intent)

sqlcon = sqlite3.connect("coordify.db")
cursor = sqlcon.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS events(server, year, month, day, event, UNIQUE(server, year, month, day, event))")

options = (
    "Usage:\n"
+   "::help     |   Brings up this menu any time\n"
+   "::add      |   To add an event\n"
+   "::remove   |   To remove an event\n"
+   "::view     |   To view this month"
)

incorrect_add = ("Usage: ::add ['event'] ['(mm/dd/yyyy)']\n*No brackets*")
incorrect_view = ("Usage: ::view *Optional*['(mm/dd/yyyy)']\n*No brackets*")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        print(guild.name)
        print(guild.id)
    # main()

@bot.command()
async def test(ctx):
   server = str(ctx.message.guild.id)
   res = cursor.execute("SELECT name FROM sqlite_master")
   out = res.fetchone()
   await ctx.send(out)

def check_err(month):
    return re.fullmatch("../../....", month) == None

def parse_month(mon) -> list:
    return (mon.split('/'))

def list_itr(results) -> str:
    out = ""
    for entry in results:
        out += "Date: " + entry[3] + "/" + entry[2] + "/" + entry[1] + "\n"
        out += "Event: " + entry[4] + "\n"
        out += "\n"
    return out

@bot.command()
async def view(ctx, *args):
    server = str(ctx.message.guild.id)
    if len(args) == 0:
        thismonth = (datetime.now().month)
        thisyear = (datetime.now().year)
        print(thismonth)
        print(thisyear)
        query = f"SELECT * FROM events WHERE server={server} AND year='{thisyear}' AND month='{thismonth}'"
        res = cursor.execute(query)
        out = cursor.fetchall()
        msg = list_itr(out)
        print(msg)
        if len(msg) == 0:
            await ctx.send("No events to show")
        else:
            await ctx.send(msg)
    elif len(args) == 1:
        if check_err(args[0]):
            await ctx.send(incorrect_view)
        else:
            date = parse_month(args[0])
            day = date[0]
            month = date[1]
            year = date[2]
            # WHERE server=? AND year=? AND month=? AND day=?"" - (server, year, month, day,)
            query = f"SELECT * FROM events WHERE server={server} AND year='{year}' AND month='{month}' AND day='{day}'"
            res = cursor.execute(query)
            out = cursor.fetchall()
            msg = list_itr(out)
            await ctx.send(msg)

@bot.command()
async def add(ctx, *args):
    server = str(ctx.message.guild.id)
    
    if len(args) == 0 or len(args) == 1:
        await ctx.send(incorrect_add)
    else:
        if check_err(args[1]):
            await ctx.send(incorrect_add)
        else:
            event = args[0]
            date = args[1]
            seperate = parse_month(date)
            day = seperate[0]
            month = seperate[1]
            year = seperate[2]
            query_add = f"INSERT OR IGNORE INTO events (server, year, month, day, event) VALUES ({server}, '{year}', '{month}', '{day}', '{event}')"
            res = cursor.execute(query_add)
            #out = res.fetchone()
            st = f"Added/Attempted to add: \"{event}\"" + " on " + date + "."
            cursor.connection.commit()
            await ctx.send(st)

@bot.listen('on_message')
async def send(message):
    if message.author == bot.user:
        return
    
    if message.content == ('::'):
        await message.channel.send(options)

bot.run(TOKEN)