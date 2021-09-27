from asyncio.windows_events import NULL
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

async def lwys(client, message, args):
    cast = ["Stage"]
    async with message.channel.typing():
        if (args):
            for castMember in args:
                if (not castMember.lower() in _lwysCast):
                    return await message.channel.send(_lwysFailed)
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
                    return await message.channel.send(_lwysFailed)
            
            model = markovify.Text(loads[castMember], well_formed=True)
            lines += [castMember + ": " + model.make_sentence(tries=100, max_words=random.randint(8, 40))]

        return await message.channel.send('\n'.join(lines))

async def mimic(client, message, args):
    chat = False
    combo = False
    haiku = False
    async with message.channel.typing():
        if(args):
            if (args[0] == "-combo"):
                combo = True
            elif (args[0] == "-chat"):
                chat = True
            elif (args[0] == "-haiku"):
                haiku = True
                
            validNoFlags = len(args) == 1 and not haiku and not combo and not chat
            validTwoArgs = len(args) == 2 and haiku
            validThreeArgs = len(args) == 3 and (combo or chat)

            if (not validNoFlags and not validTwoArgs and not validThreeArgs):
                return await message.channel.send(_incorrectArgs)
            elif (validNoFlags):
                user = re.sub("<@!*|>", "", args[0]).lower()
            elif (validTwoArgs):
                user = re.sub("<@!*|>", "", args[1]).lower()
            else:
                user1 = re.sub("<@!*|>", "", args[1]).lower()
                user2 = re.sub("<@!*|>", "", args[2]).lower()
        else:
            user = message.author.id

        # Load files based on command
        if (chat or combo):
            if (not user1 in loads):
                filename = "./data/markov/" + str(user1) + ".txt"
                try:
                    with open(filename, "r", encoding="utf-8") as mfile:
                        loads[user1] = mfile.read()
                except OSError:
                    return await message.channel.send(_makeFailed) 
            if (not user2 in loads):
                filename = "./data/markov/" + str(user2) + ".txt"
                try:
                    with open(filename, "r", encoding="utf-8") as mfile:
                        loads[user2] = mfile.read()
                except OSError:
                    return await message.channel.send(_makeFailed) 
        elif (not user in loads):
            filename = "./data/markov/" + str(user) + ".txt"
            try:
                with open(filename, "r", encoding="utf-8") as mfile:
                    loads[user] = mfile.read()
            except OSError:
                return await message.channel.send(_makeFailed) 

        # Build models and mimic appropriately
        if (chat):
            model1 = markovify.Text(loads[user1], well_formed=True)
            model2 = markovify.Text(loads[user2], well_formed=True)
            for _ in range(2):
                sentence1 = model1.make_sentence(tries=100, max_words=random.randint(8, 40))
                sentence2 = model2.make_sentence(tries=100, max_words=random.randint(8, 40))

                if (sentence1 and sentence2):
                    await message.channel.send(args[1] + ": " + sentence1 + "\r\n" + args[2] + ": " + sentence2)
                else:
                    return await message.channel.send(_makeFailed)
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
                        return await message.channel.send(parsedHaiku)
                        
                return await message.channel.send(_haikuMakeFailed)
            else:
                for _ in range(3):
                    sentence = model.make_sentence(tries=100, max_words=random.randint(8, 40))
                    if(sentence):
                        await message.channel.send(sentence)
                    else:
                        return await message.channel.send(_makeFailed)
