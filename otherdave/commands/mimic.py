import markovify
import random
import re

_makeFailed = "hahaha Oof owie Heck, guess I don't know you well enough to do that."
loads = {}

def listen(message):
    if(len(message.content.split(" ")) < 4):
        return

    user = message.author.id
    content = message.content
    if(not content.endswith(".")):
        # Markovify doesn't treat \n as punctuation...
        content = content + "."

    filename = "./data/markov/" + str(message.author.id) + ".txt"
    with open(filename, "a", encoding="utf-8") as mfile:
            mfile.write("\n" + content)
    if(user in loads):
        loads[user] += "\n" + content

async def mimic(client, message, args):
    async with message.channel.typing():
        if(args):
            user = re.sub("<@!*|>", "", args[0]).lower()
        else:
            user = message.author.id

        if(not user in loads):
            filename = "./data/markov/" + str(user) + ".txt"
            try:
                with open(filename, "r", encoding="utf-8") as mfile:
                    loads[user] = mfile.read()
            except OSError:
                return await message.channel.send(_makeFailed) 

        model = markovify.Text(loads[user], well_formed=True)

        result = ""
        for _ in range(3):
            sentence = model.make_sentence(tries=1000000, max_words=random.randint(8, 40))
            if(sentence):
                result += sentence + "\n"

        if(result):
            return await message.channel.send(sentence)
        else:
            return await message.channel.send(_makeFailed)    
        
