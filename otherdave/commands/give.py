import inflect
import pickledb
import random
import yaml
from otherdave.util import Thinger

with open("./conf.yaml") as conf:
    config = yaml.load(conf, Loader=yaml.BaseLoader)

inventoryKey = "inventory"
bagsize = int(config["bag_size"])
selftag = "<@" + config["self_id"] + ">"

_emptyBag = "Aw heck, I'm all out of stuff."
_unknownThing = "I don't have {thing}, give them one yourself."
_giftMessage = "Here, {target}, have {thing}."
_knownThing = "I've already got {thing}!"
_takeMessage = "Here, have {thing}."
_thanksMessage = selftag + " is now carrying {thing}."
_thanksfulMessage = selftag + " dropped {oldThing} and is now carrying {newThing}."

thinger = Thinger()
infl = inflect.engine()
bag = pickledb.load("./data/bag.db", True)

if (not bag.exists(inventoryKey)):
    bag.lcreate(inventoryKey)

def give(target = selftag, thing = "something"):
    if (target != selftag):
        return take(target, thing)
    
    if (thing == "something"):
        thing = thinger.make()
    
    if (bag.lexists(inventoryKey, thing)):
        return _knownThing.format(thing = infl.a(thing))
    
    if (bag.llen(inventoryKey) >= bagsize):
        oldThing = bag.lpop(inventoryKey, 0)
        bag.ladd(inventoryKey, thing)
        return _thanksfulMessage.format(oldThing = infl.an(oldThing), newThing = infl.a(thing))

    bag.ladd(inventoryKey, thing)
    return _thanksMessage.format(thing = infl.a(thing))


def take(target, thing):
    if (bag.llen(inventoryKey) == 0):
        return _emptyBag

    if (thing == "something"):
        bagIndex = random.randint(0, bag.llen(inventoryKey))
        gift = bag.lpop(inventoryKey, bagIndex)
    elif (bag.lexists(inventoryKey, thing)):
        gift = thing
        bag.lremvalue(inventoryKey, thing)
    else:
        return _unknownThing.format(thing = infl.a(thing))

    if (target == "me"):
        return _takeMessage.format(thing = infl.a(gift))
    else:
        return _giftMessage.format(target = target, thing = infl.a(gift))