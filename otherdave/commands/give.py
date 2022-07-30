import inflect
import pickledb
import random
import yaml
from datetime import *
from otherdave.util import Thinger, User

with open("./conf.yaml") as conf:
    config = yaml.load(conf, Loader=yaml.BaseLoader)

inventoryKey = "inventory"
daveBucksKey = "davebucks"

bagsize = int(config["bag_size"])
userbagsize = int(config["user_bag_size"])
greedytime = int(config["greedy_time"])
selftag = "<@" + config["self_id"] + ">"
daveid = config["dave_id"]

# TODO: It would be neat if there could be a few different madlibs for these responses.
# TODO: Or a better way to set all these than a monolith of constants
_emptyBag = "Aw heck, {whos} all out of stuff."
_inventoryPreface = "Well heck, {whove} got a whole bunch of stuff. Right now {whos} carrying:"
_unknownThing = "I don't have {thing}, give them one yourself."
_giftMessage = "Here, {target}, have {thing}."
_knownThing = "I've already got {thing}!"
_takeMessage = "Here, have {thing}."
_thanksMessage = selftag + " is now carrying {thing}."
_thanksfulMessage = selftag + " dropped {oldThing} and is now carrying {newThing}."
_userfulMessage = "..\n\t*...it looks like you've dropped {thing} - I hope it wasn't important.*"
_greedyMessage = "Noooooooo I only just got that! Get your own, you selfish gremlin."
_noBucksMessage = "Hey, you're not <@" + daveid + "> <:lwys_todd_eyeburn:912451671181893632>\n\nGet your hands off my :sparkles:DaveBucks:sparkles:, you *capitalist swine*!"
_odBucksMessage = "No thanks, dad, all I need is your approval."
_daveDaveBucksMessage = "Isn't that a bit, uhhhhh, masturbatory?"
_decimalMessage = "Whoa, you think I'm minting coinage here?"
_daveBucksResultMessage = "Alriiiight, {target} now has {daveBucks} DaveBucks! Way to goooo!"
_walletMessage = "Well heck, you've got {daveBucks} DaveBucks! Livin' *large*, buddy!"
_dropMessage = "*It looks like {who} dropped {whose} {thing} - I hope it wasn't important...*"
_noDropMessage = "Uhhh, {who} can't drop {thing}, {who} don't have one..."
_emptyUseMessage = "But {whos} not carrying anything!"
_noUseMessage = "{who} can't use {thing}, silly, {who} don't have one."
_useUsage = "Maybe try using `!help use` first, huh buddy?"

thinger = Thinger()
user = User()
infl = inflect.engine()
bag = pickledb.load("./data/bag.db", True)
if (not bag.exists(inventoryKey)):
    bag.lcreate(inventoryKey)
if (not bag.exists(daveBucksKey)):
    bag.dcreate(daveBucksKey)

# Keep a list of recently acquired things in memory that he doesn't want to give away.
newThings = {}

# Some helpers for stringMischief down below
def byteWiseAdd(sthing, ithing):
    sbytes = sthing.encode("utf-8")
    ibytes = ithing.to_bytes(len(sbytes), "big")
    return bytes(list(map(lambda x, y: min(x + y, 255), sbytes, ibytes)))

