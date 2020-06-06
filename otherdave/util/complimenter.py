import inflect
import json
import random
import re

infl = inflect.engine()

class Complimenter():
    def __init__(self):
        with open("./data/respect/adjectives.json") as adf:
            self.adjectives = json.load(adf)
        with open("./data/respect/amounts.json") as amf:
            self.amounts = json.load(amf)
        with open("./data/respect/parts.json") as parf:
            self.parts = json.load(parf)
        with open("./data/respect/persons.json") as perf:
            self.persons = json.load(perf)
        with open("./data/respect/templates.json") as temf:
            self.templates = json.load(temf)
        with open("./data/respect/things.json") as thinf:
            self.things = json.load(thinf)

        self.actions = {
            "adjective" : lambda : random.choice(self.adjectives),
            "an_adjective" : lambda : infl.an(self.actions["adjective"]()),
            "amount" : lambda : random.choice(self.amounts),
            "an_amount" : lambda : infl.an(self.actions["amount"]()),
            "parts" : lambda : random.choice(self.parts),
            "person" : lambda : random.choice(self.persons),
            "thing" : lambda : random.choice(self.things),
            "template" : lambda : random.choice(self.templates)
        }
    
    def make(self):
        template = self.actions["template"]()
        tokens = template.split(" ")
        result = ""

        for token in tokens:
            action = re.match("\{\{(.+?)\}\}", token)
            if(action):
                if(action in self.actions):
                    result += self.actions[action[1]]()
                else:
                    result += action[0]
            else:
                result += token

            result += " "

        return result.strip()
