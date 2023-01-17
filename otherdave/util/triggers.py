import discord
import json
import pickledb
import random
from otherdave.util import config, constants

grumps = pickledb.load("./data/grumps.db", True)

with open("./data/units.json") as unitsf:
    units = json.load(unitsf)

commonConversions = [
    lambda x: x * 100.0, 
    lambda x: x * (5.0/9.0) + 32,
    lambda x: x * 2.54,
    lambda x: x * 36,
    lambda x: x * 5280,
    lambda x: x * 6894.76,
    lambda x: x * 0.453592,
    lambda x: x * 0.907185,
    lambda x: x * 28.3495,
    lambda x: x * 3.78514,
]

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

    await converter(message, content)

async def converter(message, content):
    content = content.split(" ")

    for i in range(0, len(content)):
        if content[i] in units["unit"] or content[i] in units["units"]:
            if (i-1 >= 0) and content[i-1].isnumeric():
                value = random.choice(commonConversions)(float(content[i-1]))
                unit = random.choice(units["units"])
                await message.channel.send(f"{content[i-1]} {content[i]} is equivalent to {value} {unit}")