import inflect
import json
import math
import re
import textstat

sylf = open("./data/syllables.json")
masterSyllables = json.load(sylf)
infl = inflect.engine()

def parseHaiku(text, debug):
    words = re.split("\s", text)
    count = 0
    lines = [False, False, False]
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
        elif(depunct in masterSyllables):
            count += masterSyllables[depunct]
        elif(depunct.lower() in masterSyllables):
            count += masterSyllables[depunct.lower()]
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
    elif(count == 17):
        result += "*"
        return result
    else:
        return None

async def detect(message, **kwargs):
    debug = kwargs.get("debug", False)
    haiku = parseHaiku(message.content, debug)
    if(haiku != None):
        message.channel.send(haiku)