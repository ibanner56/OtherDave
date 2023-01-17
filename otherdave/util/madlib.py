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
            action = re.match("(.*)\{\{(.+?)\}\}(.*)", token)
            if(action):
                if(action[2] in self.actions):
                    result += action[1] + self.actions[action[2]]() + action[3]
                else:
                    result += action[0]
            else:
                result += token

            result += " " 

        if (re.search("\{\{(.+?)\}\}", result)):
            # Recursion with no base case -
            # I'm going to regret this some day aren't I...
            return self.make(result)

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
            json.dump(self.nouns, nf)

    def remNoun(self, noun):
        if(noun in self.nouns):
            self.nouns.remove(noun)
            with open("./data/prompt/nouns.json", "w") as nf:
                json.dump(self.nouns, nf)

    def addAdjective(self, adjective):
        self.adjectives.append(adjective)
        with open("./data/prompt/adjectives.json", "w") as adf:
            json.dump(self.adjectives, adf)

    def remAdjective(self, adjective):
        if(adjective in self.adjectives):
            self.adjectives.remove(adjective)
            with open("./data/prompt/adjectives.json", "w") as adf:
                json.dump(self.adjectives, adf)

class Thinger(MadLibber):
    def __init__(self) -> None:
        with open("./data/madlib/adjectives.json") as adf:
            self.adjectives = json.load(adf)
        with open("./data/madlib/amounts.json") as amf:
            self.amounts = json.load(amf)
        with open("./data/madlib/assets.json") as parf:
            self.assets = json.load(parf)
        with open("./data/madlib/templates.json") as temf:
            self.templates = json.load(temf)
        with open("./data/madlib/nouns.json") as nounf:
            self.nouns = json.load(nounf)
        with open("./data/madlib/ing_verbs.json") as ing_verbsf:
            self.ing_verbs = json.load(ing_verbsf)
        with open("./data/madlib/itemtypes.json") as typef:
            self.types = json.load(typef)

        self.actions = {
            "adjective" : lambda : random.choice(self.adjectives["adjectives"]),
            "an_adjective" : lambda : infl.an(self.actions["adjective"]()),
            "adverb" : lambda : random.choice(self.adjectives["adverbs"]),
            "amount" : lambda : random.choice(self.amounts),
            "an_amount" : lambda : infl.an(self.actions["amount"]()),
            "asset" : lambda : random.choice(self.assets),
            "noun" : lambda : random.choice(self.nouns),
            "ing_verb" : lambda : random.choice(self.ing_verbs),
            "template" : lambda : random.choice(self.templates["thing"]),
            "type": lambda : random.choice(self.types["allTypes"]),
            "type_food": lambda : random.choice(self.types["foodTypes"]),
            "type_standard": lambda : random.choice(self.types["standardTypes"]),
            "type_rare": lambda : random.choice(self.types["rareTypes"]),
            "type_legendary": lambda : random.choice(self.types["legendaryTypes"])
        }

    def typeThing(self, thing):
        return "(" + self.actions["type"]() + ") " + thing

    def foodifyThing(self, thing):
        return "(" + self.actions["type_food"]() + ") " + thing

    def standardifyThing(self, thing):
        return "(" + self.actions["type_standard"]() + ") " + thing

    def rarifyThing(self, thing):
        return "(" + self.actions["type_rare"]() + ") " + thing

    def legendarifyThing(self, thing):
        return "(" + self.actions["type_legendary"]() + ") " + thing

class User(MadLibber):
    def __init__(self) -> None:
        with open("./data/madlib/adjectives.json") as adf:
            self.adjectives = json.load(adf)
        with open("./data/madlib/amounts.json") as amf:
            self.amounts = json.load(amf)
        with open("./data/madlib/assets.json") as parf:
            self.assets = json.load(parf)
        with open("./data/madlib/templates.json") as temf:
            self.templates = json.load(temf)
        with open("./data/madlib/nouns.json") as nounf:
            self.nouns = json.load(nounf)
        with open("./data/madlib/present_verbs.json") as present_verbsf:
            self.present_verbs = json.load(present_verbsf)
        with open("./data/madlib/ing_verbs.json") as ing_verbsf:
            self.ing_verbs = json.load(ing_verbsf)
        with open("./data/madlib/planets.json") as planetsf:
            self.planets = json.load(planetsf)

        self.actions = {
            "adjective" : lambda : random.choice(self.adjectives["adjectives"]),
            "an_adjective" : lambda : infl.an(self.actions["adjective"]()),
            "adverb" : lambda : random.choice(self.adjectives["adverbs"]),
            "asset" : lambda : random.choice(self.assets),
            "a_noun": lambda : infl.a(self.actions["noun"]()),
            "noun" : lambda : random.choice(self.nouns),
            "planet" : lambda : random.choice(self.planets),
            "present_verb" : lambda : random.choice(self.present_verbs),
            "ing_verb": lambda : random.choice(self.ing_verbs),
            "template" : lambda : random.choice(self.templates["use"])
        }

class Relicer(MadLibber):
    def __init__(self) -> None:
        with open("./data/marketplace/coolguy_realname.json") as cgrnfile:
            self.coolguys = json.load(cgrnfile)
        with open("./data/marketplace/relic_adj.json") as radfile:
            self.radjectives = json.load(radfile)
        with open("./data/marketplace/relic_alig.json") as ralfile:
            self.raligns = json.load(ralfile)
        with open("./data/marketplace/relic_desc.json") as redfile:
            self.rdescs = json.load(redfile)
        with open("./data/marketplace/relic_site.json") as resfile:
            self.rsites = json.load(resfile)
        with open("./data/marketplace/relic_templates.json") as retfile:
            self.templates = json.load(retfile)
        with open("./data/marketplace/relics.json") as relfile:
            self.relics = json.load(relfile)
        with open("./data/marketplace/title.json") as tfile:
            self.titles = json.load(tfile)    

        self.actions = {
            "coolguy_realname" : lambda : random.choice(self.coolguys),
            "relic_adj" : lambda : random.choice(self.radjectives),
            "relic_alig" : lambda : random.choice(self.raligns),
            "relic_desc" : lambda : random.choice(self.rdescs),
            "relic_site" : lambda : random.choice(self.rsites),
            "relic" : lambda : random.choice(self.relics),
            "title" : lambda : random.choice(self.titles),
            "template" : lambda : random.choice(self.templates)
        }