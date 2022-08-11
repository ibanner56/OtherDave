import pickledb
import random
import re
import yaml
from collections import deque
from datetime import *
from math import pow
from discord import Embed
from otherdave.commands.give import find, use
from otherdave.commands.haiku import recall
from otherdave.commands.ignore import ignoreBandit
from otherdave.commands.recommend import recommend

_allQuotes = "_all"
_badKeywords = "I don't remember saying that."
_emptyBuffer = "I haven't said anything yet."
_emptyMemory = "Do I even know you people?"
_forgetSuccess = "Got it, I'll forget you said that."
_invalidArgs = "I need a user and some keywords to do that."
_notFound = "I don't remember anything they've said!"
_saveFailed = "Sorry, I don't remember that."

with open("./conf.yaml", encoding="utf-8") as conf:
    config = yaml.load(conf, Loader=yaml.FullLoader)

memCache = deque(maxlen=config["cache_length"])
memories = pickledb.load("./data/quotes.db", True)
if (not memories.get(_allQuotes)):
    memories.set(_allQuotes, [])

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

async def remember(ctx, args):
    if(len(args) < 2):
        return _invalidArgs
    else:
        nick = re.sub("<@!*|>", "", args[0])
        snippet = " ".join(args[1:])

        async for msg in ctx.channel.history(limit=config["max_lookback"]):
            # Ignore commands
            if(msg.content.startswith("!")):
                continue

            if(str(msg.author.id) == nick and snippet in msg.content):
                if(memories.get(nick)):
                    memories.append(nick, [msg.content])
                else:
                    memories.set(nick, [msg.content])

                memories.append(_allQuotes, [[nick, msg.content]])
                await ctx.message.add_reaction(config["emotions"]["_memorymoji"])
                return None

        return _saveFailed

def parrot(args = []):
    if(len(args) > 0):
        nick = re.sub("<@!*|>", "", args[0])
        if(not memories.get(nick)):
            return _notFound
        rmem = random.choice(memories.get(nick))
        memCache.append([nick, rmem])
        return rmem
    else:
        if(len(memories.get(_allQuotes)) == 0):
            return _emptyMemory
        rmem = random.choice(memories.get(_allQuotes))
        memCache.append([rmem[0], rmem[1]])
        return rmem[1]

async def toucan(client, lastMsgTime, quietTime):
    now = datetime.now()
    delta = (now - lastMsgTime).total_seconds()
    if(quietTime and now < quietTime):
        return

    if(delta >= 14400 or random.randint(0, 100) <= squawkProb(delta)):
        # Pick an action
        match random.randint(0, 100):
            case n if n == 0:
                mins = random.randint(1, 60)
                macaw = ignoreBandit(mins)
            case n if 1 <= n < 50:
                macaw = parrot()
            case n if 50 <= n < 75:
                macaw = recall()
            case n if 75 <= n < 85:
                macaw = find()
            case n if 85 <= n < 95:
                macaw = use()
            case n if 95 <= n <= 100:
                macaw = recommend()
            case _:
                return None

        if(macaw == _emptyMemory):
            return None
        parrotChan = await client.fetch_channel(config["parrot_channel"])

        if(isinstance(macaw, Embed)):
            return await parrotChan.send(embed = macaw)
        
        return await parrotChan.send(macaw)

def forget(args):
    if(len(memCache) == 0):
        return _emptyBuffer
    
    memory = None
    if(args):
        keywords = " ".join(args)
        memory = next((mem for mem in reversed(memCache) if keywords in mem[1]), None)
        if(memory):
            memCache.remove(memory)
        else:
            return _badKeywords
    else:
        memory = memCache.pop()
    
    memories.get(memory[0]).remove(memory[1])
    memories.get(_allQuotes).remove(memory)
    
    # Because pickleDB doesn't support list element removal properly, dump manually
    memories.dump()
    return _forgetSuccess
