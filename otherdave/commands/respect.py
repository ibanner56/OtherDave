from otherdave.util.madlib import Complimenter

OtherDavesGraphicRespect = Complimenter()

def respect(target):
    compliment = OtherDavesGraphicRespect.make()
    return target + ", " + compliment