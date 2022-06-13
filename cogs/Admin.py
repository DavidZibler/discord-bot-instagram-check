# ----------{ Imports requirements }----------
import discord
from discord.ext import commands
from discord.commands import slash_command

min_required_role = "Verified"
generator_role = "code-generated"
# instagram_post_channel = 984938847207034941

instagram_proof_channel = 985952165359124565


# ----------{ Debug class }----------
class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ----------{ Methods }----------
    '''< Check >
    Check when someones post an image to a specific channel whether it is an image and has its code implemented
    '''
    @commands.Cog.listener()
    async def on_message(self, message):
        # Check for roles

        # Check for right channel
        if message.channel.id == instagram_proof_channel:
            # Check for image
            if len(message.attachments) <= 0:
                await message.delete()
            else:
                user_message = message.attachments[0]
                print(str(user_message))
        else:
            print('Wrong channel')


# ----------{ Cog export }----------
def setup(bot):
    bot.add_cog(Admin(bot))
