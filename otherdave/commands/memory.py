import pickledb
import random
import re
import yaml
from collections import deque
from datetime import *
from math import pow

_badKeywords = "I don't remember saying that."
_emptyBuffer = "I haven't said anything yet."
_emptyMemory = "Do I even know you people?"
_forgetSuccess = "Got it, I'll forget you said that."
_invalidArgs = "I need a user and some keywords to do that."
_notFound = "I don't remember anything they've said!"
_saveFailed = "Sorry, I don't remember that."

with open("./conf.yaml", encoding="utf-8") as conf:
    config = yaml.load(conf, Loader=yaml.FullLoader)

memories = pickledb.load("./data/quotes.db", True)
memCache = deque(maxlen=config["cache_length"])

# Cubic Regression to match:
#     00 sec ->   0% chance
#   1800 sec ->  10% chance  
#   3600 sec ->  20% chance
#   5400 sec ->  35% chance
#   7200 sec ->  50% chance
#  10800 sec ->  80% chance
#  14400 sec -> 100% chance
squawkProb = lambda x : (
    -0.00000000003264*pow(x, 3) + 
    0.00000070566321*pow(x, 2) + 
    0.00352638263119*x + 
    0.43326434481060
)

async def remember(client, message, args):
    if(len(args) < 2):
        return await message.channel.send(_invalidArgs)
    else:
        nick = re.sub("<@!*|>", "", args[0])
        snippet = " ".join(args[1:])

        async for msg in message.channel.history(limit=config["max_lookback"]):
            # Ignore commands
            if(msg.content.startswith("!")):
                continue

            if(str(msg.author.id) == nick and snippet in msg.content):
                if(memories.get(nick)):
                    memories.append(nick, [msg.content])
                else:
                    memories.set(nick, [msg.content])
                return await message.add_reaction(config["memorymoji"])

        return await message.channel.send(_saveFailed)

def parrot_internal(args):
    if(args):
        nick = re.sub("<@!*|>", "", args[0])
        if(not memories.get(nick)):
            return _notFound
        rmem = random.choice(memories.get(nick))
        memCache.append((nick, rmem))
        return rmem
    else:
        memkeys = list(memories.getall())
        if(len(memkeys) == 0):
            return _emptyMemory
        rkey = random.choice(memkeys)
        if(len(memories.get(rkey)) == 0):
            return _emptyMemory
        rmem = random.choice(memories.get(rkey))
        memCache.append((rkey, rmem))
        return rmem

async def parrot(client, message, args):
    return await message.channel.send(parrot_internal(args))

async def toucan(client, lastMsgTime, quietTime):
    now = datetime.now()
    delta = (now - lastMsgTime).total_seconds()
    if(quietTime and now < quietTime):
        return

    if(random.randint(0, 100) <= squawkProb(delta)):
        macaw = parrot_internal([])
        if(macaw == _emptyMemory):
            return None
        parrotChan = await client.fetch_channel(config["parrot_channel"])
        return await parrotChan.send(macaw)

async def forget(client, message, args):
    if(len(memCache) == 0):
        return await message.channel.send(_emptyBuffer)
    if(args):
        keywords = " ".join(args)
        memory = next((mem for mem in reversed(memCache) if keywords in mem[1]), None)
        if(memory):
            memCache.remove(memory)
            memories.get(memory[0]).remove(memory[1])
        else:
            return await message.channel.send(_badKeywords)
    else:
        memory = memCache.pop()
        memories.get(memory[0]).remove(memory[1])
    
    # Because pickleDB doesn't support list element removal properly, dump manually
    memories.dump()
    return await message.channel.send(_forgetSuccess)
