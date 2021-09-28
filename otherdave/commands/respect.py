from otherdave.util.madlib import Complimenter

OtherDavesGraphicRespect = Complimenter()

def respect(ctx, args):
    target = " ".join(args) if args else ctx.author.mention
    compliment = OtherDavesGraphicRespect.make()
    return target + ", " + compliment