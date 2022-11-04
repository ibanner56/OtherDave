import discord
import pickledb
import random
from otherdave.util import config, constants

grumps = pickledb.load("./data/grumps.db", True)

async def react(message):
    for emotion in config.emotions:
        if(emotion in message.content.lower()):
            emoji = config.emotions[emotion]
            if(len(emoji) == len(emoji.encode())):
                emoji = discord.utils.get(message.guild.emojis, name=config.emotions[emotion])
            if emoji:
                await message.add_reaction(emoji)
            elif(random.randrange(100) > 99):
                # Deploy random banjo
                await message.add_reaction(config.emotions["_banjo"])

def grump(interaction, action):
    if (action == "enable"):
        grumps.set(str(interaction.user.id), False)
        return config.emotions["_teacher"]
    elif (action == "disable"):
        grumps.set(str(interaction.user.id), True)
        return config.emotions["_zipit"]
    else:
        return constants.pedantUsage

    return None
    
async def pedant(message):
    if (grumps.get(str(message.author.id))):
        return

    content = message.content.lower()

    if("-ass" in content):
        await message.channel.send(content.replace("-ass ", " ass-"))

    if("sonic" in content):
        await message.channel.send("Gotta love that Fast Guy.")
    
    if("lol" in content or "ioi" in content):
        await message.channel.send("lol")

    if("classic" in content):
        await message.channel.send("*classic*")
