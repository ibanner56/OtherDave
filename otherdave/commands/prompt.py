from otherdave.util.madlib import Prompter

prompter = Prompter()

async def prompt(client, message, args):
    if(len(args) == 0):
        await message.channel.send(prompter.make())
    elif(args[0] == "-forget" and args[1]):
        prompter.remNoun(args[1])
        prompter.remAdjective(args[1])
        await message.channel.send("forgotten" + args[1])
    elif(args[0] == "-add" and args[1] and args[2]):
        if(args[1].lower() == "noun"):
            prompter.addNoun(args[2])
        elif(args[1].lower() == "adjective"):
            prompter.addAdjective(args[2])
        else:
            await message.channel.send("invalid article")
    else:
        await message.channel.send("stupid command")