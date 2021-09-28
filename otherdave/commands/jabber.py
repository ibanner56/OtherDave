import random
import yaml
from sys import maxsize

with open("./conf.yaml") as conf:
    config = yaml.load(conf, Loader=yaml.BaseLoader)

_notFound = "Buddy, I think you need !help."
_joy = ["va-va-voom", "wheee", "whoopee", "woohoo", "yay", "yippee", "yowza"]
_version = "OtherDave is running version " + str(config["version"])

def beach():
    sand = random.randint(2, maxsize)
    joy = random.choice(_joy)
    return "Today I'm on a beach with {} grains of sand, {}!".format(sand, joy)

def helpNotFound():
    return _notFound

def version():
    return _version
