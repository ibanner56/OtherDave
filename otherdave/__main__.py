import asyncio
import discord
import logging
import yaml
from datetime import *
from discord.ext import tasks
from otherdave.commands import haiku
from otherdave.commands.drunkdraw import drunkdraw
from otherdave.commands.jabber import *
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
lastMsgTime = None

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

functions = {
    "beach": beach,
    "drunkdraw": drunkdraw,
    "forget": forget,
    "haiku": haiku.critique,
    "mimic": mimic,
    "parrot": parrot,
    "pedant": grump,
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

# Configure tasks
@tasks.loop(seconds=int(config["parrot_interval"]))
async def squawk():
    await toucan(client, lastMsgTime, quietTime)
    
# Configure events
@client.event
async def on_ready():
    logger.debug("Logged in as {0.user}".format(client))
    await dlog(client, "Hi, I'm OtherDave and I'm BACK FOR BUSINESS.")
    await squawk.start()

@client.event
async def on_message(message):
    global lastMsgTime
    lastMsgTime = datetime.now()
    if message.author == client.user:
        return
    
    content = message.content
    if content.startswith("!"):
        command, *args = content.lstrip("!").split(" ")
        logger.info(command + " - user: " + message.author.name)
        if command.lower() == "help":
            await botHelp(client, message, args if args else [*functions.keys()])
        elif command in functions:
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
    client.run(token)