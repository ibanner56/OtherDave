import inflect
import pickledb
import random
import re
import textstat
import uuid
from collections import deque
from otherdave.util import config, constants

infl = inflect.engine()
masterSyllables = pickledb.load("./data/syllables.db", True)
memories = pickledb.load("./data/haikus.db", True)

lastCache = deque(maxlen=config.cacheLength)
memCache = deque(maxlen=config.cacheLength)

def flushCache():
    lastCache.clear()
    memCache.clear()

def syllableCount(word):
    # Check the Moby project first because robots are bad at english.
	# If it's not in the dictionary, ask Zoltar.
    if(masterSyllables.get(word)):
        return masterSyllables.get(word)
    elif(masterSyllables.get(word.lower())):
        return masterSyllables.get(word.lower())
    else:
        return textstat.syllable_count(word)

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
        
            for digit in stringifiedDigits.split(" "):
                count += syllableCount(digit)
       
        else:
            count += syllableCount(depunct)

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
    if(len(lastCache) == 0):
        return constants.emptyBuffer
    if(keywords):
        poem = next((last for last in reversed(lastCache) if keywords in last), None)
        if(poem):
            lastCache.remove(poem)
            memories.set(str(uuid.uuid1()), poem)
        else:
            return constants.badKeywords
    else:
        memories.set(str(uuid.uuid1()), lastCache.pop())
    
    return constants.savedHaiku

def save_hku(content):
    parsedHaiku = parseHaiku(content, False)
    if (parsedHaiku):
        memories.set(str(uuid.uuid1()), parsedHaiku)
        return constants.savedHaiku
    else:
        return constants.badMessage

def recall():
    memkeys = list(memories.getall())
    if(len(memkeys) == 0):
        return constants.emptyMemory
    rkey = random.choice(memkeys)
    rmem = memories.get(rkey)
    memCache.append((rkey, rmem))

    return rmem

def forget(keywords):
    if(len(memCache) == 0):
        return constants.emptyBuffer
    if(keywords):
        memory = next((mem for mem in reversed(memCache) if keywords in mem[1]), None)
        if(memory):
            memCache.remove(memory)
            memories.rem(memory[0])
        else:
            return constants.badKeywords
    else:
        memories.rem(memCache.pop()[0])
    
    return constants.forgetSuccess

def debug(poem):
    if(poem):
        return parseHaiku(poem, True)
    else:
        last = lastCache[-1].replace("*", "").replace("\n", " ")
        return parseHaiku(last, True)

async def detect(message):
    haiku = parseHaiku(message.content, False)
    if(haiku != None):
        await message.channel.send(haiku)

def critique(debugSnippet, correctParams, saveSnippet, forgetSnippet):
    # Only one argument at a time
    args = [x for x in [debugSnippet, correctParams, saveSnippet, forgetSnippet] if x is not None]

    if (len(args) == 0):
        return recall()
    elif (len(args) > 1):
        return constants.tooManyArgs
    elif(debugSnippet):
        return debug(debugSnippet)
    elif(correctParams):
        correctArgs = correctParams.split()
        if (len(correctArgs) == 2 and correct(correctArgs[0], correctArgs[1])):
            return constants.correctionSuccess
        else:
            return constants.correctionFailed
    elif(saveSnippet):
        return save(saveSnippet)
    elif(forgetSnippet):
        return forget(forgetSnippet)
    else:
        return constants.unknownCritique
