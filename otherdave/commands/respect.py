from otherdave.util.madlib import Complimenter

OtherDavesGraphicRespect = Complimenter()

def respect(target: str) -> str:
    compliment = OtherDavesGraphicRespect.make()
    return target + ", " + compliment