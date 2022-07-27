import inflect
import pickledb
import random
import yaml
from datetime import *
from otherdave.util import Thinger

with open("./conf.yaml") as conf:
    config = yaml.load(conf, Loader=yaml.BaseLoader)

inventoryKey = "inventory"
bagsize = int(config["bag_size"])
userbagsize = int(config["user_bag_size"])
greedytime = int(config["greedy_time"])
selftag = "<@" + config["self_id"] + ">"

# TODO: It would be neat if there could be a few different madlibs for these responses.
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

thinger = Thinger()
infl = inflect.engine()
bag = pickledb.load("./data/bag.db", True)

# Keep a list of recently acquired things in memory that he doesn't want to give away.
newThings = {}

if (not bag.exists(inventoryKey)):
    bag.lcreate(inventoryKey)

def give(author, target = selftag, thing = "something"):
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
    if (bag.llen(inventoryKey) >= bagsize):
        oldThing = bag.lpop(inventoryKey, 0)
        newThings.pop(oldThing)
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
        delta = (now - newThings[thing]).total_seconds()

        if (delta < greedytime):
            return _greedyMessage

        gift = thing
        bag.lremvalue(inventoryKey, thing)

    else:
        return _unknownThing.format(thing = thing)

    if (target == "me"):
        target = author

    if (not bag.exists(target)):
        bag.lcreate(target)

    # Put the new thing in the bag
    bag.ladd(target, gift)

    if (target == author):
        response = _takeMessage.format(thing = gift)
    else:
        response = _giftMessage.format(target = target, thing = gift)

    # Throw an old thing out if they're all full
    if (bag.llen(target) >= userbagsize):
        oldThing = bag.lpop(target, 0)
        response += _userfulMessage.format(thing = oldThing)

    # Stop tracking when OD got the thing
    newThings.pop(gift)

    return response

def inventory(author, user):
    if (user is None or user == selftag):
        whove = "I've"
        whos = "I'm"

        if (bag.llen(inventoryKey) == 0):
            return _emptyBag.format(whos = whos)

        backpack = bag.lgetall(inventoryKey)

    else:
        if (author == user):
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

    return inventoryString