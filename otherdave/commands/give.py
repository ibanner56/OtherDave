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
    thing = thinger.make().split(")")
    thing = thing[0] + ")" + infl.a(thing[1])

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

def give(author, target = config.selftag, thing = "something"):
    lowerThing = thing.lower()
    if (lowerThing.endswith("davebuck")):
        thing += "s"
        lowerThing += "s"
    if ("davebucks" in lowerThing or "dave bucks" in lowerThing):
        return davebucks(author, target, thing)

    if (target != config.selftag):
        return take(author, target, thing)
    
    if (thing == "something"):
        thing = thinger.make().split(")")
        thing = thing[0] + ")" + infl.a(thing[1])
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

    if (target == "me"):
        target = author.mention

    if (not bag.exists(target)):
        bag.lcreate(target)

    # Put the new thing in the bag
    bag.ladd(target, gift)

    if (target == author.mention):
        response = constants.takeMessage.format(thing = gift)
    else:
        response = constants.giftMessage.format(target = target, thing = gift)

    # Throw an old thing out if they're all full
    if (bag.llen(target) > config.userbagsize):
        oldThing = bag.lpop(target, 0)
        response += constants.userfulMessage.format(thing = oldThing)

    # Stop tracking when OD got the thing
    newThings.pop(gift, None)

    return response

def drop(mention, thing):
    who = "I" if mention == constants.inventoryKey else "you"
    whose = "my" if mention == constants.inventoryKey else "your"

    if (not bag.exists(mention)):
        return constants.noDropMessage.format(who = who, thing = thing)

    if (not "(:" in thing
        or not ":)" in thing):
        typedThing = bag.lgetrg(mention, "^(\(:[a-z_]+:\) )*" + thing + "$")
    elif (bag.lexists(mention, thing)):
        typedThing = typedThing
    else:
        typedThing = None

    if (typedThing == None):
        return constants.noDropMessage.format(who = who, thing = thing)

    bag.lremvalue(mention, typedThing)
    return constants.dropMessage.format(who = who, whose = whose, thing = unflect.a(thing))

def selfdrop():
    thing = random.choice(bag.lgetall(constants.inventoryKey))
    return drop(constants.inventoryKey, thing)

def use(mention = constants.inventoryKey, thing = "something", who= "I", whos = "I'm", whose = "my"):
    if (thing == "something"):
        if (not bag.exists(mention)
            or bag.llen(mention) == 0):
            return constants.emptyUseMessage.format(whos = whos)
        thing = random.choice(bag.lgetall(mention))
        
    if (not bag.exists(mention)):
        return constants.noUseMessage.format(who = who, thing = thing)

    typedThing = bag.lgetrg(mention, "^(\(:[a-z_]+:\) )*" + thing + "$")
    if (typedThing == None):
        return constants.noDropMessage.format(who = who, thing = thing)

    bag.lremvalue(mention, typedThing)
    
    unflectedthing = typedThing.split(")")
    unflectedthing = unflectedthing[0] + ")" + unflect.an(unflectedthing[1])

    return user.make().format(
        who = who, 
        whose = whose, 
        thing = unflectedthing, 
        a_thing = typedThing)

def useCmd(author, *args):
    if (len(args) < 2 and args[0] == "-my"):
        return constants.useUsage
    
    args = [args[0], " ".join(args[1:])] if args[0] == "-my" else [" ".join(args)]

    mention = constants.inventoryKey if len(args) == 1 else author.mention
    thing = args[0] if len(args) == 1 else args[1]
    (who, whos, whose) = ("I", "I'm", "my") if len(args) == 1 else ("You", "you're", "your")

    return use(mention, thing, who, whos, whose)

def davebucks(author, target, thing):
    if (author.id != int(config.daveid)):
        return constants.noBucksMessage
    if (target == config.selftag):
        return constants.odBucksMessage
    if (target == author.mention):
        return constants.daveDaveBucksMessage
    if ("." in thing):
        return constants.decimalMessage

    thing = thing[:thing.lower().replace("dave bucks", "davebucks").find("davebucks")].strip()

    if (not bag.dexists(constants.daveBucksKey, target)):
        bag.dadd(constants.daveBucksKey, (target, 0))

    wallet = bag.dpop(constants.daveBucksKey, target)
    thingIsDigit = thing.isdigit() or (thing.startswith("-") and thing[1:].isdigit())

    if (thingIsDigit and isinstance(wallet, int)):
        # Both are integers
        bag.dadd(constants.daveBucksKey, (target, int(thing) + wallet))
    elif(thingIsDigit):
        bag.dadd(constants.daveBucksKey, (target, random.choice(stringMischief)(wallet, int(thing))))
    elif(isinstance(wallet, int)):
        bag.dadd(constants.daveBucksKey, (target, random.choice(stringMischief)(thing, wallet)))
    else:
        # Both are strings
        bag.dadd(constants.daveBucksKey, (target, thing + wallet))

    return constants.daveBucksResultMessage.format(target = target, daveBucks = bag.dget(constants.daveBucksKey, target))
    
def wallet(author):
    if (author.id == config.daveid):
        return ""
    
    if (not bag.dexists(constants.daveBucksKey, author.mention)):
        bag.dadd(constants.daveBucksKey, (author.mention, 0))
    
    return constants.walletMessage.format(daveBucks = bag.dget(constants.daveBucksKey, author.mention))

def inventory(author, user):
    if (user is None or user == config.selftag):
        whove = "I've"
        whos = "I'm"

        if (bag.llen(constants.inventoryKey) == 0):
            return constants.emptyBag.format(whos = whos)

        backpack = bag.lgetall(constants.inventoryKey)

    else:
        if (author.mention == user):
            whove = "you've"
            whos = "you're"
        else:
            whove = "they've"
            whos = "they're"

        if (bag.exists(user)):
            if (bag.llen(user) == 0):
                return constants.emptyBag.format(whos = whos)
            
            backpack = bag.lgetall(user)

        else:
            return constants.emptyBag.format(whos = whos)

        
    inventoryString = constants.inventoryPreface.format(whove = whove, whos = whos)
    
    for thing in backpack:
        inventoryString += "\n\t- " + thing

    # ka-CHING
    if (not (user is None) and user != config.selftag and not (config.daveid in user)):
        if (not bag.dexists(constants.daveBucksKey, user)):
            bag.dadd(constants.daveBucksKey, (user, 0))
        inventoryString += "\n\naaaand **" + str(bag.dget(constants.daveBucksKey, user)) + "** DaveBucks!"

    return inventoryString
