import markovify
import random
import re
from .haiku import parseHaiku

_haikuMakeFailed = "*It seems that today*\n*this request that you have made*\n*is simply too hard.*"
_incorrectArgs = "The haha to arguments sorry, for correct not are command that <@ACCIDENTAL_USER_TAG>."
_lwysFailed = "Stage: Everyone stares at you, wondering what you're trying to do."
_makeFailed = "hahaha Oof owie Heck, guess I don't know you well enough to do that."
_lwysCast = ["fixit", "hattie", "oldie", "sophie", "todd", "tomo"]

loads = {}

def listen(message):
    if(len(message.content.split(" ")) < 4):
        return

    user = message.author.id
    content = re.sub("<@\d+>", "<@USER>", message.content)
    if(not content.endswith(".")):
        # Markovify doesn't treat \n as punctuation...
        content = content + "."

    filename = "./data/markov/" + str(message.author.id) + ".txt"
    with open(filename, "a", encoding="utf-8") as mfile:
            mfile.write("\n" + content)
    if(user in loads):
        loads[user] += "\n" + content

def lwys(args):
    cast = ["stage"]
    if (args):
        for castMember in args:
            if (not castMember.lower() in _lwysCast):
                return _lwysFailed
            cast += [castMember]            
    else:
        cast += [random.choice(_lwysCast)] + [random.choice(_lwysCast)]

    lines = []
    for castMember in cast:
        if (not castMember in loads):
            filename = "./data/markov/lwys/" + castMember + ".txt"
            try:
                with open(filename, "r", encoding="utf-8") as cfile:
                    loads[castMember] = cfile.read()
            except OSError:
                return _lwysFailed
        
        model = markovify.Text(loads[castMember], well_formed=True)
        lines += [castMember + ": " + model.make_sentence(tries=100, max_words=random.randint(8, 40))]

    return '\n'.join(lines)

def mimic(ctx, args):
    chat = False
    combo = False
    haiku = False

    if(args):
        if (args[0] == "-combo"):
            combo = True
        elif (args[0] == "-chat"):
            chat = True
        elif (args[0] == "-haiku"):
            haiku = True
            
        validNoFlags = len(args) == 1 and not haiku and not combo and not chat
        validOneArg = len(args) == 1 and haiku
        validTwoArgs = len(args) == 2 and haiku
        validThreeArgs = len(args) == 3 and (combo or chat)

        if (not validNoFlags and not validTwoArgs and not validThreeArgs):
            return [_incorrectArgs]
        elif (validNoFlags):
            user = re.sub("<@!*|>", "", args[0]).lower()
        elif (validOneArg):
            user = ctx.author.id
        elif (validTwoArgs):
            user = re.sub("<@!*|>", "", args[1]).lower()
        else:
            user1 = re.sub("<@!*|>", "", args[1]).lower()
            user2 = re.sub("<@!*|>", "", args[2]).lower()
    else:
        user = ctx.author.id

    # Load files based on command
    if (chat or combo):
        if (not user1 in loads):
            filename = "./data/markov/" + str(user1) + ".txt"
            try:
                with open(filename, "r", encoding="utf-8") as mfile:
                    loads[user1] = mfile.read()
            except OSError:
                return [_makeFailed]
        if (not user2 in loads):
            filename = "./data/markov/" + str(user2) + ".txt"
            try:
                with open(filename, "r", encoding="utf-8") as mfile:
                    loads[user2] = mfile.read()
            except OSError:
                return [_makeFailed]
    elif (not user in loads):
        filename = "./data/markov/" + str(user) + ".txt"
        try:
            with open(filename, "r", encoding="utf-8") as mfile:
                loads[user] = mfile.read()
        except OSError:
            return [_makeFailed]

    # Build models and mimic appropriately
    result = []

    if (chat):
        model1 = markovify.Text(loads[user1], well_formed=True)
        model2 = markovify.Text(loads[user2], well_formed=True)
        for _ in range(2):
            sentence1 = model1.make_sentence(tries=100, max_words=random.randint(8, 40))
            sentence2 = model2.make_sentence(tries=100, max_words=random.randint(8, 40))

            if (sentence1 and sentence2):
                result.append(args[1] + ": " + sentence1 + "\r\n" + args[2] + ": " + sentence2)
            else:
                return [_makeFailed]
    else:
        if (combo):
            model1 = markovify.Text(loads[user1], well_formed=True)
            model2 = markovify.Text(loads[user2], well_formed=True)
            model = markovify.combine([model1, model2])
        else:
            model = markovify.Text(loads[user], well_formed=True)

        if (haiku):
            for _ in range(1000):
                sentence1 = model.make_sentence(tries=100, max_words=5)
                sentence2 = model.make_sentence(tries=100, max_words=7)
                sentence3 = model.make_sentence(tries=100, max_words=5)
                parsedHaiku = None

                if (sentence1 and sentence2 and sentence3):
                    parsedHaiku = parseHaiku(sentence1 + " " + sentence2 + " " + sentence3, False)

                if (parsedHaiku):
                    result.append(parsedHaiku)
                    break
                    
            if (len(result) == 0):
                return [_haikuMakeFailed]
        else:
            for _ in range(3):
                sentence = model.make_sentence(tries=100, max_words=random.randint(8, 40))
                if(sentence):
                    result.append(sentence)
                else:
                    return [_makeFailed]
    
    return result
