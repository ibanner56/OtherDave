import discord
import logging
from commands import dlog
from commands import update

# Configure client
ver = "2.0.0, now proudly on python :snake:"
client = discord.Client()
async def ping(client, message, args):
    await message.channel.send("pong")
async def version(client, message, args):
    await message.channel.send("OtherDave is running version " + ver)

functions = {
    "ping": ping,
    "update": update.do,
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
    await dlog.log(client, "Hi, I'm OtherDave and I'm BACK FOR BUSINESS.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    content = message.content
    if content.startswith("!"):
        command, *args = content.lstrip("!").split(" ", 1)
        logger.info(command + " - user: " + message.author.name)
        if command in functions:
            await functions[command](client, message, args)
        else:
            await message.channel.send("I'm sorry Dave, I'm afraid I can't do that.")

if __name__ == "__main__":
    tokenFile = open("bot.tkn", "r")
    token = tokenFile.read()
    client.run(token)