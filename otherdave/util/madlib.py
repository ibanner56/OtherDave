import inflect
import json
import random
import re

infl = inflect.engine()

class MadLibber():
    def make(self):
        template = self.actions["template"]()
        tokens = template.split(" ")
        result = ""

        for token in tokens:
            action = re.match("\{\{(.+?)\}\}", token)
            if(action):
                if(action[1] in self.actions):
                    result += self.actions[action[1]]()
                else:
                    result += action[0]
            else:
                result += token

            result += " "

        return result.strip()

class Complimenter(MadLibber):
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

class Prompter(MadLibber):
    def __init__(self):
        with open("./data/prompt/adjectives.json") as adf:
            self.adjectives = json.load(adf)
        with open("./data/prompt/nouns.json") as nf:
            self.nouns = json.load(nf)

        self.actions = {
            "adjective" : lambda : random.choice(self.adjectives),
            "noun" : lambda : random.choice(self.noun),
            "template" : r"{{adjective}} {{noun}}"
        }

    def addNoun(self, noun):
        self.nouns.append(noun)
        with open("./data/prompt/nouns.json", "w") as nf:
            json.dump(nf)

    def remNoun(self, noun):
        if(noun in self.nouns):
            self.nouns.remove(noun)
            with open("./data/prompt/nouns.json", "w") as nf:
                json.dump(nf)

    def addAdjective(self, adjective):
        self.adjectives.append(adjective)
        with open("./data/prompt/adjectives.json", "w") as adf:
            json.dump(adf)

    def remNoun(self, adjective):
        if(adjective in self.adjectives):
            self.adjectives.remove(adjective)
            with open("./data/prompt/adjectives.json", "w") as adf:
                json.dump(adf)