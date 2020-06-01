import inflect
import json
import re
import textstat

sylf = open("./data/syllables.json")
masterSyllables = json.load(sylf)
infl = inflect.engine()

async def detect(message, **kwargs):
    words = re.split("\s", message.content)
    count = 0
    lines = [False, False, False]
    result = "*"
    debugResult = ""

    for word in words:
        # Check for digits and properly split them out, 
		# then convert from digit to text.
        if(re.match("\d+", word)):
            splitDigits = re.match("[a-zA-Z]+|[0-9]+", word)
            stringifiedDigits = ""

            for i in range(0, len(splitDigits)):
                # Do the whole digit thing here
                print("")
        
            count += textstat.syllable_count(stringifiedDigits)
            
        # Check the Moby project first because robots are bad at english.
		# If it's not in the dictionary, ask Zoltar.
        elif(word in masterSyllables):
            count += masterSyllables[word]
        elif(word.lower() in masterSyllables):
            count += masterSyllables[word.lower()]
        else:
            count += textstat.syllable_count(word)

        result += word
        debugResult += word + " - " + count + "\n"

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

        if(kwargs.get("debug", False)):
            await message.channel.send(debugResult)
        elif(count == 17):
            result += "*"
            await message.channel.send(result)

print(infl.number_to_words("200s"))