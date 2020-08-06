import discord
import random
import yaml

with open("./conf.yaml") as conf:
    config = yaml.load(conf, Loader=yaml.BaseLoader)

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
                await message.add_reaction(config["banjo"])

async def pedant(message):
    content = message.content.lower()

    if("-ass" in content):
        await message.channel.send(content.replace("-ass ", " ass-"))

    if("sonic" in content):
        await message.channel.send("Gotta love that Fast Guy.")
    
    if("lol" in content or "ioi" in content):
        await message.channel.send("lol")

    if("classic" in content):
        await message.channel.send("*classic*")
