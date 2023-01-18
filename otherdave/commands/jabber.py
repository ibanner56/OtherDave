import random
from otherdave.util import constants
from sys import maxsize

with open("./data/dad.txt", encoding="utf-8") as dadf:
    dadjokes = dadf.read().splitlines()

def beach() -> str:
    sand = random.randint(2, maxsize)
    joy = random.choice(constants.joy)
    return "Today I'm on a beach with {} grains of sand, {}!".format(sand, joy)

def dad() -> str:
    return random.choice(dadjokes)