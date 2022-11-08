import inflect
import random
from datetime import *
from otherdave.util import config, constants, pickledb, Thinger, unflect, User
from otherdave.util.stringmischief import stringMischief

thinger = Thinger()
user = User()
infl = inflect.engine()
bag = pickledb.load("./data/bag.db", True)
if (not bag.exists(constants.inventoryKey)):
    bag.lcreate(constants.inventoryKey)
if (not bag.exists(constants.daveBucksKey)):
    bag.dcreate(constants.daveBucksKey)

# Keep a list of recently acquired things in memory that he doesn't want to give away.
newThings = {}

def find():
    thing = thinger.make()
    thing = infl.a(thing)
    thing = thinger.typeThing(thing)

    # Put the new thing in the bag
    bag.ladd(constants.inventoryKey, thing)
    newThings[thing] = datetime.now()

    # Throw an old thing out if we're all full
    if (bag.llen(constants.inventoryKey) > config.bagsize):
        oldThing = bag.lpop(constants.inventoryKey, 0)
        newThings.pop(oldThing, None)
        return constants.foundfulMessage.format(oldThing = oldThing, newThing = thing)
    else:
        return constants.foundMessage.format(thing = thing)

def give(author, target, thing = "something"):
    lowerThing = thing.lower()
    if (lowerThing.endswith("davebuck")):
        thing += "s"
        lowerThing += "s"
    if ("davebucks" in lowerThing or "dave bucks" in lowerThing):
        return davebucks(author, target, thing)

    if (str(target.id) != config.selfid):
        return take(author, target, thing)
    
    if (thing == "something"):
        thing = thinger.make()
        thing = infl.a(thing)
        thing = thinger.typeThing(thing)
    else:
        if (bag.lexistsrg(constants.inventoryKey, "^(\(:[a-z_]+:\) )*" + thing + "$")):
            return constants.knownThing.format(thing = thing)        
        
        if (not "(:" in thing
            or not ":)" in thing):
            thing = thinger.typeThing(thing)
    
    # Put the new thing in the bag
    bag.ladd(constants.inventoryKey, thing)
    newThings[thing] = datetime.now()

    # Throw an old thing out if we're all full
    if (bag.llen(constants.inventoryKey) > config.bagsize):
        oldThing = bag.lpop(constants.inventoryKey, 0)
        newThings.pop(oldThing, None)
        return constants.thanksfulMessage.format(oldThing = oldThing, newThing = thing)
    else:
        return constants.thanksMessage.format(thing = thing)

def take(author, target, thing):
    targetKey = str(target.id)

    if (bag.llen(constants.inventoryKey) == 0):
        return constants.emptyBag.format(whos = "I'm")

    if (thing == "something"):
        bagIndex = random.randint(0, bag.llen(constants.inventoryKey)-1)
        gift = bag.lpop(constants.inventoryKey, bagIndex)

    elif (bag.lexistsrg(constants.inventoryKey, "^(\(:[a-z_]+:\) )*" + thing + "$")):
        gift = bag.lgetrg(constants.inventoryKey, "^(\(:[a-z_]+:\) )*" + thing + "$")
        
        now = datetime.now()
        if (gift in newThings):
            delta = (now - newThings[gift]).total_seconds()

            if (delta < config.greedytime):
                return constants.greedyMessage

        bag.lremvalue(constants.inventoryKey, gift)

    else:
        return constants.unknownThing.format(thing = thing)

    if (not bag.exists(targetKey)):
        bag.lcreate(targetKey)

    # Put the new thing in the bag
    bag.ladd(targetKey, gift)

    if (target.id == author.id):
        response = constants.takeMessage.format(thing = gift)
    else:
        response = constants.giftMessage.format(target = target.mention, thing = gift)

    # Throw an old thing out if they're all full
    if (bag.llen(targetKey) > config.userbagsize):
        oldThing = bag.lpop(targetKey, 0)
        response += constants.userfulMessage.format(thing = oldThing)

    # Stop tracking when OD got the thing
    newThings.pop(gift, None)

    return response

def drop(target, thing):
    who = "you" if target else "I"
    whose = "your" if target else "my"

    targetKey = target.Id if target else constants.inventoryKey

    if (not bag.exists(targetKey)):
        return constants.noDropMessage.format(who = who, thing = thing)

    if (not "(:" in thing
        or not ":)" in thing):
        typedThing = bag.lgetrg(targetKey, "^(\(:[a-z_]+:\) )*" + thing + "$")
    elif (bag.lexists(targetKey, thing)):
        typedThing = thing
    else:
        typedThing = None

    if (typedThing == None):
        return constants.noDropMessage.format(who = who, thing = thing)

    bag.lremvalue(targetKey, typedThing)
    return constants.dropMessage.format(who = who, whose = whose, thing = unflect.a(thing))

