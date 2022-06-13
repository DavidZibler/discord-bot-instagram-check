# -----{ Imports requirements }-----
import discord
from discord.ext import commands
import os   # default module
from dotenv import load_dotenv

# ----------{ Global variables }----------
guild_id = '954021637060173884'
guild_id_test = '961268598800777286'    # Testing


load_dotenv()   # load all the variables from the env file
bot = commands.Bot(guild_ids=[guild_id, guild_id_test],
                   command_prefix="/",
                   intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("---------------------------------------------------")
    print("RRC - Code Generator, bot is loaded & ready to use!")
    print(f"{bot.user} is online & Watching {len(bot.guilds)} servers.")
    print("---------------------------------------------------")


cogFiles = []
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        cogFiles.append("cogs." + filename[:-3])


for cogFile in cogFiles:
    try:
        print("Loading file " + cogFile)
        bot.load_extension(cogFile)
    except Exception as err:
        print(err)


bot.run(os.getenv('TOKEN'))
