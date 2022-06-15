# ----------{ Imports requirements }----------
import io
import requests
import discord
import re
import pytesseract
from discord.ext import commands
from discord.utils import get
from discord.commands import slash_command
from PIL import Image


min_required_role = "Verified"
generator_role = "code-generated"
instagram_verified_role = 'instagram-verified'

# Live
# generated_code_channel = 984938847207034941
# instagram_proof_channel = 986306991221768262
# failed_proof_channel = 986307051904991232

# Testing
generated_code_channel = 983717228098760794
instagram_proof_channel = 985952165359124565
failed_proof_channel = 986543485060513813


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
        # Set variables
        member = message.author
        member_id = int(member.id)
        gen_role = get(message.guild.roles, name=generator_role)
        min_role = get(message.guild.roles, name=min_required_role)
        insta_role = get(message.guild.roles, name=instagram_verified_role)
        # Channels
        _generated_code_channel = self.bot.get_channel(generated_code_channel)
        _failed_proof_channel = self.bot.get_channel(failed_proof_channel)
        # Resending
        code_string: str = ''

        if message.channel.id == instagram_proof_channel:   # Check for right channel
            if member != self.bot.user:     # Check for bot (don't react to own message)
                if min_role in member.roles:    # Check for roles "Verified" role
                    if gen_role in member.roles:     # Check for roles "generate-role"
                        if insta_role not in member.roles:
                            if len(message.attachments) <= 0:   # Check for image
                                await message.channel.send("Missing image to social proof yourself.", delete_after=3)
                            else:
                                # Get image url from message
                                image_url = message.attachments[0].url  # Get image from discord message
                                response = requests.get(image_url)  # Get image response
                                tesseract_image = Image.open(io.BytesIO(response.content))  # Create tesseract image

                                # Get string by tesseract image
                                image_string = pytesseract.image_to_string(tesseract_image, 'eng')
                                print('Image string ' + image_string)
                                tesseract_string_array = re.split(r',|\n| ', image_string)
                                print(tesseract_string_array)

                                # Get user code
                                message_list = await _generated_code_channel.history().flatten()

                                # Control boolean
                                member_found = False
                                code_found = False

                                # Check messages & compare code
                                for i in message_list:
                                    name_id = int(str(str(i.content).split()[0]).replace("<", "").replace(">", "").replace("@", ""))
                                    if name_id == member_id and not member_found:
                                        code_string = str(str(i.content).split()[2])    # Get user code
                                        member_found = True

                                        # Check for code
                                        for j in tesseract_string_array:
                                            print(str(j) + ' ')     # + str(code_string)
                                            if str(j) == str(code_string) and not code_found:
                                                code_found = True

                                if not member_found:
                                    # Create failed proof embed
                                    image_embed = discord.Embed(
                                        title='Failed proof',
                                        description='Reason: @name not found \n'
                                                    '@name: ' + str(member.mention) + '\n'
                                                                                 'Code: ' + code_string,
                                        color=discord.Color.dark_magenta()
                                    )
                                    image_embed.set_image(url=message.attachments[0].url)

                                    await _failed_proof_channel.send(embed=image_embed)

                                    # Create private message embed
                                    embed = discord.Embed(
                                        title='🚨 **Warning** 🚨',
                                        description='We were no able to find your @name.\n'
                                                    '\n'
                                                    'We are manually checking what happened.\n'
                                                    'This might take some time, stay tuned.\n'
                                                    '\n'
                                                    'We are going to contact you as soon as we know more.',
                                        color=discord.Color.dark_magenta()
                                    )
                                    await member.send(embed=embed)
                                    await message.channel.send("We didn't find your name. Please contact an admin or moderator.", delete_after=3)
                                if code_found and member_found:
                                    embed = discord.Embed(
                                        title='🎉 **Congratulations** 🎊',
                                        description='Your instagram story got proofed correctly.\n'
                                                    'We added the instagram-verified role to your account.',
                                        color=discord.Color.dark_magenta()
                                    )

                                    await member.add_roles(insta_role)
                                    await member.send(embed=embed)
                                    await message.channel.send('Instagram code found & proofed.', delete_after=2)  # Code proofed
                                else:
                                    # Create failed proof
                                    image_embed = discord.Embed(
                                        title='Failed proof',
                                        description='Reason: Code not found \n'
                                                    '@name: ' + str(member.mention) + '\n'
                                                                                 'Code: ' + code_string,
                                        color=discord.Color.dark_magenta()
                                    )
                                    image_embed.set_image(url=message.attachments[0].url)

                                    await _failed_proof_channel.send(embed=image_embed)

                                    # Create private message embed
                                    embed = discord.Embed(
                                        title='🚨 **Warning** 🚨',
                                        description='We were no able to find your code.\n'
                                                    '\n'
                                                    'We are manually checking what happened.\n'
                                                    'This might take some time, stay tuned.\n'
                                                    '\n'
                                                    'We are going to contact you as soon as we know more.',
                                        color=discord.Color.dark_magenta()
                                    )

                                    await member.send(embed=embed)
                                    await message.channel.send("We didn't find your code. Please contact an admin or moderator.", delete_after=3)
                        else:
                            await message.channel.send("You already proofed your instagram account!", delete_after=3)
                    else:
                        await message.channel.send("To social proof yourself generate your code first!", delete_after=3)
                else:
                    await message.channel.send("To social proof yourself verify yourself first!", delete_after=3)
                # Delete message at the end
                await message.delete()


# ----------{ Cog export }----------
def setup(bot):
    bot.add_cog(Admin(bot))
