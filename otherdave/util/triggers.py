import discord
import pickledb
import random
import yaml

_pedantUsage = "*Actually*, the correct usage is '!pedant -me | -stop'."

with open("./conf.yaml") as conf:
    config = yaml.load(conf, Loader=yaml.BaseLoader)

grumps = pickledb.load("./data/grumps.db", True)

async def react(message):
    for emotion in config["emotions"]:
        if(emotion in message.content.lower()):
            emoji = config["emotions"][emotion]
            if(len(emoji) == len(emoji.encode())):
                emoji = discord.utils.get(message.guild.emojis, name=config["emotions"][emotion])
            if emoji:
                await message.add_reaction(emoji)
            elif(random.randrange(100) > 99):
                # Deploy random banjo
                await message.add_reaction(config["emotions"]["_banjo"])

async def grump(client, message, args):
    if (len(args) != 1):
        await message.channel.send(_pedantUsage)
    
    if (args[0] == "-me"):
        grumps.set(str(message.author.id), False)
        await message.add_reaction(config["emotions"]["_teacher"])
    elif (args[0] == "-stop"):
        grumps.set(str(message.author.id), True)
        await message.add_reaction(config["emotions"]["_zipit"])
    else:
        await message.channel.send(_pedantUsage)
    

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
