from otherdave.util.madlib import Complimenter

OtherDavesGraphicRespect = Complimenter()

async def respect(client, message, args):
    target = " ".join(args) if args else message.author.mention
    compliment = OtherDavesGraphicRespect.make()
    await message.channel.send(target + ", " + compliment)