import pickledb
import yaml
from collections import deque

_invalidArgs = "I need a user and some keywords to do that."
_saveSuccess = "Got it, I'll save that one for later."
_saveFailed = "Sorry, I don't remember that."

memories = pickledb.load("./data/quotes.db", True)
memCache = deque(maxlen=config["cache_length"])
with open("./conf.yaml", encoding="utf-8") as conf:
    config = yaml.load(conf, Loader=yaml.FullLoader)

async def remember(client, message, args):
    nick = args[0]
    snippet = " ".join(args[1:])

    if(not nick or not snippet):
        await message.channel.send(_invalidArgs)

    async with message.channel.typing():
        async for msg in message.channel.history(limit=config["max_lookback"]):
            if(msg.author == nick and snippet in msg.content):
                memories.append(nick, msg.content)
                await message.channel.send(_saveSuccess)
                return

        await message.channel.send(_saveFailed)

async def forget(client, message, args):
    return