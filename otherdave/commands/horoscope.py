from otherdave.util.madlib import Horoscope

OtherDavesTerribleHoroscope = Horoscope()

def horoscope(variant=None):
    omen = OtherDavesTerribleHoroscope.make_horoscope(variant)
    return omen