def weirdIntAddAndReByte(sthing, ithing):
    sVal = sum(sthing.encode("utf-8")) + ithing
    return sVal.to_bytes((sVal.bit_length() + 7) // 8, "big")

def dodgeControlBytes(byteVal):
    byteVal = max(byteVal, 36)
    if 127 <= byteVal <= 160:
        return 161
    return byteVal

# A few insane ways to add an int to a string
stringMischief = [
    lambda sthing, ithing: str(sthing) + str(ithing),                           # (STR) Simple string concat
    lambda sthing, ithing: str(byteWiseAdd(sthing, ithing), "utf-8"),           # (STR) Bytewise addition
    lambda sthing, ithing: int.from_bytes(byteWiseAdd(sthing, ithing), "big"),  # (INT) Bytewise addition
    lambda sthing, ithing: sum(sthing.encode("utf-8")) + ithing,                # (INT) Sum the string bytes and add the int
                                                                                # (STR) Uhhhhhh, don't ask me about this next one
    lambda sthing, ithing: "".join(list(map(lambda x: chr(dodgeControlBytes(x)), weirdIntAddAndReByte(sthing, ithing))))
]

# Strip all these indefinite articles we're adding
def unflect_a(word: str) -> str:
    if (word.startswith("a ")):
        return word[2:]
    if (word.startswith("an ")):
        return word[3:]
    # No indefinite article
    return word

# Alias an to a to be cute like inflect
def unflect_an(word: str) -> str: return unflect_a(word)


def give(author, target = selftag, thing = "something"):
    lowerThing = thing.lower()
    if (lowerThing.endswith("davebuck")):
        thing += "s"
        lowerThing += "s"
    if ("davebucks" in lowerThing or "dave bucks" in lowerThing):
        return davebucks(author, target, thing)

    if (target != selftag):
        return take(author, target, thing)
    
    if (thing == "something"):
        thing = infl.a(thinger.make())
    
    if (bag.lexists(inventoryKey, thing)):
        return _knownThing.format(thing = thing)
    
    # Put the new thing in the bag
    bag.ladd(inventoryKey, thing)
    newThings[thing] = datetime.now()

    # Throw an old thing out if we're all full
    if (bag.llen(inventoryKey) > bagsize):
        oldThing = bag.lpop(inventoryKey, 0)
        newThings.pop(oldThing, None)
        return _thanksfulMessage.format(oldThing = oldThing, newThing = thing)
    else:
        return _thanksMessage.format(thing = thing)

def take(author, target, thing):
    if (bag.llen(inventoryKey) == 0):
        return _emptyBag.format(whos = "I'm")

    if (thing == "something"):
        bagIndex = random.randint(0, bag.llen(inventoryKey)-1)
        gift = bag.lpop(inventoryKey, bagIndex)

    elif (bag.lexists(inventoryKey, thing)):
        now = datetime.now()
        if (thing in newThings):
            delta = (now - newThings[thing]).total_seconds()

            if (delta < greedytime):
                return _greedyMessage

        gift = thing
        bag.lremvalue(inventoryKey, thing)

    else:
        return _unknownThing.format(thing = thing)

    if (target == "me"):
        target = author.mention

    if (not bag.exists(target)):
        bag.lcreate(target)

    # Put the new thing in the bag
    bag.ladd(target, gift)

    if (target == author.mention):
        response = _takeMessage.format(thing = gift)
    else:
        response = _giftMessage.format(target = target, thing = gift)

    # Throw an old thing out if they're all full
    if (bag.llen(target) > userbagsize):
        oldThing = bag.lpop(target, 0)
        response += _userfulMessage.format(thing = oldThing)

    # Stop tracking when OD got the thing
    newThings.pop(gift, None)

    return response

def drop(mention, thing):
    who = "I" if mention == inventoryKey else "you"
    whose = "my" if mention == inventoryKey else "your"

    if (not bag.exists(mention)
        or not bag.lexists(mention, thing)):
        return _noDropMessage.format(who = who, thing = thing)

    bag.lremvalue(mention, thing)
    return _dropMessage.format(who = who, whose = whose, thing = unflect_a(thing))

def selfdrop():
    thing = random.choice(bag.lgetall(inventoryKey))
    return drop(inventoryKey, thing)

def use(author, *args):
    if (len(args) < 2 and args[0] == "-my"):
        return _useUsage
    
    args = [args[0], " ".join(args[1:])] if args[0] == "-my" else [" ".join(args)]

    mention = inventoryKey if len(args) == 1 else author.mention
    thing = args[0] if len(args) == 1 else args[1]
    (who, whos, whose) = ("I", "I'm", "my") if len(args) == 1 else ("You", "you're", "your")

    if (thing == "something"):
        if (not bag.exists(mention)
            or bag.llen(mention) == 0):
            return _emptyUseMessage.format(whos = whos)
        thing = random.choice(bag.lgetall(mention))
        
    if (not bag.exists(mention)
        or not bag.lexists(mention, thing)):
        return _noUseMessage.format(who = who, thing = thing)

    bag.lremvalue(mention, thing)
    
    return user.make().format(
        who = who, 
        whose = whose, 
        thing = unflect_a(thing), 
        a_thing = thing)

def davebucks(author, target, thing):
    if (author.id != int(daveid)):
        return _noBucksMessage
    if (target == selftag):
        return _odBucksMessage
    if (target == author.mention):
        return _daveDaveBucksMessage
    if ("." in thing):
        return _decimalMessage

    thing = thing[:thing.lower().replace("dave bucks", "davebucks").find("davebucks")].strip()

    if (not bag.dexists(daveBucksKey, target)):
        bag.dadd(daveBucksKey, (target, 0))

    wallet = bag.dpop(daveBucksKey, target)
    thingIsDigit = thing.isdigit() or (thing.startswith("-") and thing[1:].isdigit())

    if (thingIsDigit and isinstance(wallet, int)):
        # Both are integers
        bag.dadd(daveBucksKey, (target, int(thing) + wallet))
    elif(thingIsDigit):
        bag.dadd(daveBucksKey, (target, random.choice(stringMischief)(wallet, int(thing))))
    elif(isinstance(wallet, int)):
        bag.dadd(daveBucksKey, (target, random.choice(stringMischief)(thing, wallet)))
    else:
        # Both are strings
        bag.dadd(daveBucksKey, (target, thing + wallet))

    return _daveBucksResultMessage.format(target = target, daveBucks = bag.dget(daveBucksKey, target))
    
def wallet(author):
    if (author.id == daveid):
        return ""
    
    if (not bag.dexists(daveBucksKey, author.mention)):
        bag.dadd(daveBucksKey, (author.mention, 0))
    
    return _walletMessage.format(daveBucks = bag.dget(daveBucksKey, author.mention))

def inventory(author, user):
    if (user is None or user == selftag):
        whove = "I've"
        whos = "I'm"

        if (bag.llen(inventoryKey) == 0):
            return _emptyBag.format(whos = whos)

        backpack = bag.lgetall(inventoryKey)

    else:
        if (author.mention == user):
            whove = "you've"
            whos = "you're"
        else:
            whove = "they've"
            whos = "they're"

        if (bag.exists(user)):
            if (bag.llen(user) == 0):
                return _emptyBag.format(whos = whos)
            
            backpack = bag.lgetall(user)

        else:
            return _emptyBag.format(whos = whos)

        
    inventoryString = _inventoryPreface.format(whove = whove, whos = whos)
    
    for thing in backpack:
        inventoryString += "\n\t- " + thing

    # ka-CHING
    if (not (user is None) and user != selftag and not (daveid in user)):
        if (not bag.dexists(daveBucksKey, user)):
            bag.dadd(daveBucksKey, (user, 0))
        inventoryString += "\n\naaaand **" + str(bag.dget(daveBucksKey, user)) + "** DaveBucks!"

    return inventoryString
