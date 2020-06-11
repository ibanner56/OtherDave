import markovify
import random
import re

loads = {}

def listen(message):
    if(len(message.content.split(" ")) < 4):
        return

    user = message.author.id
    if(user in loads):
        loads[user] += "\n" + message.content

    filename = "./data/markov/" + str(message.author.id) + ".txt"
    with open(filename, "a", encoding="utf-8") as mfile:
            mfile.write(message.content + "\n")

async def mimic(client, message, args):
    async with message.channel.typing():
        if(args):
            user = re.sub("<@!*|>", "", args[0])
        else:
            user = message.author.id

        if(not user in loads):
            filename = "./data/markov/" + str(user) + ".txt"
            with open(filename, "r", encoding="utf-8") as mfile:
                loads[user] = mfile.read()

        model = markovify.Text(loads[user], well_formed=True)

        for i in range(3):
            sentence = model.make_sentence(tries=1000000, max_words=random.randint(4, 40))
            await message.channel.send(sentence)
    
        
