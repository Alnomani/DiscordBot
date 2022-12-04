import discord
import random
import csv
import os
import dotenv
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()
token = os.getenv('TOKEN')
channel_id = int(os.getenv('CHAN'))
ad_role_code = int(os.getenv('AD_ROLE'))

intents = discord.Intents.default()
from_command = False
intents.members = True
intents.presences = True
intents.message_content = True
#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/',intents=intents)
#callback is a function that is called when something else happens.

@bot.tree.command(name = "neakyname", description = "Changes nickname to a random neaky name.")
async def neakyname(interaction: discord.Interaction):
    print("inside neakyname()")
    await interaction.response.defer( ephemeral = True) #delay response failed till followup
    with open("Names.txt","r",encoding='utf8') as file:
        names = file.readlines()
    randomName = random.choice(names)
    print("Change made by:",interaction.user.nick)
    roles = [role.name for role in interaction.user.roles]
    if "Daddy Sunshine" not in roles:
        global from_command
        from_command = True
        await interaction.user.edit(nick=randomName)
        from_command = False
        await interaction.followup.send("You are now known as {rndName}! Good luck.".format(rndName = randomName))
    else:
        await interaction.followup.send("Stop trying to change your name! You're not {rndName}!".format(rndName = randomName))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("No permissions for that shizzle")
        await ctx.message.delete(delay=2)
        
@bot.event
async def on_ready():
    print('Blijf thuis')

@bot.event
async def on_message(message):
    if message.author.bot: # message.author == bot.user:
        return
    if message.content == 'hello':
        print("message receiverd!")
        await message.channel.send("Knurt!")
    await bot.process_commands(message)

@bot.event
async def on_member_update(before, after):
    if before.nick != after.nick and (before.nick and after.nick) and not from_command:
        print(before.nick+ " changed to " + after.nick)
        userName = "**" + before.name + "**: "
        print(userName)
        channel=bot.get_channel(channel_id)
        await channel.send(userName + after.nick)
        with open("Names.txt","a",encoding='utf8') as file:
            file.write(after.nick + "\n")
        

@commands.has_role(ad_role_code)
@bot.tree.command(name = "synccmds", description= "syncs new commands, requires admin role.")
async def syncCmd(interaction: discord.Interaction):
    await bot.tree.sync()
    await interaction.response.send_message("done syncing via command", ephemeral=True)



@commands.has_role(int(ad_role_code))
@bot.tree.command(name = "savenames", description= "saves names from neaky-names to txt")
async def saveNames(interaction: discord.Interaction):
    await interaction.response.defer( ephemeral = True)
    channel=bot.get_channel(channel_id)
    names = []
    async for message in channel.history(limit=None):
        if ":" in message.content:
            msg = message.content.split(":")[1].replace("**", "").strip()
            if msg not in names:
                names.append(msg)
    with open("Names.txt","w+",encoding='utf8') as file:
        for name in names:
            file.write(name + "\n")
    await interaction.followup.send("Successfully written to file!")
bot.run(token)