def selfdrop():
    thing = random.choice(bag.lgetall(constants.inventoryKey))
    return drop(None, thing)

def use(target, thing = "something", who= "I", whos = "I'm", whose = "my"):
    userKey = target if target else constants.inventoryKey

    if (not bag.exists(userKey)):
        return constants.noUseMessage.format(who = who, thing = thing)
        
    if (thing == "something"):
        if (not bag.exists(userKey)
            or bag.llen(userKey) == 0):
            return constants.emptyUseMessage.format(whos = whos)
        thing = random.choice(bag.lgetall(userKey))

    if (not "(:" in thing
        or not ":)" in thing):
        typedThing = bag.lgetrg(userKey, "^(\(:[a-z_]+:\) )*" + thing + "$")
    elif (bag.lexists(userKey, thing)):
        typedThing = thing
    else:
        typedThing = None

    if (typedThing == None):
        return constants.noUseMessage.format(who = who, thing = thing)

    bag.lremvalue(userKey, typedThing)
    
    unflectedthing = typedThing.split(")")
    unflectedthing = unflectedthing[0] + ")" + unflect.an(unflectedthing[1])

    return user.make().format(
        who = who, 
        whose = whose, 
        thing = unflectedthing, 
        a_thing = typedThing)

def useCmd(author, my, thing):
    mention = constants.inventoryKey if not my else str(author.id)
    (who, whos, whose) = ("I", "I'm", "my") if not my else ("You", "you're", "your")

    return use(mention, thing, who, whos, whose)

def davebucks(author, target, thing):
    if (author.id != int(config.daveid)):
        return constants.noBucksMessage
    if (str(target.id) == config.selfid):
        return constants.odBucksMessage
    if (target.id == author.id):
        return constants.daveDaveBucksMessage
    if ("." in thing):
        return constants.decimalMessage
    
    targetId = str(target.id)

    thing = thing[:thing.lower().replace("dave bucks", "davebucks").find("davebucks")].strip()
    thingIsDigit = thing.isdigit() or (thing.startswith("-") and thing[1:].isdigit())
    
    if (not bag.dexists(constants.daveBucksKey, targetId)):
        bag.dadd(constants.daveBucksKey, (targetId, 0 if thingIsDigit else ""))

    wallet = bag.dpop(constants.daveBucksKey, targetId)

    if (thingIsDigit and isinstance(wallet, int)):
        # Both are integers
        bag.dadd(constants.daveBucksKey, (targetId, int(thing) + wallet))
    elif(thingIsDigit):
        bag.dadd(constants.daveBucksKey, (targetId, random.choice(stringMischief)(wallet, int(thing))))
    elif(isinstance(wallet, int)):
        bag.dadd(constants.daveBucksKey, (targetId, random.choice(stringMischief)(thing, wallet)))
    else:
        # Both are strings
        bag.dadd(constants.daveBucksKey, (targetId, thing + wallet))

    return constants.daveBucksResultMessage.format(
        target = target.mention, 
        daveBucks = bag.dget(constants.daveBucksKey, targetId))
    
def wallet(author):
    if (author.id == config.daveid):
        return constants.daveWalletMessage
    
    authorId = str(author.id)
    
    if (not bag.dexists(constants.daveBucksKey, authorId)):
        bag.dadd(constants.daveBucksKey, (authorId, 0))
    
    return constants.walletMessage.format(daveBucks = bag.dget(constants.daveBucksKey, authorId))

def inventory(author, target):
    userId = str(target.id) if target else config.selfid

    if (userId == config.selfid):
        whove = "I've"
        whos = "I'm"

        if (bag.llen(constants.inventoryKey) == 0):
            return constants.emptyBag.format(whos = whos)

        backpack = bag.lgetall(constants.inventoryKey)

    else:
        if (author.id == userId):
            whove = "you've"
            whos = "you're"
        else:
            whove = "they've"
            whos = "they're"

        if (bag.exists(userId)):
            if (bag.llen(userId) == 0):
                return constants.emptyBag.format(whos = whos)
            
            backpack = bag.lgetall(userId)

        else:
            return constants.emptyBag.format(whos = whos)

        
    inventoryString = constants.inventoryPreface.format(whove = whove, whos = whos)
    
    for thing in backpack:
        inventoryString += "\n\t- " + thing

    # ka-CHING
    if (not (target is None) and userId != config.selfid and not (config.daveid in userId)):
        if (not bag.dexists(constants.daveBucksKey, userId)):
            bag.dadd(constants.daveBucksKey, (userId, 0))
        inventoryString += "\n\naaaand **" + str(bag.dget(constants.daveBucksKey, userId)) + "** DaveBucks!"

    return inventoryString
