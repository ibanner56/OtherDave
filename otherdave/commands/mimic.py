import markovify
import random
import re
from otherdave.commands.haiku import parseHaiku
from otherdave.util import constants

loads = {}

def listen(message):
    if(len(message.content.split(" ")) < 4):
        return

    user = message.author.id
    content = message.content
    
    if("<@&" in content):
        content = re.sub("<@&\d+>", "<@&ROLE>", content)
    content = re.sub("<@!*\d+>", "<@USER>", content)
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
            if (not castMember.lower() in constants.lwysCast):
                return constants.lwysFailed
            cast += [castMember]            
    else:
        cast += [random.choice(constants.lwysCast)] + [random.choice(constants.lwysCast)]

    lines = []
    for castMember in cast:
        if (not castMember in loads):
            filename = "./data/markov/lwys/" + castMember + ".txt"
            try:
                with open(filename, "r", encoding="utf-8") as cfile:
                    loads[castMember] = cfile.read()
            except OSError:
                return constants.lwysFailed
        
        model = markovify.Text(loads[castMember], well_formed=True)

        if (castMember == "stage"):
            lines += ["*\*" + model.make_sentence(tries=100, max_words=random.randint(8, 40)) + "\**"]
        else:
            lines += [castMember + ": " + model.make_sentence(tries=100, max_words=random.randint(8, 40))]

    return '\n'.join(lines)

def mimicUser(user):
    userId = str(user.id)

    if (not userId in loads):
        filename = "./data/markov/" + userId + ".txt"
        try:
            with open(filename, "r", encoding="utf-8") as mfile:
                loads[userId] = mfile.read()
        except OSError:
            return [constants.makeFailed]

    model = markovify.Text(loads[userId], well_formed=True)

    result = []
    for _ in range(3):
        sentence = model.make_sentence(tries=100, max_words=random.randint(8, 40))
        if(sentence):
            result.append(sentence)
        else:
            return [constants.makeFailed]
    
    return result

def mimicCombo(user1, user2):
    if (not user1 in loads):
        filename = "./data/markov/" + str(user1) + ".txt"
        try:
            with open(filename, "r", encoding="utf-8") as mfile:
                loads[user1] = mfile.read()
        except OSError:
            return [constants.makeFailed]
    if (not user2 in loads):
        filename = "./data/markov/" + str(user2) + ".txt"
        try:
            with open(filename, "r", encoding="utf-8") as mfile:
                loads[user2] = mfile.read()
        except OSError:
            return [constants.makeFailed]

    # Build models and mimic appropriately
    result = []
    model1 = markovify.Text(loads[user1], well_formed=True)
    model2 = markovify.Text(loads[user2], well_formed=True)
    model = markovify.combine([model1, model2])

    for _ in range(3):
        sentence = model.make_sentence(tries=100, max_words=random.randint(8, 40))
        if(sentence):
            result.append(sentence)
        else:
            return [constants.makeFailed]
    
    return result

def mimicChat(user1, user2):
    userId1 = str(user1.id)
    userId2 = str(user2.id)

    if (not userId1 in loads):
        filename = "./data/markov/" + str(userId1) + ".txt"
        try:
            with open(filename, "r", encoding="utf-8") as mfile:
                loads[userId1] = mfile.read()
        except OSError:
            return [constants.makeFailed]
    if (not userId2 in loads):
        filename = "./data/markov/" + str(userId2) + ".txt"
        try:
            with open(filename, "r", encoding="utf-8") as mfile:
                loads[userId2] = mfile.read()
        except OSError:
            return [constants.makeFailed]

    # Build models and mimic appropriately
    result = []
    model1 = markovify.Text(loads[userId1], well_formed=True)
    model2 = markovify.Text(loads[userId2], well_formed=True)

    for _ in range(2):
        sentence1 = model1.make_sentence(tries=100, max_words=random.randint(8, 40))
        sentence2 = model2.make_sentence(tries=100, max_words=random.randint(8, 40))

        if (sentence1 and sentence2):
            result.append(user1.display_name + ": " + sentence1 + "\r\n" + user2.display_name + ": " + sentence2)
        else:
            return [constants.makeFailed]

    return result

def mimicHaiku(user):
    userId = str(user.id)

    if (not userId in loads):
        filename = "./data/markov/" + userId + ".txt"
        try:
            with open(filename, "r", encoding="utf-8") as mfile:
                loads[userId] = mfile.read()
        except OSError:
            return [constants.makeFailed]

    model = markovify.Text(loads[userId], well_formed=True)

    result = []

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
        return [constants.haikuMakeFailed]

    return result

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

        if (not validNoFlags and not validOneArg  and not validTwoArgs and not validThreeArgs):
            return [constants.incorrectArgs]
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
                return [constants.makeFailed]
        if (not user2 in loads):
            filename = "./data/markov/" + str(user2) + ".txt"
            try:
                with open(filename, "r", encoding="utf-8") as mfile:
                    loads[user2] = mfile.read()
            except OSError:
                return [constants.makeFailed]
    elif (not user in loads):
        filename = "./data/markov/" + str(user) + ".txt"
        try:
            with open(filename, "r", encoding="utf-8") as mfile:
                loads[user] = mfile.read()
        except OSError:
            return [constants.makeFailed]

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
                return [constants.makeFailed]
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
                return [constants.haikuMakeFailed]
        else:
            for _ in range(3):
                sentence = model.make_sentence(tries=100, max_words=random.randint(8, 40))
                if(sentence):
                    result.append(sentence)
                else:
                    return [constants.makeFailed]
    
    return result
