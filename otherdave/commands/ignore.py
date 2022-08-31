import pickledb
import re
from datetime import *
from otherdave.util import config, constants

ignoreDb = pickledb.load("./data/ignore.db", True)
slideDb = pickledb.load("./data/slide.db", True)

async def ignore(ctx, args):
    if (len(args) < 1 or len(args) > 2):
        return constants.ignoreUsage
    
    try:
        if (len(args) == 2):
            mins = int(args[1])
        else:
            mins = 5
    except ValueError:
        return constants.ignoreUsage
    
    ignoreTime = datetime.now() + timedelta(minutes=mins)

    if (args[0] == "-me"):
        ignoreDb.set(str(ctx.author.id), ignoreTime.isoformat())
        await ctx.message.add_reaction(config.emotions["_zipit"])
        return None
    else:
        author = ctx.author.name
        if (author != "Isaac" and author != "MercWorks"):
            return "Mama Mia! Only Dave can do that!"

        nick = re.sub("<@!*|>", "", args[0])
        ignoreDb.set(nick, ignoreTime.isoformat())
        return f"Got it, I'll ignore {args[0]} for {mins} minutes. They must have been *naughty!*"

def ignoreBandit(mins):
    bandit = "442747712400654337"
    ignoreTime = datetime.now() + timedelta(minutes=mins)
    ignoreDb.set(bandit, ignoreTime.isoformat())
    return f"Got it, I'll ignore <@!{bandit}> for {mins} minutes. They must have been *naughty!*"

def dms(userId, flag):
    userId = str(userId)
    if (flag == "-enable"):
        if (slideDb.get(userId)):
            slideDb.rem(userId)
        return "Got it, I'll be sliding into those dms sometime soon."
    elif (flag == "-disable"):
        slideDb.set(userId, True)
        return "Okay, I won't send you any direct messages."
    else:
        return constants.dmsUsage

def shouldIgnore(userId):
    userId = str(userId)
    timeStr = ignoreDb.get(userId)
    if (timeStr):
        ignoreTime = datetime.fromisoformat(timeStr)
        if (datetime.now() > ignoreTime):
            ignoreDb.rem(userId)
            return False
        return True
    return False

def canDm(userId):
    userId = str(userId)
    return slideDb.get(userId) != True