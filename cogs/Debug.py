# ----------{ Imports requirements }----------
import discord
from discord.ext import commands
from discord.commands import slash_command


# ----------{ Debug class }----------
class Debug(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ----------{ Methods }----------
    '''< Ping call >
    Check if bot responds to your first call.
    '''
    @slash_command(name="ping", description="pong")
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx):
        print("pong")
        await ctx.respond("pong", delete_after=3)


# ----------{ Cog export }----------
def setup(bot):
    bot.add_cog(Debug(bot))
