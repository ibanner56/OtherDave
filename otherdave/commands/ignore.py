import pickledb
from datetime import *
from otherdave.util import config, constants

ignoreDb = pickledb.load("./data/ignore.db", True)
slideDb = pickledb.load("./data/slide.db", True)

async def ignore(interaction, user, mins):
    ignoreTime = datetime.now() + timedelta(minutes=mins)

    if (interaction.user.id == user.id):
        ignoreDb.set(str(user.id), ignoreTime.isoformat())
        await interaction.message.add_reaction(config.emotions["_zipit"])
        return None
    else:
        author = interaction.user.name
        if (author != "Isaac" and author != "MercWorks"):
            return "Mama Mia! Only Dave can do that!"

        ignoreDb.set(user.id, ignoreTime.isoformat())
        return f"Got it, I'll ignore {user.mention} for {mins} minutes. They must have been *naughty!*"

def ignoreBandit(mins):
    bandit = "442747712400654337"
    ignoreTime = datetime.now() + timedelta(minutes=mins)
    ignoreDb.set(bandit, ignoreTime.isoformat())
    return f"Got it, I'll ignore <@!{bandit}> for {mins} minutes. They must have been *naughty!*"

def dms(userId, flag):
    userId = str(userId)
    if (flag == "enable"):
        if (slideDb.get(userId)):
            slideDb.rem(userId)
        return "Got it, I'll be sliding into those dms sometime soon."
    elif (flag == "disable"):
        slideDb.set(userId, True)
        return "Okay, I won't send you any direct messages."
    else:
        return constants.dmsUsage

def callerNotIgnored(interaction):
    return not shouldIgnore(interaction.user.id)

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