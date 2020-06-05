import discord
import yaml

with open("./conf.yaml") as conf:
    config = yaml.load(conf, Loader=yaml.BaseLoader)

async def react(message):
    for emotion in config["emotions"]:
        if(emotion in message.content):
            emoji = discord.utils.get(message.guild.emojis, name=emotion)
            if emoji:
                message.add_reaction(emoji)

async def pedant(message):
    content = message.content.lower()

    if("-ass" in content):
        await message.channel.send(content.replace("-ass ", " ass-"))

    if("mario" in content):
        await message.channel.send("Mario? Is that like Hop Dude?\n*cough cough*")

    if("sonic" in content):
        await message.channel.send("Gotta love that Fast Guy.")
    
    if("lol" in content or "ioi" in content):
        await message.channel.send("lol")