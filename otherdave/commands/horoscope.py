from otherdave.util.madlib import Horoscope

OtherDavesTerribleHoroscope = Horoscope()

def horoscope(variant):
    if variant not in OtherDavesTerribleHoroscope.get_variants():
        return "Hooo boy, \"" + variant + "\" is a funky sounding star sign. I'm also a case-sensitive little baby."
    return OtherDavesTerribleHoroscope.make_horoscope(variant)