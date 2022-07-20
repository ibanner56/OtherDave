import inflect
import json
import random
import re

infl = inflect.engine()

class MadLibber():
    def make(self, template = None):
        if(template is None):
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
        with open("./data/madlib/adjectives.json") as adf:
            self.adjectives = json.load(adf)
        with open("./data/madlib/amounts.json") as amf:
            self.amounts = json.load(amf)
        with open("./data/madlib/parts.json") as parf:
            self.parts = json.load(parf)
        with open("./data/madlib/persons.json") as perf:
            self.persons = json.load(perf)
        with open("./data/madlib/templates.json") as temf:
            self.templates = json.load(temf)
        with open("./data/madlib/things.json") as thinf:
            self.things = json.load(thinf)

        self.actions = {
            "adjective" : lambda : random.choice(self.adjectives["adjectives"]),
            "an_adjective" : lambda : infl.an(self.actions["adjective"]()),
            "amount" : lambda : random.choice(self.amounts),
            "an_amount" : lambda : infl.an(self.actions["amount"]()),
            "parts" : lambda : random.choice(self.parts),
            "person" : lambda : random.choice(self.persons),
            "thing" : lambda : random.choice(self.things),
            "template" : lambda : random.choice(self.templates["respect"])
        }

class Horoscoper(MadLibber):
    def __init__(self):
        with open("./data/madlib/adjectives.json") as adf:
            self.adjectives = json.load(adf)
        with open("./data/madlib/amounts.json") as amf:
            self.amounts = json.load(amf)
        with open("./data/madlib/assets.json") as parf:
            self.assets = json.load(parf)
        with open("./data/madlib/persons.json") as perf:
            self.persons = json.load(perf)
        with open("./data/madlib/templates.json") as temf:
            self.templates = json.load(temf)
        with open("./data/madlib/nouns.json") as thinf:
            self.nouns = json.load(thinf)
        with open("./data/madlib/ing_verbs.json") as ing:
            self.ing_verbs = json.load(ing)
        with open("./data/madlib/present_verbs.json") as pres:
            self.present_verbs = json.load(pres)
        with open("./data/madlib/planets.json") as pla:
            self.planets = json.load(pla)

        self.actions = {
            "adjective" : lambda : random.choice(self.adjectives["adjectives"]),
            "an_adjective" : lambda : infl.an(self.actions["adjective"]()),
            "adverb" : lambda : random.choice(self.adjectives["adverbs"]),
            "amount" : lambda : random.choice(self.amounts),
            "an_amount" : lambda : infl.an(self.actions["amount"]()),
            "asset" : lambda : random.choice(self.assets),
            "person" : lambda : random.choice(self.persons),
            "present_verb" : lambda : random.choice(self.present_verbs),
            "noun" : lambda : random.choice(self.nouns),
            "nouns" : lambda : infl.plural_noun(random.choice(self.nouns)),
            "ing_verb" : lambda : random.choice(self.ing_verbs),
            "planet" : lambda : random.choice(self.planets)
        }
    
    def get_variants(self):
        return self.templates["horoscope"].keys()
    
    def make_horoscope(self, variant):
        return self.make(random.choice(self.templates["horoscope"][variant]))

class Prompter(MadLibber):
    def __init__(self):
        with open("./data/prompt/adjectives.json") as adf:
            self.adjectives = json.load(adf)
        with open("./data/prompt/nouns.json") as nf:
            self.nouns = json.load(nf)

        self.actions = {
            "adjective" : lambda : random.choice(self.adjectives),
            "noun" : lambda : random.choice(self.nouns),
            "template" : lambda : r"{{adjective}} {{noun}}"
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

    def remAdjective(self, adjective):
        if(adjective in self.adjectives):
            self.adjectives.remove(adjective)
            with open("./data/prompt/adjectives.json", "w") as adf:
                json.dump(adf)