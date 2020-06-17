import asyncio
import discord
import logging
import yaml
from datetime import *
from otherdave.commands import haiku
from otherdave.commands.drunkdraw import drunkdraw
from otherdave.commands.memory import *
from otherdave.commands.mimic import *
from otherdave.commands.prompt import prompt
from otherdave.commands.respect import respect
from otherdave.util.dlog import dlog
from otherdave.util.triggers import *

# Configure client
with open("./conf.yaml") as conf:
    config = yaml.load(conf, Loader=yaml.BaseLoader)
client = discord.Client()
quietTime = None
parakeet = True

async def ping(client, message, args):
    await message.channel.send("pong")

async def quiet(client, message, args):
    global quietTime
    try:
        min = 5
        if(len(args)):
            min = int(args[0])

        quietTime = datetime.now() + timedelta(minutes=min)
        await message.channel.send("Got it, I'll keep quiet for " + args[0] + " minutes.")
    except:
        await message.channel.send("Sorry, not sure how long that is...defaulting to 5 min")
        quietTime = datetime.now() + timedelta(minutes=5)

async def version(client, message, args):
    await message.channel.send("OtherDave is running version " + str(config["version"]))

async def squawk():
    await client.wait_until_ready()
    while(not client.is_closed()):
        await asyncio.sleep(int(config["parrot_interval"]))

        global parakeet
        if(parakeet):
            await toucan(client)
        else:
            parakeet = True

functions = {
    "drunkdraw": drunkdraw,
    "haiku": haiku.critique,
    "forget": forget,
    "mimic": mimic,
    "parrot": parrot,
    "ping": ping,
    "prompt": prompt,
    "quiet": quiet,
    "remember": remember,
    "respect": respect,
    "version": version
}

# Set up logging
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="./logs/otherdave.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

# Configure events
@client.event
async def on_ready():
    logger.debug("Logged in as {0.user}".format(client))
    await dlog(client, "Hi, I'm OtherDave and I'm BACK FOR BUSINESS.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    global parakeet
    parakeet = False
    content = message.content
    if content.startswith("!"):
        command, *args = content.lstrip("!").split(" ")
        logger.info(command + " - user: " + message.author.name)
        if command in functions:
            await functions[command](client, message, args)
        else:
            await message.channel.send("I'm sorry Dave, I'm afraid I can't do that.")

    else:
        global quietTime
        if(quietTime and datetime.now() > quietTime):
            quietTime = None

        if(not quietTime):
            await haiku.detect(message)
            await react(message)
            await pedant(message)

        # otherdave is always listening...
        listen(message)

@client.event
async def on_reaction_add(reaction, user):
    if(reaction.message.author != client.user):
        return
    if(reaction.count == 1 and reaction.emoji in config["rereactions"]):
        await reaction.message.channel.send(config["rereactions"][reaction.emoji])

if __name__ == "__main__":
    tokenFile = open("bot.tkn", "r")
    token = tokenFile.read()
    client.loop.create_task(squawk())
    client.run(token)