import discord
import pickledb
import random
import re
from collections import deque
from datetime import *
from math import pow
from discord import Embed
from otherdave.commands.give import find, use
from otherdave.commands.haiku import recall
from otherdave.commands.ignore import ignoreBandit
from otherdave.commands.recommend import recommend
from otherdave.util import config, constants

memCache = deque(maxlen=config.cacheLength)
memories = pickledb.load("./data/quotes.db", True)
if (not memories.get(constants.allQuotes)):
    memories.set(constants.allQuotes, [])

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

async def remember(interaction: discord.Interaction, member: discord.Member, snippet: str) -> str:
    async for msg in interaction.channel.history(limit=config.maxLookback):
        if(msg.author.id == member.id and snippet in msg.content):
            return await remember_msg(msg)

    return constants.saveFailed


async def remember_msg(msg: discord.Message) -> str:
    if(memories.get(msg.author.id)):
        memories.append(str(msg.author.id), [msg.content])
    else:
        memories.set(str(msg.author.id), [msg.content])

    memories.append(constants.allQuotes, [[msg.author.id, msg.content]])
    await msg.add_reaction(config.emotions["_memorymoji"])
    return constants.saveSuccessful

def parrot(mention: str) -> str:
    if(mention):
        nick = re.sub("<@!*|>", "", mention)
        if(not memories.get(nick)):
            return constants.notFound
        rmem = random.choice(memories.get(nick))
        memCache.append([nick, rmem])
        return rmem
    else:
        if(len(memories.get(constants.allQuotes)) == 0):
            return constants.emptyMemory
        rmem = random.choice(memories.get(constants.allQuotes))
        memCache.append([rmem[0], rmem[1]])
        return rmem[1]

async def toucan(client: discord.Client, lastMsgTime: datetime, quietTime: datetime) -> None:
    now = datetime.now()
    delta = (now - lastMsgTime).total_seconds()
    if(quietTime and now < quietTime):
        return

    if(delta >= 14400 or random.randint(0, 100) <= squawkProb(delta)):
        # Pick an action
        match (random.randint(0, 100)):
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

        if(macaw == constants.emptyMemory):
            return None
        parrotChan = await client.fetch_channel(config.parrotChan)

        if(isinstance(macaw, Embed)):
            return await parrotChan.send(embed = macaw)
        
        return await parrotChan.send(macaw)

def forget(snippet: str) -> str:
    if(len(memCache) == 0):
        return constants.emptyBuffer
    
    memory = None
    if(snippet):
        memory = next((mem for mem in reversed(memCache) if snippet in mem[1]), None)
        if(memory):
            memCache.remove(memory)
        else:
            return constants.badKeywords
    else:
        memory = memCache.pop()
    
    memories.get(memory[0]).remove(memory[1])
    memories.get(constants.allQuotes).remove(memory)
    
    # Because pickleDB doesn't support list element removal properly, dump manually
    memories.dump()
    return constants.forgetSuccess

def forget_msg(message: discord.Message) -> str:
    if (message.author != config.selfid):
        return constants.forgetYou
    return forget(message.content)