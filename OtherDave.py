import discord
import logging
from lib import dlog
from lib import update

# Configure client
version = "2.0.0, now proudly on python :snake:"
client = discord.Client()
functions = {
    "ping": lambda client, message, args: message.channel.send("pong"),
    "update": update.do,
    "version": lambda client, message, args: message.channel.send("OtherDave is running version " + version)
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
    dlog.log(client, "Hi, I'm OtherDave and I'm BACK FOR BUSINESS.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    content = message.content
    if content.startswith("!"):
        command, args = content.lstrip("!").split(" ", 1)
        logger.info(command + " - user: " + message.author)
        if command in functions:
            functions[command](client, message, args)
        else:
            message.channel.send("I'm sorry Dave, I'm afraid I can't do that.")

if __name__ == "__main__":
    tokenFile = open("bot.tkn", "r")
    token = tokenFile.read()
    client.run(token)