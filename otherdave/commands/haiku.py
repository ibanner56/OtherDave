import inflect
import pickledb
import math
import random
import re
import textstat

_correctionSuccess = "*I've taken your word*\n*that this word was not quite right,*\n*but now it should be.*"
_correctionFailed = "*Corrections require*\n*a word and a whole number*\n*What'chu doin', fool?*"
_savedHaiku = "*Alright then, sounds good,*\n*I'll keep that one for later.*\n*Refrigerator.*"
_badSaveKeywords = "*The words that you seek,*\n*I simply don't remember.*\n*Did you spell them right?*"
_unknownCritique = "*What you're asking for -*\n*I don't know how to do it.*\n*So piss off, nerd! Yeah!*"

masterSyllables = pickledb.load("./data/syllables.db", True)
memories = pickledb.load("./data/saved/haikus.db", True)
infl = inflect.engine()
lastCache = []

def parseHaiku(text, debug):
    words = re.split("\s", text)
    count = 0
    lines = [False, False]
    result = "*"
    debugResult = ""

    for word in words:
        # Strip punctuation and make sure we don't then have an empty token
        depunct = re.sub("[^\w\d]", "", word)
        if(not depunct):
            continue

        # Check for digits and properly split them out, 
		# then convert from digit to text.
        if(re.match("\d+", depunct)):
            splitDigits = re.findall("[a-zA-Z]+|[0-9]+", depunct)
            stringifiedDigits = ""

            for i in range(0, len(splitDigits)):
                # Assume a trailing s means that the digits before it 
				# are pluralized, but only if it's the only other token
                if(len(splitDigits) == 2 and i == 1 and splitDigits[i].lower() == "s"):
                    stringifiedDigits += splitDigits[i]

                    # Sneaky order-of-magnitudes
                    if(re.match("^10*s$", depunct)):
                        stringifiedDigits = stringifiedDigits.lstrip("one ")
                elif(re.match("\d+", splitDigits[i])):
                    stringifiedDigits += infl.number_to_words(splitDigits[i])
                else:
                    stringifiedDigits += " " + splitDigits[i]
        
            count += textstat.syllable_count(stringifiedDigits)
            
        # Check the Moby project first because robots are bad at english.
		# If it's not in the dictionary, ask Zoltar.
        elif(masterSyllables.get(depunct)):
            count += masterSyllables.get(depunct)
        elif(masterSyllables.get(depunct.lower())):
            count += masterSyllables.get(depunct.lower())
        else:
            count += textstat.syllable_count(depunct)

        result += word
        debugResult += word + " - " + str(count) + "\n"

        if(count == 5):
            lines[0] = True
            result += "*\n*"
        elif(count > 5 and not lines[0]):
            break
        elif(count == 12):
            lines[1] = True
            result += "*\n*"
        elif(count > 12 and not lines[1]):
            break
        elif(count > 17):
            break
        elif(count != 17):
            result += " "

    if(debug):
        return debugResult
    elif(count == 17 and lines[0] and lines[1]):
        result += "*"
        while(len(lastCache) > 10):
            lastCache.popleft()
        lastCache.append(result)
        return result
    else:
        return None

def correct(word, syllables):
    try:
        syllables = int(syllables)
        masterSyllables.set(word, syllables)
        return True
    except ValueError:
        return False

def save(keywords):
    if(keywords):
        poem = next((last for last in lastCache.reverse if keywords in last), None)
        if(poem):
            memories.set(len(memories.getall()), poem)
        else:
            return _badSaveKeywords
    else:
        memories.set(len(memories.getall()), lastCache[-1])
    
    return _savedHaiku

async def detect(message):
    haiku = parseHaiku(message.content, False)
    if(haiku != None):
        await message.channel.send(haiku)

async def critique(client, message, args):
    if(len(args) == 0):
        await message.channel.send(random.choice(memories))
    elif(args[0] == "-debug"):
        await message.channel.send(parseHaiku(" ".join(args[1:]), True))
    elif(args[0] == "-correct" and len(args) == 3):
        if(correct(args[1], args[2])):
            message.channel.send(_correctionSuccess)
        else:
            message.channel.send(_correctionFailed)
    elif(args[0] == "-save"):
        await message.channel.send(save(" ".join(args[1:])))
    else:
        await message.channel.send(_unknownCritique)