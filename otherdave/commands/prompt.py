from otherdave.util.madlib import Prompter

prompter = Prompter()

async def prompt(client, message, args):
    # TODO: other stuff
    await message.channel.send(prompter.make())