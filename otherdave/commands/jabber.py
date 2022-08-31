import random
from otherdave.util import constants
from sys import maxsize

with open("./data/dad.txt", encoding="utf-8") as dadf:
    dadjokes = dadf.read().splitlines()

def beach():
    sand = random.randint(2, maxsize)
    joy = random.choice(constants.joy)
    return "Today I'm on a beach with {} grains of sand, {}!".format(sand, joy)

def helpNotFound():
    return constants.notFound

def version():
    return constants.version

def dad():
    return random.choice(dadjokes)