import markovify

loads = {}

def listen(message):
    user = message.author.id

    if(user in loads):
        loads[user].append(message.content)

    filename = "./data/markov/" + str(message.author.id) + ".txt"
    with open(filename, "a", encoding="utf-8") as mfile:
            mfile.write(message.content + "\n")

async def mimic(client, message, args):
    async with message.channel.typing():
        if(args):
            user = args[0]
        else:
            user = message.author.id

        if(not user in loads):
            filename = "./data/markov/" + str(user) + ".txt"
            with open(filename, "r", encoding="utf-8") as mfile:
                loads[user] = mfile.read()

        model = markovify.Text(loads[user], state_size=3, well_formed=True)

        for i in range(3):
            await message.channel.send()
    
        